from math import radians, sin, cos, sqrt, atan2, ceil
class Distance:
    def calculateDistance(fromLocation, toLocation):
        #from location is a tuple 
       
        # Haversine formula to calculate the distance between two points on Earth
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in kilometers
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  # Convert to radians
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        lat1, lon1 = fromLocation
        lat2, lon2 = toLocation

        # Calculate distance in kilometers
        distance_km = haversine(lat1, lon1, lat2, lon2)

        walking_speed = 4  #walking speed in km/h
        public_transport_speed = 20  #public transport speed in km/h
        car_speed = 80  #driving speed in km/h

        walking_time = ceil((distance_km / walking_speed) * 60)
        public_transport_time = ceil((distance_km / public_transport_speed) * 60)
        car_time = ceil((distance_km / car_speed) * 60)

        return {
            "distance_km": round(distance_km, 2),
            "walking_time_minutes": walking_time,
            "public_transport_time_minutes": public_transport_time,
            "car_time_minutes": car_time
        }

   


            