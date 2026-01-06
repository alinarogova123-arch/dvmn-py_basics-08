import json
import requests
import folium
import os
from geopy import distance
from dotenv import load_dotenv


load_dotenv('.env')

APIKEY = os.getenv("APIKEY")


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_cof(user):
    return user['distance']


def coffee_nearest(locate_a):
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        file_contents = my_file.read()
    file_contents_list = json.loads(file_contents)
    coords_a = fetch_coordinates(APIKEY, locate_a)[::-1]
    cof_list = []

    for cof in file_contents_list:
        cof_list.append({
            'title': cof['Name'],
            'distance': distance.distance(coords_a, (cof['Latitude_WGS84'], cof['Longitude_WGS84'])).km,
            'latitude': cof['Latitude_WGS84'],
            'longitude': cof['Longitude_WGS84']
        })

    m = folium.Map(location=coords_a, zoom_start=15)
    folium.Marker(
        location=coords_a,
        tooltip="Вы здесь",
        popup="Timberline Lodge",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    for cof_map in sorted(cof_list, key=get_distance_cof)[:5]:
        folium.Marker(
            location=(cof_map['latitude'], cof_map['longitude']),
            tooltip=cof_map['title'],
            popup="Timberline Lodge",
            icon=folium.Icon(color="green"),
        ).add_to(m)
    m.save("index.html")


def main():
    locate_a = input('Укажите ваше местоположение: ')
    coffee_nearest(locate_a)


if __name__ == '__main__':
    main()
