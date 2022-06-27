#!/bin/sh

filtered_args=()

last_arg_was_opt=

for entry in "$@"
do
    if [[ -n "$last_arg_was_opt" && -z "$entry" ]]; then
        unset 'filtered_args[${#filtered_args[@]}-1]'
    else
        filtered_args+=("$entry")
    fi

    if [[ $entry = -* ]]; then
        last_arg_was_opt=yes
    else
        last_arg_was_opt=
    fi
done

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

$SCRIPT_DIR/dataset_verify.py "${filtered_args[@]}"

