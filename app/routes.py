from flask import render_template, request
from app import app

import geocoder
import random

words = {
    "header": [
        "here's your fucking public connection data.",
        "here it is.  that fucking info you asked for.  is that <i>all</i>?",
        "here's your goddamn shit, asshat.  next time just curl canhazip.com.",
        ],
    "ip": [
        "your goddamn public IP address",
        "your fucking public IP address",
        "your router's fucking public address",
        "the fucking ip address you can be found at",
        "your fucking public IP",

    ],
    "address": [
        "an approximate fucking location that's probably wrong as shit",
        "fucking best guess at location",
        "this might be near your fucking house",
        "is this where you live?  I hear it's fucking nice there.",
    ],
    "zipcode": [
           "stupid motherfucking zip code",
        "fucking zip code",
        "here's your stupid fucking zipcode",
        "fuck, who gives a fuck about zipcodes???",
        "here's your fuckin' fancy little fuckin' zip code, bitch"
        ],
    "lat": [
        "your fucking latitude",
        "your goddamn fucking stupid latitude",
        "your motherfucking latitude",
        "your dumb fuckin' latitude",
        "your whore-ass latitude",
        "your fucking latitude coordinate"
        ],
    "long": [
        "and your fucking longitude",
        "and your goddamn fucking stupid longitude",
        "and your motherfucking longitude",
        "and your dumb fuckin' longitude",
        "and your whore-ass longitude",
        "and your fucking longitude coordinate"
        ],
    "maps": [
        "here's a fucking google maps link",
        "here's a fuckin' link in case you didn't know where your general area is",
        "here's a handy motherfucking google maps link",
        "here, fuckin' click this link so Google knows where you live"
    ],
    "hostname": [
        "a bullshit fucking hostname from your ISP",
        "your fucking IP address in a DNS name, depending on your fucking ISP",
        "some fucking DNS shit that might not be right",
        "your associated fucking DNS record",
        "some random fucking dns fuckery",
    ],
    "isp": [
           "might be the cocksucker you pay for internet",
            "best guess at the assole you pay for internet",
            "Your Fucking Internet Service Provider",
            "Your Internet Fucking Service Provider",
            "Your Fucking Interfuckingnet Service Provider",
            "i bet this fucking asshole overcharges you for internet",
    ]
}




# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data = request.environ['REMOTE_ADDR']
    else:
        data = request.environ['HTTP_X_FORWARDED_FOR']

    if data == '127.0.0.1':
        header = random.choice(words['header'])


        payload = {
            random.choice(words['ip']): '127.0.0.1',
            random.choice(words['address']): 'Your fuckin house',
            random.choice(words['zipcode']): '69420',
            random.choice(words['lat']): '11.01',
            random.choice(words['long']): '11.11',
            random.choice(words['maps']): 'https://thc-lab.net',
            random.choice(words['hostname']): 'home.thc-lab.net',

        }

        isp_payload = {
            "header": random.choice(words['isp']),
            "url": "thc-lab.net",
            "name": "Fuckin' THC's Lab, Bitch!"
        }

        return render_template('fuckingip.html',
                               payload=payload,
                               isp_payload=isp_payload,
                               header=header)
    else:
        loc_data = geocoder.ip(data).json
        if 'hostname' in loc_data.keys():
            hostname = loc_data['hostname']
        else:
            hostname = ''

        maps_url = f'https://www.google.com/maps/place/@{loc_data["lat"]},{loc_data["lng"]}'


        header = random.choice(words['header'])

        payload = {
            random.choice(words['ip']): loc_data['ip'],
            random.choice(words['address']): loc_data['address'],
            random.choice(words['zipcode']): loc_data['postal'],
            random.choice(words['lat']): loc_data['lat'],
            random.choice(words['long']): loc_data['lng'],
            random.choice(words['maps']): maps_url,
            random.choice(words['hostname']): hostname,

        }

        isp_payload = {
            "header": random.choice(words['isp']),
            "url": "https://ipinfo.io/" + loc_data['org'].split(" ")[0],
            "name": loc_data['org']
        }

        return render_template('fuckingip.html',
                               isp_payload=isp_payload,
                               payload=payload,
                               header=header)
