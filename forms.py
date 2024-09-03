from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

'''
Форма выбора максимальной длины слова.
Представляет собой поле выбора из 2 вариантов.
'''


class LengthChoiceForm(FlaskForm):
    word_length = SelectField('word_length', choices=[('6', '6'),
                                                      ('12', '12')], validators=[DataRequired()])
