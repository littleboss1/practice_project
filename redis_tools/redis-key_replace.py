#!/usr/bin/env python
# coding: utf-8

# In[86]:


#!/usr/bin/python
# 操作前做好redis数据备份
import redis
import re
list_key = []

r = redis.Redis(host='192.168.100.102',port=6379,db=0,password='xxxxxxxxxx')
r_list = r.keys()
for s in r_list:
    try:
    #print(s.decode('utf8'))
    #print(type(s.decode('utf8')))
        if re.match('hs_',str(s.decode('utf8'))):
            pass
        else:
            dd = 'hs_' + str(s.decode('utf8'))
    except  UnicodeDecodeError:
        print("hulu %s" % s)
    except redis.exceptions.ResponseError:
        print("hulu %s" % s)
    else:
        if re.match('hs_',str(s.decode('utf8'))):
            pass
        else:
            r.rename(s,dd)
            list_key.append(dd)
        
print(list_key)

