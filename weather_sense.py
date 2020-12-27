#!/usr/bin/python3
import socket
import json
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_rotation(180)

while True:
    inside_temp      = str(round(sense.temp))
    inside_humidity  = str(round(sense.humidity))
    inside_pressure  = str(round(sense.pressure))

    try:
        s = socket.socket()
        addr = socket.getaddrinfo('api.openweathermap.org', 80)

        s.connect(addr[0][4])
        s.send(b'GET http://api.openweathermap.org/data/2.5/weather?lat=53.26&lon=-6.21&appid=84ddwwfccdada49bc40acvvev3ef7&units=metric HTTP/1.0\r\n\r\n')

        html = s.recv(1000)
        div = html.split(b'\r\n\r\n')[-1]
        data = json.loads(div)
        s.close()

        outside_temp = str(round(data['main']['temp']))
        outside_humidity = str(round(data['main']['humidity']))
        feel = str(round(data['main']['feels_like']))
        desc = data['weather'][0]['description']
        wind = str(round((data['wind']['speed']) * 3.6))
        outside_pressure = str(round(data['main']['pressure']))
        outside_max = str(round(data['main']['temp_max']))
        outside_min = str(round(data['main']['temp_min']))

        sense.show_message("Inside: "  + inside_temp  + "'C " + inside_humidity  + "% " + inside_pressure + "mb", text_colour = (0,155,0), scroll_speed=0.03)
        sense.show_message("Outside: " + outside_temp + "'C " + outside_humidity + "% " + outside_pressure + "mb", text_colour = (155,0,0), scroll_speed=0.03)
        sense.show_message("Feels: " + feel + "'C Min: " + outside_min + "\'C Max: " + outside_max + "\'C", text_colour = (155,0,155), scroll_speed=0.03)
        sense.show_message("Wind: " + wind + "km/h " + desc.title(), text_colour = (155,0,155), scroll_speed=0.03)

    except Exception as e:
        #print(e)
        sense.show_message("Inside: "  + inside_temp  + "'C " + inside_humidity  + "% " + inside_pressure + "mb", text_colour = (0,155,0), scroll_speed=0.03)

    time.sleep(1)
