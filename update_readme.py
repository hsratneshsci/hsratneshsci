import json

# Load config data
with open('config.json', 'r') as f:
    config = json.load(f)

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

# Write the updated README
with open('README.md', 'w') as f:
    f.write(readme)
