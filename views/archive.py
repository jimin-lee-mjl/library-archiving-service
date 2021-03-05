from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from app import db
from model import Book, Rental
from auth import login_required
from service import comment_service, mark_service, book_service
from error_msg import CommentError

bp = Blueprint('archive', __name__, url_prefix='/archive')


@bp.route('/marks', methods=['GET', 'POST'])
@login_required
def mark_archive():
    marks = mark_service.get_marks(g.user.id)
    return render_template('mark_archive.html', marks=marks, service=book_service, user_id=g.user.id)


@bp.route('/books', methods=['GET'])
@login_required
def book_archive():
    books = Rental.query.filter(
        (Rental.user_id_history == g.user.id) & (Rental.return_date)
    ).order_by(Rental.rental_date.desc()).all()
    return render_template('book_archive.html', books=books) 


@bp.route('/comment/<int:book_id>', methods=['GET'])
@login_required
def manage_comment(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comment = comment_service.get_user_comment(book_id, g.user.id)
    return render_template('book_comment.html', book=book, comment=comment)


@bp.route('/comment/<int:book_id>/create', methods=['POST'])
@login_required
def create_comment(book_id):
    content = request.form['comment']
    rating = request.form['rating']
    if not content:
        flash(CommentError.content.REQUIRED, 'comment_error')
    elif not rating:
        flash(CommentError.star.REQUIRED, 'comment_error')
    else:
        comment_service.create_comment(book_id, g.user.id, content, rating)
    return redirect(url_for('archive.manage_comment', book_id=book_id))



@bp.route('/comment/<int:book_id>/update', methods=['POST'])
@login_required
def update_comment(book_id):
    content = request.form['comment']
    rating = request.form['rating']
    comment_service.update_comment(book_id, g.user.id, content, rating)
    comment_service.update_rating(book_id)
    return redirect(url_for('archive.manage_comment', book_id=book_id))



@bp.route('/comment/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_comment(book_id):
    comment_service.delete_comment(book_id, g.user.id)
    comment_service.update_rating(book_id)
    return redirect(url_for('archive.manage_comment', book_id=book_id))
