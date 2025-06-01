import tomllib
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path

@dataclass
class Flashcard:
    '''A class representing a single flashcard.'''
    term: str
    definition: str

@dataclass
class FlashcardSet:
    '''A class representing a set of flashcards.'''
    name: str
    description: str
    flashcards: List[Flashcard] = field(default_factory=list)
    
    def add_flashcard(self, flashcard: Flashcard):
        '''Adds a flashcard to the set.'''
        self.flashcards.append(flashcard)
        
    def remove_flashcard(self, flashcard: Flashcard):
        '''Removes a flashcard from the set.'''
        self.flashcards.remove(flashcard)
        
    def get_flashcards(self) -> List[Flashcard]:
        '''Returns the list of flashcards in the set.'''
        return self.flashcards
    
    
    @classmethod
    def from_file(cls, file_path: Path) -> Dict[str, 'FlashcardSet']:
        '''Loads a flashcard set from a TOML file.'''
        res = {}
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)
            decks = data.get('deck', [])
            
            for deck_name, deck_data in decks.items():
                description = deck_data.get('description', '')
                flashcards = [Flashcard(**card) for card in deck_data.get('cards', [])]
                res[deck_name] = cls(name=deck_name, description=description, flashcards=flashcards)
        return res