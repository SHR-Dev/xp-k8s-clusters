from git import Repo
from requests import get,post
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

token = post(
    f'{api}/users/{user}/tokens',
    json={"name":''.join(random.choice(string.ascii_letters) for i in range(10))},
    auth = auth ).json().get('sha1')

headers={'Authorization': f'token {token}'}

response = post(
    f'{api}/admin/users/{user}/orgs',
    headers = headers,
    json={
        'username': 'bootstrap'
    }
)

src_repos = [
'https://github.com/SHRGroup/oscal-cli',
'https://github.com/mruge-shr/xp-k8s-clusters'
]
for src_repo in src_repos:
    with TemporaryDirectory() as repo_dir:
        name = src_repo.split('/')[-1]
        response = post(
            f'{api}/orgs/{org}/repos',
            headers = headers,
            data={'name':name}
        )
        source = Repo.clone_from(src_repo, repo_dir)
        source.create_remote('gitea', url=f'http://{user}:{password}@{host}/{org}/{name}.git')
        source.remotes.gitea.push()

