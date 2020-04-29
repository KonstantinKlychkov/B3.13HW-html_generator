class Tag:
    pass


class HTML:
    """Класс создаёт HTML-контейнер в котором хранится генерируемый HTML-код. 
    Контейнер может быть строкой или файлом *.html"""

    def __init__(self, output_file = False, file_name = 'index', file_path = ''):
        self.output_file = output_file
        self.code = ''
        self.file_name = file_name
        self.file_path = file_path

        # Если оутпут в файл, то сразу же создадим файл c именем 'file_name.html' в директории 'file_path' или той же директории где модуль Питона и добавим в него:
        """<!DOCTYPE html>
            <html lang="en">
            
            </html>"""
        if self.output_file == False:
            # создадим элемент класса - строку с шаблоном HTML.
            self.code = ('<!DOCTYPE html>\n'
                            '<html lang="en">\n\n'
                            '</html>')
        elif self.output_file == True:
            #создадим элемент класса - HTML- файл и запишем туда
            with open(f'{self.file_path}{self.file_name}.html', 'w+') as file:
                file.write('<!DOCTYPE html>\n'
                            '<html lang="en">\n\n'
                            '</html>')

    def __str__(self):
        if self.output_file == True:
            with open(f'{self.file_path}{self.file_name}.html', 'r') as file:
                self.code = file.read()
        return  self.code      



class TopLevelTag:
    def __add__(self, other):
        """Функция добавляет кусок html кода в переменную или в файл, в зависимости от аргумента 'output' элемента класса"""
        # Если оутпут в переменную, то вставить кусок кода в конец перед тэгом </html>
        # Если оутпут в файл, то вставить кусок кода в конец файла перед тэгом </html> записать и закрыть файл.
        #if self.output_file == True:
         #   with open(f'{self.file_name}.html', 'r') as file:
          #      self.code = file.read()    pass


if __name__ == "__main__":
   doc = HTML(output_file = True, file_name = 'main', file_path = '/Users/a18301335/Python/Skill_Factory_FullStack/b2.14-hw-dummy-access/')
   print(doc)
   
"""with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body"""