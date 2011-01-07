from fabric.api import cd, env, run


env.hosts = [
    'philosophie@174.123.227.198',
]

def deploy_staging():
    """Deploys a branch (defaults to staging branch) to the staging server."""
    branch = 'paypal-ipn'

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
