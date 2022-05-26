#!/bin/bash

source .env

echo "$GITHUB_API_TOKEN"

current_time=$(date "+%Y.%m.%d-%H.%M.%S")

perceval github ansible ansible \
    --category pull_request  \
    --tag bug  \
    --sleep-for-rate  \
    -t "$GITHUB_API_TOKEN" \
    --json-line \
    --archive-path perceval_archive \
    -o "raw/raw_pull_requests-$current_time" 

