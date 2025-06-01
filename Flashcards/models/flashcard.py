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
        
    def remove_flashcard(self, flashcard: Flashcard | str):
        '''Removes a flashcard from the set.'''
        print(f"Removing flashcard: {flashcard}")
        if isinstance(flashcard, str):
            # If a string is provided, remove by term
            self.flashcards = [fc for fc in self.flashcards if fc.term != flashcard]
        elif isinstance(flashcard, Flashcard):
            self.flashcards = [fc for fc in self.flashcards if fc.term != flashcard.term]
        
        
    def get_flashcards(self) -> List[Flashcard]:
        '''Returns the list of flashcards in the set.'''
        return self.flashcards
    
    def get_flashcard(self, term: str) -> Flashcard | None:
        '''Returns a flashcard by its term, or None if not found.'''
        for flashcard in self.flashcards:
            if flashcard.term == term:
                return flashcard
    
    
    @classmethod
    def from_file(cls, file_path: Path) -> Dict[str, 'FlashcardSet']:
        '''Loads a flashcard set from a TOML file.'''
        res = {}
        try:
            with open(file_path, 'rb') as f:
                data = tomllib.load(f)
                decks = data.get('deck', [])
                
                for deck_name, deck_data in decks.items():
                    description = deck_data.get('description', '')
                    flashcards = [Flashcard(**card) for card in deck_data.get('cards', [])]
                    res[deck_name] = cls(name=deck_name, description=description, flashcards=flashcards)
            return res
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found.")
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Error decoding TOML file {file_path}: {e}")