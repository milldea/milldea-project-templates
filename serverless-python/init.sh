#!/bin/bash
rm -rf .serverless

yarn init -y && yarn install
pip install --upgrade pip
pip install -r requirements.txt

sls dynamodb install
sls requirements install
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-offline
sls plugin install -n serverless-dynamodb-local
sls plugin install -n serverless-prune-plugin