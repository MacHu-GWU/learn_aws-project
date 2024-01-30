# -*- coding: utf-8 -*-

import typing as T


def build_unload_sql(
    raw_sql: str,
    s3_uri: str,
    iam_role: str = "default",
    format: T.Optional[str] = None,
    header: T.Optional[bool] = None,
    delimiter: T.Optional[str] = None,
    fixedwidth: T.Optional[str] = None,
    add_quotes: T.Optional[bool] = None,
    encrypted: T.Optional[bool] = None,
    manifest: T.Optional[str] = None,
    bzip2: T.Optional[bool] = None,
    gzip: T.Optional[bool] = None,
    zstd: T.Optional[bool] = None,
    null_as: T.Optional[str] = None,
    escape: T.Optional[str] = None,
    allow_overwrite: T.Optional[bool] = None,
    clean_path: T.Optional[bool] = None,
    parallel: T.Optional[bool] = None,
    max_file_size: T.Optional[int] = None,
    max_file_size_unit: str = "MB",
    row_group_size: T.Optional[int] = None,
    row_group_size_unit: str = "MB",
    extension: T.Optional[str] = None,
) -> str:
    """
    Given a "SELECT ..." statement, build the correspoending ``UNLOAD`` statement.

    .. note::

        This function doesn't support all UNLOAD options.

    :param raw_sql: the raw SQL statement. Usually it is a ``SELECT`` statement
    :param s3_uri: the S3 URI where you want to dump the result to.
    :param format: CSV | PARQUET | JSON

    Reference:

    - UNLOAD: https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html
    """
    if not s3_uri.endswith("/"):
        s3_uri += "/"
    raw_sql = raw_sql.replace("'", "''")
    final_sql_lines = [
        f"UNLOAD('{raw_sql}')",
        "TO",
        f"'{s3_uri}'",
        f"IAM_ROLE {iam_role}",
    ]
    if format is not None:
        final_sql_lines.append(f"FORMAT AS {format.upper()}")
    if header is not None:
        final_sql_lines.append(f"HEADER")
    if delimiter is not None:
        final_sql_lines.append(f"DELIMITER '{delimiter}'")
    if fixedwidth is not None:
        final_sql_lines.append(f"FIXEDWIDTH '{fixedwidth}'")
    if add_quotes:
        final_sql_lines.append(f"ADDQUOTES")
    if encrypted:
        final_sql_lines.append(f"ENCRYPTED")
    if manifest is not None:
        final_sql_lines.append(f"MANIFEST")
    if bzip2 is not None:
        final_sql_lines.append(f"BZIP2")
    if gzip is not None:
        final_sql_lines.append(f"GZIP")
    if zstd is not None:
        final_sql_lines.append(f"ZSTD")
    if null_as is not None:
        final_sql_lines.append(f"NULL AS '{null_as}'")
    if escape is not None:
        final_sql_lines.append(f"ESCAPE")
    if allow_overwrite:
        final_sql_lines.append(f"ALLOWOVERWRITE")
    if clean_path:
        final_sql_lines.append(f"CLEANPATH")
    if parallel is not None:
        if parallel:
            final_sql_lines.append(f"PARALLEL ON")
        else:
            final_sql_lines.append(f"PARALLEL OFF")
    if max_file_size is not None:
        final_sql_lines.append(f"MAXFILESIZE {max_file_size} {max_file_size_unit}")
    if row_group_size is not None:
        final_sql_lines.append(f"ROW_GROUP_SIZE {row_group_size} {row_group_size_unit}")
    if extension is not None:
        final_sql_lines.append(f"FILE_EXTENSION '{extension}'")
    return "\n".join(final_sql_lines)
