import json

# Load config data
with open('config.json', 'r') as f:
    config = json.load(f)

# Replace placeholders in the template
def generate_readme():
    with open('README_template.md', 'r') as f:
        readme = f.read()

    readme = readme.replace('{{name}}', config['name'])
    readme = readme.replace('{{location}}', config['location'])
    readme = readme.replace('{{occupation}}', config['occupation'])
    readme = readme.replace('{{studying}}', config['studying'])
    readme = readme.replace('{{primary_interest}}', config['interests']['primary'])
    readme = readme.replace('{{secondary_interest}}', config['interests']['secondary'])

    skills = "\n".join([f"![{skill}](https://img.shields.io/badge/{skill.replace(' ', '%20')}-100000?style=for-the-badge&logo={skill.lower()}&logoColor=white)" for skill in config['skills']])
    readme = readme.replace('{{skills}}', skills)

    main_projects = "\n".join([f"- **[{project['name']}]({project['url']})**" for project in config['main_projects']])
    readme = readme.replace('{{main_projects}}', main_projects)

    other_projects = "\n".join([f"- **[{project['name']}]({project['url']})**" for project in config['other_projects']])
    readme = readme.replace('{{other_projects}}', other_projects)

    readme = readme.replace('{{public_repos}}', str(config['public_repos']))
    readme = readme.replace('{{private_repos}}', str(config['private_repos']))
    readme = readme.replace('{{total_commits}}', str(config['total_commits']))

    # Write the updated README
    with open('README.md', 'w') as f:
        f.write(readme)

# Run the function
generate_readme()
