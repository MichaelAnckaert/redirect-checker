#!/usr/bin/env python3
"""checker.py
Check redirect from a given CSV file 
"""
import argparse
import requests
import csv
import sys

from typing import Optional


def check_redirects(from_url, to_url):
    response = requests.get(from_url, allow_redirects=False)
    if response.status_code == 404:
        print(f"ERROR: 404 response for {from_url}")
    elif response.status_code == 301:
        if to_url != response.next.url:
            print(
                f"ERROR: Wrong 301 redirect for {from_url}! Expected '{to_url}' but got '{response.next_url}'"
            )
        else:
            print(f"SUCCESS: Good redirect for {from_url}")
    else:
        print(f"Wrong response for '{from_url}': status code {response.status_code}")


def get_redirects(
    filename: str,
    skip_header: bool,
    from_domain: Optional[str],
    to_domain: Optional[str],
):
    redirects = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader)

        for from_url, to_url in reader:
            from_url = f"{from_domain}/{from_url}" if from_domain else from_url
            to_url = f"{to_domain}/{to_url}" if to_domain else to_url

            redirects.append((from_url, to_url))

    return redirects


def run(filename, skip_header=False, from_domain=None, to_domain=None):
    try:
        redirects = get_redirects(filename, skip_header, from_domain, to_domain)
    except ValueError:
        print(f"Error processing CSV file '{filename}'. Check file structure.")
        sys.exit(1)

    for from_url, to_url in redirects:
        check_redirects(from_url, to_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Checker",
        description="Check URL redirects based on a given list",
    )
    parser.add_argument("filename")
    parser.add_argument("--skip-header", action="store_true")
    parser.add_argument("--from-domain")
    parser.add_argument("--to-domain")
    args = parser.parse_args()

    run(
        filename=args.filename,
        skip_header=args.skip_header,
        from_domain=args.from_domain,
        to_domain=args.to_domain,
    )
