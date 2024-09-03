from flask import Flask, redirect, render_template, request, url_for
from forms import LengthChoiceForm
from models import db, Word
from flask_wtf.csrf import CSRFProtect
import random

'''
Инициация приложения, базы данных и csfr-защиты.
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = b'b5dcce18896741e207a586ddec41365f525811129583f8f9000b713ccbb180b5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
csrf = CSRFProtect(app)
db.init_app(app)


# Константа, хранящая список разрешенных к вводу букв
REQUIRED_LETTERS = [chr(i) for i in range(ord('а'), ord('я')+1)]
BORDER_1 = 6  # Константа максимальной длины слова - 6 букв


'''
Определение переменных, которые будут использованы в функциях-представлениях.
'''
word = Word()  # переменная для хранения загаданного слова
word_to_display = ''  # переменная для хранения слова, угадываемого пользователем
message = ''  # сообщение для игрока
tries = 0  # количество использованных игроком попыток
guessed_letters = []  # список уже угаданных букв для избежания дублирования
max_length = 6  # максимальная длина слова, которую выберет игрок, по умолчанию - 6 букв
fails = 0  # количество неудачных попыток игрока
# уровень сложности на основании максимальной длины слова, по умолчанию - легкий
is_hard = False


'''
Функция случайного выбора слова из базы данных.
Слово должно быть длиной либо 6 и менее букв, либо от 7 до 12 букв.
Принимает выбранную игроком границу длины слова, возвращает случайно выбранное слово в указанном диапазоне.
'''


def get_word(maximum_len):
    if maximum_len == BORDER_1:
        word_list = Word.query.filter(Word.word_len <= maximum_len).all()
    else:
        word_list = Word.query.filter(Word.word_len > BORDER_1).all()
    word = random.choice(word_list).text
    return word


'''
Запуск стартовой страницы.
'''


@app.get('/')
def start():
    return render_template('start.html')


'''
Запуск финишной страницы.
'''


@app.get('/finish')
def finish():
    return render_template('finish.html')


'''
Запуск страницы с формой выбора максимальной длины слова.
'''


@app.route('/choose_length', methods=["POST", "GET"])
def choose_length():
    global max_length
    form = LengthChoiceForm()
    # получение максимальной длины слова из формы
    if request.method == 'POST' and form.validate():
        max_length = int(form.word_length.data)
        return redirect(url_for('guess'))  # переход к началу игры
    return render_template('choose_length.html', form=form)


'''
Запуск страницы с началом игры.
'''


@app.get('/guess')
@csrf.exempt
def guess():
    global tries
    global word
    global word_to_display
    global fails
    global max_length
    global is_hard

    word = get_word(max_length)  # выбор загадываемого слова

    # определение количества попыток на основании длины слова
    tries = 6 if len(word) <= 6 else 9
    if tries == 9:
        is_hard = True

    # обнуление количества неудачных попыток при повторном запуске игры
    fails = 0

    # исходный вариант отображаемого слова: первая и последняя буквы
    word_to_display = word[0] + '_' * (len(word)-2) + word[-1]
    return render_template('guess.html', word_to_display=word_to_display, tries=tries, fails=fails, is_hard=is_hard)


'''
Основная логика игры.
'''


@app.post('/guess')
@csrf.exempt
def guess_post():

    global tries
    global word_to_display
    global fails
    global message
    global is_hard

    if tries >= 1:
        # считывание и сохранение введенной буквы
        message = ''
        letter = request.form.get('letter').lower()

        # проверка на корректность введенной буквы
        while not letter in REQUIRED_LETTERS:
            message = 'Введи корректную букву русского алфавита'
            return render_template('guess.html', word_to_display=word_to_display, tries=tries, fails=fails, message=message)

        # проверка: использована ли буква ранее
        while letter in guessed_letters:
            message = 'Эта буква уже использована, введи другую'
            return render_template('guess.html', word_to_display=word_to_display, tries=tries, fails=fails, message=message)

        # уменьшение количества попыток, сохранение введенной буквы в списке использованных
        tries -= 1
        guessed_letters.append(letter)

        # если буква есть в слове, она выводится столько раз, сколько встречается, если нет - увеличивается количество неудачных попыток
        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    word_to_display = word_to_display[:i] + \
                        letter+word_to_display[i+1:]
        else:
            fails += 1

        # Успешное завершение игры, слово угадано. Очистка списка использованных букв, перенаправление на финальную страницу.
        if word_to_display == word:
            message = f'Молодец! Ты угадал слово {word}'
            guessed_letters.clear()
            return redirect(url_for('final', message=message))

        # Окончание попыток, слово не угадано. Очистка списка использованных букв, перенаправление на финальную страницу.
        if tries == 0:
            message = f'Не угадал! Слово {word}'
            guessed_letters.clear()
            return redirect(url_for('final', message=message))

        return render_template('guess.html', word_to_display=word_to_display, tries=tries, fails=fails, message=message, is_hard=is_hard)


'''
Запуск финальной страницы игры:
отображает либо сообщение о выигрыше либо о проигрыше игрока.
'''


@app.get('/final')
def final():
    return render_template('final.html', word=word, message=message)


'''
Команда для инициации базы данных.
'''


@app.cli.command("init-db")
def init_db():
    db.create_all()


'''
Команда для заполнения базы данных словами из файла.
'''


@app.cli.command("add-words")
def add_words():
    with open('word_list.txt', 'r', encoding='utf-8') as file:
        for line in file:
            word = Word(text=line[:-1], word_len=len(line[:-1]))
            db.session.add(word)

    db.session.commit()


'''
Команда для удаления базы данных.
'''


@app.cli.command("delete-db")
def delete_db():
    db.drop_all()


if __name__ == "__main__":
    app.run(port=8001)
