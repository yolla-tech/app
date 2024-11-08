from abc import ABC

from models.input import BaseInput, LetterInput, BoxInput
from models.output import Bill

class BaseService(ABC):
    # should return at max 4 depending on the from and to services being availible
    def search(self, input: BaseInput) -> list[Bill]:
        ...
    
    def search_letter(self, letter_input: LetterInput):
        return self.search(letter_input)
    
    def search_box(self, box_input: BoxInput):
        return self.search(box_input)
    
    @staticmethod
    def is_letter_search(input: BaseInput):
        return isinstance(input, LetterInput)
    
    @staticmethod
    def is_box_search(input: BaseInput):
        return isinstance(input, BoxInput)