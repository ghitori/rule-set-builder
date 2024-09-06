import os
import sys
import yaml
import awavenue_format
from env import *

args = sys.argv[1:]

def adblock_convert(lines: list):
    rules = []
    for i in lines:
        if len(i.replace(" ", "")) != 0 and i[0] != "!" :
            temp = i
            if i[:2] == "||" and i[-1:] == "^":
                temp = temp[2:-1]
                rules.append(temp)
    for i in lines:
        if len(i.replace(" ", "")) != 0 and i[0] != "!" :
            temp = i
            if i[:4] == "@@||" and i[-1:] == "^":
                temp = temp[4:-1]
                if temp in rules:
                    rules.remove(temp)
    return rules
    

def get_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        list = f.read().splitlines()
    return list


def build_rule_set(rule):
    try:
        domain_files_path = eval(rule).get("domain")
        domain_regex_files_path = eval(rule).get("domain_regex")
        adblock_files_path = eval(rule).get("adblock")
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
                domain.append(awavenue_format.wildcard(i))
        if adblock_files_path:
            if isinstance(adblock_files_path, list):
                for file_path in adblock_files_path:
                    domain += adblock_convert(get_list(file_path))
            else:
                domain += adblock_convert(get_list(adblock_files_path))
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