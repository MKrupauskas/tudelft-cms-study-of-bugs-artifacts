#!/bin/bash

cd ..
# git clone git@github.com:puppetlabs/puppet.git
cd puppet

../tudelft-research/git-json.sh > commits.json

mv commits.json ../tudelft-research/commits.json
cd ../tudelft-research