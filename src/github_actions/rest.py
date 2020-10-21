#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import getenv

import requests
from requests.auth import HTTPBasicAuth

from .pyside2 import *
from .workflowrun import WorkflowRuns


def uiobject(pType=QObject):
    def w(f):
        prop = PS2Property(pType, constant=True)
        return prop(f)
    return w


class Rest(QObject):
    def __init__(self, repo, owner, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.owner = owner
        self.s = requests.Session()

        self.m_workflowruns = WorkflowRuns(self)

    def do_request(self, action: str, api_url: str, **kw):
        try:
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/{api_url}"
            print(f"* API: {action.upper()} @ {url}")

            if 'auth' not in kw:
                kw['auth'] = HTTPBasicAuth(self.owner, getenv('GITHUB_TOKEN'))

            if headers := kw.get('headers', {}):
                headers['Accept'] = "application/vnd.github.v3+json"

            if action.lower() == 'delete':
                r = self.s.delete(url, **kw)
            if action.lower() == 'post':
                print(f"* payload json: {kw.get('json')}")
                r = self.s.post(url, **kw)
            else:  # GET by default
                r = self.s.get(url, **kw)

            if r.text:
                print("<=", r)

            return r.text
        except requests.exceptions.RequestException as e:
            print("ERROR: ", e)
            sys.exit(1)

    # properties
    @uiobject(WorkflowRuns)
    def UiWorkflowRuns(self):
        return self.m_workflowruns

    @PS2Property(str, constant=True)
    def REPO(self):
        return self.repo
