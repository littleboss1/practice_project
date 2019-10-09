#!/usr/bin/env python
#coding=utf-8
#__author__="little boss"

import sys
import dns.resolver

iplist = []

def get_iplist(domain):
    try:
        A = dns.resolver.query(domain,"A")
    except:
        print('dns reslover fail')
        return 2
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                iplist.append(j.address)
    return 1


try:
    appdomain = sys.argv[1]
except:
    appdomain = None

if __name__ == "__main__":
    if appdomain is None:
        print(3)
    if get_iplist(appdomain) and len(iplist) > 0:
        print(1)
    else:
        print(2)

