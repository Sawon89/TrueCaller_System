from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import webbrowser
from threading import Timer
from geopy.geocoders import OpenCage
import folium

# Replace with your OpenCage API key
geolocator = OpenCage('93fee26030594b0181f1af0b78bda335')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    info = None
    if request.method == "POST":
        number = request.form["phone"]
        map_html = None

        try:
            parsed_number = phonenumbers.parse(number, "BD")
            location_name = geocoder.description_for_number(parsed_number, "en")

            # Get coordinates from OpenCage
            location = geolocator.geocode(location_name)

            if location:
                latitude = location.latitude
                longitude = location.longitude

                # Professional styled map
                m = folium.Map(
                    location=[latitude, longitude],
                    zoom_start=8,
                    tiles="CartoDB positron"
                )
                folium.Marker(
                    [latitude, longitude],
                    popup=f"{location_name}",
                    tooltip="Phone Location 📍",
                    icon=folium.Icon(color="blue", icon="phone", prefix="fa")
                ).add_to(m)

                map_html = m.get_root().render()

            info = {
                "Number": number,
                "Valid": phonenumbers.is_valid_number(parsed_number),
                "Possible": phonenumbers.is_possible_number(parsed_number),
                "Country": geocoder.description_for_number(parsed_number, "en"),
                "Operator": carrier.name_for_number(parsed_number, "en"),
                "Time Zone": timezone.time_zones_for_number(parsed_number)
            }
            if map_html:
                info["Map"] = map_html

        except Exception as e:
            info = {"Error": str(e)}

    return render_template("index.html", info=info)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
