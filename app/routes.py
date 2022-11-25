from flask import render_template, request
from app import app



# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    ip_addr = request.environ['REMOTE_ADDR']
    print(ip_addr)
    return render_template('index.html',ip=ip_addr)

