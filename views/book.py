from flask import (
    Blueprint,
    render_template,
    request,
    g,
    redirect,
    url_for,
    flash
)
from app import db
from model import Book, Rental, Comment
from auth import login_required
from error_msg import RentalError, CommentError, ServiceError
from service import book_service, comment_service

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET'])
@bp.route('/<int:page_num>', methods=['GET'])
@login_required
def book_main(page_num=1):
    books = Book.query.paginate(per_page=8, page=page_num, error_out=False)
    return render_template('book_main.html', book_list=books, service=book_service, user_id=g.user.id)


@bp.route('/detail/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comments = comment_service.show_comments(book_id)
    return render_template('book_detail.html', book=book, comments=comments)


@bp.route('/rental', methods=['POST'])
@login_required
def rental_book():
    book_id = request.form['book_id']
    try:
        book_service.rental_book(book_id, g.user.id)
    except ServiceError:
        flash(RentalError.stock.INAVAILABLE, 'book_error')
        return redirect(url_for('book.book_main'))

    return redirect(url_for('archive.rental_current'))


@bp.route('/return', methods=['POST'])
@login_required
def return_book():
    book_id = request.form['book_id']
    book_service.return_book(book_id, g.user.id)
    return redirect(url_for('archive.rental_current'))
