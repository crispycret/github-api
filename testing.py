
token = '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'


from github import Github

# using an access token
g = Github(token)
#g = Github("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")

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")


for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    print(dir(repo))
