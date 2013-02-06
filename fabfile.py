from fabric.api import cd, env, run

env.hosts = ['carshare@SOMESERVER:22']

def deploy(version='tip'):
    with cd('~/carshare/'):
        run('hg pull')
        run('hg up {0}'.format(version))
        run('buildout init')
        run('bin/buildout prod')
