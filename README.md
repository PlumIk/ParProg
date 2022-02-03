# ComonsParaLibLinux

## Compile program

```shell
./compile
```

## Run program

```shell
mpiexec -n 2 ./program.exe -nx 120 -ny 5000 -reverse 0 -threadnum 1 -dec 0  -visual 0 -progress 1
```

## Task parametrs
```
-nx : X axis grid size ( default: 5000)
```
```
-ny : Y axis grid size ( default: 120)
```

## Selected parametrs
```
-n : number of proccesses
```
```
-reverse : cycl order, acceptable values [0, 1] ( default: 0)
```
```
-threadnum : threads per proccess ( default: 1)
```
```
-dec : decomposition, acceptable values [0 - X, 1 - Y] ( default: 0)
```

## Aditional parametrs
```
-visual : visualization, write data files or not [0 - not, 1 - write] 
```
```
-progress : progress of executing a program, writes delta every 100 iterations, acceptable values [0, 1] ( default: 0)
```

## Output

```
Exaple output:
x : true
y : false
Data inited...
iteration number: 1200 delta: 1.01607e-06
Delta: 9.99959e-07
Error: 0.000145447
Iterations: 1203
Time: 11.247591
```
```
Decomposition
x : true
y : false
```
```
Delta - final delta, should be less then 1e-06
```
```
Error - final error, should be small
```
```
Time - time consumed
```

## Run script
```
Parametrs description in needed order:
1) Compiler
2) Compiler key
3) Executable program name
4) Number of processes (-n)
5) X size (-nx)
6) Y size (-ny)
7) Cycl order (-reverse)
8) Threads count (-threadnum)
9) Decomposition (-dec)
```
## Example command for run script
```shell
./run /usr/local/mpich-3.3-gcc-7/bin/mpic++-7 -O3 testrun.out 8 120 5000 0 1 0
```
