#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  This file is part of "github actions gui" project
#
#  Author: Roman Gladyshev <remicollab@gmail.com>
#  License: MIT License
#
#  SPDX-License-Identifier: MIT
#  License text is available in the LICENSE file and online:
#  http://www.opensource.org/licenses/MIT
#
#  Copyright (c) 2020 remico

import hmac
import json
import shlex
import subprocess
import sys
from atexit import register as onExit
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from multiprocessing import Process, Pipe
from os import getpgid, getpid, getenv

from .path import path
from .pyside2 import *
from .worker import WorkerThread


class PostHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, pipe, *args, **kwargs) -> None:
        self.pipe = pipe
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # validate sender
        token = getenv('GITHUB_WEBHOOKS_TOKEN').encode()
        expected_signature = "sha256=" + hmac.new(token, msg=body, digestmod="sha256").hexdigest()
        received_signature = self.headers['X-Hub-Signature-256']
        is_valid = hmac.compare_digest(received_signature, expected_signature)

        if is_valid:
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(500, "Signatures didn't match!")
            self.end_headers()
            print(f"@ WARNING: mismatch signatures in the received webhook: got '{received_signature}', expected '{expected_signature}'")
            return

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

        def _on_quit():
            print("> REQUESTING HTTPD SHUTDOWN...")
            self.parent_conn.send("http_server_shutdown")
            # block current process until the child process ends correctly, then close the child
            self.p.join()
            self.p.close()

        qApp.aboutToQuit.connect(_on_quit)  # terminate children processes before app exit
        self.p.start()

    dataReady = PS2Signal()

    def read(self):
        return self.parent_conn.recv() if self.parent_conn.poll() else None


def listen_to_webhooks(pipe=None):
    settings = QSettings(path.home().join(".actions_gui.conf"), QSettings.IniFormat)
    settings.beginGroup("webhooks")
    (domain := settings.value("domain")) or settings.setValue("domain", "")
    (local_port := settings.value("local_port")) or settings.setValue("local_port", "")
    settings.endGroup()

    if not domain or not local_port:
        print("@ ERROR: Bad domain name or port. Adjust config before running the application.")
        print("@ Stop http server process.")
        sys.exit(1)

    local_port = int(local_port)

    # expose local webhook listener to the internet
    try:
        port_forwarder = shlex.split(f"lt -s {domain} -p {local_port}")  # https://<domain>.loca.lt
        p = subprocess.Popen(port_forwarder)
    except OSError as e:
        print("@ ERROR in the child http server process:", e)
        print("@ Stop http server process.")
        sys.exit(2)

    # create a web server
    httpd = HTTPServer(('localhost', local_port), partial(PostHTTPRequestHandler, pipe))

    # and run it in a separate python thread
    WorkerThread(httpd.serve_forever)

    # block current thread just waiting for the HTTPD SHUTDOWN request
    # from another side of the pipe (i.e. another python process)
    # NOTE: despite pipe's recv() and send() operations perform in different threads,
    # no sync is done however, because these operations don't conflict each other
    # (one thread only sends and another one only receives)
    if pipe.recv() == "http_server_shutdown":
        print("> HTTPD SHUTTING DOWN...")
        p.kill()
        p.wait()
        httpd.shutdown()
        print("> DONE")


# main entry point if used in a python app
def run():
    http_server = HTTPServerProcess(listen_to_webhooks)
    return http_server
