#!/usr/bin/env python

import argparse
import json
import subprocess
import sys
import traceback

class Verifier():
    @staticmethod
    def less_than(target):
        return Verifier("less than", target)

    @staticmethod
    def equal_to(target):
        return Verifier("equal to", target)

    @staticmethod
    def greater_than(target):
        return Verifier("greater than", target)
    
    def __init__(self, op_name, target):
        self.op_name = op_name
        self.target = target

    def apply(self, actual):
        if self.op_name == 'less than':
            return actual < self.target
        elif self.op_name == 'greater than':
            return actual > self.target
        elif self.op_name == 'equal to':
            return actual == self.target
        else:
            raise ValueError(f"Unknown operation name: {self.op_name}")
   
    def __str__(self):
        return f"{self.op_name} {self.target}"

def verify(tool_path, scalyr_server, token, query, verifier, purpose, start, end):
    try:
        process = subprocess.Popen([tool_path, '--token', token, '--server', scalyr_server, '--start', start, '--end', end, '--output', 'json', 'power-query', query],
                                   stdout=subprocess.PIPE, text=True)
        query_stdout, query_stderr = process.communicate()
        exit_code = process.wait()
        if exit_code != 0:
            print(f"The scalyr tool returned a non-zero exit code: {exit_code}", file=sys.stderr)
            print("The stdout and stderr was:", file=sys.stderr)
            print(query_stdout, file=sys.stderr)
            print(query_stderr, file=sys.stderr)
            return exit_code
        query_result = json.loads(query_stdout)

        if query_result['status'] != 'success':
            print(f"Server returned non-success: {query_result['status']}", file=sys.stderr)
            return 1

        if query_result['omittedEvents'] > 0:
            print(f"Failing since query could not process all data.  Omitted events: {query_result['omittedEvents']}", file=sys.stderr)
            return 1

        if len(query_result['warnings']) > 0:
            print(f"Failing since query returned warnings: {query_result['warnings']}", file=sys.stderr)
            return 1

        actual_row_count = len(query_result['values'])
        if not verifier.apply(actual_row_count):
            print(f"Check to verify {purpose} failed.  Query returned {actual_row_count} rows when expected {verifier}.", file=sys.stderr)
            return 1
        print(f"Check to verify {purpose} succeeded.  Query returned {actual_row_count} rows which met the expection of {verifier}.")
        return 0
            
    except Exception as e:
        print("Failed to execute the query due to an exception")
        print(traceback.format_exc(), file=sys.stderr)
        print("The stdout and stderr was:", file=sys.stderr)
        print(query_stdout, file=sys.stderr)
        print(query_stderr, file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-tp", "--tool-path", type=str, help="The path to the scalyr-tool script", default="./scalyr")
    parser.add_argument("-t", "--token", type=str, help="", required=True)
    parser.add_argument("--scalyr-server", type=str, help="", default="https://www.scalyr.com")
    parser.add_argument("-p", "--purpose", type=str, default="required query")
    parser.add_argument("-s", "--start", type=str, help="", default="4h")
    parser.add_argument("-e", "--end", type=str, help="", default="now")
    parser.add_argument("query", type=str, help="")

    verify_option_group = parser.add_mutually_exclusive_group(required=True)
    verify_option_group.add_argument("-eq", "--row-count-eq", type=int, help="")
    verify_option_group.add_argument("-lt", "--row-count-lt", type=int, help="")
    verify_option_group.add_argument("-gt", "--row-count-gt", type=int, help="")

    args = parser.parse_args()

    if not args.row_count_eq is None:
        verifier = Verifier.equal_to(args.row_count_eq)
    elif not args.row_count_lt is None:
        verifier = Verifier.less_than(args.row_count_lt)
    elif not args.row_count_gt is None:
        verifier = Verifier.greater_than(args.row_count_gt)

    return verify(args.tool_path, args.scalyr_server, args.token, args.query, verifier, args.purpose, args.start, "" if args.end == "now" else args.end)
    
    # Arguments
    # location of scalyr tool script
    # query
    # row_count_equals
    # row_count_less_than
    # row_count_greater_than
    # api key
    # scalyr server
    # purpose
    
if __name__ == '__main__':
   sys.exit(main())
