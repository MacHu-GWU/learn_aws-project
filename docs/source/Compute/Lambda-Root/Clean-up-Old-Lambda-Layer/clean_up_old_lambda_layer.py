# -*- coding: utf-8 -*-

"""
AWS Lambda Layer Version Cleanup Utility

This module provides functionality to clean up old AWS Lambda Layer versions to optimize storage usage.
It allows you to maintain the N most recent versions of each layer while removing older versions
based on their creation date.

Key Features:

- Lists all Lambda layers filtering by runtime family (e.g., Python)
- Keeps a specified number of most recent layer versions
- Deletes versions older than a specified retention period
- Supports dry run mode for safety
- Handles pagination for AWS API calls

Requirements:

- boto3

Usage:

.. code-block:: python

    boto_ses = boto3.Session(profile_name="your_profile")
    lbd_client = boto_ses.client("lambda")

    # List all Python runtime layers
    layers = list_layers(lbd_client, runtime_family="python")

    # Clean up each layer
    for layer_name in layers:
        delete_old_layer_version(
            lbd_client=lbd_client,
            layer_name=layer_name,
            keep_n_latest=3,
            retention_period_days=90,
            real_run=False  # Set to True for actual deletion
        )
"""

import typing as T
from itertools import islice
from datetime import datetime, timezone, timedelta

import boto3

# from rich import print as rprint


def list_layers(
    lbd_client,
    runtime_family: str = "python",
) -> T.List[str]:
    """
    List all Lambda layers that are compatible with the specified runtime family.

    :param lbd_client: Boto3 Lambda client instance
    :param runtime_family: Runtime family to filter layers (e.g., "python", "node")

    :return: List of layer names compatible with the specified runtime
    """
    paginator = lbd_client.get_paginator("list_layers")
    response_iterator = paginator.paginate(
        PaginationConfig={
            "MaxItems": 1000,
            "PageSize": 50,
        }
    )
    layer_name_list = list()
    for response in response_iterator:
        # rprint(response)  # for debug only
        for layer_data in response.get("Layers"):
            for runtime in layer_data.get("LatestMatchingVersion", {}).get(
                "CompatibleRuntimes", []
            ):
                if runtime.startswith(runtime_family):
                    layer_name_list.append(layer_data["LayerName"])
                    break
    return layer_name_list


def iter_layer_version(
    lbd_client,
    layer_name: str,
) -> T.Iterable[T.Dict[str, T.Any]]:
    """
    Generate an iterator of all versions for a specific Lambda layer.

    :param lbd_client: Boto3 Lambda client instance
    :param layer_name: Name of the Lambda layer

    :return: iterator of Dict[str, Any], Layer version data including Version, CreatedDate, etc.
    """
    paginator = lbd_client.get_paginator("list_layer_versions")
    response_iterator = paginator.paginate(
        LayerName=layer_name,
        PaginationConfig={"MaxItems": 1000, "PageSize": 50},
    )
    for response in response_iterator:
        # rprint(response)  # for debug only
        yield from response.get("LayerVersions")


def take(n: int, iterable: T.Iterable):
    "Return first n items of the iterable as a list."
    return list(islice(iterable, n))


MAGNITUDE_OF_DATA = {
    i: v for i, v in enumerate(["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"])
}


def repr_data_size(
    size_in_bytes: int,
    precision: int = 2,
) -> str:
    """
    Return human readable string represent of a file size. Doesn't support
    size greater than 1YB.

    For example:
    - 100 bytes => 100 B
    - 100,000 bytes => 97.66 KB
    - 100,000,000 bytes => 95.37 MB
    - 100,000,000,000 bytes => 93.13 GB
    - 100,000,000,000,000 bytes => 90.95 TB
    - 100,000,000,000,000,000 bytes => 88.82 PB
    - and more ...

    Magnitude of data::

        1000         kB    kilobyte
        1000 ** 2    MB    megabyte
        1000 ** 3    GB    gigabyte
        1000 ** 4    TB    terabyte
        1000 ** 5    PB    petabyte
        1000 ** 6    EB    exabyte
        1000 ** 7    ZB    zettabyte
        1000 ** 8    YB    yottabyte
    """
    if size_in_bytes < 1024:
        return "%s B" % size_in_bytes

    index = 0
    while 1:
        index += 1
        size_in_bytes, mod = divmod(size_in_bytes, 1024)
        if size_in_bytes < 1024:
            break
    template = "{0:.%sf} {1}" % precision
    s = template.format(size_in_bytes + mod / 1024.0, MAGNITUDE_OF_DATA[index])
    return s


def delete_old_layer_version(
    lbd_client,
    layer_name: str,
    keep_n_latest: int = 3,
    retention_period_days: int = 90,
    utc_now: T.Optional[datetime] = None,
    real_run: bool = False,
) -> None:
    """
    Delete old versions of a Lambda layer based on specified criteria.

    :param lbd_client: Boto3 Lambda client instance
    :param layer_name: Name of the Lambda layer to clean up
    :param keep_n_latest: Number of most recent versions to keep regardless of age
    :param retention_period_days: Delete versions older than this many days
    :param utc_now: Current UTC time (useful for testing)
    :param real_run: If False, only print what would be deleted without actual deletion

    The function will:

    1. Always keep the N most recent versions specified by ``keep_n_latest``
    2. Delete remaining versions that are older than ``retention_period_days``
    3. Print size and creation date information for deleted versions
    4. Only perform actual deletions if ``real_run`` is True
    """
    if utc_now is None:
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    ago = utc_now - timedelta(days=retention_period_days)

    # Get iterator for all versions and skip the N latest ones
    layer_version_data_iterator = iter_layer_version(
        lbd_client=lbd_client,
        layer_name=layer_name,
    )
    # print(list(layer_version_data_iterator))
    take(keep_n_latest, layer_version_data_iterator)

    # Process remaining versions
    for layer_version_data in layer_version_data_iterator:
        # rprint(layer_version_data)  # for debug only
        created_date = datetime.strptime(
            layer_version_data["CreatedDate"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        if created_date < ago:
            version = layer_version_data["Version"]
            _response = lbd_client.get_layer_version(
                LayerName=layer_name,
                VersionNumber=version,
            )
            code_size = _response["Content"]["CodeSize"]
            code_size_for_human = repr_data_size(code_size)
            print(
                f"delete: {layer_name}:{version} (created at = {created_date}, size = {code_size_for_human})"
            )
            if real_run:
                lbd_client.delete_layer_version(
                    LayerName=layer_name,
                    VersionNumber=layer_version_data["Version"],
                )


if __name__ == "__main__":
    # Example usage of the module
    boto_ses = boto3.Session(profile_name="bmt_app_devops_us_east_1")
    lbd_client = boto_ses.client("lambda")

    # List all Python runtime layers
    layer_name_list = list_layers(
        lbd_client=lbd_client,
        runtime_family="python",
    )

    # Clean up each layer
    for layer_name in layer_name_list:
        delete_old_layer_version(
            lbd_client=lbd_client,
            layer_name=layer_name,
            keep_n_latest=3,
            retention_period_days=90,
            real_run=False,  # Set to True for actual deletion
        )
