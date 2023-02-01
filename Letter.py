from greeting_analysis.SchemaMaker import SchemaMaker

class Letter:
    def __init__ (self,  band: int, page: int, sender: str, receiver: str, date: str,
                  greeting: str):
        self.band = band
        self.page = page
        self.sender = sender
        self.receiver = receiver
        self.date = date
        self.greeting = greeting
        self.schema_maker = SchemaMaker()


    def get_sender(self) -> str:
        return self.sender

    def get_receiver(self) -> str:
        return self.receiver

    def get_date(self) -> str:
        return self.date

    def get_greeting(self) -> str:
        return self.greeting

    def get_band(self) -> int:
        return self.band

    def get_page(self) -> int:
        return self.page

    def get_short_schema(self, manual=False) -> str:
        return self.schema_maker.get_schema(self.greeting, False, False, manual)

    def get_long_schema(self, manual=False) -> str:
        return self.schema_maker.get_schema(self.greeting, True, True, manual)