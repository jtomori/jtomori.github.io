import os
import re
import sys
import glob
import requests
from concurrent.futures import ThreadPoolExecutor


AGENT = os.getenv("AGENT", "Mozilla/5.0 ()")


def get_status(link):
    """Return a 2-tuple, first item is a bool whether the check has passed, the second is int with the status code."""
    status = requests.head(link, headers={"User-Agent": AGENT}).status_code

    if status in [200, 301, 302, 303]:
        return True, status
    
    return False, status


def main():
    html_files = glob.glob("**/*.html", recursive=True)

    links = []
    re_link = re.compile("http[s]?://[a-zA-Z0-9./~=?_%:#-]*")

    for html_file in html_files:
        with open(html_file, encoding="utf-8") as f:
            contents = f.read()
        
        links += re_link.findall(contents)
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        codes_generator = executor.map(get_status, links)

    codes_checks = list(codes_generator)

    all_good = True
    for i, (passed, code) in enumerate(codes_checks):
        if not passed:
            print(f"Fail: {links[i]} ({code})")
            all_good = False
    
    if not all_good:
        sys.exit(1)


if __name__ == "__main__":
    main()
