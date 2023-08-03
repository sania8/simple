import traci
from f2 import *
sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:/Users/HP/Downloads/simple/traffic.sumocfg"]
traci.start(sumoCmd)
steps = 0
# Define the necessary parameters for VAC
threshold_gap_straight = 2.0
threshold_gap_turning = 3.0
detector_timeout = 12.0
tl_id = traci.trafficlight.getIDList()[0]  # Assuming only one traffic light in the network
logic_list = traci.trafficlight.getAllProgramLogics(tl_id)
phases = logic_list[0]
induction_loop_id = "myLoop1"
# Other parameters from the provided text
q = 0.22# Your value for vehicle arrival rate throughout the cycle (veh/s)
e0 = 5# Your value for the unit extension time setting (s)
t0 = 1# Your value for the time during which detector is occupied by passing vehicle (s)
delta_min_arrival = 2# Your value for minimum arrival (intra-bunch) headway (s)
phi = 0.8# Your value for the proportion of free (unbunched) vehicles
lambda_value = 0.15# Your value for the parameter calculated in vehicles per second for all lane groups
def vac_algorithm():
    # Initialize variables
    last_detection_time = traci.simulation.getTime()
    straight_traffic_detected = False
    turning_traffic_detected = False
    current_phase_idx = 0  # Start with the first phase in the phases list

    while traci.simulation.getMinExpectedNumber() > 0:
        # Call the function inside the simulation loop to get arrivals, departures, and time gaps
        num_arrivals, num_departures, time_gaps = get_number_of_vehicles_passed(induction_loop_id)

        # Check for straight and turning traffic detection
        for time_gap in time_gaps:
            if time_gap > threshold_gap_straight:
                straight_traffic_detected = True
            if time_gap > threshold_gap_turning:
                turning_traffic_detected = True

        # Implement VAC logic here
        if straight_traffic_detected or turning_traffic_detected:
            green_extension = calculate_extended_green_time(q, e0, t0, delta_min_arrival, phi, lambda_value)
            

            # If there is demand, move to the next phase (cycle through the phases)
            current_phase_idx = (current_phase_idx + 1) % len(phases)

        

        traci.simulationStep()

    traci.close()

# Run the VAC algorithm
vac_algorithm()

