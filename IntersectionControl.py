import time

from flask_socketio import emit

from captureframe import capture_frames
from detactV import detect_vehicles_and_emergency


# Calculate the dynamic green light time
def calculate_adjusted_time(vehicles, max_vehicles=28, default_time=42):
    adjusted_times = []
    for num_vehicles in vehicles:
        if num_vehicles > max_vehicles:
            percentage_diff = ((num_vehicles - max_vehicles) / max_vehicles) * 100
            adjusted_time = default_time * (1 + percentage_diff / 100)
        elif num_vehicles < max_vehicles:
            percentage_diff = ((max_vehicles - num_vehicles) / max_vehicles) * 100
            adjusted_time = default_time * (1 - (percentage_diff / 100))
        else:
            adjusted_time = default_time
        adjusted_times.append(round(adjusted_time))
    if adjusted_time < 10:
        adjusted_time = 10
    elif adjusted_time > 80:
        adjusted_time = 80
    return adjusted_times


def intersection_control(road_vehicles):
    num_roads = len(road_vehicles)
    roads_cycle = [1, 2, 3, 4]
    flag = 0

    while True:  # Infinite loop for continuous traffic light control
        # Sort roads based on emergency vehicles first and then by the number of vehicles in descending order
        initial_sorted_roads = sorted(
            road_vehicles.items(), key=lambda x: (-x[1]["emergency"], -x[1]["vehicles"])
        )
        if flag == 1:
            initial_sorted_roads = sorted_roads
            flag = 0

        data = []
        for road_index, (road, road_info) in enumerate(initial_sorted_roads):
            if road not in roads_cycle:  # Maintain the cycle of green light
                continue
            if not roads_cycle:  # If a cycle is complete
                roads_cycle = [1, 2, 3, 4]
            # Display current state
            print(
                f"\nTotal Vehicles: {sum(info['vehicles'] for info in road_vehicles.values())}"
            )

            for r, info in road_vehicles.items():

                data.append({"no": r, "v": info["vehicles"], "e": info["emergency"]})

                print(
                    f"Road {r} - Vehicles: {info['vehicles']}, Emergency: {info['emergency']}"
                )

            # Calculate adjusted time for the current road
            adjusted_time = calculate_adjusted_time([road_info["vehicles"]])[0]

            # Display switch to Yellow light
            print(f"\nSwitching to Yellow Light for Road {road}")

            # Wait for 5 seconds for the Yellow light
            # time.sleep(3)

            # Display current green light information
            print(f"Green Light Time for Road {road}: {adjusted_time} seconds")
            print(f"Green Light: Road {road}")
            # marking this road as done
            roads_cycle.remove(road)

            # Get other road indexes except the current road
            other_roads = [r for r in road_vehicles if r != road]
            other_roads_str = ", ".join(map(str, other_roads))

            # Print other road indexes
            print(f"Green Light for left turn: Road {other_roads_str}\n")

            yield {"road": road, "at": adjusted_time, "data": data}
            # For simulation wait for 10 seconds to change light
            time.sleep(10)
            capture_frames(10)
            # Wait for the adjusted time
            # capture_frames(adjusted_time)

            # Update number of vehicles and emergency vehicles on each road after green light cycle
            for r, info in road_vehicles.items():
                if r != road:
                    image_path = f"frames/frame_road({r}).jpg"
                    total_vehicles, emergency_detected = detect_vehicles_and_emergency(
                        image_path
                    )  # Only update vehicles for roads not currently on green light
                    # Input number of vehicles and emergency status for each road
                    road_vehicles[r] = {
                        "vehicles": total_vehicles,
                        "emergency": emergency_detected,
                    }

            # Reset the number of vehicles and emergency vehicles for the road to simulate vehicle clearance
            road_vehicles[road]["vehicles"] = 0
            road_vehicles[road]["emergency"] = 0
            # Sort roads based on updated number of vehicles and emergency status
            sorted_roads = sorted(
                road_vehicles.items(),
                key=lambda x: (-x[1]["emergency"], -x[1]["vehicles"]),
            )
            if sorted_roads != initial_sorted_roads:
                flag = 1
                break
