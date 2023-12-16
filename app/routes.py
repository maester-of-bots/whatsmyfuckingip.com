from flask import render_template, request
from app import app
from app.data import *
from dotenv import load_dotenv
import os
import geocoder
import random
import requests


def loc_get_IPInfo(data):
    """Use Geocoder / IPInfo to get data"""

    loc_data = geocoder.ipinfo(data).json

    if loc_data:

        data = {
            "ip": loc_data['ip'],
            "hostname": loc_data['hostname'],
            "address": loc_data['address'],
            "postal": loc_data['postal'],
            "lat": loc_data['lat'],
            'lng': loc_data['lng'],
            'org': loc_data['org'],
            'src1': "https://ipinfo.io/",
            'src2': "IPInfo"
        }

        return data

    else:
        return False

def loc_get_IPGeolocation(ip_address):
    """Use the free API key for IPGeolocation.io to get data"""

    load_dotenv()
    api_key = os.getenv('ipgeolocation_key')
    url = f"http://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        data = {
            "ip": results['ip'],
            "hostname": "Missing",
            "address": f"{results['city']} {results['state_prov']}, {results['country_name']}",
            "postal": results['zipcode'],
            "lat": results['latitude'],
            'lng': results['longitude'],
            'org': "Missing",
            'src1': "https://ipgeolocation.io/",
            'src2': "IP Geolocation"
        }
        return data
    else:
        return False
def loc_get_ipapi(ip_address):
    """Get data using a nifty free no-key API"""

    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        data = {
            "ip": results['query'],
            "hostname": "Missing",
            "address": f"{results['city']} {results['regionName']}, {results['country']}",
            "postal": results['zip'],
            "lat": results['lat'],
            'lng': results['lon'],
            'org': results['as'],
            'src1': "http://ip-api.com/",
            'src2': "IP-API"
        }
        return data
    else:
        return False




def master_getter(IP):
    try:
        data_best = loc_get_IPInfo(IP)
        if data_best:
            return data_best
        else:
            raise
    except Exception as e:
        print(e)

    try:
        data_mid = loc_get_IPGeolocation(IP)
        if data_mid:
            return data_mid
        else:
            raise
    except Exception as e:
        print(e)

    try:
        data_desperate = loc_get_ipapi(IP)
        if data_desperate:
            return data_desperate
        else:
            raise
    except Exception as e:
        print(e)
        return False







# Main page, there's nothing here...
@app.route('/dns.html', methods=['GET', 'POST'])
def dns():
    data = request.environ['REMOTE_ADDR']


# Main page, there's nothing here...
@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data = request.environ['REMOTE_ADDR']
    else:
        data = request.environ['HTTP_X_FORWARDED_FOR']

    loc_data = master_getter(data)
    return loc_data['ip']

# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data = request.environ['REMOTE_ADDR']
    else:
        data = request.environ['HTTP_X_FORWARDED_FOR']

    loc_data = master_getter(data)

    # Set the hostname or leave it blank
    if 'hostname' in loc_data.keys():
        if loc_data['hostname'] != "Missing":
            hostname = loc_data['hostname']
        else:
            hostname = 'hah, like they\'d give you a fucking hostname'
    else:
        hostname = 'hah, like they\'d give you a fucking hostname'

    # Craft a URL for Google Maps based on the lat/lon
    maps_url = f'https://www.google.com/maps/place/@{loc_data["lat"]},{loc_data["lng"]}'

    # Pull the header
    header = random.choice(words['header'])

    # Generate the payload with random phrases, and their corresponding data from the location data
    payload = {
        random.choice(words['ip']): loc_data['ip'],
        random.choice(words['hostname']): hostname,
        random.choice(words['address']): loc_data['address'],
        random.choice(words['zipcode']): loc_data['postal'],
        random.choice(words['lat']): loc_data['lat'],
        random.choice(words['long']): loc_data['lng']
    }

    src_payload = {
        'src_url': loc_data['src1'],
        'src_name': loc_data['src2']
    }

    # Create Google Maps payload because this needs to be separate from the others smh
    map_payload = {
        random.choice(words['maps']): maps_url,
    }

    # Create the ISP payload / information
    if " " in loc_data['org']:
        url = "https://ipinfo.io/" + loc_data['org'].split(" ")[0]
    else:
        url = "Missing"
    isp_payload = {
        "header": random.choice(words['isp']),
        "url": url,
        "name": loc_data['org']
    }

    return render_template('fuckingip.html',
                           isp_payload=isp_payload,
                           payload=payload,
                           header=header,
                           map_payload=map_payload,
                           src_payload=src_payload)
