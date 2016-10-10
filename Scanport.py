#!/usr/bin/env python

import sys
import time
import socket


def getaddresslist(addr):
    """
    getaddresslist(addr) -> IP address file

    IP address read from the file.
    """
    try:
        with open(addr, "r") as iplist:
            line = iplist.readlines()
            address = [item.strip("\n") for item in line]
        return address
    except (IOError, IndexError), err:
        return str(err)


def scan(iplist, port):
    """
    scan() -> getaddresslist()

    getaddresslist() function returns the IP address of the list.
    """
    if not isinstance(iplist, list):
        sys.exit("Function getaddresslist() return error message: %s" % iplist)
    # start_time = time.time()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    f = open('D:\em_logs\scan.log', 'ab')
    for addr in iplist:
        host = (addr, int(port))
        try:
            s.connect(host)
            f.write("Host %s:%s connection success \r\n" % (host[0], host[1]))
        except Exception, e:
            f.write("Host %s:%s connection failure: %s \r\n" % (host[0], host[1], e))
    f.close()
    s.close()
    # print "Port scanning to complate, Elapsed time: %.2f" % (time.time() - start_time)


def main():
    """
    main() -> Program start

    Program entrance,
    Call the main() function will begin to execute a program.
    """
    addrs = sys.argv[1]
    # scanport = raw_input("Enter the scan port <default is 80 port>: ")
    isNone = True
    while isNone:
        scanport = raw_input('Enter the scan port: ').strip()
        if scanport:
            isNone = False
        else:
            continue
    scan(getaddresslist(addrs), scanport)


if __name__ == '__main__':

    main()
