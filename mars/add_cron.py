#! /usr/bin/env python
# add or update the crontab to avoid the repeat

import getopt
import os
import sys
import subprocess
from os.path import basename
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

HEADER = "### %s - DO NOT REMOVE THIE LINE!"


def add_update_crontab(header, crontask, user=None):
    if len(crontask.split()) < 6:
        raise RuntimeError("invalid cront task '%s'" % crontask)

    cmds = ['crontab', '-l']
    if user is not None:
        cmds = cmds + ['-u', user]
    output = ""
    try:
        output = subprocess.check_output(cmds)
    except:
        pass

    skip_next_line = False
    task_updated = False
    new_crontab = []
    space_line_counter = 0
    for line in output.split("\n"):
        line = line.strip()
        if skip_next_line:
            skip_next_line = False
            continue

        if line.startswith(HEADER % header):
            skip_next_line = True
            new_crontab.append(line)
            new_crontab.append(crontask)
            task_updated = True
        else:
            if len(line) == 0 and space_line_counter >= 1:
                pass
            elif len(line) == 0:
                space_line_counter += 1
                new_crontab.append(line)
            else:
                space_line_counter = 0
                new_crontab.append(line)

    if not task_updated:
        new_crontab.append("\n")
        new_crontab.append(HEADER % header)
        new_crontab.append(crontask)
    
    try:
        f = NamedTemporaryFile(mode='w', delete=False)
        for line in new_crontab:
            f.write("%s\n" % line)
        f.close()
        cmds = ['crontab']
        if user is not None:
            cmds = cmds + ['-u', user]
        cmds.append(f.name)
        subprocess.check_call(cmds)

        if task_updated:
            print("updated the crontab item '%s'" % header)
        else:
            print("added a new crontab item '%s'" % header)
    finally:
        os.unlink(f.name) 


def usage():
    print("""usage: {sname} [-u user] header task

for example:
{sname} -u redis 'redis dump' '2 3 * * * /srv/redis/tool/dump > /dev/null &'
""".format(sname=basename(sys.argv[0])))


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:h")
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(1)

    user = None            
    for o, a in opts:
        if o in ("-h",):
            usage()
            sys.exit(0)
        elif o in ("-u",):
            user = a
        else:
            assert False, "unknow option '%s'" % (o,)

    if len(args) != 2:
        print("invalid input parameters!")
        usage()
        sys.exit(1)

    add_update_crontab(args[0], args[1], user=user)
