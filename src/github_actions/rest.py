#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from os import getenv

import requests
from requests.auth import HTTPBasicAuth

from .pyside2 import *
from .workflowrun import WorkflowRunsModel


class Rest(QObject):
    # static attributes
    owner = "remico"
    token = getenv('GITHUB_TOKEN')
    auth = HTTPBasicAuth(owner, token)
    api_url = f"https://api.github.com/repos/{owner}"

    # methods
    def __init__(self, repo, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.s = requests.Session()

        self.m_workflowruns = WorkflowRunsModel(self)

    def do_request(self, action: str, url: str, **kw):
        print(f"API * {action.upper()}:", url)
        try:
            url = Rest.api_url + f"/{self.repo}/{url}"
            if 'auth' not in kw:
                kw['auth'] = Rest.auth

            if action.lower() == 'delete':
                r = self.s.delete(url, **kw).text
            if action.lower() == 'post':
                r = self.s.post(url, **kw).text
            else:  # GET by default
                r = self.s.get(url, **kw).text

            return r
        except requests.exceptions.RequestException as e:
            print("ERROR: ", e)
            sys.exit(1)

    # properties
    @PS2Property(WorkflowRunsModel, constant=True)
    def WorkflowRuns(self):
        return self.m_workflowruns

    @PS2Property(str, constant=True)
    def REPO(self):
        return self.repo
