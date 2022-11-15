from git import Repo
import requests 
from requests.auth import HTTPBasicAuth
from tempfile import TemporaryDirectory
import random, string 

# Create Remote Repo
host = 'localhost:9000'
api = f'http://{host}/api/v1'
user = 'gitea_admin'
password = 'r8sA8CPHD9!bt6d'
auth = HTTPBasicAuth(user, password)
org = 'bootstrap'

token = requests.post(
    f'{api}/users/{user}/tokens',
    json={"name":''.join(random.choice(string.ascii_letters) for i in range(10))},auth = auth ).json().get('sha1')
headers={'Authorization': f'token {token}'}

response = requests.post(
    f'{api}/admin/users/{user}/orgs',headers = headers,
    json={
        'username': 'bootstrap'
    })

def post(path,data):
    response = requests.post(path, headers=headers,json=data)
    if int(response.status_code) < 400:
        return True
    else:
        return False

src_repos = [
'https://github.com/SHRGroup/oscal-cli',
'https://github.com/mruge-shr/xp-k8s-clusters'
]
for src_repo in src_repos:
    with TemporaryDirectory() as repo_dir:
        name = src_repo.split('/')[-1]

        # Create Repo
        post(f'{api}/orgs/{org}/repos', {'name':name})
        # Create WebHook
        post(f'{api}/repos/{org}/{name}/hooks', {
            'active': True,
            'config': {
                'url': 'http://webhook-eventsource-svc.default.svc.cluster.local:12000/build',
                'content_type': 'json'
            },
            'type': 'gogs'
        })

        source = Repo.clone_from(src_repo, repo_dir)
        source.create_remote('gitea', url=f'http://{user}:{password}@{host}/{org}/{name}.git')
        source.remotes.gitea.push()




