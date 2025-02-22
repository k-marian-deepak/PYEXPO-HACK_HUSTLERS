import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kgkite@123",
        database="TrafficDB"
    )

def get_vehicle_counts(lane):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT car_count, bike_count, heavy_vehicle_count FROM traffic_data WHERE lane = %s ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(query, (lane,))
    result = cursor.fetchone()
    db.close()
    if result:
        return {'Car': result[0], 'Bike': result[1], 'Heavy Vehicles': result[2]}
    return {'Car': 0, 'Bike': 0, 'Heavy Vehicles': 0}

def insert_traffic_data(lane, car_count, bike_count, heavy_vehicle_count, congestion_level, green_time):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO traffic_data (lane, car_count, bike_count, heavy_vehicle_count, congestion_level, green_time) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (lane, car_count, bike_count, heavy_vehicle_count, congestion_level, green_time)
    cursor.execute(query, values)
    db.commit()
    db.close()

def get_congestion_level(vehicle_count):
    total_vehicles = sum(vehicle_count.values())
    if total_vehicles <= 10:
        return "Low Traffic", 10
    elif 10 <= total_vehicles <= 20:
        return "Moderate Traffic", 30
    elif total_vehicles > 20:
        return "High Traffic", 60

def process_traffic_data(vehicle_count):
    lanes = ["Lane 1", "Lane 2", "Lane 3", "Lane 4"]
    traffic_signals = {}

    for lane in lanes:
        # Use the provided vehicle_count for processing
        status, green_time = get_congestion_level(vehicle_count)
        traffic_signals[lane] = green_time
        print(f"{lane}: {status}, Green Time: {green_time}s")
        insert_traffic_data(lane, vehicle_count['Car'], vehicle_count['Bike'], vehicle_count['Heavy Vehicles'], status, green_time)
        print (f"Inserted traffic data for {lane}")
        
    return traffic_signals