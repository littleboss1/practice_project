
#!/usr/bin/env python
#!coding=utf-8
import os
import time
import datetime

Src_Dir = "/data/auto_log/data_log"

def Confirm_Dir():
    Current_Dir = os.getcwd()
    if Current_Dir == Src_Dir:
        pass
    else:
        os.chdir(Src_Dir)


Date_time = int((datetime.datetime.now() - datetime.timedelta(days=8)).timestamp())
Confirm_Dir()
for file in os.listdir():
    if os.path.isfile(file) is True:
        if int(os.stat(file).st_atime) < Date_time:
            print("remove file is %s",file)
            os.remove(file)
                                                

