from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

data = None
try: 
    with open('../temp/settings.json') as json_file:
        data = json.load(json_file)
        print("Settings loaded successfully")
except:
    print("Settings file doesn't exist, run main.py first!")


@app.route('/', methods=['POST', 'GET'])
def splash():
    if request.method == 'GET':
        return render_template('form.html', data=data)
    if request.method == 'POST':
        form_data = request.form
        for key, value in data.items():
            data[key] = False

        for key, value in form_data.items():
            if key == 'slider_brightness':
                data[key] = int(value)
            else:
                data[key] = value == 'true'


        with open('../temp/settings.json', 'w') as outfile:
            json.dump(data, outfile)

        return render_template('form.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
