# -*- coding: utf-8 -*-

import typing as T
import json
from pathlib_mate import Path

print("build learnaws full text search anything dataset ...")

dir_here = Path.dir_here(__file__)
dir_source = dir_here.joinpath("docs", "source")

dir_home = Path.home()
dir_afwf_fts_anything = dir_home.joinpath(".alfred-afwf", "afwf_fts_anything")
dataset = "learnaws"
path_data = dir_afwf_fts_anything.joinpath(f"{dataset}-data.json")
path_setting = dir_afwf_fts_anything.joinpath(f"{dataset}-setting.json")
dir_whoosh_index = dir_afwf_fts_anything.joinpath(f"{dataset}-whoosh_index")

header1 = "=" * 50


def try_to_parse_doc_file(
    path: Path,
) -> T.Union[T.Optional[str], T.Optional[T.List[str]]]:
    """
    获取每个文档的 title 和 keywords
    """
    lines = path.read_text().splitlines()
    title = None
    keywords = None
    for ind, line in enumerate(lines):
        if line.startswith(header1):
            title = lines[ind - 1]

        line = line.lower()
        if line.startswith("keywords: "):
            keywords = [
                word.strip()
                for word in line.lstrip("keywords: ").split(",")
                if word.strip()
            ]

    return (title, keywords)


domain = "https://learn-aws.readthedocs.io/"
data = list()
for path in dir_source.select_file(recursive=True):
    if path.basename == "index.rst":
        title, keywords = try_to_parse_doc_file(path)
        if title is not None:
            # 创建每篇文档的 URL
            url = f"{domain}{path.change(new_basename=path.fname).relative_to(dir_source)}.html"
            # 构建最终被 index 的数据
            if keywords is None:
                search = title
            else:
                search = " ".join([title, " ".join(keywords)])
            row = {
                "title": title,
                "search": search,
                "url": url,
            }
            data.append(row)

settings = {
    "fields": [
        {
            "name": "title",
            "type_is_store": True,
        },
        {
            "name": "search",
            "type_is_store": False,
            "type_is_ngram": True,
            "ngram_minsize": 2,
            "ngram_maxsize": 10,
        },
        {
            "name": "url",
            "type_is_store": True,
        },
    ],
    "title_field": "{title}",
    "subtitle_field": "read '{title}'",
    "arg_field": "{url}",
    "autocomplete_field": "{title}",
}

dir_whoosh_index.remove_if_exists()
path_data.write_text(json.dumps(data, indent=4))
path_setting.write_text(json.dumps(settings, indent=4))

print(f"done! check '{path_data}' and '{path_setting}' file")
