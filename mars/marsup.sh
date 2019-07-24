#!/bin/bash
   
start_up(){
    num=`ps -ef | grep sip_deny_list | grep -v grep | awk '{print $2}'`
    if [ -z "$num" ]; then
        python3 /srv/mars/sip_deny_list.py &
    fi
}

stop_down(){
    num=`ps -ef | grep sip_deny_list | grep -v grep | awk '{print $2}'`
    if [ -n "$num" ]; then
        kill -9 $num
    fi
        
}


case $1 in 
    "start")
        start_up
        echo "mars start success"
        ;;
    "stop")
        stop_down
        echo "mars stop success"
        ;;
    *)
        echo "参数无效"
        ;;
esac
