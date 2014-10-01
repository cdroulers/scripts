#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import fnmatch
import re

parser = argparse.ArgumentParser(description="Convert files recursively in a folder.")
parser.add_argument("path", help="The path to scan")
parser.add_argument("-v", "--vcodec", dest="vcodec", default="copy", help="What to do with the video codec. Default is copy.")
parser.add_argument("-a", "--acodec", dest="acodec", default="copy", help="What to do with the audio codec. Default is copy.")
parser.add_argument("-c", "--container", dest="container", default="mkv", help="Which container to output to. Default is mkv.")
parser.add_argument("-f", "--filter", dest="filter", default="*.*", help="Filter which files to process. Default is *.*.")
parser.add_argument("-nb", "--nobackup", dest="no_backup", action="store_true", help="Does not backup the file.")
parser.add_argument("-wi", "--whatif", dest="what_if", action="store_true", help="Only previews what would happen.")

args = parser.parse_args()

fileRegex = fnmatch.translate(args.filter)

for root, dirs, files in os.walk(args.path):
    for file in files:
        if re.match(fileRegex, file):
            original = os.path.join(root, file)
            print "Processing file " + original
            fileName, extension = os.path.splitext(original)
            tmpFile = os.path.join(root, file.replace(extension, ".tmp" + extension))
            backup = os.path.join(root, file + ".bak")
            newName = os.path.join(root, file.replace(extension, "." + args.container))
            avconv_call = ["avconv", "-i", original, "-vcodec", args.vcodec, "-acodec", args.acodec]
            if args.acodec == "aac":
                avconv_call.append("-strict")
                avconv_call.append("experimental")
            avconv_call.append(tmpFile)
            result = 0
            if args.what_if:
                print "    WHATIF: Would call avconv with the following parameters"
                print "    WHATIF: " + str(avconv_call)
            else:
                result = subprocess.call(avconv_call)

            if result == 0:
                if not args.no_backup:
                    if args.what_if:
                        print "    WHATIF: Would backup %s to %s" % (original, backup)
                    else:
                        os.rename(original, backup)
                if args.what_if:
                    print "    WHATIF: Would rename %s to %s" % (tmpFile, newName)
                else:
                    os.rename(tmpFile, newName)

            print ""