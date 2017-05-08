import oacis

class CandidatesProvider():

    def __init__(self, base_param, candidate_params, watcher):
        self.watcher = watcher
        self.base = base_param
        self.candidates = candidate_params

        self.sim = oacis.Simulator.find_by_name("sequential_trial_test")
        self.host = oacis.Host.find_by_name("localhost")
        self.host_param = self.host.default_host_parameters()

    def initial_parameter(self):
        param = self.base.copy()
        param.update( self.candidates[0] )
        return param

    def create_ps_and_run(self, param):
        ps = self.sim.find_or_create_parameter_set( param )
        ps.find_or_create_runs_upto(1, submitted_to=self.host, host_param=self.host_param)
        print("Created a new PS: %s" % repr(ps.v()) )

        def on_ps_finished(ps):
            if self.need_another_trial( ps ):
                print("ParameterSet: %s needs another trial. Creating a next run." % repr(ps.v()) )
                self.create_next_ps_and_run( ps )
            else:
                print("ParameterSet: %s does not need another trial." % repr(ps.v()) )
        self.watcher.watch_ps( ps, on_ps_finished )

    def need_another_trial(self, ps):
        return (ps.runs().first().result()["result"] == 0)

    def create_next_ps_and_run(self, ps):
        next_param = self.find_next_candidate( ps.v() )
        if next_param:
            self.create_ps_and_run( next_param )

    def find_next_candidate(self, current_param):
        found_idx = None
        for idx,cand in enumerate(self.candidates):
            if all( current_param[key]==val for key,val in cand.items() ):
                found_idx = idx
                break
        assert isinstance( found_idx, int )
        next_idx = found_idx + 1
        if next_idx >= len(self.candidates):
            return None
        else:
            param = self.base.copy()
            param.update( self.candidates[next_idx] )
            return param

if __name__ == "__main__":
    import json,sys
    def main():
        watcher = oacis.OacisWatcher()
        f = open(sys.argv[1])
        y = json.load(f)
        f.close()

        for cand in y:
            print(repr(cand))
            c = CandidatesProvider( cand['base'], cand['candidates'], watcher )
            c.create_ps_and_run( c.initial_parameter() )
        watcher.loop()

    main()
