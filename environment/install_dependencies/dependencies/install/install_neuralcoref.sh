#!/usr/bin/env bash
cd ../third-party-software/
git clone https://github.com/julianser/neuralcoref
cd neuralcoref
git reset --hard 5a2520e6be7aeee3baa4ae5b1e9a2140758800fd # Revert to stable version we are using
sudo pip3 install .
cd ../../install