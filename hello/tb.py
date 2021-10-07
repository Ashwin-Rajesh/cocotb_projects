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

# Import library
import cocotb
from cocotb.triggers import Timer

# All testcases
test_in  = [(0,0), (0, 1), (1, 0), (1, 1)]
test_out = [l[0] and l[1] for l in test_in]

# First test function
@cocotb.test()
async def test_fn(dut):

    dut._log.info("Running test...")
    
    # Initialize variables
    dut.a   <= 0
    dut.b   <= 0

    dut.clk <= 1

    for cycle in range(10):

        dut.a   <= test_in[cycle % 4][0]
        dut.b   <= test_in[cycle % 4][1]

        # Clock negative edge
        await Timer(1, units="ns")
        dut.clk <= 0

        assert(dut.d.value == test_out[cycle % 4], 
            " Inputs : %d, %d, Output : %d, Target : %d"%(
                test_in[cycle % 4][0], test_in[cycle % 4][1], dut.d.value, test_out[cycle % 4]
            ))

        # Clock positive edge
        await Timer(1, units="ns")
        dut.clk <= 1
