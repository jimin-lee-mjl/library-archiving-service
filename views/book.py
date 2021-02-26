from flask import (
    Blueprint,
    render_template,
    request,
    g,
    redirect,
    url_for,
    flash
)
from db import Book, Rental, Comment, db
from auth import login_required
from error_msg import RENTAL_ERROR

bp = Blueprint('book', __name__, url_prefix='/book')


def calculate_rating(comments):
    total = 0
    for comment in comments:
        rating = int(comment.rating)
        total += rating
    total_rating = round(total/len(comments))
    print('rating:', total_rating)

    return total_rating


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
            book_id=book_id,
            user_id_history=current_user.id
        )
        current_user.rentals.append(rental_book)
        target.available -= 1
        db.session.commit()
        return redirect(url_for('personal.personal_rental'))

    books = Book.query.all()
    return render_template('book_main.html', book_list=books)


@bp.route('/<book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comments = book.comment

    if request.method == 'POST':
        content = request.form['comment']
        rating = request.form['rating']
        current_user = g.user

        comment = Comment(
            content=content,
            rating=rating,
            user_id=current_user.id
        )
        comments.append(comment)
        book.rating = calculate_rating(comments)
        db.session.commit()
        return redirect(url_for('.book_detail', book_id=book_id))

    comments.reverse()
    return render_template('book_detail.html', book=book, comments=comments)

