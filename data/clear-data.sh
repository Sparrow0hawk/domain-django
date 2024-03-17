#!/usr/bin/env bash

set -e

curl -X DELETE --location "http://127.0.0.1:8000/polls/questions" \
    -H "Authorization: API-key test"
