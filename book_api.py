from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from db import Book

bp = Blueprint('book_api', __name__, url_prefix='/api/book')
api = Api(bp)


class BookMain(Resource):
    def get(self):
        book_list = []
        books = Book.query.all()
        for book in books:
            book_list.append({
                'name': book.name,
                'rating': book.rating,
                'available': book.available
            })
        return jsonify(status='success', result=book_list)


api.add_resource(BookMain, '/')
