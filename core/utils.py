import os

from github import Github


def get_issue_title(url):
    github_handle = Github(os.environ.get('GITHUB'))
    url = url.split("/")
    repo_name = "/".join(url[3:5])
    repository = github_handle.get_repo(repo_name)
    issue = repository.get_issue(number=int(url[-1]))
    return issue.title
