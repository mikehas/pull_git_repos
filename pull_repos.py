#!/usr/bin/env python
import sys
import os
import subprocess
import re

'''
Edit the repos dictionary below, add, delete, or modify them according to your environment.
'''

repos = {}

repos["REPO_TITLE1"] = {
    "dir": '/gitroot1',
    "checkout": 'branch',
    "merge": 'branch'
}
repos["REPO_TITLE2"] = {
    "dir": '/gitroot2',
    "checkout": 'branch',
    "merge": 'branch'
}
repos["REPO_TITLE3"] = {
    "dir": '/gitroot3',
    "checkout": 'branch',
    "merge": 'branch'
}

def check_output(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def printvars(repo, k):
    print "################# Performing work on " + repo + "#################"
    for key, val in k.items():
        print "\t" + key + ": " + val
    
def cd(dir):
    print "Changing directory to: " + dir
    os.chdir(dir)
    
def pwd_ok(dir):
    return os.getcwd() == dir
        

def gitfetch():
    print "\nFetching latest objects and refs... \n"
    fetchout = check_output(['git', 'fetch'])
    print fetchout
    
def gitbranch():
    print "\nGetting current branch..."
    branchout = check_output(['git', 'branch'])    
    print branchout
    curbranch = re.findall('\* (.*)', branchout)[0]
    
    return curbranch
    
def gitmerge(mergebranch):
    print "\nMerging changes from: " + mergebranch + "..."
    mergeout = check_output(['git', 'merge', mergebranch])    
    print mergeout
    
def gitcheckout(c):
    print "\Checkout out branch: " + c + "..."
    cout = check_output(['git', 'checkout', c])    
    print cout
    
for repo, k in repos.items():
    printvars(repo,k)
    cd(k["dir"])
    if not pwd_ok(k["dir"]):
        continue
    else: 
        print "SUCCESS"
        
    gitfetch()
    curbranch = gitbranch()

    if curbranch != k['checkout']:
        checkout_before_merge = query_yes_no("\nThe current branch, " + curbranch + ", is not the same as your specified checkout branch, " + k['checkout'] + ", would you like to checkout the target branch before merge? ", default="no")
        
        if checkout_before_merge:
            proceed_checkout = query_yes_no("\nI'm about to checkout " + k['checkout'] + ". Continue?", default="no")
            if proceed_checkout:
                gitcheckout(k['checkout'])
        
    proceed_merge = query_yes_no("\nI'm in: " + os.getcwd() + "\nOn branch: " + gitbranch() + "\nMerge changes from:  " + k['merge'] + "\nContinue?", default="no")
    if proceed_merge:
        gitmerge(k['merge'])
