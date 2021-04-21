#!/usr/bin/env python
# This file is part of tcollector.
# Copyright (C) 2011  The tcollector Authors.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.
"""Collector for checking mail command status"""

import sys
import json
import subprocess
import time
import requests
import socket
import random
import uuid
from collectors.lib import utils



COLLECTION_INTERVAL = 600  # seconds

log_file = '/var/log/mail.log'
log_file_1 = '/var/log/mail.log.1'

def search_word_in_file(search_word, filename):
    with open(filename) as file:
        contents = file.read()
        if search_word in contents:
            return True
        else:
            return False

def main():

    collection_interval=DEFAULT_COLLECTION_INTERVAL

    utils.drop_privileges()

    while True:
        ts = time.time()
        ts_int = int(ts)
        email_ts = str(ts).split('.')[0]
        #print(email_ts)
        mail_to = email_ts + '@houzz.com'
        #print('***Sending email to test user!***')
        mail_cmd = 'echo \'This is a test\' | mail -s \"Sending test email.\" ' + mail_to
        #print(mail_cmd)
        subprocess.run(mail_cmd, shell=True)
        time.sleep(15)
        #print('***Check if mail is sent!***')
        if search_word_in_file(mail_to, log_file):
            #print('Mail sent successfully!')
            #print('Log found in /var/log/mail.log!')
            print ("mail_cmd_failure %d %s" % (ts_int, 0))
        elif search_word_in_file(mail_to, log_file_1):
            #print('Mail sent successfully!')
            #print('Log found in /var/log/mail.log.1!')
            print ("mail_cmd_failure %d %s" % (ts_int, 0))
        else:
            #print('Failed to send the mail!')
            print ("mail_cmd_failure %d %s" % (ts_int, 1))

        sys.stdout.flush()
        time.sleep(collection_interval)

if __name__ == "__main__":
    main()
