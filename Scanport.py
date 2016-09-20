#!/usr/bin/env python

import sys
import time
import socket


def getaddresslist(addr):
    """
    getaddresslist(addr) -> IP address file

    IP address read from the file.
    :param addr: IP file
    :return: Scan ip address list, or error message.
    """
    address = []
    try:
        with open(addr, "r") as iplist:
            line = iplist.readlines()
            for item in line:
                address.append(item.strip("\n"))
        return address

    except (IOError, IndexError), e:
        return str(e)


def scan(iplist, port=80):
    """
    scan() -> getaddresslist()

    getaddresslist() function returns the IP address of the list.
    :param iplist: getaddresslist() Function return value.
    :param port: Need to scan the port.
    :return: None
    """
    if not isinstance(iplist, list):
        sys.exit("Function getaddresslist() return error message: %s" % iplist)

    for addr in iplist:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        host = (addr, int(port))
        try:
            s.connect(host)
            print "Host %s:%s connection success." % (host[0], host[1])
        except Exception, e:
            print "Host %s:%s connection failure: %s" % (host[0], host[1], e)

        s.close()


if __name__ == '__main__':

    addrs = sys.argv[1]
    ScanPort = input("Enter the scan port: ")
    Total = input("Enter the scan time <minutes>: ")
    Interval = input("Enter the scanning interval <minutes>: ")
    EndTime = time.time() + Total * 60
    
    while time.time() < EndTime:
        scan(getaddresslist(addrs), ScanPort)
        time.sleep(Interval * 60)
        continue
    else:
        print "\nwhile end."
