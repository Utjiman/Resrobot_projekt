from backend.connect_to_api import ResRobot

class TimeTable:

    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def show_departure_from_stop(self, stop_id: int):
        """
        Show departures from a specific stop
        """
        data = self.resrobot.timetable_departure(location_id=stop_id)  # Gets data from resrobot
        departures = data.get("Departure", [])
        
        result = []
        for departure in departures:
            line = departure.get("ProductAtStop", {}).get("name", "Okänd linje")
            direction = departure.get("direction", "Okänd destination")
            time = departure.get("time", "N/A")
            result.append({"Linje": line, "Destination": direction, "Avgångstid": time})

        return result




   
    def filter_stop():
       pass

    
    
    
    
    def show_time_to_departure():
        pass


    
    
    
    
    def show_one_hour_ahead():
        pass
