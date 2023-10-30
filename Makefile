# Makefile

APP_PATH=todos
TESTS_PATH=tests
DEPLOY_OPTIONS="--aws-s3-accelerate"

# Use the locally installed binary to avoid global conflict
SLS=./node_modules/serverless/bin/serverless.js
NPX=./node_modules/npx/index.js

serverless:
	# Reset node_modules to install properly
	rm -rf node_modules
	mkdir node_modules

	npm install serverless@3.34.0 --save-dev
	${SLS} plugin install -n serverless-dynamodb
	${SLS} plugin install -n serverless-offline


py_requirements:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry env list
	poetry env info
	poetry lock
	poetry install --all-extras

requirements: py_requirements
setup: serverless requirements

localserver:
	AWS_SDK_LOAD_CONFIG=1 AWS_DEFAULT_PROFILE=woven_local			\
		poetry run ${SLS} offline start 							\
			--noTimeout 											\
			--reloadHandler											\
			--verbose												\
			--config serverless.yml

deploy:
	poetry run ${SLS} deploy										\
		-s $(stage)													\
		${DEPLOY_OPTIONS}

test:
	poetry run pytest -s -vv

.PHONY: serverless requirements setup localserver deploy test
