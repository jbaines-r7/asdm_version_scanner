import requests
import sys
import csv
import re
import string
import argparse
from urllib.parse import quote

requests.packages.urllib3.disable_warnings()

def fetch_data(ip, port):
    try:
        session = requests.Session()
        asdm_endpoint = "https://" + ip + ":" + port + "/admin/public/index.html"
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
            'Accept-Encoding':'gzip, deflate, br'
        }
        print("Try " + asdm_endpoint, file=sys.stderr)
        response = session.get(asdm_endpoint, headers=headers, verify=False, timeout=4)
        if response.status_code == 200:
            re_result = re.findall(r'<title>(.*)</title>', response.text)
            if (len(re_result) == 1):
                print(ip + "," + port + "," + re_result[0], file=sys.stdout, flush=True)
                return
    except:
        pass

    print("Error for " + ip + "," + port, file=sys.stderr)
    return


if __name__ == '__main__':
    top_parser = argparse.ArgumentParser(description='pinkasfloyd.py - Cisco ASDM Endpoint Scanner')
    top_parser.add_argument("--csv", action="store", dest="csv", help="The CSV of addresses to scan")
    args = top_parser.parse_args()

    if args.csv == None:
        print("--csv is a required argument")
        sys.exit(0)

    with open(args.csv, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        for row in csv_data:
            fetch_data(row[0], row[1].strip())

