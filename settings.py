import os


valid_email = "firstguest@mail.ru"
valid_password = '111'

invalid_email = "firstguest_mail.ru"
invalid_password = 'kqnbn'

name_HTML = """
            <html>
            <head>
            <title>Пример 1</title>
            </head>
            <body>
            <H1>Привет!</H1>
            <P> Это простейший пример HTML-документа. </P>
            </body>
            </html>
            """
animal_type_HTML = """
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
                <html>
                 <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                  <title>Пример веб-страницы</title>
                 </head>
                 <body>
                  <h1>Заголовок</h1>
                  <!-- Комментарий -->
                  <p>Первый абзац.</p>
                  <p>Второй абзац.</p>
                 </body>
                </html>
                """

# Прочитаем большой текст из файла
file_name = os.path.join('files', 'huge_text.txt')
with open(os.path.join(os.path.dirname(__file__), file_name), 'r' ) as file:
    huge_text = file.read()
huge_text.encode('utf-8')
# Удалим из текста переводы строк, чтобы его можно было передавать в headers
huge_text_without_returns = huge_text.replace('\n', '')
