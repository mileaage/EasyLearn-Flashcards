import pytest
from Flashcards.models.flashcard import Flashcard, FlashcardSet


@pytest.fixture
def flashcard_set():
    """Fixture to create a sample FlashcardSet for testing."""
    return FlashcardSet(
        name="Test Deck",
        description="A deck for testing purposes",
        flashcards=[
            Flashcard(term="Python", definition="A programming language"),
            Flashcard(term="Pytest", definition="A testing framework for Python")
        ]
    )

def test_flashcardset_name(flashcard_set):
    assert flashcard_set.name == "Test Deck"

def test_flashcardset_description(flashcard_set):
    assert flashcard_set.description == "A deck for testing purposes"

def test_flashcardset_flashcards_count(flashcard_set):
    assert len(flashcard_set.flashcards) == 2

def test_flashcardset_flashcard_content(flashcard_set):
    terms = [fc.term for fc in flashcard_set.flashcards]
    definitions = [fc.definition for fc in flashcard_set.flashcards]
    assert "Python" in terms
    assert "Pytest" in terms
    assert "A programming language" in definitions
    assert "A testing framework for Python" in definitions

def test_add_flashcard(flashcard_set):
    new_flashcard = Flashcard(term="Django", definition="A Python web framework")
    flashcard_set.add_flashcard(new_flashcard)
    assert any(fc.term == "Django" for fc in flashcard_set.flashcards)
    assert len(flashcard_set.flashcards) == 3

def test_remove_flashcard(flashcard_set):
    flashcard_set.remove_flashcard("Python")
    terms = [fc.term for fc in flashcard_set.flashcards]
    assert "Python" not in terms
    assert len(flashcard_set.flashcards) == 1

def test_get_flashcard(flashcard_set):
    fc = flashcard_set.get_flashcard("Pytest")
    assert fc is not None
    assert fc.term == "Pytest"
    assert fc.definition == "A testing framework for Python"

def test_get_flashcard_not_found(flashcard_set):
    fc = flashcard_set.get_flashcard("Nonexistent")
    assert fc is None