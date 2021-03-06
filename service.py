from datetime import datetime
from app import db
from model import Book, Rental, User, Comment, Mark
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
        return user.check_rental(book_id)

    def get_search_book(self, word):
        search = '%{}%'.format(word)
        result = Book.query.filter(Book.name.like(search)).all()
        return result


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

    def show_comments(self, book_id):
        book = self.get_book(book_id)
        book.comment.reverse()
        return book.comment

    def get_user_comment(self, book_id, user_id):
        comment = Comment.query.filter(
            (Comment.book_id == book_id) & (Comment.user_id == user_id)
        ).first()
        return comment 

    def update_comment(self, book_id, user_id, content, rating):
        comment = Comment.query.filter(
            (Comment.book_id == book_id) & (Comment.user_id == user_id)
        ).first()
        updated_at = datetime.now().date()
        comment.update(content, rating, updated_at)
        db.session.commit()

    def delete_comment(self, book_id, user_id):
        comment = Comment.query.filter(
            (Comment.book_id == book_id) & (Comment.user_id == user_id)
        ).first()
        db.session.delete(comment)
        db.session.commit()

    def update_rating(self, book_id):
        book = self.get_book(book_id)
        book.rating = book.calculate_rating()
        db.session.commit()


class MarkService():
    def get_book(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        return book
    
    def get_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def get_marks(self, user_id):
        user = self.get_user(user_id)
        return user.marks

    def create_mark(self, book_id, user_id):
        user = self.get_user(user_id)
        user.create_mark(book_id)
        db.session.commit()

    def delete_mark(self, book_id, user_id):
        book = Mark.query.filter(
            (Mark.book_id == book_id) & (Mark.user_id == user_id)
        ).first()
        db.session.delete(book)
        db.session.commit()

    def check_mark(self, book_id, user_id):
        user = self.get_user(user_id)
        return user.check_mark(book_id)


book_service = BookService()
comment_service = CommentService()
mark_service = MarkService()