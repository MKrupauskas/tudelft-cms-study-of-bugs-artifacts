#!/bin/bash

# clone the puppet repo if that's not already done
# git clone git@github.com:puppetlabs/puppet.git
cd puppet

../git-json.sh > commits.json

mv commits.json ../commits.json
cd ..