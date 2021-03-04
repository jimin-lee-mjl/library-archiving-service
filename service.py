from db import db, Book, Rental, User
from error_msg import ServiceError


class BookService():
    def __init__(self, book_id, user_id):
        self.book = Book.query.filter_by(id=book_id).first()
        self.user = User.query.filter_by(id=user_id).first()

    def rental_book(self):
        if self.book.is_available():
            self.user.rental_book(self.book.id)
            self.book.rental_book()
            db.session.commit()
        else:
            raise ServiceError

    def return_book(self):
        target_book = Rental.query.filter(
            (Rental.book_id == self.book.id) & (Rental.user_id == self.user.id)
        ).first()
        self.user.return_book(target_book)
        self.book.return_book()
        target_book.return_book()
        db.session.commit()


class CommentService():
    def __init__(self, book_id, user_id):
        self.book = Book.query.filter_by(id=book_id).first()
        self.user = User.query.filter_by(id=user_id).first()

    def create_comment(self, content, rating):
        self.user.create_comment(content, rating, self.book.id)
        self.book.rating = self.book.calculate_rating()
        db.session.commit()

            