import requests
from flask import Blueprint, render_template, request, url_for
from db import Book

bp = Blueprint('book', __name__, url_prefix='/book')


# api를 만들고 requests를 통해 data를 받아와서 html 파일에 건네주는 방법
@bp.route('/', methods=['GET'])
def book_main():
    URL = 'http://127.0.0.1:5000/api/book'
    data = requests.get(URL).json()
    result = data['result']
    return render_template('book_main.html', book_list=result)


# db에서 바로 Book 테이블을 가져와서 데이터를 html 파일에 건네주는 방법
@bp.route('/<book_id>', methods=['GET'])
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return render_template('book_detail.html', book=book)