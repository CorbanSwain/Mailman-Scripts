#!/bin/python3
# mm_members.py


import re
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pprint as pp
import time
import urllib.parse as urlparse
import random
import math
import uuid
import selenium
from utilities import *
from string import ascii_lowercase


def get_password(list_name):
    list_pass = None
    try:
        with open('.mailman', 'r') as mm_fle:
            for line in mm_fle.readlines():
                if line.strip().startswith('#'):
                    continue
                if line.strip().startswith(list_name):
                    list_pass = line.split(':')[1].strip()
    except FileNotFoundError:
        pass

    if not list_pass:
        list_pass = input('What is the "%s" list password?\n\t> ' % list_name)

    return list_pass

def get_admin_url(list_name):
    mm_root = 'http://mailman.mit.edu/mailman/'
    return mm_root + 'admin/' + list_name


def get_page_members(url):
    soup = get_soup(url)
    rows = [r for r in soup.find_all('tr') if '@' in r.text]
    emails = [list(r.children)[3].text.strip() for r in rows]
    return emails


def get_all_members(list_name):
    list_pass = get_password(list_name)
    url_fmt = url_change_query(get_admin_url(list_name) + '/members',
                               adminpw=list_pass,
                               letter='{:s}')
    emails = []
    for letter in ascii_lowercase:
        page_url = url_fmt.format(letter)
        emails += get_page_members(page_url)
    return emails


def refine_email_list(emails):
    new_emails = []
    for email in emails:
        head, tail = email.split('@')
        new_emails.append('@'.join([head.strip(), tail.lower().strip()]))
    new_emails = set(new_emails)
    return new_emails


def subscribe_members(list_name, emails):
    list_pass = get_password(list_name)
    url_fmt = url_change_query(get_admin_url(list_name) + '/members/add',
                               adminpw=list_pass,
                               subscribees='{:s}')

    l1 = len(emails)
    emails = refine_email_list(emails)
    l2 = len(emails)
    if l2 < l1:
        print('%d duplicate emails removed.' % (l1 - l2))
    current_emails = refine_email_list(get_all_members(list_name))
    emails = {email for email in emails if email not in current_emails}
    l3 = len(emails)
    if l3 < l2:
        print('%d emails already in the database removed.' % (l2 - l3))

    print('Subscribing %d emails to the "%s" mailman list.' % (l3, list_name))
    [requests.get(url_fmt.format(email)) for email in emails]

    updated_emails = refine_email_list(get_all_members(list_name))

    [print('%s successfully added.' % email) if email in updated_emails
     else print('%s -- FAILED TO ADD' % email) for email in emails]


if __name__ == "__main__":
    subscribe_members('bgsa', ['DJuan.Sampson@tufts.edu'])
