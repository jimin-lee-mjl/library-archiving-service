import requests
from flask import Blueprint, render_template, request, url_for

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET'])
def book_main():
    URL = 'http://127.0.0.1:5000/api/book'
    data = requests.get(URL).json()
    result = data['result']
    return render_template('book_main.html', book_list=result)