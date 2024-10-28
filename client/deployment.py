import os
from ghapi.core import GhApi

owner,repo = os.environ['REPO'].split('/')
run_id = os.environ['WANDB_RUN_ID']
pr_num = os.environ['PR_NUM']
registry_url = os.environ['REGISTRY_URL']
environment = os.getenv('DEPLOY_ENVIRONMENT', 'staging')

gapi = GhApi(owner=owner, repo=repo)
branch_name = gapi.pulls.get(pr_num).head.ref


deploy = gapi.repos.create_deployment(ref=branch_name,
                                       environment=environment,
                                       auto_merge=False,
                                       payload={'run_id': run_id, 'registry_url':registry_url})

status = gapi.repos.create_deployment_status(deployment_id=deploy.id,
                                             environment=environment,
                                             log_url=registry_url,
                                             state='success')
