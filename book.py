from flask import (
    Blueprint,
    render_template,
    request,
    g,
    redirect,
    url_for,
    flash
)
from db import Book, Rental, db
from auth import login_required
from error_msg import RENTAL_ERROR

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def book_main():
    if request.method == 'POST':
        current_user = g.user
        book_id = request.form['book_id']
        target = Book.query.filter_by(id=book_id).first()

        if target.available == 0:
            flash(RENTAL_ERROR['no_stock'])
            return redirect(url_for('.book_main'))

        rental_book = Rental(
            book_id=book_id
        )
        current_user.rentals.append(rental_book)
        target.available -= 1
        db.session.commit()
        return redirect(url_for('personal.personal_rental'))

    book_list = []
    books = Book.query.all()

    for book in books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'rating': book.rating,
            'available': book.available
        })
    return render_template('book_main.html', book_list=book_list)


@bp.route('/<book_id>', methods=['GET'])
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return render_template('book_detail.html', book=book)
