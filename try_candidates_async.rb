require 'yaml'

SIM       = Simulator.find_by_name("sequential_trial_test")
LOCALHOST = Host.find_by_name("localhost")

def create_ps_and_run( param )
  ps = SIM.find_or_create_parameter_set( param )
  ps.find_or_create_runs_upto(1, submitted_to: LOCALHOST)
  $stderr.puts "Created a new PS: #{ps.v}"
  ps
end

def is_result_satisfactory?( ps )
  ps.runs.first.result["result"] == 1
end

OacisWatcher::start do |w|
  j = JSON.load( File.open(ARGV.first) )
  j.each do |base_candidates|
    w.async {
      base_param = base_candidates["base"]
      candidates = base_candidates["candidates"]
      candidates.each do |cand|
        param = base_param.merge( cand )
        ps = create_ps_and_run( param )
        OacisWatcher.await_ps( ps )
        if is_result_satisfactory?( ps )
          $stdout.puts "Found a satisfactory PS : #{ps.v}"
          break
        end
      end
    }
  end
end

