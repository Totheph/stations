import csv
from datetime import datetime
from geopy import distance

def bus_stations():
  with open("bus_stops.csv", "r", encoding="windows-1251") as input_file:
    fields = ["ID", "Name", "Longitude_WGS84","Latitude_WGS84", "AdmArea", "District", "RouteNumbers", "StationName", "Direction", "Pavilion", "OperatingOrgName", "EntryState", "global_id", "PlaceDescription", "Works", "geodata_center", "geoarea"]
    reader = csv.DictReader(input_file, fields, delimiter=";")
    number_of_stations = {}
    for station in reader:
      if station['PlaceDescription']:
        number_of_stations[station['PlaceDescription'].split(', ')[0]] = number_of_stations.get(station['PlaceDescription'].split(', ')[0], 0) + 1
    print(f"Улица с наибольшим количеством остановок: {max(number_of_stations, key = number_of_stations.get)}")


def metro_repair_of_escalators():
  with open('metro_stations.csv', 'r', encoding="windows-1251") as input_file:
    fields = ["ID","Name", "OnTerritoryOfMoscow", "AdmArea", "District", "Longitude_WGS84", "Latitude_WGS84", "VestibuleType", "NameOfStation", "Line", "CulturalHeritageSiteStatus","ModeOnEvenDays", "ModeOnOddDays", "FullFeaturedBPAAmount", "LittleFunctionalBPAAmount", "BPAAmount", "RepairOfEscalators", "ObjectStatus", "global_id"]
    reader = csv.DictReader(input_file, fields, delimiter=";")
    stations = set()
    for station in reader:
      if station["RepairOfEscalators"]:
        dates_of_repair = [element.lstrip("RepairOfEscalators:").split("-") for element in station["RepairOfEscalators"].split("\n") if element]
        for date_pair in dates_of_repair:
          end_of_repair = date_pair[-1]
          try:
            date_end_of_repair = datetime.strptime(end_of_repair, "%d.%m.%Y") 
            if date_end_of_repair > datetime.today():
              stations.add(station["Name"].split(", ")[0])
          except ValueError:
            print(f"Ошибка в идентификации времени на станции {station['Name'].split(', ')[0]}")
    print(*stations, sep = "\n")

def stops_near_metro():
  with open("bus_stops.csv", "r", encoding="windows-1251") as bus_stops, open("metro_stations.csv", "r", encoding="windows-1251") as metro_stations:
    fields_bus = ["ID", "Name", "Longitude_WGS84","Latitude_WGS84", "AdmArea", "District", "RouteNumbers", "StationName", "Direction", "Pavilion", "OperatingOrgName", "EntryState", "global_id", "PlaceDescription", "Works", "geodata_center", "geoarea"]
    fields_metro = ["ID","Name", "OnTerritoryOfMoscow", "AdmArea", "District", "Longitude_WGS84", "Latitude_WGS84", "VestibuleType", "NameOfStation", "Line", "CulturalHeritageSiteStatus","ModeOnEvenDays", "ModeOnOddDays", "FullFeaturedBPAAmount", "LittleFunctionalBPAAmount", "BPAAmount", "RepairOfEscalators", "ObjectStatus", "global_id"]
    reader_bus = list(csv.DictReader(bus_stops, fields_bus, delimiter=";"))
    reader_metro = list(csv.DictReader(metro_stations, fields_metro, delimiter=";"))
    stops_near_stations = {}
    for metro_station in reader_metro:
      metro_coordinates = (float(metro_station["Latitude_WGS84"]), float(metro_station["Longitude_WGS84"]))
      for bus_stop in reader_bus:
        bus_coordinates = (float(bus_stop["Latitude_WGS84"]), float(bus_stop["Longitude_WGS84"]))
        try:
          distance_between = distance.distance(metro_coordinates, bus_coordinates).meters
        except Exception:
          distance_between = None
        if distance_between is not None and distance_between <= 500:
          stops_near_stations[metro_station['Name'].split(", ")[0]] = stops_near_stations.get(metro_station['Name'], 0) + 1
    print(stops_near_stations)
    

def main():
  bus_stations()
  metro_repair_of_escalators()
  stops_near_metro()

if __name__ == "__main__":
  main()

    

  