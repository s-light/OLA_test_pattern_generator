# OLA_test_pattern_generator
OLA python client to generate test-patterns

## usage:
for interactive mode
```
./main.py -i
```
for interactive mode with configuration file
```
./main.py -i -c ./olad_configurations/spi_12ports_6x2x72pixel/multiuniverse_test.json
```
for other command-line options try
```
./main.py -h
```

interactive menu:
```
$ ./main.py -i
******************************************
Python Version: 2.7.14 (default, Sep 23 2017, 22:06:14)
[GCC 7.2.0]
******************************************
******************************************

ola test pattern generator.

    generates some test patterns.

******************************************
start_ola
run

******************************************
select pattern:
  '0' stop
  '1' channelcheck
 >'2' colors_multiuniverse
  '3' gradient
  '4' gradient2
  '5' gradient_8bit
  '6' gradient_integer
  '7' rainbow
  '8' static
  '9' strobe
  running
set option:
  'f': freez pattern generator 'f'
  'r': run pattern generator 'r'
  't': toggle running pattern generator 't'
  '-': 
  'ui': update interval 'ui:1000 (1.0Hz)'
  'uo': set universe output 'uo:1'
  'uc': set universe count 'uc:12'
  'pc': set pixel count 'pc:72'
  'rc': set repeate count 'rc:4'
  'rs': set repeate snake 'rs:True'
  'mo': set mode_16bit 'mo:False'
  '-':
  'vh': set value high 'vh:5000'
  'vl': set value low 'vl:2100'
  'vo': set value off 'vo:0'
  'gd': set global_dimmer 'gd:50'
  'pd': set use_pixel_dimming 'pd:1'
  '-':
  'sc': save config 'sc'
  'q': Ctrl+C or 'q' to stop script
******************************************

self.state: OLAThread_States.waiting
waiting for olad....
get client
run ola wrapper.
```
