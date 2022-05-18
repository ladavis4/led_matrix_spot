from flask import Flask, render_template, request

app = Flask(__name__)
data={'button_img':True, 'button_time': True, 'button_cal':True}



@app.route('/', methods=['POST', 'GET'])
def splash():
    if request.method == 'GET':
        return render_template('form.html', data=data)
    if request.method == 'POST':
        form_data = request.form
        for key, value in data.items():
            data[key] = False

        for key, value in form_data.items():
            data[key] = value == 'true'
        return render_template('form.html', data=data)

if __name__ == '__main__':
    app.run()
