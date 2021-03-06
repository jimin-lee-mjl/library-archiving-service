from flask import Blueprint, g, render_template, url_for, redirect, request
from auth import login_required
from service import book_service

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def dashboard():
    rentals = g.user.rentals
    return render_template('dashboard.html', rentals=rentals,
                                             username=g.user.username,
                                             length=len(rentals))


@bp.route('/search', methods=['GET'])
@login_required
def search_book():
    word = request.args.get('search')
    books = book_service.get_search_book(word)
    return render_template('search_book.html', books=books, 
                                               user_id=g.user.id, 
                                               service=book_service)
