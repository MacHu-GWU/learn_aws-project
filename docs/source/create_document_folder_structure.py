# -*- coding: utf-8 -*-


import textwrap
from pathlib_mate import Path

dir_source = Path.dir_here(__file__)
dir_static = dir_source.joinpath("_static")
dir_arch = dir_source.joinpath("_static", "aws-icons", "arch")
dir_cate = dir_source.joinpath("_static", "aws-icons", "cate")
dir_root = dir_source.joinpath("root")

for dir_group in dir_arch.select_dir(recursive=False):
    if dir_group.basename in [
        "General-Icons",
    ]:
        continue
    dir_base = dir_root.joinpath(dir_group.basename)
    dir_base.mkdir_if_not_exists()

    title = dir_group.basename.replace("-", " ")
    ruler = "=" * 78
    path_png_5x = dir_cate.joinpath(f"{dir_group.basename}_64_5x.png")
    relpath_image = path_png_5x.relative_to(dir_source)
    content = textwrap.dedent(f"""
    {title} Root
    {ruler}
    .. image:: /{relpath_image}
        :width: 128px
        
    .. autotoctree::
        :maxdepth: 1
    """).strip() + "\n"
    path_readme = dir_base.joinpath("index.rst")
    path_readme.write_text(content)

    for path_png in dir_group.select_by_ext(".png"):
        if "_5x" not in path_png.fname:
            fname = path_png.fname.split("_64")[0].replace("_", "-").replace("Amazon-", "").replace("AWS-", "")
            dir_service = dir_base.joinpath(fname + "-Root")
            dir_service.mkdir_if_not_exists()
            path_png_5x = path_png.change(new_fname=path_png.fname + "_5x")
            title = dir_service.basename.replace("-", " ")
            ruler = "=" * 78
            relpath_image = path_png_5x.relative_to(dir_source)
            content = textwrap.dedent(f"""
                {title}
                {ruler}
                
                .. image:: /{relpath_image}
                    :width: 128px
                
                .. autotoctree::
                    :maxdepth: 1
                """).strip() + "\n"
            path_readme = dir_service.joinpath("index.rst")
            path_readme.write_text(content)
