from enum import Enum


class AuthError(Enum):
    username = (
        None,
        '3글자 이상 15글자 이하로 작성해주세요. 숫자나 특수문자가 들어가서는 안 됩니다.',
        None
    )
    email = (
        '이미 존재하는 이메일입니다.',
        '이메일 형식이 유효하지 않습니다.',
        '존재하지 않는 사용자입니다.'
    )
    password = (
        '비밀번호가 틀렸습니다.',
        '비밀번호는 알파벳 소문자와 대문자, 숫자 중 한 가지와 특수문자를 포함해 10글자 이상이어야 합니다.',
        '비밀번호가 일치하지 않습니다.'
    )

    def __init__(self, INAVAILABLE, INVALID, NO_MATCH):
        self.INAVAILABLE = INAVAILABLE
        self.INVALID = INVALID
        self.NO_MATCH = NO_MATCH


class RentalError(Enum):
    stock = (
        '재고가 없습니다.'
    )

    def __init__(self, INAVAILABLE):
        self.INAVAILABLE = INAVAILABLE


class CommentError(Enum):
    content = (
        '한 글자 이상 감상을 적어야 합니다. '
    )
    star = (
        '별점을 매겨주세요.'
    )

    def __init__(self, REQUIRED):
        self.REQUIRED = REQUIRED


class ServiceError(Exception):
    pass