#!/bin/bash

echo "Setting up repo"

cd /root

git clone https://$GHA_TOKEN@github.com/modelia-ai/mvp.git 

cd mvp
