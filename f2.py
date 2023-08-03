import traci

# Define a dictionary to store the departure times for each vehicle
departure_times_dict = {}
def update_detector_data(detector_id):
    global departure_times_dict
    # Get the list of vehicles detected by the induction loop
    detected_vehicles = traci.inductionloop.getVehicleData(detector_id)
    # Update the departure_times_dict with new data
    current_time = traci.simulation.getTime()
    for vehicle in detected_vehicles:
        vehicle_id = vehicle[0]
        if vehicle_id not in departure_times_dict:
            departure_times_dict[vehicle_id] = current_time

def get_number_of_vehicles_passed(detector_id):
    global departure_times_dict

    # Update the detector data
    update_detector_data(detector_id)

    # Calculate the number of arrivals and departures
    num_arrivals = len(departure_times_dict)  # Since each arrival corresponds to a new vehicle in the departure_times_dict
    num_departures = len(departure_times_dict)

    # Calculate the time gap between Vehicle 1 leaving and Vehicle 2 approaching, Vehicle 2 leaving and Vehicle 3 approaching, and so on
    time_gaps = []
    vehicle_ids = sorted(departure_times_dict.keys())  # Sort the vehicle IDs to ensure correct order
    for i in range(len(vehicle_ids) - 1):
        gap_duration = departure_times_dict[vehicle_ids[i + 1]] - departure_times_dict[vehicle_ids[i]]
        time_gaps.append(gap_duration)
        # Check if the time gap exceeds the threshold gap
    return num_arrivals, num_departures, time_gaps
'''def calculate_average_green_time(q, e0, t0, delta_min_arrival, phi, lambda_value):
    # HCM 2000 formulas for queue service time (Gs) and green extension time (ge)
    qr = q / 3600.0  # Convert arrival rate from veh/s to veh/h
    s = 1800.0 / q  # Saturation flow rate: 1800 vehicles/hour per lane (HCM 2000 assumption)
    fq = 1.08 - 0.1 * ((e0 + t0) / q) ** 2  # Queue calibration factor
    Gs = fq * (qr / (s - qr))  # Queue service time
    ge = (e0 * (1 - (t0 / delta_min_arrival))) / (q - 1)  # Green extension time

    # Calculate average green time (Gavg) as sum of queue service time and green extension time
    Gavg = Gs + ge

    # Apply the proportion of free (unbunched) vehicles (phi) and lambda factor
    Gavg *= phi * lambda_value

    return Gavg'''
def calculate_extended_green_time(q, e0, t0, delta_min_arrival, phi, lambda_value):
    # Your implementation of calculating the extended green time (ge) using the provided formulas goes here
    qr = q / 3600.0  # Convert arrival rate from veh/s to veh/h
    s = 1800.0 / q  # Saturation flow rate: 1800 vehicles/hour per lane (HCM 2000 assumption)
    fq = 1.08 - 0.1 * ((e0 + t0) / q) ** 2  # Queue calibration factor
    Gs = fq * (qr / (s - qr))  # Queue service time
    ge = (e0 * (1 - (t0 / delta_min_arrival))) / (q - 1)  # Green extension time

    # Apply the proportion of free (unbunched) vehicles (phi) and lambda factor
    ge *= phi * lambda_value

    return ge


