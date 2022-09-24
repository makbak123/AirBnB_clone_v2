#!/usr/bin/python3
"""
With Facric , creates a tgz archive
from web_static content folder
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Creates a tgz archive using fabric"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception as ex:
        return None
