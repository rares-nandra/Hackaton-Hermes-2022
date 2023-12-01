from geopy.geocoders import Nominatim
from geopy import distance
from googleplaces import GooglePlaces, types, lang
import requests
import json


class pletea():
    def __init__(self):
        self.geolocator = Nominatim(user_agent="SafeBreak")
        self.google_places = GooglePlaces("AIzaSyAO_OXz74nqN9y2OLk_iOjhW5ifMwajt7Y")

    def decodeToName(self, lat, long):
        return self.geolocator.reverse(lat,long).address
    
    def decodeToLatLong(self,name):
        location = self.geolocator.geocode(name)

        return {
            "lat": location.lat,
            "long": location.long
        }
    
    def distanceLatLong(self, lat1, long1, lat2, long2):
        return round(distance.distance((lat1, long1), (lat2, long2)).km)

    def distanceLocation(self, loc1, loc2):
        loc1d = self.decodeToLatLong(loc1)
        loc2d = self.decodeToLatLong(loc2)

        return self.distanceLatLong(loc1d["lat"], loc1d["long"], loc2d["lat"], loc2d["long"])

    def nearbyHospital(self, lat, long):
        query_result = self.google_places.nearby_search(lat_lng = {'lat': lat, 'lng': long}, radius = 5000, types =[types.TYPE_HOSPITAL])

        if query_result.places == []:
            return None
            
        return {
            "name": query_result.places[0].name,
            "distance": self.distanceLatLong(lat, long, query_result.places[0].geo_location["lat"], query_result.places[0].geo_location["lng"])
        }

    






