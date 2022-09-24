#!/usr/bin/python3
"""
Deploying tgz file to our servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['34.73.133.125', '52.201.252.232']


def do_deploy(archive_path):
    """deploy web static with fabric"""
    if exists(archive_path) is False:
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_excep = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_excep))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(filename, path, no_excep))
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, no_excep))
        run('sudo rm -rf {}{}/web_static'.format(path, no_excep))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_excep))
        return True
    except BaseException:
        return False
