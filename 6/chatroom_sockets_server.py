#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pickle
import zmq
from zmq.error import ZMQError

context = zmq.Context()
rep_socket = context.socket(zmq.REP)  # create response socket
pub_socket = context.socket(zmq.PUB)  # create a publish socket


def bind():
    """
    Binds sockets to ports.
    :return:
    """
    rep_socket.bind("tcp://*:7600")
    pub_socket.bind("tcp://*:7601")


def wait_for_requests():
    """
    Waits for client requests to come and processes them.
    :return:
    """
    while True:
        try:
            message = pickle.loads(rep_socket.recv())
            print("Received message: %s" % message['content'])
            rep_socket.send_string("ACK")
            channel = message['channel']
            content = message['content']
            print(f'Sending message = {content} to channel {channel}')
            pub_socket.send_string(f'{channel} {content}')
        except ZMQError as err:
            print(f"Exception: {err}")


if __name__ == "__main__":
    bind()
    print("Server started")
    wait_for_requests()
