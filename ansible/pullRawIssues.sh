#!/bin/bash

source .env

current_time=$(date "+%Y.%m.%d-%H.%M.%S")

perceval github ansible ansible \
    --category issue  \
    --tag bug  \
    --sleep-for-rate  \
    -t "$GITHUB_API_TOKEN" \
    --json-line \
    --archive-path perceval_archive \
    --fetch-archive \
    -o "raw/raw_issues-$current_time" 

