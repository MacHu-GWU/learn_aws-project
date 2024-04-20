# -*- coding: utf-8 -*-

"""
Conclusion:

1. 对于同一个文件 Textract 处理的速度在不同时间可能不同. 这可能是因为异步 API 涉及到 AWS 服务端的调度, 导致不同时间的处理速度不同.
2. 对于同一个文件, 一次性处理比分页后依次处理要快. 但是你要确保一次性处理的文件的大小不要太大.
3. 你可以将同一个文件分拆成小文件, 然后并行调用 API 进行处理.
"""

from datetime import datetime
from pathlib_mate import Path
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager
import aws_textract.api as aws_textract

dir_here = Path.dir_here(__file__)
path_fw2 = dir_here / "fw2.pdf"
path_page_list = [dir_here / f"fw2-{i}.pdf" for i in range(1, 6 + 1)]

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)
s3dir_root = S3Path(
    f"s3://{bsm.aws_account_alias}-{bsm.aws_region}-data/projects/tmp/"
).to_dir()
s3dir_input = s3dir_root.joinpath("input").to_dir()
s3dir_output = s3dir_root.joinpath("output").to_dir()
s3dir_root.delete()


def try_one_file():
    print(f"working on {path_fw2.basename} ...")
    s3path = s3dir_root.joinpath(path_fw2.basename)
    s3path.write_bytes(path_fw2.read_bytes())
    document_location, output_config = (
        aws_textract.better_boto.preprocess_input_output_config(
            input_bucket=s3path.bucket,
            input_key=s3path.key,
            input_version=None,
            output_bucket=s3dir_output.bucket,
            output_prefix=s3dir_output.key,
        )
    )
    start_time = datetime.now()
    res = bsm.textract_client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=["FORMS"],
        OutputConfig=output_config,
    )
    job_id = res["JobId"]
    aws_textract.better_boto.wait_document_analysis_job_to_succeed(
        textract_client=bsm.textract_client,
        job_id=job_id,
        delays=1,
        timeout=300,
    )
    print("")
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    print(f"One file elapsed: {elapsed:.6f}")


def try_many_file():
    for path in path_page_list:
        s3path = s3dir_root.joinpath(path.basename)
        s3path.write_bytes(path.read_bytes())

    start_time = datetime.now()
    for path in path_page_list:
        print(f"working on {path.basename} ...")
        s3path = s3dir_root.joinpath(path.basename)
        document_location, output_config = (
            aws_textract.better_boto.preprocess_input_output_config(
                input_bucket=s3path.bucket,
                input_key=s3path.key,
                input_version=None,
                output_bucket=s3dir_output.bucket,
                output_prefix=s3dir_output.key,
            )
        )
        res = bsm.textract_client.start_document_analysis(
            DocumentLocation=document_location,
            FeatureTypes=["FORMS"],
            OutputConfig=output_config,
        )
        job_id = res["JobId"]
        aws_textract.better_boto.wait_document_analysis_job_to_succeed(
            textract_client=bsm.textract_client,
            job_id=job_id,
            delays=1,
            timeout=300,
        )
        print("")

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    print(f"Many file elapsed: {elapsed:.6f}")


if __name__ == "__main__":
    try_one_file()
    try_many_file()
    pass
