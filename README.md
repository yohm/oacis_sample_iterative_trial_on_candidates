# Iterative Trial of Candidate Parameters

Some simulations, such as convergence calculations, need trials and errors for selecting appropriate parameters until an expected result is obtained.

In this sample, we demonstrate how to automate this kind of iterations.
This sample tries candidate parameters, which are given by us in advance, one by one until an expected result is obtained.

## Prerequisites

Register simulator as follows.

- Name: "sequential_trial_test"
- Parameter Definitions:
    - "p1", String, "foo"
    - "p2", Float, 1.0
    - "p3", Float, 2.0
- Command:
    - `ruby -r json -e 'res=(rand<0.5)?1:0; puts({"result"=>res}.to_json)' > _output.json`
- Input type: JSON
- Executable_on : localhost

The following command will register this simulator in your OACIS.

```
oacis_ruby prepare_simulator.rb
```

# What does this sample code do?

For each parameter "p1", we try several set of values "p2" and "p3" until we found an expected results.
In this sample, we find a result satisfactory when the `result=1` is obtained from the simulator.

The candidates of ("p2","p3")-pair are given in YAML in the following format.

```candidates.yml
-
  base: {p1: "foo"}
  candidates:
    - {p2: 1.0, p3: 1.0}
    - {p2: 1.5, p3: 2.0}
    - {p2: 2.0, p3: 2.0}
    - {p2: 2.5, p3: 3.0}
-
  base: {p1: "bar"}
  candidates:
    - {p2: 10.0, p3: 0.0}
    - {p2: 11.0, p3: 1.0}
    - {p2: 12.0, p3: 2.0}
    - {p2: 13.0, p3: 3.0}
-
  base: {p1: "baz"}
  candidates:
    - {p2: 5.0, p3: -1.0}
    - {p2: 4.0, p3: -2.0}
    - {p2: 3.0, p3: -3.0}
    - {p2: 2.0, p3: -4.0}
```

For each "p1", we try the first candidates. If they are not satisfactory, find the next candidate and executes the job.
The iteration continues until we found satisfactory results or no futher candidate is found.

# How to run

There are two scripts written in Ruby and Python. You can use either one of them.

```sh
oacis_ruby try_candidates.rb candidates.yml
```

or 

```sh
oacis_python try_candidates.py candidates.yml
```

# LICENSE

The MIT License (MIT)

Copyright (c) 2017 RIKEN, AICS

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

