from flask import Flask, render_template, request
from hhparsing import parce
from hhparsingAlh import parce_Alh
from sqlite3 import connect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/form/', methods=['GET'])
def form_get():
    return render_template('form.html')

@app.route('/form/', methods=['POST'])
def form_post():
    # Получаем данные формы поиска
    vacancy = request.form['vacancy']
    where = request.form['where']
    region = request.form['where_area']
    search = [vacancy, where, region]
    data = parce_Alh(vacancy, where, region)
    return render_template('results.html', data=data, search=search)


@app.route('/about/')
def results_get():
    return render_template('about.html')

@app.route('/contacts/')
def test_get():
    return render_template('contacts.html')

if __name__ == "__main__":
    app.run(debug=True)