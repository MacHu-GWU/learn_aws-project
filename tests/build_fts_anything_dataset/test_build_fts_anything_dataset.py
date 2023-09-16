# -*- coding: utf-8 -*-

import typing as T
import pytest
from pathlib import Path
from build_fts_anything_dataset import (
    tokenize,
    get_url,
    extract_title_and_keywords_from_rst,
    extract_title_and_keywords_from_ipynb,
    build_fts_anything_dataset,
)

dir_here = Path(__file__).absolute().parent
dir_source = dir_here
dir_home = Path.home()
dir_afwf_fts_anything = dir_home.joinpath(".alfred-afwf", "afwf_fts_anything")
path_index_rst = dir_source / "chapter1" / "section1" / "index.rst"
path_index_ipynb = dir_source / "chapter1" / "section2" / "index.ipynb"


def test_tokenize():
    assert tokenize("a b, c\td    e . f;g") == list("abcdefg")


def test_get_url():
    url = get_url(
        domain="https://my_dataset.readthedocs.io/",
        dir_source=dir_source,
        path_index_rst=path_index_rst,
    )
    assert url == "https://my_dataset.readthedocs.io/chapter1/section1/index.html"


def test_extract_title_and_keywords_from_rst():
    title, keywords = extract_title_and_keywords_from_rst(path_index_rst)
    assert title == "Chapter1 - Section1"
    assert keywords == ["chapter1", "section1", "word1", "word2"]


def test_extract_title_and_keywords_from_ipynb():
    title, keywords = extract_title_and_keywords_from_ipynb(path_index_ipynb)
    assert title == "Chapter1 - Section2"
    assert keywords == ["chapter1", "section2", "word1", "word2"]


def test_build_fts_anything_dataset():
    build_fts_anything_dataset(
        domain="https://learn-aws.readthedocs.io/",
        dataset_name="learnaws",
        dir_source=dir_source,
        dir_afwf_fts_anything=dir_afwf_fts_anything,
        dry_run=True,
    )


if __name__ == "__main__":
    pytest.main([Path(__file__).name, "-s", "--tb=native"])
