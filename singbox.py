import os
import sys
import json
import awavenue_format
from env import *

args = sys.argv[1:]

def get_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        list = f.read().splitlines()
    return list


def build_rule_set(rule):
    try:
        rule_set = {"version":2, "rules": [{}]}
        ipcidr_files_path = eval(rule).get("ipcidr")
        ipcidr = []
        if ipcidr_files_path:
            if isinstance(ipcidr_files_path, list):
                for file_path in ipcidr_files_path:
                    ipcidr += get_list(file_path)
            else:
                ipcidr += get_list(ipcidr_files_path)
        if len(ipcidr) != 0:
            rule_set["rules"][0]["ip_cidr"] = ipcidr

        domain_files_path = eval(rule).get("domain")
        domain = []
        if domain_files_path:
            if isinstance(domain_files_path, list):
                for file_path in domain_files_path:
                    domain += get_list(file_path)
            else:
                domain += get_list(domain_files_path)
        if len(domain) != 0:
            rule_set["rules"][0]["domain"] = domain
        domain_regex_files_path = eval(rule).get("domain_regex")
        domain_regex = []
        if domain_regex_files_path:
            if isinstance(domain_regex_files_path, list):
                for file_path in domain_regex_files_path:
                    domain_regex += get_list(file_path)
            else:
                domain_regex += get_list(domain_regex_files_path)
            domain_regex_format = []
            for i in domain_regex:
                print(i)
                domain_regex_format.append(awavenue_format.regex(i))
        if len(domain) != 0:
            rule_set["rules"][0]["domain_regex"] = domain_regex_format

        with open(f"./out/singbox.json", "w") as f:
            json.dump(rule_set, f, indent=4)
        print(f"Success build rule-set for {rule}")
        
    except:
        print(f"Unknow config: {rule}")


if len(args) == 0:
    print("Missing args")
    exit(1)

for rule in args:
    build_rule_set(rule)
