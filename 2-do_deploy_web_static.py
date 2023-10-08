#!/usr/bin/python3
""" 
    Fabric script that distributes an archive to your web servers
"""

from fabric.api import *
from os.path import exists
env.hosts = ['52.87.153.255', '54.85.142.216']


def do_deploy(archive_path):
    """
        Function to deploy
    """
    if exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(folder_name, folder_name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(folder_name))
        return True
    except:
        return False
