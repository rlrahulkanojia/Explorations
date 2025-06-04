#!/bin/bash

echo "Setting up repo"

cd /root

touch test.txt

git clone https://$GHA_TOKEN@github.com/modelia-ai/mvp.git 

cd mvp
