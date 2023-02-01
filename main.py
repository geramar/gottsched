from Parser import Parser
from Uploader import Uploader
from greeting_analysis.FormulaParser import FormulaParser
from greeting_analysis.elements.JsonDictionaryAnalyzer import JsonDictionaryAnalyzer
from greeting_analysis.SchemaMaker import SchemaMaker

if __name__ == '__main__':
    uploader = Uploader("localhost", "birdie", "12345Cat", "letters")

    """table_name = "letters"
    uploader.create_table(table_name)
    for i in range(10):
        parser = Parser(f"books\gottsched{i+1}.pdf")
        letters = parser.parse()
        j = 0
        uploader.insert_band(letters, table_name)"""

    table_name = "schems"
    selection = uploader.select("SELECT id, greeting FROM letters")
    schema_maker = SchemaMaker()
    i = int(uploader.select("SELECT COUNT(*) from schems")[0][0])
    for element in selection:
        id, greeting = element
        schema = schema_maker.get_schema(greeting, True)
        if schema:
            uploader.insert_schema(id, schema, table_name)
    i -= int(uploader.select("SELECT COUNT(*) from schems")[0][0])
    print(f"Inserted {i} schemas")





