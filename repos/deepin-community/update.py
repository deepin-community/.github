#!/usr/bin/python3
import json
import os
import sys
import requests

ORG = "deepin-community"

# repo that not sync template
excludeRepo = [
    "SIG",
    "deepin-overlay",
    "repo",
    "dde-repo-rebuild",
    "repo",
    "deepin-dde-repo",
    'deepin-dde-deps-repo',
    "create-tag",
    "cla-test",
    "cla-data",
    "deepin-chatopt-script",
    "debian-sid-dde-deps-repo",
    "cla",
    "ci-test",
    "web",
    "push-sleep",
    ".github",
    "de-dock",
    "dde-control-center-plugin-example",
    "debian-sid-dde-repo",
    "deepin-keyring",
    "deepin-kwin-multitasking",
    "deepin-music-pkg",
    "deepin-network-proxy",
    "release",
    "monitorBoard",
    "dtkcore",
    'actions-database',
    "arch-dde-repo",
    "screen-usage-module"
]

api_url = "https://api.github.com/orgs/{ORG}/repos".format(ORG=ORG)
github_token = os.environ.get("GITHUB_TOKEN")

header = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + github_token
}

class repo_workflow:
    def __init__(self, repo, workflows=list()) -> None:
        self.repo = repo
        self.workflows = list()
        for workflow in workflows:
            self.workflows.append(workflow.get("src").split('/')[-1])
        self.added_workflow = list(workflows)

    def add_workflow(self, workflows):
        for workflow in workflows:
            src_workflow_path = "workflow-templates/" + workflow
            dest_workflow_path = ORG + "/" + self.repo + "/.github/workflow/" + workflow
            if not os.path.exists(src_workflow_path):
                print(workflow + " do not exists!")
                continue
            if workflow not in self.workflows:
                print(src_workflow_path, dest_workflow_path)
                self.added_workflow.append({
                    "branch": ["master"],
                    "src": src_workflow_path,
                    "dest": dest_workflow_path
                })
            else:
                print(workflow + " has already added in this repo: " + self.repo)
    
    def write_workflow(self):
        print(id(self.added_workflow))
        with open("repos/" + ORG + "/" + self.repo + ".json", "w+") as f:
            f.write(json.dumps(self.added_workflow, indent=2, separators=(',', ': ')))

# 获取组织下的所有仓库
def getRepos(repo_type="public", size=100):
    repos = []
    page = 1
    while True:
        res = requests.get(url=api_url, headers=header,params={
            "type": repo_type,
            "per_page": size,
            "page": page
        }).json()
        page +=1
        for repo in res:
            repo = repo.get("name")
            if (repo not in excludeRepo) and not repo.startswith("sig-"):
                repos.append(repo)
        if len(res) != size: break # request less page size, which means get latest page
    return repos

# 更新每个仓库中的工作流
def update(repo, workflows):
    repo_path_prefix = "repos/" + ORG + "/"
    repo_path = repo_path_prefix + repo + ".json"
    if os.path.exists(repo_path):
        with open(repo_path, "r") as f:
            data = json.load(f)
            repo = repo_workflow(repo, data)
    else:
        repo = repo_workflow(repo)
    repo.add_workflow(workflows)
    repo.write_workflow()


def main():
    workflows = sys.argv[1:]
    repos = getRepos()
    for repo in repos:
        update(repo, workflows)

if __name__=="__main__":
    main()
