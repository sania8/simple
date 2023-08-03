import traci
from f2 import *

sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:/Users/HP/Downloads/simple/traffic.sumocfg"]
traci.start(sumoCmd)
steps = 0

threshold_gap = 5.0
detector_timeout = 12.0
tl_id = traci.trafficlight.getIDList()[0]  # Assuming only one traffic light in the network
logic_list = traci.trafficlight.getAllProgramLogics(tl_id)
phases = logic_list[0]
induction_loop_id = "myLoop1"

last_detection_time = traci.simulation.getTime()
while traci.simulation.getMinExpectedNumber() > 0:
    # Call the function inside the simulation loop to get arrivals, departures, and time gap
    num_arrivals, num_departures, time_gaps = get_number_of_vehicles_passed(induction_loop_id)
    for time_gap in time_gaps:
        print("Time gap between Vehicle 1 leaving and Vehicle 2 approaching:",time_gap)
        # Calculate the time since the last detection
        if(time_gap > threshold_gap):
            traci.trafficlight.setRedYellowGreenState(tl_id, "rrrrrGGGGGGGGGGGGGGG")
            traci.trafficlight.setPhaseDuration(tl_id , 30)
        else:
            traci.trafficlight.setRedYellowGreenState(tl_id, "GGGGGrrrrrrrrrrrrrrr")
            traci.trafficlight.setPhaseDuration(tl_id ,30)

    traci.simulationStep()

    steps += 1

traci.close()
# Print the results after the simulation ends
print("Number of arrivals:", num_arrivals)
print("Number of departures:", num_departures)
