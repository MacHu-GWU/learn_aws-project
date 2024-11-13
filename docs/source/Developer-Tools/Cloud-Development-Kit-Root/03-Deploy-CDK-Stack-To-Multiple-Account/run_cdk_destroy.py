# -*- coding: utf-8 -*-

from lib import params_dev, bsm_dev, params_test, bsm_test, destroy_cdk

destroy_cdk(params_dev, bsm_dev)
destroy_cdk(params_test, bsm_test)
