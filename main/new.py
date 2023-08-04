import traci
import time

sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:/Users/HP/Downloads/simple/main/sumo.sumocfg"]

traci.start(sumoCmd)

step = 0
total = 0
num_vehicles_waiting = 0

while step < 3200:
    # Calculate waiting time for vehicles at the traffic light
    for veh_id in traci.vehicle.getIDList():
        waiting_time = traci.vehicle.getWaitingTime(veh_id)
        if waiting_time > 0:
            total += waiting_time
            num_vehicles_waiting += 1

    traci.simulationStep()
    step += 1

traci.close()

print("Total number of vehicles:", num_vehicles_waiting)

average_waiting_time = total / num_vehicles_waiting
print("Average waiting time:", average_waiting_time)
