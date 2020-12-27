#!/usr/bin/python3
import socket
import json
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_rotation(180)

# Get Weather data
def api_call():
    s = socket.socket()
    addr = socket.getaddrinfo('api.openweathermap.org', 80)

    s.connect(addr[0][4])
    s.send(b'GET http://api.openweathermap.org/data/2.5/weather?lat=53.26&lon=-6.21&appid=84d996853fcc4db149bc40acb09a3ef7&units=metric HTTP/1.0\r\n\r\n')

    html = s.recv(1000)
    div = html.split(b'\r\n\r\n')[-1]
    data = json.loads(div)

    s.close()

    temp = str(int(data['main']['temp']))
    humidity = str(int(data['main']['humidity']))
    feel = str(int(data['main']['feels_like']))
    desc = data['weather'][0]['description']
    wind = str(int((data['wind']['speed']) * 3.6))
    pressure = str(int(data['main']['pressure']))

    return temp, humidity, feel, desc, wind, pressure


while True:
    inside_temp      = str(int(sense.temp))
    inside_humidity  = str(int(sense.humidity))
    inside_pressure  = str(int(sense.pressure))

    try:
        api              = api_call()
        outside_temp     = api[0]
        outside_humidity = api[1]
        outside_pressure = api[5]
        feel             = api[2]
        desc             = api[3]
        wind             = api[4]

        sense.show_message("Inside: "  + inside_temp  + "'C " + inside_humidity  + "% " + inside_pressure, text_colour = (0,155,0), scroll_speed=0.03)
        sense.show_message("Outside: " + outside_temp + "'C " + outside_humidity + "% " + outside_pressure, text_colour = (155,0,0), scroll_speed=0.03)
        sense.show_message("Feels Like: " + feel + "'C " + "Wind: " + wind + "km/h " + desc.title(), text_colour = (155,0,155), scroll_speed=0.03)

    except Exception as e:
        #print(e)
        sense.show_message("In: " + inside_temp  + "'C " + inside_humidity  + "%", text_colour = (0,155,0), scroll_speed=0.03)
        
    time.sleep(1)
