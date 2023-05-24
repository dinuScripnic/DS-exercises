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


class Clock:
    def increment_internal(self):
        pass

    def increment_received(self, received_counter):
        pass

    def to_string(self) -> str:
        pass

    def get_internal_count(self):
        pass

# TO IMPLEMENT
class LamportClock(Clock):
    
    def __init__(self) -> None:
        self.counter = 0
    
    def increment_internal(self) -> None:
        self.counter += 1
    
    def increment_received(self, received_counter:int) -> None:
        self.counter = max(self.counter, received_counter) + 1
        
    def to_string(self) -> str:
        return str(self.counter)
    
    def get_internal_count(self) -> int:
        return self.counter



# TO IMPLEMENT
class VectorClock(Clock):

    def __init__(self, iproc:int, nproc:int) -> None:
        self.iproc = iproc
        self.nproc = nproc
        self.vclock = [0] * nproc
    
    def increment_internal(self) -> None:
        self.vclock[self.iproc] += 1
    
    def increment_received(self, received_counter) -> None:
        self.vclock = received_counter
        self.increment_internal()
        
    def to_string(self) -> str:
        return str(self.vclock)
    
    def get_internal_count(self) -> list:
        return self.vclock
    
    
        

