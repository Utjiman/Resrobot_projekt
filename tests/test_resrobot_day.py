from backend.resrobot_day import ResRobotDay

def main():
    rr_day = ResRobotDay()
    station_id = 740000002  # Göteborg central
    df_dep = rr_day.departures_until_now(station_id)
    print("Antal avgångar:", len(df_dep))
    print(df_dep.head())

    df_arr = rr_day.arrivals_until_now(station_id)
    print("Antal ankomster:", len(df_arr))
    print(df_arr.head())

if __name__ == "__main__":
    main()
    
# kör python tests/test_resrobot_day.py i terminalen
