from fabric.api import env
from fabric.context_managers import cd
from fabric.decorators import hosts
from fabric.operations import prompt, run


env.hosts = [
    'philosophie@174.123.227.198',
]
env.password = 'abbyd000'

@hosts('philosophie@174.123.227.198')
def deploy_staging(branch=None):
    """Deploys a branch (defaults to staging branch) to the staging server."""
    if not branch:
        branch = prompt('Deploy what branch?', default='staging')

    # Check out and update the branch to deploy
    with cd('~/webapps/buythebay/buybay/'):
        run('git status')
        run('git fetch')
        run('git checkout %s' % branch)
        run('git merge origin/%s' % branch)
        run('python2.6 manage.py syncdb')
        run('python2.6 manage.py migrate')

    # Kick apache
    with cd('~/webapps/buythebay/apache2/bin'):
        run('./restart')
