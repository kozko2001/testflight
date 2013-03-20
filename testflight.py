#!/usr/bin/env python

from subprocess import Popen
import os
import sys
import glob
from optfunc import optfunc
import json

def execute(cmd, cwd):
    print cmd
    h = Popen(cmd, cwd=cwd, shell=True)
    h.wait()
    return h.returncode

def exit(msg):
    print "ERROR: ", msg
    sys.exit(1)



def testflight(project_folder, comment="", configuration="DEBUG",
        distribution=None, config="/etc/testflight/testflight.json",
        testflight_token="", testflight_team="", testflight_distributionlist=""):
    "Usage: testflight %xcode_proj_folder testflight_comment"

    if os.path.exists(config):
        config_values = json.load(open(config))
        config_values = filter(lambda e: e["name"] == project_folder, config_values)
        if len(config_values) > 0:
            config_value = config_values[0]
            project_folder = config_value["project"]
            testflight_token = config_value["testflight_token"]
            testflight_team  = config_value["testflight_team"]
            testflight_distributionlist = config_value["testflight_distributionlist"]



    project_folder = os.path.abspath(project_folder)
    build_folder ="%s/build" % project_folder
    ipa_file = "%s/build/app.ipa" % (project_folder)

    # Step 1) xcodebuild
    cmd = "xcodebuild -configuration %s" % ( configuration) 
    value = execute(cmd, project_folder)

    if value != 0:
        exit("ERROR step1 (xcodebuild)")


    # Step 2) xcrun
    files = []
    for root, dirnames, filenames in os.walk(build_folder):
        files.extend(glob.glob(root+ "/*.app"))
    if len(files) > 0:
        app_file = files[0]
    else:
        exit("ERROR step2.1 finding the app file... ")

    cmd = "xcrun --sdk iphoneos PackageApplication -v %s -o %s" % (app_file, ipa_file)
    value = execute(cmd, project_folder)

    if value != 0:
        exit("ERROR step2.2 (xcrun)")

    if testflight_token == "" or testflight_team == "" or comment == "":
        exit("Cannot upload without testflight_token and testflight_team please fill your conf file: %s" % config)

    cmd = "curl http://testflightapp.com/api/builds.json  -F file=@'%s' -F api_token='%s' -F team_token='%s' -F notes='%s'" % (ipa_file, testflight_token, testflight_team, comment)

    if testflight_distributionlist != "":
        cmd ="%s -F distribution_lists='%s'" % (cmd, testflight_distributionlist)

    value = execute(cmd, project_folder)

if __name__ == "__main__":
    optfunc.run(testflight)
