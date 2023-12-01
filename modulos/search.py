from modulos import mongodb
from covid import Covid
from countryinfo import CountryInfo
import requests
import json
from modulos import geo


db = mongodb.mongodb()
pletea = geo.pletea()


class Search:
    def location_lat_long(self,latt,lonn,rangee,typee,radius):
        headers = {
            'accept': 'application/json',
        }

        params = (
            ('radius', str(radius)),
            ('lon', lonn),
            ('lat', latt),
            ('kinds', typee),
            ('rate', '2h'),
            ('format', 'json'),
            ('limit', str(rangee)),
            ('apikey', '5ae2e3f221c38a28845f05b6bb345c95c2512f932ee7eaba63765f27'),
        )

        response = requests.get('http://api.opentripmap.com/0.1/en/places/radius', headers=headers, params=params)
        resp = json.loads(response.text)
        print("ooresp", resp)
        r = []

        for i in resp:
            r.append({
                "name": i["name"],
                "lat": i["point"]["lat"],
                "lon": i["point"]["lon"],
            })

        return r


    def GetCountryCenterRadius(self, Location):
        Country = CountryInfo(Location)

        CenterLong = 0
        CenterLat = 0

        Coordinates = Country.geo_json()["features"][0]["geometry"]["coordinates"][0]

        try:
            for Coord in Coordinates:
                CenterLong = CenterLong + Coord[0]
                CenterLat = CenterLat + Coord[1]

            CenterLong = CenterLong / len(Coordinates)
            CenterLat = CenterLat / len(Coordinates)
        except:
            Coordinates = Country.geo_json()["features"][0]["geometry"]["coordinates"][0][0]

        for Coord in Coordinates:
            CenterLong = CenterLong + Coord[0]
            CenterLat = CenterLat + Coord[1]

        CenterLong = CenterLong / len(Coordinates)
        CenterLat = CenterLat / len(Coordinates)

        return CenterLat, CenterLong, 1000000
    
    def imageSearch(self,img):
        headers = {
            'Ocp-Apim-Subscription-Key': 'bec23011abd84073a04ea2a607702578',
        }

        params = (
            ('q', img),
        )

        response = requests.get('https://api.bing.microsoft.com/v7.0/images/search', headers=headers, params=params)
        data = json.loads(response.text)
        # print("niezo", data)
        return data["value"][0]["contentUrl"]

    def s(self, user, vacationtype, covid, distance):
        
        print(user,vacationtype,covid,distance,"vvs")
        diseases = db.data(user)["diseases"]
        distance = float(distance)

        countries_to_search = []

        if "Blindness" in diseases:
            copy = self.get_blind_countries()
            
            for country in copy:
                if country not in countries_to_search:
                    countries_to_search.append(country)

        if "Deafness" in diseases:
            copy = self.get_deaf_countries()
            
            for country in copy:
                if country not in countries_to_search:
                    countries_to_search.append(country)

        if "Locomotory" in diseases:
            copy = self.get_locomotory_countries()
            
            for country in copy:
                if country not in countries_to_search:
                    countries_to_search.append(country)

        if "Asthma" in diseases:
            copy = self.get_asthm_countries()
            
            for country in copy:
                if country not in countries_to_search:
                    countries_to_search.append(country)
        
        if "Allergies" in diseases:
            copy = self.get_allergies_countries()
            
            for country in copy:
                if country not in countries_to_search:
                    countries_to_search.append(country)

        # print("countries:", countries_to_search)

        if covid:
            countries_to_search = [country for country in countries_to_search if self.get_covid_safeness(country.lower())]

        # countries_to_search = list(dict.fromkeys(countries_to_search))

        # print("countries:", countries_to_search)

        r = []
        for country in countries_to_search:
            lat,long,radius = self.GetCountryCenterRadius(country.lower())
            debug = self.location_lat_long(lat,long, 20, vacationtype, radius)
            r.append(debug)
        
        res = []
        for x in r:
            if x not in res:
                res.append(x)

        # print(res, r, "res")
        ress = []
        for i in res[0]:
            print("johny", i)
            urll = self.imageSearch(i["name"])
            h = pletea.nearbyHospital(i["lat"], i["lon"])

            if h == None:
                print("pass1")
                pass
            elif h["distance"] >= distance :
                print("pass2")
                pass
            else:
                ress.append({
                    "name": i["name"],
                    "lat": i["lat"],
                    "long": i["lon"],
                    "image_url": urll,
                    "hospital": h["name"], 
                    "hospital_distance": h["distance"]
                })
                print(h["distance"], "DIStAnta")

        print(ress)

        return ress

                
    

    def get_covid_safeness(self, country_name):
        if country_name == "united states":
            country_name="US"

        covid = Covid()
        cases = covid.get_status_by_country_name(country_name)["confirmed"]
        # print("cases: ", cases)
        country = CountryInfo(country_name)
        if country_name == "US":
            country_name="usa"
        population = country.info()["population"]

        # print(cases, population, "jfjjf")
        # print(cases / population < 0.5, cases / population)
        return cases / population < 0.5
    

    def get_blind_countries(self):
        return ["United States", "United Kingdom", "Australia", "France", 'Italy', "Germany", "China"]


    def get_locomotory_countries(self):
        return ["Australia", "United Kingdom", "United States", "Austria", "Spain", "France", "Ireland", "Netherlands"]
    

    def get_deaf_countries(self):
        return ["Australia", "France", "United States", "Germany", "Romania"]

    
    def get_asthm_countries(self):
        return ["Australia", "France", "United States", "Germany", "Romania", "Austria", "Spain"]


    def get_allergies_countries(self):
        return ["Australia", "France", "United States", "Germany", "Turkey", "Hungary"]
    
    


        