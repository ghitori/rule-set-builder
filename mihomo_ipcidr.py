import os
import sys
import yaml
from env import *

args = sys.argv[1:]

def get_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        list = f.read().splitlines()
    return list


def build_rule_set(rule):
    try:
        ipcidr_files_path = eval(rule).get("ipcidr")
        ipcidr = []
        if ipcidr_files_path:
            if isinstance(ipcidr_files_path, list):
                for file_path in ipcidr_files_path:
                    ipcidr += get_list(file_path)
            else:
                ipcidr += get_list(ipcidr_files_path)
        if len(ipcidr) == 0:
            print(f"No avaliable rule for {rule}")
            return
        rule_set = {
            "payload": ipcidr
        }
        with open(f"./out/mihomo-ipcidr.yaml", "w") as f:
            yaml.dump(rule_set, f)
        print(f"Success build rule-set for {rule}")
        
    except:
        print(f"Unknow config: {rule}")


if len(args) == 0:
    print("Missing args")
    exit(1)

for rule in args:
    build_rule_set(rule)