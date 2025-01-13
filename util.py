import argparse
import re
import sys
from pathlib import Path


timestamp_pattern = re.compile(r"\b\d{2}:\d{2}:\d{2}\b")
ipv4_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
ipv6_pattern = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b")

def parse_args():
    parser = argparse.ArgumentParser(
        description="A utility for parsing log files.",
        usage="./util.py [OPTION]... [FILE]",
    )
    parser.add_argument("file", nargs="?", type=str, help="Path to the log file.")
    parser.add_argument("-f", "--first", type=int, help="Print first NUM lines.")
    parser.add_argument("-l", "--last", type=int, help="Print last NUM lines.")
    parser.add_argument(
        "-t", "--timestamps", action="store_true", help="Print lines with timestamps."
    )
    parser.add_argument(
        "-i", "--ipv4", action="store_true", help="Print lines with IPv4 addresses."
    )
    parser.add_argument(
        "-I", "--ipv6", action="store_true", help="Print lines with IPv6 addresses."
    )
    
    return parser.parse_args()

def read_lines(file_path):
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        sys.exit(f"Error: File '{file_path}' not found.")

def filter_lines(lines, pattern):
    return [line for line in lines if pattern.search(line)]

def main():
    args = parse_args()

    if args.file:
        lines = read_lines(args.file)
    else:
        lines = sys.stdin.readlines()

    if args.first:
        lines = lines[: args.first]
    if args.last:
        lines = lines[-args.last :]
    if args.timestamps:
        lines = filter_lines(lines, timestamp_pattern)
    if args.ipv4:
        lines = [re.sub(ipv4_pattern, lambda m: f"\033[92m{m.group(0)}\033[0m", line) for line in filter_lines(lines, ipv4_pattern)]
    if args.ipv6:
        lines = [re.sub(ipv6_pattern, lambda m: f"\033[92m{m.group(0)}\033[0m", line) for line in filter_lines(lines, ipv6_pattern)]

    sys.stdout.writelines(lines)

if __name__ == "__main__":
    main()
