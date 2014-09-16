#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

path = sys.argv[1] if len(sys.argv) > 1 else "."

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".avi"):
            original = os.path.join(root, file)
            backup = os.path.join(root, file + ".bak")
            newName = os.path.join(root, file.replace(".avi", ".mp4"))
            print "{0} => {1} => {2}".format(original, backup, newName)
            subprocess.call(["avconv", "-i", original, "-vcodec", "libx264", "-acodec", "copy", newName])
            os.rename(original, backup)