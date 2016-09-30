#!/usr/bin/env python

import os
import wmi
import time
import socket
import smtplib
import logging
from email.mime.text import MIMEText


def get_stop_service(designation):
    """To obtain a list of running the service name,
    check whether the monitoring server is present in the list.
    """
    lines = os.popen('net start').readlines()
    line = [item.strip() for item in [i for i in lines]]
    if designation in line:
        return True
    else:
        logging.error('Service [%s] is down, try to restart the service. \r\n' % designation)
        return False

def monitor(sname):
    """Send the machine IP port 20000 socket request,
    If capture the abnormal returns false.
    """
    s = socket.socket()
    s.settimeout(3)  # timeout
    host = ('127.0.0.1', 20000)
    try:  # Try connection to the host
        s.connect(host)
    except socket.error as e:
        logging.warning('[%s] service connection failed: %s \r\n' % (sname, e))
        return False
    return True


def restart_service(rstname, conn, run):
    """First check whether the service is stopped,
    if stop, start the service directly.
    The check whether the zombies,
    if a zombie, then restart the service.
    """
    flag = False
    try:
        # From get_stop_service() to obtain the return value, the return value
        if not run:
            ret = os.system('sc start "%s"' % rstname)
            if ret != 0:
                raise Exception('[Errno %s]' % ret)
            flag = True
        elif not conn:
            retStop = os.system('sc stop "%s"' % rstname)
            retSart = os.system('sc start "%s"' % rstname)
            if retSart != 0:
                raise Exception('retStop [Status code %s] '
                                'retSart [Status code %s] ' % (retStop, retSart))
            flag = True
        else:
            logging.info('[%s] service running status to normal' % rstname)
            return True
    except Exception as e:
        logging.warning('[%s] service restart failed: %s \r\n' % (rstname, e))
        return flag


def send_mail(to_list, sub, contents):
    """
    Send alarm mail.
    """
    mail_server = 'mail.stmp.com'  # STMP Server
    mail_user = 'YouAccount'  # Mail account
    mail_pass = 'Password'  # password
    mail_postfix = 'smtp.com'  # Domain name

    me = 'Monitor alarm<%s@%s>' % (mail_user, mail_postfix)
    message = MIMEText(contents, _subtype='html', _charset='utf-8')

    message['Subject'] = sub
    message['From'] = me
    message['To'] = ';'.join(to_list)

    flag = False  # To determine whether a mail sent successfully
    try:
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, message.as_string())
        s.close()
        flag = True
    except Exception, e:
        logging.warning('Send mail failed, exception: [%s]. \r\n' % e)

    return flag


def main(sname):
    """Parameter type in the name of the service need to monitor,
    perform functions defined in turn, and the return value is correct.
    After the program is running, will test two times,
    each time interval to 10 seconds.
    """
    retry = 2
    count = 0
    retValue = False  # Used return to the state of the socket
    while count < retry:
        ret = monitor(sname)
        if not ret:  # If socket connection is normaol, return retValue
            retValue = ret
            return retValue
        isDown = get_stop_service(sname)
        restart_service(rstname=sname, conn=ret, run=isDown)

        host = socket.gethostname()
        address = socket.gethostbyname(host)
        mailto_list = ['mail@smtp.com', ]  # Alarm contacts
        send_mail(mailto_list,
                  'Alarm',
                  ' <h4>Level: <u>ERROR</u></br> Host name: %s</br>'
                  ' IP Address: %s</br>'
                  ' Service name:</h4> <h5>%s</h5>'
                  % (host, address, sname))
        count += 1
        time.sleep(10)
    else:
        logging.error('[%s] service try to restart more than three times \r\n' % sname)

    return retValue


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename='D:\\logs\\Monitor.log',
                        filemode='ab')

    name = 'Service Name'
    response = main(name)
    if response:
        logging.info('The [%s] service connection is normal \r\n' % name)
