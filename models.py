from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
Модель загадываемого слова, которое будет храниться в базе данных.
Содержит поля: id, текстовое поле - слово, длина слова.
'''


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), unique=True,
                     nullable=False)
    word_len = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Word({self.word}, {self.word_len} symbols)'
