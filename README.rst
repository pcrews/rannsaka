rannsaka
========

mayhem-generation and analysis tool for testing

rannsaka?
---------

It is what Google translate says is Icelandic for 'probe' ;)

Design
-------

This tool is designed to produce stressful, randomized workloads
for OpenStack systems.

It leverages locust.io for general test execution and would-be testers
create locust files that model the behavior to be tested.

The tool should serve a similar purpose as the random query generator
does for database systems.

The idea is that complex system cannot be adequately tested via
individually crafted test-cases.  This is because human validation
is time and brain intensive and several projects' experience has been
that such tests are often shallow.  By utilizing software to better
emulate random, real world workloads, more bugs can be found before
making their way to the end user.

This is not intended to replace other testing tools.
One may think of it as a tool to help generate more formal test cases
for the regression suite - fishing with dynamite, as it were.

Future work
------------

- API calls for more openstack functions
- Validation modules that can be turned on / off for requests
- Utilization of core tempest code (config, logging, tempest libs)

Usage
-----

::

    usage: rannsaka.py [-h] [--config CONFIG_FILE] [--test-file WORKER_CONFIG]
                       [--host LOCUST_HOST] [--requests REQUEST_COUNT]
                       [--workers WORKER_COUNT] [--verbose] [--debug]
    
    ransakka.py: API probe / testing tool for OpenStack projects

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG_FILE  File defining test credentials, etc for rannsaka to
                            use. NOT YET IMPLEMENTED
      --test-file WORKER_CONFIG, -t WORKER_CONFIG
                            locust file to execute
      --host LOCUST_HOST    Test host
      --requests REQUEST_COUNT
                            Total number of requests to make across all workers
      --workers WORKER_COUNT, -w WORKER_COUNT
                            Number of workers to use for test execution.
      --verbose, -v         Controls internal output. Utilize multiple times to
                            increase output
      --debug, -d           Controls debug output. NOT YET IMPLEMENTED
    

Example
-------

::
    
    python rannsaka.py --host=http://127.0.0.1 --requests 50
    locust --no-web -c 1 -f test_files/basic.py -n 50 --host http://127.0.0.1
    [2014-10-17 15:45:13,906] mahmachine/INFO/locust.main: Starting Locust 0.7.2
    [2014-10-17 15:45:13,907] mahmachine/INFO/locust.runners: Hatching and swarming 1 clients at the rate 1 clients/s...
    ...
    [2014-10-17 15:45:17,224] mahmachine/INFO/locust.runners: All locusts dead
    
    [2014-10-17 15:45:17,224] mahmachine/INFO/locust.main: Shutting down (exit code 0), bye.
     Name                                                          # reqs      # fails     Avg     Min     Max  |  Median   req/s
    --------------------------------------------------------------------------------------------------------------------------------------------
     POST /v2.0/tokens                                                  2     0(0.00%)     192     186     198  |     190    0.00
     GET /v2/74e5bfa2cb734763aa9acce564efecca/flavors                   8     0(0.00%)      23      22      28  |      23    0.00
     GET /v2/74e5bfa2cb734763aa9acce564efecca/flavors/detail            5     0(0.00%)      23      23      25  |      23    1.00
     GET /v2/74e5bfa2cb734763aa9acce564efecca/limits                   10     0(0.00%)      25      23      30  |      25    0.00
     GET /v2/74e5bfa2cb734763aa9acce564efecca/servers                  12     0(0.00%)      35      33      40  |      34    0.00
     GET /v2/74e5bfa2cb734763aa9acce564efecca/servers/detail           13     0(0.00%)      36      34      42  |      35    1.00
    --------------------------------------------------------------------------------------------------------------------------------------------
     Total                                                             50     0(0.00%)                                       2.00
    
    Percentage of the requests completed within given times
     Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
    --------------------------------------------------------------------------------------------------------------------------------------------
     POST /v2.0/tokens                                                   2    200    200    200    200    200    200    200    200    198
     GET /v2/74e5bfa2cb734763aa9acce564efecca/flavors                    8     24     24     24     24     28     28     28     28     28
     GET /v2/74e5bfa2cb734763aa9acce564efecca/flavors/detail             5     23     25     25     25     25     25     25     25     25
     GET /v2/74e5bfa2cb734763aa9acce564efecca/limits                    10     25     25     27     27     30     30     30     30     30
     GET /v2/74e5bfa2cb734763aa9acce564efecca/servers                   12     34     36     39     39     39     40     40     40     40
     GET /v2/74e5bfa2cb734763aa9acce564efecca/servers/detail            13     35     36     38     39     39     42     42     42     42
    --------------------------------------------------------------------------------------------------------------------------------------------
