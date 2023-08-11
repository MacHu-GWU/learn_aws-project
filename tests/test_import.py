# -*- coding: utf-8 -*-

import os
import pytest
import learn_aws


def test_import():
    _ = learn_aws


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
