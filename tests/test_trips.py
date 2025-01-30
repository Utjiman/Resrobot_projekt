from backend.trips import TripPlanner


def main():

    origin_id = 740000195  # Sandviken Station
    destination_id = 740000002  # Göteborg Centralstation

    trip_planner = TripPlanner(origin_id, destination_id)
    total_stops = trip_planner.calc_number_of_stops_(trip_index=0)
    print(f"Total number of stops for the selected trip: {total_stops}")


if __name__ == "__main__":
    main()
