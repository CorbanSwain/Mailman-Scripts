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


def get_admin_url(list_name):
    mm_root = 'http://mailman.mit.edu/mailman/'
    return mm_root + 'admin/' + list_name


def get_page_members(url):
    soup = get_soup(url)
    rows = [r for r in soup.find_all('tr') if '@' in r.text]
    emails = [list(r.children)[3].text.strip() for r in rows]
    return emails


def get_all_members(list_name):
    list_pass = input('What is the "%s" list password?' % list_name)
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
        new_emails.append('@'.join([head, tail.lower()]))
    new_emails = set(new_emails)
    return new_emails


if __name__ == "__main__":
    list_name = 'bgsa'
    print('\n')
    print('Fetching Members for list: {:s}'.format(list_name))
    all_emails = refine_email_list(get_all_members(list_name))
    pp.pprint('corbanswain@gmail.com' in all_emails)
    pp.pprint('Number of total emails: %d' % len(all_emails))
