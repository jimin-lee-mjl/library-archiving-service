from flask import Blueprint, render_template, g, request, redirect, url_for
from datetime import datetime, timedelta
from app import db
from model import Book, Rental
from auth import login_required
from service import BookService

bp = Blueprint('archive', __name__, url_prefix='/archive')


@bp.route('/current', methods=['GET', 'POST'])
@login_required
def rental_current():
    current_user = g.user
    return render_template('personal_rental.html', rentals=current_user.rentals)


@bp.route('/history', methods=['GET'])
@login_required
def rental_history():
    current_user = g.user
    books = Rental.query.filter_by(user_id_history = current_user.id).all()
    return render_template('book_archive.html', books=books)



