# beebug - A tool for checking exploitability

<p align="center">
<img src="beebug.png" width="50%"></img>
</p>
<p align="center">
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3-yellow.svg"></a> <img src="https://img.shields.io/badge/license-GPLv3-red.svg"> 
</p>

## Description
**beebug** is a tool that can be used to verify if a program crash could be exploitable.

This tool was presented the first time at [r2con](https://rada.re/con/2018/) 2018 in Barcelona.

Some implemented functionality are:
* Stack overflow on libc 
* Crash on Program Counter
* Crash on branch
* Crash on write memory
* Heap vulnerabilities 
* Read access violation (some exploitable cases)
* Help to analyze a crash (graph view)


## Dependencies

* r2pipe
* pydot
* graphviz
* pyqtgraph

## Installation
```shell
~ $ wget https://github.com/radare/radare2/archive/2.7.0.tar.gz
~ $ tar xzvf 2.7.0.tar.gz
~ $ cd radare2-2.7.0/
~/radare2-2.7.0 $ ./configure --prefix=/usr
~/radare2-2.7.0 $ make -j8
~/radare2-2.7.0 $ sudo make install
# apt-get install graphviz
# pip3 install -r requirements.txt
```

## Usage

### help

```shell
$ python3 ./beebug.py -h
usage: beebug.py [-h] [-t TARGET] [-a TARGETARGS] [-f FILE] [-g GRAPH] [-i]
                 [-r REPORT_FILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target program to analyze
  -a TARGETARGS, --targetargs TARGETARGS
                        arguments for the target program
  -f FILE, --file FILE  input file
  -g GRAPH, --graph GRAPH
                        generate the graph
  -i, --instrumentation
                        instrumentation option
  -r REPORT_FILE, --report_file REPORT_FILE
                        DynamoRIO report file to parse
```

### Simple usage

```shell
# python3 ./beebug.py -t tests/crash_on_pc
Process with PID 7691 started...
File dbg:///home/invictus1306/Documents/r2conf/beebug/beebug/tests/crash_on_pc  reopened in read-write mode
= attach 7691 7691
child stopped with signal 11
[+] SIGNAL 11 errno=0 addr=0x00601038 code=2 ret=0
Crash on PC - Generally it is exploitable, the PC could be tainted
backtrace
0  0x601038           sp: 0x0                 0    [??]  obj.foo obj.foo0
1  0x4004f1           sp: 0x7ffdfa75d8e8      0    [sym.main]  main+27 
2  0x7f2669d00830     sp: 0x7ffdfa75d908      32   [??]  r11+240 
3  0x7f266a0ba7cb     sp: 0x7ffdfa75d998      144  [??]  sym.dl_rtld_di_serinfo+29051 
4  0x400409           sp: 0x7ffdfa75d9c8      48   [??]  entry0+41
registers
rax = 0x00601038
rbx = 0x00000000
rcx = 0x00000000
rdx = 0x7ffdfa75d9f8
r8 = 0x00400570
r9 = 0x7f266a0baab0
r10 = 0x00000846
r11 = 0x7f2669d00740
r12 = 0x004003e0
r13 = 0x7ffdfa75d9e0
r14 = 0x00000000
r15 = 0x00000000
rsi = 0x7ffdfa75d9e8
rdi = 0x0000000a
rsp = 0x7ffdfa75d8e8
rbp = 0x7ffdfa75d900
rip = 0x00601038
rflags = 0x00010206
orax = 0xffffffffffffffff
```

### Graph generation

```shell
# python3 ./beebug.py -t tests/crash_on_pc -g crash_on_pc
...
$ display crash_on_pc.png
```
![crash_on_pc](https://github.com/invictus1306/beebug/blob/master/crash_on_pc.png)

### Report parsing

Parse the report produced by [functrace](https://github.com/invictus1306/functrace), and graph generation.

##### Generate report using *libtrace*

```shell
$ drrun -c libfunctrace.so -report_file ./tests/reports/report1 -disas_func main -- ./tests/reports/simple_test
Please enter a message: 
AAAA
Hello! This is the default message, the number is 22
```

##### Run *beebug* for graph generation

```shell
$ python3 beebug.py -i -r ./tests/reports/report1 -g tests/reports/report1
```

[beebugreport](https://github.com/invictus1306/beebug/blob/master/tests/reports/report1.pdf)

## Future direction

* Support different architectures
* Improvement of the graph view (based on radare2)
* Analyze core dumps (based on radare2)
* Use instrumentation for the graph view generation

## Lead Developer
* Andrea Sindoni - [Twitter](https://twitter.com/invictus1306)
