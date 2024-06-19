import os
import json
import requests
from github import Github, InputGitAuthor

# Load config data
with open('config.json', 'r') as f:
    config = json.load(f)

# Fetch GitHub data
g = Github(os.getenv("PRIVATE_KEY"))
user = g.get_user()
repos = user.get_repos()

public_repos = user.public_repos
private_repos = user.owned_private_repos
total_commits = sum(repo.get_commits().totalCount for repo in repos)

# Read the README template
with open('README_template.md', 'r') as f:
    readme = f.read()

# Update placeholders in the template
readme = readme.replace('{{name}}', config['name'])
readme = readme.replace('{{location}}', config['location'])
readme = readme.replace('{{occupation}}', config['occupation'])
readme = readme.replace('{{studying}}', config['studying'])
readme = readme.replace('{{primary_interest}}', config['interests']['primary'])
readme = readme.replace('{{secondary_interest}}', config['interests']['secondary'])

# Update skills
skills = "\n".join([f"![{skill}](https://img.shields.io/badge/{skill.replace(' ', '%20')}-100000?style=for-the-badge&logo={skill.lower()}&logoColor=white)" for skill in config['skills']])
readme = readme.replace('{{skills}}', skills)

# Update projects
main_projects = "\n".join([f"- **[{project['name']}]({project['url']})**" for project in config['main_projects']])
readme = readme.replace('{{main_projects}}', main_projects)

other_projects = "\n".join([f"- **[{project['name']}]({project['url']})**" for project in config['other_projects']])
readme = readme.replace('{{other_projects}}', other_projects)

# Update GitHub data
readme = readme.replace('{{public_repos}}', str(public_repos))
readme = readme.replace('{{private_repos}}', str(private_repos))
readme = readme.replace('{{total_commits}}', str(total_commits))

# Write the updated README
with open('README.md', 'w') as f:
    f.write(readme)

# Commit changes back to GitHub
repo = g.get_repo("hsratneshsci/hsratneshsci")
with open('README.md', 'r') as file:
    content = file.read()

repo.update_file(
    path="README.md",
    message="Updated README with latest data",
    content=content,
    sha=repo.get_contents("README.md").sha,
    branch="main",
    author=InputGitAuthor("Your Name", "your-email@example.com")
)
