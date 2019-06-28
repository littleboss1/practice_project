
#!/usr/bin/env python
#!coding=utf-8
#author=little boss
import os
import time
import shutil
import logging
import datetime

Src_Dir = "/data/freeswitch/recordings/archive"
Drc_Dir = "/data/back/"

def Confirm_Dir():
    Current_Dir = os.getcwd()
    if Current_Dir == Src_Dir:
        pass
    else:
        os.chdir(Src_Dir)


Date_time = int((datetime.datetime.now() - datetime.timedelta(days=90)).timestamp())
Confirm_Dir()
for file in os.listdir():
    if os.path.isfile(file) is True:
        print("file is",file)
        if int(os.stat(file).st_atime) < Date_time:
            D_time = int(os.stat(file).st_atime)
            print("file time is",D_time)
            print("curr time is",Date_time)
            T_dir = datetime.datetime.fromtimestamp(D_time).strftime("%Y-%m-%d")
            D_dir = Drc_Dir + T_dir 
            if os.path.isdir(D_dir):
                pass
            else:
                os.mkdir(D_dir)
            print("remove file is %s",file)
            #os.remove(file)
            shutil.move(file,D_dir)
                                                

