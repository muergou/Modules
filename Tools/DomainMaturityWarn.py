#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
sys.path.append('..')


def ComposrSql(domain):
    sql = "SELECT * FROM DOMAINS WHETE domain_neme=%s" % domain
