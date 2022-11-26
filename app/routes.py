from flask import render_template, request
from app import app

import geocoder


# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data = request.environ['REMOTE_ADDR']
    else:
        data = request.environ['HTTP_X_FORWARDED_FOR']

    if data == '127.0.0.1':
        return render_template('fuckingip.html', ip='127.0.0.1', address='Your fucking computer', hostname='Your fucking hostname.',
                               lat='idfk', lon='idfc', isp='lol',
                               isp_url="127.0.0.1", zipcode="eat it")
    else:
        loc_data = geocoder.ip(data).json
        if 'hostname' in loc_data.keys():
            hostname = loc_data['hostname']
        else:
            hostname = ''
        return render_template('fuckingip.html', ip=loc_data['ip'],address=loc_data['address'],hostname=hostname,lat=loc_data['lat'],lon=loc_data['lng'],isp=loc_data['org'],isp_url="https://ipinfo.io/"+loc_data['org'].split(" ")[0],zipcode=loc_data['postal'])
