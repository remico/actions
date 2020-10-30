#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shlex
import subprocess
import sys
from atexit import register as onExit
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from multiprocessing import Process, Pipe
from os import getpgid, getpid

from .path import path
from .pyside2 import *


class PostHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, pipe, *args, **kwargs) -> None:
        self.pipe = pipe
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

        # response = BytesIO()
        # response.write(b'This is POST request. ')
        # response.write(b'Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())

        body = json.loads(body)

        if self.pipe is not None:
            self.pipe.send((body['action'], body['check_run']['status'], body['check_run']['conclusion']))
        else:
            check_run = body['check_run']
            print("-----------------------------------------")
            print("@ check_run webhook received:")
            print("action:", body['action'])
            print("status:", check_run['status'])
            print("conclusion:", check_run['conclusion'])
            print("started_at:", check_run['started_at'])
            print("completed_at:", check_run['completed_at'])
            print("-----------------------------------------")


class HTTPServerProcess(QObject):

    def __init__(self, handler, parent=None) -> None:
        super().__init__(parent)
        self.parent_conn, self.child_conn = Pipe()

        self.notifier = QSocketNotifier(self.parent_conn.fileno(), QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.dataReady)

        self.p = Process(target=handler, args=(self.child_conn,))
        qApp.aboutToQuit.connect(self.p.kill)  # terminate children processes before exit
        self.p.start()

    dataReady = PS2Signal()

    def read(self):
        return self.parent_conn.recv() if self.parent_conn.poll() else None


def listen_to_webhooks(pipe=None):
    settings = QSettings(path("config.ini"), QSettings.IniFormat)
    settings.beginGroup("webhooks")
    (domain := settings.value("domain")) or settings.setValue("domain", "")
    (local_port := settings.value("local_port")) or settings.setValue("local_port", "")
    settings.endGroup()

    if not domain or not local_port:
        print("@ ERROR: Fill config.ini before running the application")
        print("@ Stop http server process.")
        sys.exit(1)

    local_port = int(local_port)

    # expose local webhook listener to the internet
    try:
        port_forwarder = shlex.split(f"lt -s {domain} -p {local_port}")  # https://<domain>.loca.lt
        subprocess.Popen(port_forwarder)
    except OSError as e:
        print("@ ERROR in the child http server process:", e)
        print("@ Stop http server process.")
        sys.exit(2)

    # run web server
    httpd = HTTPServer(('localhost', local_port), partial(PostHTTPRequestHandler, pipe))
    httpd.serve_forever()


# kill all spawned processes by PGID on app exit
def _cleaner():
    pid = getpid()
    pgid = getpgid(pid)
    print("@@ kill process group:", pgid)
    cmd_kill = shlex.split(f"kill -- -{pgid}")
    subprocess.check_call(cmd_kill)
onExit(_cleaner)


# main entry point if used in a python app
def run():
    ipc = HTTPServerProcess(listen_to_webhooks)
    return ipc
