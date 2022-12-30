#！/esr/bin/env python3
from update import excludeRepo, ORG, header
import os
import requests

ORG = "deepin-community"

api_url = "https://api.github.com/repos/" + ORG + "/{repo}"

configs_path = os.path.join("repos", ORG)

# 检查仓库是否存在
#curl https://api.github.com/repos/<user>/<repo>
def check(repo):
    res = requests.get(url=api_url.format(repo=repo), headers=header).json()
    return res.get("id", None) == None

# 清理配置            
def clean(repo):
    json_file = repo + ".json"
    os.remove(os.path.join(configs_path, json_file))

def main():
    for i in os.listdir(configs_path):
        repo = i[:-5]
        if check(repo) or repo in excludeRepo:
            clean(repo)
        else:
            print(repo + " exists")

if __name__=="__main__":
    main()
