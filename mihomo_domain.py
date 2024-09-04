import os
import sys
import yaml
import awavenue_format
from env import *

args = sys.argv[1:]

def get_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        list = f.read().splitlines()
    return list


def build_rule_set(rule):
    try:
        domain_files_path = eval(rule).get("domain")
        domain_regex_files_path = eval(rule).get("domain_regex")
        domain = []
        domain_regex = []
        if domain_files_path:
            if isinstance(domain_files_path, list):
                for file_path in domain_files_path:
                    domain += get_list(file_path)
            else:
                domain += get_list(domain_files_path)
        if domain_regex_files_path:
            if isinstance(domain_regex_files_path, list):
                for file_path in domain_regex_files_path:
                    domain_regex += get_list(file_path)
            else:
                domain_regex += get_list(domain_regex_files_path)
            for i in domain_regex:
                print(i)
                domain.append(awavenue_format.wildcard(i))
        if len(domain) == 0:
            print(f"No avaliable rule for {rule}")
            return
        rule_set = {
            "payload": domain
        }
        with open(f"./out/mihomo-domain.yaml", "w") as f:
            yaml.dump(rule_set, f)
        print(f"Success build rule-set for {rule}")

    except:
        print(f"Unknow config: {rule}")


if len(args) == 0:
    print("Missing args")
    exit(1)

for rule in args:
    build_rule_set(rule)