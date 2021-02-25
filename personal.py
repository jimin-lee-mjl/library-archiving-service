from flask import Blueprint, render_template, g, request, redirect, url_for
from datetime import datetime, timedelta
from auth import login_required
from db import Book, Rental, db

bp = Blueprint('personal', __name__, url_prefix='/personal')


@bp.route('/book', methods=['GET', 'POST'])
@login_required
def personal_rental():
    current_user = g.user
    if request.method == 'POST':
        book_id = request.form['book_id']
        target = Book.query.filter_by(id=book_id).first()
        rental_book = Rental.query.filter(
            Rental.book_id == book_id and Rental.user_id == current_user.id
        ).first()
        target.available += 1
        rental_book.return_date = (datetime.now()+timedelta(hours=9)).date()
        current_user.rentals.remove(rental_book)
        db.session.commit()
        return redirect(url_for('.personal_rental'))

    rental_list = []
    for book in current_user.rentals:
        rental_list.append({
            'book_id': book.book_id,
            'name': book.book_detail.name,
            'rental_date': book.rental_date
        })

    return render_template('personal_rental.html', rentals=rental_list)
