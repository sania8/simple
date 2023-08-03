import traci
sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:/Users/HP/Downloads/simple/traffic.sumocfg"]
traci.start(sumoCmd)
tl_id = traci.trafficlight.getIDList()[0]  # Assuming only one traffic light in the network
# Initial states for all directions
traci.trafficlight.setRedYellowGreenState(tl_id, "GGGGGrrrrrrrrrrrrrrr")
# Timers and flags for each phase
north_timer = 0
east_timer = 0
south_timer = 0
west_timer = 0
north_active = True
east_active = False
south_active = False
yellow_timer = 0  # Timer for the yellow phase
yellow_duration = 5  # Duration of the yellow phase in seconds
is_yellow_phase = False  # Flag to check if the yellow phase is active
west_active = False
total_waiting_time = 0
num_vehicles_waiting = 0
step = 0
while step < 12000:  # Modify the number of simulation steps as needed
    # Increment timers for each active phase
        if north_active:
            north_timer += 1
        elif east_active:
            east_timer += 1
        elif south_active:
            south_timer += 1
        elif west_active:
            west_timer += 1
        # Check if the timer for a phase has exceeded its predefined duration
        if north_timer >= 40 and north_active:
            # Switch to east phase
            traci.trafficlight.setRedYellowGreenState(tl_id, "rrrrrGGGGGrrrrrrrrrr")
            north_active = False
            east_active = True
            west_active = False
            south_active = False
            north_timer = 0
        if east_timer >= 40 and east_active:
            # Switch to south phase
            traci.trafficlight.setRedYellowGreenState(tl_id, "rrrrrrrrrrGGGGGrrrrr")
            north_active = False
            east_active = False
            west_active = False
            south_active = True
            east_timer = 0
        if south_timer >= 40 and south_active:
            # Switch to west phase
            traci.trafficlight.setRedYellowGreenState(tl_id, "rrrrrrrrrrrrrrrGGGGG")
            south_active = False
            west_active = True
            east_active = False  # Corrected variable name from "east_phase" to "east_active"
            north_active = False  # Corrected variable name from "north_phase" to "north_active"
            south_timer = 0
        if west_timer >= 40 and west_active:
            # Switch back to North phase
            traci.trafficlight.setRedYellowGreenState(tl_id, "GGGGGrrrrrrrrrrrrrrr")
            west_active = False
            north_active = True
            east_active = False  # Corrected variable name from "east_phase" to "east_active"
            south_active = False  # Corrected variable name from "south_phase" to "south_active"
            west_timer = 0
        # Calculate waiting time for vehicles at the traffic light
        for veh_id in traci.vehicle.getIDList():
            waiting_time = traci.vehicle.getWaitingTime(veh_id)
            print(waiting_time)
            if waiting_time > 0:
                total_waiting_time += waiting_time
                num_vehicles_waiting += 1
        # Advance the simulation
        traci.simulationStep()
        step += 1

traci.close()

# Calculate average waiting time
if num_vehicles_waiting > 0:
        average_waiting_time = total_waiting_time / num_vehicles_waiting
        print("Average Waiting Time:", average_waiting_time, "seconds")