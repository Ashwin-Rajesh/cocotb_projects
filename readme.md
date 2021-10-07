## Cocotb

cocotb is a COroutine based COsimulation TestBench environment for verifying VHDL and SystemVerilog RTL using Python.

It requires a simulator to run. It is basically a testbench written in python.

---

## Makefile

```make
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
```
Sets the vaiables SIM and TOPLEVEL_LANG if they are not set already.

```make
VERILOG_SOURCES += $(PWD)/module.v
```

Adds verilog source files

```make
TOPLEVEL = test
```

Adds the module name of toplevel module in the .v file

```
MODULE = tb
```

The name of test python file

```
include $(shell cocotb-config --makefiles)/Makefile.sim
```

Invoke cocotb makefile

---

## Python file

A bare minimum "testbech" if you can even call it that!

```python
# Import library
import cocotb

# Test 1
@cocotb.test()
async def test_fn(dut):
    dut._log.info('hello there!')

# Test 2
@cocotb.test()
async def test_fn_2(dut):
    dut._log.info("hello again!")
```

- cocotb runs all functions that have the decorator ```cocotb.test()```.

- The test functions get the dut object as argument

- Output has "hello there!" and "hello again!", so both tests are run

---

A more functional example :

```python
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
```

Imagine dut is an and gate with a flip flop triggered on the negative edge. 

---

## References

1) [cocotb quickstart](https://docs.cocotb.org/en/stable/quickstart.html)
2) []()
3) 
