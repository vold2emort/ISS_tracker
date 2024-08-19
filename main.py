import requests
from datetime import datetime
import smtplib
from app_password import PASSWORD

MY_LAT = 27.664400
MY_LONG = 85.318794
MY_EMAIL = "pramishkc066@gmail.com"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


def pos(my_lat, my_lng, iss_lat, iss_lng):
    is_within_lat = my_lat - 5 <= iss_lat <= my_lat + 5
    is_within_lng = my_lng - 5 <= iss_lng <= my_lng + 5
    if is_within_lat and is_within_lng:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(f"The sunset time is {data['results']['sunset']} UTC")
print(f"The sunrise time is {data['results']['sunrise']} UTC")
time_now = datetime.now().hour
print(f"Time now is {datetime.now().time()} UTC")
print(iss_latitude, iss_longitude)


def is_dark(time, sun_rise, sun_set):
    dark = sun_set < time < sun_rise
    if dark:
        return True
    else:
        return False
# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


if is_dark and pos(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="pramishkc76@gmail.com",
                            msg=f"Subject:Alert!!\n\nISS STATION")
else:
    print(f"The current Position of INTERNATIONAL SPACE STATION "
          f"is ({iss_longitude} lng,{iss_latitude} lat), Your position is ({MY_LONG} lng, {MY_LAT} lat"
          f"!!\nThe ISS is not near SO YOU WILL NOT GET ANY EMAIL.")
