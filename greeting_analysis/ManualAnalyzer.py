from JsonDictionaryAnalyzer import JsonDictionaryAnalyzer
from prettytable import PrettyTable

class ManualAnalyzer:
    def __init__(self):
        self.dictionary_analyzer = JsonDictionaryAnalyzer()

    """def analyze(self, rare_formula):
        print(f"{rare_formula.words}\n {rare_formula.groups}\n Do you want to make any changes? y - yes, n - no, i - ignore")
        answer = input()
        if answer == "y":
            print("Make one of the commands:\n 1) del INDEX \n 2) word INDEX VALUE -r ROOT \n "
                  "3) word INDEX -a ANALOG \n 4) group INDEX VALUE")
            answer = list(input().split())
            try:
                command, index, value = answer[0], int(answer[1]), None if len(answer) < 3 else answer[2]
                if command == 'del':
                    rare_formula.delete_element(index)
                elif command == 'word':
                    if len(answer) == 5:
                        if answer[3] == "-r":
                            self.dictionary_analyzer.set_value("word_to_root", value, answer[4])
                    elif value == '-a':
                            self.dictionary_analyzer.set_value("analogs", answer[4], rare_formula.words[index])
                    elif len(answer) > 3:
                        print("Incorrect input")
                        return self.analyze(rare_formula)
                    rare_formula.change_word(index, value)
                elif command == 'group':
                    rare_formula.change_group(index, value)
                return self.analyze(rare_formula)
            except IndexError:
                print("Incorrect input")
                return self.analyze(rare_formula)
        elif answer == "n":
            return rare_formula
        elif answer == "i":
            return None
        else:
            print("Incorrect answer")
            return self.analyze(rare_formula)"""

    def __print_help(self):
        print("-s |-> save\n"
              "-i |-> ignore\n"
              "-d INDEXES |-> delete\n"
              "-g INDEX VALUE |-> set group\n"
              "-w INDEX VALUE |-> set word\n"
              "-w INDEX -a ORIGINAL |-> add word to analogs\n"
              "-w INDEX -r ROOT |-> add to word_to_roots\n")

    def __request_instructions(self):
        print("Print your instructions. -h for help")
        return input()

    def __speaking(self, rare_formula):
        answer = self.__request_instructions()
        try:
            if answer == "-h":
                self.__print_help()
                self.__speaking(rare_formula)
            elif answer == "-s":
                return rare_formula
            elif answer == "-i":
                return None
            else:
                answer_list = answer.split()
                command = answer_list[0]
                if command == "-d":
                    indexes = sorted(answer_list[1:], reverse=True)
                    for index in indexes:
                        rare_formula.delete_element(int(index))
                elif command == "-g":
                    index, value = answer_list[1:]
                    rare_formula.change_group(int(index), value)
                elif command == "-w":
                    index = int(answer_list[1])
                    if answer_list[2] == "-a":
                        self.dictionary_analyzer.set_value("analogs", answer_list[3], rare_formula.words[index])
                    elif answer_list[2] == "-r":
                        self.dictionary_analyzer.set_value("word_to_root", rare_formula.words[index], answer_list[3])
                    else:
                        rare_formula.change_word(index, " ".join(answer_list[2:]))
                else:
                    print("Incorrect input")
                    self.__speaking(rare_formula)
                return self.analyze(rare_formula)
        except IndexError:
            print("Try again")
            self.__speaking(rare_formula)


    def analyze(self, rare_formula):
        table = PrettyTable()
        table.field_names = rare_formula.indexes
        table.add_rows([rare_formula.words, rare_formula.groups])
        print(table)
        return self.__speaking(rare_formula)

