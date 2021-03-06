from flask import Blueprint, jsonify, g
from flask_restful import Api, Resource, reqparse
from service import mark_service

bp = Blueprint('mark', __name__, url_prefix='/mark')
api = Api(bp)

parser = reqparse.RequestParser()
parser.add_argument('book_id')


class Mark(Resource):
    def post(self):
        args = parser.parse_args()
        mark_service.create_mark(args['book_id'], g.user.id)
        return jsonify(
            status = 'success',
            result = {'book_id':args['book_id']}
        )

    def delete(self):
        args = parser.parse_args()
        mark_service.delete_mark(args['book_id'], g.user.id)
        return jsonify(
            status = 'success',
            result = {'book_id':args['book_id']}
        )


api.add_resource(Mark, '/')
