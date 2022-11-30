#!/bin/bash
rm -rf .serverless
yarn sls dynamodb install
yarn sls requirements install
yarn sls plugin install -n serverless-python-requirements
yarn sls plugin install -n serverless-offline
yarn sls plugin install -n serverless-dynamodb-local
yarn sls plugin install -n serverless-prune-plugin