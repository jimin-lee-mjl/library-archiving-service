from app import db
from model import Book, Rental, User
from error_msg import ServiceError


class BookService():
    def get_book(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        return book
    
    def get_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def rental_book(self, book_id, user_id):
        book = self.get_book(book_id)
        user = self.get_user(user_id)

        if book.is_available():
            user.rental_book(book_id)
            book.rental_book()
            db.session.commit()
        else:
            raise ServiceError

    def return_book(self, book_id, user_id):
        book = self.get_book(book_id)
        user = self.get_user(user_id)

        target_book = Rental.query.filter(
            (Rental.book_id == book_id) & (Rental.user_id == user_id)
        ).first()
        user.return_book(target_book)
        book.return_book()
        target_book.return_book()
        db.session.commit()

    def user_has_book(self, book_id, user_id):
        user = self.get_user(user_id)
        try:
            rent_book = [book for book in user.rentals if book.book_id == book_id][0]
            return True
        except:
            return False


class CommentService():
    def get_book(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        return book

    def get_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def create_comment(self, book_id, user_id, content, rating):
        book = self.get_book(book_id)
        user = self.get_user(user_id)

        user.create_comment(content, rating, book_id)
        book.rating = book.calculate_rating()
        db.session.commit()

    def show_comment(self, book_id):
        book = self.get_book(book_id)
        book.comment.reverse()
        return book.comment
           

book_service = BookService()
comment_service = CommentService()