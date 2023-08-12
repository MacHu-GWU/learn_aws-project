# -*- coding: utf-8 -*-

import mpire
import subprocess
from pathlib_mate import Path

bin_pngquant = Path.home() / "pngquant" / "pngquant"


def compress_image(in_path: Path, out_path: Path):
    print(f"compress image from {in_path}")
    print(f"  to {out_path}")
    subprocess.run(
        [
            bin_pngquant,
            "8",
            f"{in_path}",
            "--quality",
            "0-70",
            "--output",
            f"{out_path}",
        ]
    )


def process_many_images(dir_before: Path, dir_after: Path):
    if dir_after.exists():
        raise FileExistsError(f"{dir_after} already exists")
    for subdir_before in dir_before.select_dir():
        subdir_after = dir_after.joinpath(subdir_before.relative_to(dir_before))
        subdir_after.mkdir_if_not_exists()

    args = list()
    for in_path in dir_before.glob("**/*.png"):
        out_path = dir_after.joinpath(in_path.relative_to(dir_before))
        args.append(
            dict(
                in_path=in_path,
                out_path=out_path,
            )
        )

    with mpire.WorkerPool() as pool:
        results = pool.map(compress_image, args)


dir_here = Path.dir_here(__file__)
dir_before = dir_here / "_static" / "aws-icons"
dir_after = dir_here / "_static" / "aws-icons-after"
process_many_images(dir_before, dir_after)
