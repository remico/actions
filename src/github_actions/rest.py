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
        try:
            url = Rest.api_url + f"/{self.repo}/{url}"
            print(f"* API: {action.upper()} @ {url}")

            if 'auth' not in kw:
                kw['auth'] = Rest.auth

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
    @PS2Property(WorkflowRunsModel, constant=True)
    def WorkflowRuns(self):
        return self.m_workflowruns

    @PS2Property(str, constant=True)
    def REPO(self):
        return self.repo
