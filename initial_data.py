from docx import Document
from docx.oxml import OxmlElement

class WordEquationReplacer:
    def __init__(self, file_path, **kwargs):
        self.doc = Document(file_path)
        self.replacements = kwargs

    def replace_text_in_paragraph(self, p):
        for old, new in self.replacements.items():
            if old in p.text:
                for run in p.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)

    def process_document(self):
        # Проходим по всем параграфам
        for p in self.doc.paragraphs:
            self.replace_text_in_paragraph(p)

        # Проходим по всем таблицам
        for table in self.doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.replace_text_in_paragraph(cell)

                    # Проверка на окончание строки на *
                    if cell.text.endswith('*'):
                        # Пример уравнения с заменёнными значениями
                        equation = f'2{self.replacements.get("dd", "d")}=√(({self.replacements.get("HH", "HH")}-hbm)^2+(nn*{self.replacements.get("HH", "HH")}+b0)^2)'

                        # Заменяем ячейку на новое уравнение
                        cell.clear()

                        # Добавляем элемент уравнения в формате Word XML
                        math_element = OxmlElement('m:oMath')
                        math_element.append(OxmlElement('m:r').append(OxmlElement('m:t', text=equation)))

                        cell._element.append(math_element)

    def save_document(self, new_file_path):
        self.doc.save(new_file_path)

# Пример использования класса
if __name__ == "__main__":
    replacer = WordEquationReplacer('templateWord.docx', dd='7', HH='11.8', nn="6.1")
    replacer.process_document()
    replacer.save_document('templateWord1.docx')
