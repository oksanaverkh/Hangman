Hangman

Данный проект представляет собой игру "Виселица".
Игроку необходить отгадать загаданное программой слово. Гарантируется, что это существительное слово русского языка.
Игрок выбирает максимальную длину слова, которое он будет угадывать:
- 6: слова до 6 букв
- 12: слова от 7 до 12 букв.
- 
За слова до 6 букв игроку дается 6 попыток для угадывания, за слова до 12 букв - 9 попыток.
В начале игры игрок видит слово, в котором открыты первая и последняя буквы, на месте остальных букв стоят прочерки.
Также игрок видит количество оставшихся попыток: изначально 6 либо 9, и первый элемент написованной виселицы.
Игрок вводит букву в специальное поле и, если буква есть слове, она добавляется вместо прочерков столько раз, сколько встречается в слове.
Если буквы нет - уменьшается количество попыток и добавляется элемент к виселице.
Нельзя использовать одну и ту же букву несколько раз, а также вводить некорректные символы - в таких случаях выводится предупреждающее сообщение.
Если игрок угадал слово или если закончились попытки, выводится соответствующее сообщение и ему предлагается сыграть еще раз.


На данном проекте я выступила в роли fullstack-разработчика, написала код для backend и для frontend частей. 
Использованный стек технологий: Python 3.12, Flask (включая WTF и SQLAlchemy), HTML, CSS, база данных SQlite.

Для запуска проекта необходимо склонировать репозиторий на локальное устройство.
В строке 11 файла app.py вместо SECRET_KEY в строке b'SECRET_KEY' необходимо указать секретный ключ.
Запустить файл app.py и в браузере зайти на localhost, порт 8001.

  
