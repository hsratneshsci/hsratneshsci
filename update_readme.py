import json
import requests

# Load config data
with open('config.json', 'r') as f:
    config = json.load(f)

# Fetch GitHub data
headers = {'Authorization': f'token {config["GITHUB_TOKEN"]}'}
user_response = requests.get('https://api.github.com/user', headers=headers)
repos_response = requests.get('https://api.github.com/user/repos', headers=headers)

user_data = user_response.json()
repos_data = repos_response.json()

public_repos = len([repo for repo in repos_data if not repo['private']])
private_repos = len([repo for repo in repos_data if repo['private']])
total_commits = 0

for repo in repos_data:
    commits_response = requests.get(repo['commits_url'].replace('{/sha}', ''), headers=headers)
    total_commits += len(commits_response.json())

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
