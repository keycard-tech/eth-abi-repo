import argparse
import csv
import json
import os
import requests

def fetch_json(chain, address, apikey, out):
    res = requests.get(f"https://api.etherscan.io/v2/api?module=contract&action=getabi&address={address}&chainid={chain}&apikey={apikey}").json()
    if not res["status"] == "1":
        raise Exception(f"Couldn't fetch ABI for contract {address} from Etherscan")
    with open(out, 'w') as f:
        json.dump(json.loads(res["result"]), f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Fetch and store ABI files from a CSV list')
    parser.add_argument('-l', '--csv-list', help="the CSV list of tokens", default="abi_list.csv")
    parser.add_argument('-k', '--api-key', help="the Etherscan API key file", default=".etherscan_apikey")
    parser.add_argument('-o', '--output', help="the output directory", default="repo")
    args = parser.parse_args()

    api_key = None

    with open(args.api_key, 'r') as f:
        api_key = f.read()

    with open(args.csv_list, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output = os.path.join(args.output, f"{row[0]}.json")
            if not os.path.exists(output):
                fetch_json(row[1], row[2], api_key, output)

if __name__ == "__main__":
    main()