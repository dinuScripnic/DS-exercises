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

import json
from mpi4py import MPI

comm = MPI.COMM_WORLD
num_procs = comm.Get_size()
print(f'[{comm.rank}]: num_procs {num_procs}')

if comm.rank == 0:
    tasks = [
        json.dumps(
            {"command": "ADD", "parameter1": 2, "parameter2": 3, "parameter3": 1}
        ),
        json.dumps(
            {"command": "SUB", "parameter1": 3, "parameter2": 1, "parameter3": 2}
        ),
        json.dumps(
            {"command": "POW", "parameter1": 1, "parameter2": 2, "parameter3": 3}
        ),
        json.dumps(
            {
                "command": "Karameldansen",
                "parameter1": 1,
                "parameter2": 2,
                "parameter3": 3,
            }
        ),
    ]
    scatter_tasks = [] * num_procs
    current = 0
    for task in tasks:
        if scatter_tasks[current] is None:
            scatter_tasks[current] = list[str]()
        scatter_tasks[current].append(task)
        current = (current + 1) % num_procs
else:
    tasks = list[str]()


# Scatter parameters arrays
units = comm.scatter(tasks, root=0)
calcs = list[str]()
for unit in units:
    p = json.loads(unit)
    print(f'[{comm.rank}]: parameters {p}')
    if p["command"] == "ADD":
        calc = p["parameter1"] + p["parameter2"] + p["parameter3"]
    elif p["command"] == "SUB":
        calc = p["parameter1"] + p["parameter2"] - p["parameter3"]
    elif p["command"] == "POW":
        calc = p["parameter1"] ** p["parameter2"] ** p["parameter3"]
    else:
        calc = "Unknown command"
    calc = [calc, comm.rank]
    calcs.append(calc)



# gather results
result = comm.gather(calcs, root=0)

if comm.rank == 0:
    print("[root]: Result is ", result)

