from flask import render_template, request
from app import app

import geocoder


# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():

    # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    data1 = (request.environ['REMOTE_ADDR'])

    data2 = (request.environ)  # if behind a proxy

    data3 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    loc_data = geocoder.ip(data1).json
    if 'hostname' in loc_data.keys():
        hostname = loc_data['hostname']
    else:
        hostname = ''
    # return render_template('fuckingip.html', ip=loc_data['ip'],address=loc_data['address'],hostname=hostname,lat=loc_data['lat'],lon=loc_data['lng'],isp=loc_data['org'],isp_url="https://ipinfo.io/"+loc_data['org'].split(" ")[0],zipcode=loc_data['postal'])
    return render_template('fuckingip.html', ip=data1,address=data2,hostname=data3,lat=loc_data['lat'],lon=loc_data['lng'],isp=loc_data['org'],isp_url="https://ipinfo.io/"+loc_data['org'].split(" ")[0],zipcode=loc_data['postal'])
