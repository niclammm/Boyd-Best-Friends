import gspread
from oauth2client.service_account import ServiceAccountCredentials
import folium
from folium.plugins import PolyLineTextPath

def read_google_sheet():
    # Google Sheets setup
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheets spreadsheet
    sheet = client.open("Boyd_Best_Friends").sheet1

    # Extract the data from the first sheet
    data = sheet.get_all_values()
    return data

def write_to_file(data):
    with open("locations.txt", "w") as file:
        for row in data:
            try:
                name, latitude, longitude = row
                file.write(f"{name},{latitude},{longitude}\n")
            except ValueError:
                print(f"Skipping row with invalid data: {row}")

def read_locations_from_file():
    locations = []
    with open("locations.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                name, latitude, longitude = line.strip().split(',')
                locations.append({"name": name, "latitude": float(latitude), "longitude": float(longitude)})
            except ValueError:
                print(f"Skipping line with invalid data: {line.strip()}")
    return locations

def create_map(locations):
    if not locations:
        print("No valid locations found.")
        return

    # Calculate the center of all locations
    avg_lat = sum(loc["latitude"] for loc in locations) / len(locations)
    avg_lon = sum(loc["longitude"] for loc in locations) / len(locations)

    # Create a map centered at the average location
    mymap = folium.Map(location=[avg_lat, avg_lon], zoom_start=25)

    # Add markers for each location and connect them with a polyline with directional arrows
    previous_location = None
    for location in locations:
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mymap)
        if previous_location:
            polyline = folium.PolyLine(
                locations=[
                    (previous_location["latitude"], previous_location["longitude"]),
                    (location["latitude"], location["longitude"])
                ],
                color='blue'
            ).add_to(mymap)
            # Add directional arrows to the polyline
            PolyLineTextPath(
                polyline,
                '→',
                repeat=True,
                offset=7,
                attributes={'font-size': '24', 'fill': 'blue'}
            ).add_to(mymap)
        previous_location = location

    # Save the map as an HTML file
    mymap.save("mymap.html")

if __name__ == "__main__":
    data = read_google_sheet()
    write_to_file(data)
    locations = read_locations_from_file()
    create_map(locations)
