#!/usr/bin/env bash
for account in $(cat src/accounts.txt)
do

    docker-compose up
done
