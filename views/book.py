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
from error_msg import RentalError, CommentError, ServiceError
from service import BookService, CommentService

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET'])
@bp.route('/<int:page_num>', methods=['GET'])
@login_required
def book_main(page_num=1):
    books = Book.query.paginate(per_page=8, page=page_num, error_out=False)
    return render_template('book_main.html', book_list=books)


@bp.route('/detail/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comments = book.comment

    if request.method == 'POST':
        content = request.form['comment']
        rating = request.form['rating']
        if not content:
            flash(CommentError.content.required, 'comment_error')
        elif not rating:
            flash(CommentError.star.required, 'comment_error')
        else:
            current_user = g.user
            current_user.create_comment(content, rating, book_id)
            book.rating = book.calculate_rating()
            db.session.commit()
        return redirect(url_for('.book_detail', book_id=book_id))

    comments.reverse()
    return render_template('book_detail.html', book=book, comments=comments)


@bp.route('/rental', methods=['POST'])
@login_required
def rental_book():
    # current_user = g.user
    book_id = request.form['book_id']
    # target_book = Book.query.filter_by(id=book_id).first()
    
    book_service = BookService(book_id, g.user.id)
    try:
        book_service.rental_book()
    except ServiceError:
        flash(RentalError.stock.INAVAILABLE)
        return redirect(url_for('book.book_main'))

    # if target_book.is_available():
    #     target_book.rental_book()
    #     current_user.rental_book(target_book.id)
    #     db.session.commit()
    # else:
    #     flash(RentalError.stock.INAVAILABLE)
    #     return redirect(url_for('book.book_main'))

    return redirect(url_for('personal.personal_rental'))

    

