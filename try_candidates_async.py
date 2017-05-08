import oacis

SIM  = oacis.Simulator.find_by_name("sequential_trial_test")
HOST = oacis.Host.find_by_name("localhost")

def create_ps_and_run( param ):
    ps = SIM.find_or_create_parameter_set( param )
    ps.find_or_create_runs_upto(1, submitted_to=HOST)
    print("Created a new PS: %s" % repr(ps.v()) )
    return ps

def is_result_satisfactory( ps ):
    return (ps.runs().first().result()["result"] == 1)

import json,sys
f = open(sys.argv[1])
y = json.load(f)
f.close()

w = oacis.OacisWatcher()

def call_async( base_param, candidates ):
    def f():
        for cand in candidates:
            param = base_param.copy()
            param.update( cand )
            ps = create_ps_and_run( param )
            oacis.OacisWatcher.await_ps( ps )
            if is_result_satisfactory( ps ):
                print("Found a satisfactory PS : %s" % ps.v() )
                break
    w.async( f )

for base_candidates in y:
    base_param = base_candidates["base"]
    candidates = base_candidates["candidates"]
    call_async( base_param, candidates )

w.loop()

