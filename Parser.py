import re
import fitz
from Letter import Letter
from typing import Union, NoReturn

class Parser:
    def __init__(self, pdf_file: str) -> NoReturn:

        self.pages = fitz.open(pdf_file)
        self.band = int(re.search(r"\d{1,2}", pdf_file).group(0))

    def parse(self) -> list[Letter]:
        letters = []
        for i in range(len(self.pages)):
            page = self.pages.load_page(i)
            text = page.get_text()
            letter_inf = re.search(r'\d\.(\D*) an ([A-ZÖÜÄ]\D*),\n(.*\D\d{4})', text)
            if letter_inf:
                sender, receiver = letter_inf.group(1), letter_inf.group(2)
                date = self.__check_date(letter_inf.group(3))
                greeting = self.__find_greeting(page)
                if greeting == None:
                    greeting = self.__find_greeting(self.pages.load_page(i + 1), True)
                if greeting:
                    letter = Letter(self.band, i+1, sender, receiver, date, greeting)
                    letters.append(letter)
        return letters

    def __find_greeting(self, page: fitz.fitz.Page, second_page: bool = False) -> Union[str, bool, None]:
        html_page = page.get_textpage().extractHTML()
        lines = \
            [{"size": line.group(1), "text": line.group(2), "sup": line.group(3)} for line in (
                re.search(r"font-size:(\d{1,2}\.\d)pt\">([^<]*)</span>(<sup>)?.*</p>", line)
                                                        for line in html_page.split("\n")) if line]
        for i in range(1, len(lines)-1):
            if (not second_page and lines[i]['size'] == '10.7' and lines[i-1]['size'] == '9.1') or \
                    (second_page and i>1 and lines[i]['size'] == '10.7'):
                greeting_i = i
                greeting = self.__set_german_chairs(lines[greeting_i]['text'])
                if re.search(r"[#&]", greeting):  #to delete not german greetings
                    return False
                if re.search(r"\d", greeting):  #in occasion of finding a date instead of a greeting
                    greeting = self.__set_german_chairs(lines[i + 1]['text'])
                    greeting_i = i+1
                next_line = lines[greeting_i + 1]   #checking the next line
                next_text = self.__set_german_chairs(next_line['text'])
                if greeting_i < len(lines) - 1 and len(next_text) < 60 \
                        and not next_line["sup"]: #<sup> make lines shorter and not found in greetings
                    greeting += next_text #if len < 60 it is probably a greeting, not the main text
                if re.search(r"[#&]", greeting): #to delete not german greetings considering the second line
                    return False
                return greeting
        return None

    @staticmethod
    def __set_german_chairs(text: str) -> str:
        new = text.replace("&#xe4;", "ä").replace("&#xf6;", "ö").replace("&#xfc;", "ü").replace("&#xdf;", "ß")
        return new

    def __check_date(self, date: str) -> str:
        full_date = re.search(r"\d{1,2}\.[^/]*\d{4}", date)
        if full_date:
            formated_date = self.__format_date(full_date.group(0))
            return formated_date
        else:
            year = re.search(r'\d{4}', date)
            return year.group(0)

    @staticmethod
    def __format_date(date: str) -> str:
        months = {
            "Januar": "01.",  "Februar" : "02.", "März" : "03.", "April" : "04.",
            "Mai" : "05.", "Juni" : "06.", "Juli" : "07.", "August" : "08.",
            "September" : "09.", "Oktober" : "10.", "November" : "11.", "Dezember" : "12."
        }
        month = re.search(r"[JFMASOND]\w{2,8}", re.search(r"\d\.(.*)\d{4}", date).group(1).strip()).group(0)
        formatted_date = re.sub("[^\d.]", '', date.replace(month, months[month]))
        return formatted_date