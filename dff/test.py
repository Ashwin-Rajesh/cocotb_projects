# MIT License

# Copyright (c) 2021 Ashwin-Rajesh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.clock import Clock
from cocotb.monitors import Monitor
from cocotb.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess

import random

def generator(max_time):
    while(True):
        yield random.randint(1, max_time), random.randint(1, max_time)

class BitMonitor(Monitor):
    """Observe a single-bit input or output of the DUT."""
    def __init__(self, signal, clk, name, callback=None, event=None):
        self.name = name
        self.signal = signal
        self.clk = clk
        Monitor.__init__(self, callback, event)

    async def _monitor_recv(self):
        clkedge = RisingEdge(self.clk)

        while True:
            # Capture signal at rising edge of clock
            await clkedge
            vec = self.signal.value
            self._recv(vec)

class testbench:
    def __init__(self, dut, init_val, input_gen):
        self.dut = dut
        self.stopped = False

        self.q          = init_val

        self.d_drv = BitDriver(dut.d, dut.clk, generator=input_gen())
        self.q_mon = BitMonitor(dut.q, dut.clk, name="output")

        self.target_out = [init_val]

        self.scoreboard = Scoreboard(dut)
        self.scoreboard.add_interface(self.q_mon, self.target_out)

        self.d_mon = BitMonitor(dut.d, dut.clk, name="input", callback=self.model)

    def model(self, inp):
        self.dut._log.debug("transaction : %d"%(inp))
        if(not self.stopped):
            self.target_out.append(inp)

    def start(self):
        self.d_drv.start()
        self.stopped = False

    def stop(self):
        self.d_drv.stop()
        self.stopped = True

@cocotb.test()
async def test_1(dut):
    cocotb.fork(Clock(dut.clk, 10, 'us').start(start_high=False))

    tb = testbench(dut, init_val=BinaryValue(0), input_gen=lambda:generator(5))

    clkedge = RisingEdge(dut.clk)

    tb.start()

    for _ in range(10000):
        await clkedge
        dut._log.debug("clk edge")

    tb.stop()
    await clkedge

    raise tb.scoreboard.result

    dut._log.info("hellooo")

@cocotb.test()
async def test_2(dut):
    cocotb.fork(Clock(dut.clk, 10, 'us').start(start_high=False))

    tb = testbench(dut, init_val=BinaryValue(0), input_gen=lambda:generator(10))

    clkedge = RisingEdge(dut.clk)

    tb.start()

    for _ in range(10000):
        await clkedge
        dut._log.debug("clk edge")

    tb.stop()
    await clkedge

    raise tb.scoreboard.result

    dut._log.info("hellooo")
