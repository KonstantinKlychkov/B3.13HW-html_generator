from bs4 import BeautifulSoup

class HTML:
    """Класс создаёт HTML-контейнер в котором хранится генерируемый HTML-код.
    Контейнер может быть строкой или файлом *.html в зависимости от параметра output_file"""

    def __init__(self, output_file=False, file_name = 'index', file_path = ''):
        self.output_file = output_file
        self.file_name = file_name
        self.file_path = file_path
        self.code = ''
        self.codeGeneration(firstGeneration=True)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        return self.code

    def __add__(self, other):
        #Обновим строковое представление добавляемого тэга, вдруг в экземпляр класса что-то добавили
        other.tagStringCreation()
        #Добавим новый тэг и обновим строковое представление текущего тэга
        self.codeGeneration(tag=other.tagString)   
        return self

    def codeGeneration(self, firstGeneration = False, tag = ''):
        #Если генерируем код первый раз, то начнём с шаблона
        if firstGeneration == True:
            if self.output_file == False:
            # создадим строку с шаблоном HTML.
                self.code = ('<!DOCTYPE html>\n'
                            '<html lang="en">\n'
                            '\n</html>')
            elif self.output_file == True:
            #создадим HTML- файл и запишем код туда
                with open(f'{self.file_path}{self.file_name}.html', 'w+') as file:
                    file.write('<!DOCTYPE html>\n'
                            '<html lang="en">\n'
                            '\n</html>')
                #чтобы меньше работать с файлом сохраним HTML-код в атрибут текущего тэга
                with open(f'{self.file_path}{self.file_name}.html', 'r') as file:
                    self.code = file.read()
        else:
            #добавим новый блок в конец, но перед закрывающим тэгом
            codeLine = (self.code).split('\n')
            codeLine.insert(-2, tag)
            self.code = '\n'.join(codeLine)
            #Наведём красоту в HTML-коде
            self.code = (BeautifulSoup(self.code, "lxml")).prettify(formatter='html5')
            #запишем в файл, если нужно
            if self.output_file == True:
                with open(f'{self.file_path}{self.file_name}.html', 'w+') as file:
                  file.write(self.code)
        
        return self.code


class TopLevelTag:
    
    def __init__(self, tag):
        self.tag = tag
        self.text = ""
        self.tagString = ''
        
        self.tagStringCreation()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        return self.tagString

    def __add__(self, other):
        #Обновим строковое представление добавляемого тэга, вдруг в экземпляр класса что-то добавили
        other.tagStringCreation()
        #Добавим новый тег и обновим строковое представление текущего тэга
        self.text += f'{other.tagString}'
        self.tagStringCreation()
        return self
            
    def tagStringCreation(self):
    #Соберём весь блок тэга в одну строку.
        self.tagString = (
            "<{tag}>{text}</{tag}>".format(
                tag=self.tag, text=self.text
            )
        )
        return self.tagString



class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.klass = klass
        self.attributes = {}
        self.text = ""
        self.is_single = is_single
        self.tagString = ''

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        #Сформируем словарь атрибутов будещего тэга.
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-") # приведём синтаксис тэга к принятому стандарту в HTML.
            self.attributes[attr] = value
        
        self.tagStringCreation()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        return self.tagString

    def __add__(self, other):
        other.tagStringCreation()
        if self.is_single == False:
                self.text += f'{other.tagString}'
        self.tagStringCreation()
        return self
            
    def tagStringCreation(self):
    #Соберём весь блок тэга в одну строку.
        ##Начнём с того, что соберём все аттрибуты тэга в лист.
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        ##Вот теперь сформируем строку тэга.
        if self.is_single:
            self.tagString = ("<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs))
        else:
            self.tagString = (
                "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )
            )
        return self.tagString

if __name__ == "__main__":
    with HTML(output_file=False) as doc:
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
            doc += body
            print(doc)