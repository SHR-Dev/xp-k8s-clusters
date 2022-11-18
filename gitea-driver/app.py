import requests, os, random, string

GITEA_URI = os.environ.get('GITEA_URI','http://mgmt-gitea-http')
GITEA_USERNAME = os.environ.get('GITEA_USERNAME','gitea_admin')
GITEA_PASSWORD = os.environ.get('GITEA_PASSWORD')

api = f"{GITEA_URI}/api/v1"
auth = requests.auth.HTTPBasicAuth(GITEA_USERNAME, GITEA_PASSWORD)


token = requests.post(
    f'{api}/users/{GITEA_USERNAME}/tokens',
    json={"name":''.join(random.choice(string.ascii_letters) for i in range(10))},auth = auth ).json().get('sha1')
headers={'Authorization': f'token {token}'}


def post(path,data):
    response = requests.post(path, headers=headers,json=data)
    print(f"{path} - {response.status_code}")
    if int(response.status_code) < 400:
        return True
    else:
        return False

def create_org(orgname):
    print(f"Creating Org {orgname}")
    post(f'{api}/admin/users/{GITEA_USERNAME}/orgs',
    {'username': orgname})

def create_repo(orgname, reponame):
    print(f"Creating Repo {orgname}/{reponame}")
    post(f'{api}/orgs/{orgname}/repos', {'name':reponame})


ORGNAME  = os.environ.get('ORGNAME', False)
REPONAME = os.environ.get('REPONAME', False)
if ORGNAME and REPONAME:
    create_org(ORGNAME)
    create_repo(ORGNAME, REPONAME)