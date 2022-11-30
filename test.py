#!/usr/bin/python3
import json
import os
import sys
import requests

ORG = "deepin-community"

def main():
    config_dir = "repos/deepin-community/"
    repos = os.listdir(config_dir)
    for repo in repos:
        if not repo.endswith(".json"):
            continue
        with(open(config_dir + repo)) as file:
            print(repo)
            data = json.load(file)
            for workflow in data:
                if workflow.get('src').__eq__('workflow-templates/call-clacheck.yml'):
                    workflow['dest'] = 'deepin-community/' + repo[:-5] + '/.github/workflows/call-clacheck.yml'
        with open("repos/" + ORG + "/" + repo, "w+") as f:
            f.write(json.dumps(data, indent=2, separators=(',', ': ')))

if __name__=="__main__":
    main()
