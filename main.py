from tkinter import *
from tkinter import messagebox
import json
import requests

from PIL import ImageTk, Image
import io




OWM_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'

weather_api_key = 'YOUR API KEY'

city_endpoint = 'https://api.openweathermap.org/data/2.5/weather'

OWM_PNG_ENDPOINT = 'https://openweathermap.org/img/wn/09d@2x.png'


''' Kelvin to fahrenheit conversion function:'''
def kel_to_feh(kel:float):
    feh = int((kel - 273.15) * 1.8 + 32)
    print(f'kelvin -> Fahrenheit: {feh}')
    return feh

'''Find location based off of location input(CITY ONLY).
    - overides gui placeholders with new info to then send back to tkinter to update.'''
def find_location_data():

    location = location_entry.get()

    city = {
        'q': location,
        'appid': weather_api_key
    }

    test_city = requests.get(url=city_endpoint, params=city)
    if test_city:
        test_city.raise_for_status()
        city_data = test_city.json()
        print(f"city data search:\n{city_data}")

        city_name = city_data['name']
        country_init = city_data['sys']['country']
        kelvin_temp = city_data['main']['temp']
        kelvin_feels = city_data['main']['feels_like']
        icon = city_data['weather'][0]['icon']
        city_weather = city_data['weather'][0]['main'] 

        print(city_name, country_init, kelvin_temp, kelvin_feels)
        feh_temp = kel_to_feh(kelvin_temp)
        feh_feels = kel_to_feh(kelvin_feels)
        print(f'feh temps: {feh_temp}, {feh_feels}')

        location_label['text'] = f'{city_name}, {country_init}'
        
        asset = f'./assets/{icon}.png'
        img['bitmap'] = f'{asset}'

        temp_label['text'] = f'Temp: {feh_temp}, feels like {feh_feels}'
        weather_label['text'] = f'{city_weather}'
    
    else:
        location_label['text'] = f'Please check spelling (city name only).\nCity info not available.'

 

'''Main Code starts Here:
    -GUI Frame.'''
window = Tk()
window.title('Weather App')
window.geometry('300x300')
window.resizable(0,0)


# Location Entry:
location_entry = Entry(width=20)
location_entry.pack()

# Search Button:
generate_location_weather = Button(text="Search Location", width=15, command=find_location_data)
generate_location_weather.pack()

# Location Label:
location_label = Label(text='City Location:')
location_label.pack()

img = Label(window, text='img here', bitmap='')
img.pack()

temp_label = Label(text='City Temp')
temp_label.pack()

weather_label = Label(text='Weather')
weather_label.pack()


window.mainloop()

