#!/bin/sh

env

for var in "$@"
do
    echo "HERE: '$var'"
done

exit 1
