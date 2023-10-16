<!--
title: 'AWS Serverless REST API with DynamoDB store example in Python'
description: 'This example demonstrates how to setup a RESTful Web Service allowing you to create, list, get, update and delete Todos. DynamoDB is used to store the data.'
layout: Doc
framework: v1
platform: AWS
language: Python
priority: 10
authorLink: 'https://github.com/helveticafire'
authorName: 'Ben Fitzgerald'
authorAvatar: 'https://avatars0.githubusercontent.com/u/1323872?v=4&s=140'
-->
# Serverless REST API

This example demonstrates how to setup a [RESTful Web Services](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_web_services) allowing you to create, list, get, update and delete Todos. DynamoDB is used to store the data. This is just an example and of course you could use any data storage as a backend.

## Structure

This service has a separate directory for all the todo operations. For each operation exactly one file exists e.g. `todos/delete.py`. In each of these files there is exactly one function defined.

The idea behind the `todos` directory is that in case you want to create a service containing multiple resources e.g. users, notes, comments you could do so in the same service. While this is certainly possible you might consider creating a separate service for each resource. It depends on the use-case and your preference.

## Use-cases

- API for a Web Application
- API for a Mobile Application

## Setup
### Node
```bash
npm install
```

### Python environment
```bash
brew install pyenv pyenv-virtualenv
pyenv install 3.9
cd /path/to/dapi-demo/
pyenv local 3.9
python3 -m venv .venv
.venv/bin/activate
make setup
```

## Run locally
Add the following line to `~/.aws/config`.
Note: The keys are expired. These are just needed for pynamodb to work locally

```
    [profile woven_local]
    # Expired keys used for local development. This is needed to trick
    # boto into working with `make localserver`
    aws_access_key_id=ASIA6EUHFPR3BRZQZ6ZT
    aws_secret_access_key=PlqNw0YiEcKFZ/aQtA0a1Hjvy5Id0jy9FEj1qETe
```

Run the following to activate the localserver
```bash
.venv/bin/activate
make localserver
```

The expected result should be similar to:

```bash
Starting Offline at stage local (us-east-1)

Offline [http for lambda] listening on http://localhost:3002
Function names exposed for local invocation by aws-sdk:
           * create: dapi-demo-local-create
           * list: dapi-demo-local-list
           * get: dapi-demo-local-get
           * update: dapi-demo-local-update
           * delete: dapi-demo-local-delete

 ┌────────────────────────────────────────────────────────────────────────────┐
 │                                                                            │
 │   POST   | http://localhost:3000/local/todos                               │
 │   POST   | http://localhost:3000/2015-03-31/functions/create/invocations   │
 │   GET    | http://localhost:3000/local/todos                               │
 │   POST   | http://localhost:3000/2015-03-31/functions/list/invocations     │
 │   GET    | http://localhost:3000/local/todos/{todo_id}                     │
 │   POST   | http://localhost:3000/2015-03-31/functions/get/invocations      │
 │   PUT    | http://localhost:3000/local/todos/{todo_id}                     │
 │   POST   | http://localhost:3000/2015-03-31/functions/update/invocations   │
 │   DELETE | http://localhost:3000/local/todos/{todo_id}                     │
 │   POST   | http://localhost:3000/2015-03-31/functions/delete/invocations   │
 │                                                                            │
 └────────────────────────────────────────────────────────────────────────────┘

Server ready: http://localhost:3000 🚀
Initializing DynamoDB Local with the following configuration:
Port:	8000
InMemory:	true
DbPath:	null
SharedDb:	true
shouldDelayTransientStatuses:	true
CorsParams:	*

```

## Usage

You can create, retrieve, update, or delete todos with the following commands:

### Create a Todo

```bash
curl -X POST http://localhost:3000/dev/todos --data '{ "text": "Learn Serverless" }'
```

No output

### List all Todos

```bash
curl http://localhost:3000/dev/todos
```

Example output:
```bash
[{"text":"Deploy my first service","id":"ac90feaa11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","id":"206793aa11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

### Get one Todo

```bash
# Replace the <id> part with a real id from your todos table
curl http://localhost:3000/dev/todos/<id>
```

Example Result:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":false,"updatedAt":1479138570824}%
```

### Update a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X PUT http://localhost:3000/dev/todos/<id> --data '{ "text": "Learn Serverless", "checked": true }'
```

Example Result:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

### Delete a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE http://localhost:3000/dev/todos/<id>
```

No output
