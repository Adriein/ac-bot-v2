import json

class TradeScript:
    __FILE_READ_MODE = 'r'

    __items: list[str] = list()


    def __init__(self, script_json_data: dict):
        for item in script_json_data['item']:
            self.__items.append(item)


    @staticmethod
    def load(name: str) -> 'TradeScript':
        with open(name, TradeScript.__FILE_READ_MODE) as file:
            script_data = json.load(file)

        return TradeScript(script_data)

    def items(self) -> list[str]:
        return self.__items
