# -*- coding: utf-8 -*-

from lib import params_dev, bsm_dev, params_test, bsm_test, deploy_cdk

deploy_cdk(params_dev, bsm_dev)
deploy_cdk(params_test, bsm_test)
