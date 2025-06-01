from models.flashcard import FlashcardSet
import models.keyDetect as keyDetect
import customtkinter as ctk
from pynput.keyboard import Key

from pathlib import Path
import random


script_dir = Path(__file__).parent
config_path = script_dir / "config.toml"
Deck = FlashcardSet.from_file(Path(config_path).resolve())

#TODO: Needs a grid system
# I made everything with PACK so it looks like a mess


class ScreenManager:
    def __init__(self, root):
        self.root = root
        self.screens = {}
        self.current_screen = None
        self.should_exit = False

    def add_screen(self, name, screen_class):
        screen = screen_class(self.root, self)
        screen.pack_forget()
        self.screens[name] = screen

    def show_screen(self, name) -> ctk.CTkFrame:
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = self.screens[name]
        self.current_screen.pack(fill="both", expand=True)
        return self.current_screen

    def request_exit(self):
        self.should_exit = True


class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        ctk.CTkLabel(self,
            text="Flashcard App",
            font=ctk.CTkFont('Bold', 30)
        ).pack(pady=100)

        for deck_name in Deck.keys():
            ctk.CTkButton(
                self,
                text=f'{deck_name} ({len(Deck[deck_name].get_flashcards())} cards)',
                width=300,
                height=60,
                command=lambda name=deck_name: self.start_learning(name),
                font=ctk.CTkFont('Helvetica Bold', 20)
            ).pack(pady=5)

    def start_learning(self, name):
        print(f"Starting learning for deck: {name}")
        card_screen = self.manager.show_screen("cards")
        card_screen.load_deck(name)


class CardScreen(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager
        self.block = True

    def load_deck(self, deck_name):
        cards = Deck[deck_name].get_flashcards()
        random.shuffle(cards)

        for card in cards:
            if self.manager.should_exit:
                return

            ctk.CTkLabel(self, text=f"Current Deck:  {deck_name}").pack(pady=20)
            
            # Wrap the text
            ctk.CTkLabel(
                self, 
                text=card.term, 
                font=ctk.CTkFont('Arial Bold', 40),
                wraplength=1100,  # Wrap when it gets to the edge (1280-180)
                justify="center"
            ).pack(pady=50, padx=20)

            if not self._block_until_pressed():
                return

            # Definition with text wrapping and scrollable frame if very long
            definition_frame = ctk.CTkScrollableFrame(self, height=200)
            definition_frame.pack(pady=20, padx=20, fill="x")
            
            ctk.CTkLabel(
                definition_frame, 
                text=card.definition, 
                font=ctk.CTkFont('Arial', 15),
                wraplength=1050,
                justify="left",
                anchor="w"
            ).pack(pady=10, padx=10, fill="x")

            if not self._block_until_pressed():
                return

            self.clear_screen()

            if self.manager.should_exit:
                return

            self.block = True
            
            ctk.CTkLabel(
                self, 
                text="Add this card to the end of the deck?", 
                font=ctk.CTkFont('Helvetica Bold', 40),
                wraplength=1000,
                justify="center"
            ).pack(pady=75, padx=20)
            
            # Make the text fill the button width
            ctk.CTkButton(
                self,
                text="Yes",
                command=lambda d=Deck[deck_name], c=card: self.add_card_to_end(d, c),
                height=100,
                font=ctk.CTkFont('Helvetica Bold', 40),
                width=250,
                
            ).pack(pady=5)
            
            ctk.CTkButton(
                self,
                text="No",
                command=self.set_block_false,
                height=100,
                width=250,
                font=ctk.CTkFont('Helvetica Bold', 40)
            ).pack(pady=5)

            while self.block and not self.manager.should_exit:
                try:
                    self.update()
                except:
                    return

            if self.manager.should_exit:
                return

            self.clear_screen()

        if self.manager.should_exit:
            return

        ctk.CTkLabel(self, text="End of Deck").pack(pady=20)

        if not self._block_until_pressed():
            return

        self.manager.show_screen("home")

    def add_card_to_end(self, deck, card):
        deck.add_flashcard(card)
        self.block = False

    def set_block_false(self):
        self.block = False

    def clear_screen(self):
        try:
            for widget in self.winfo_children():
                widget.destroy()
        except:
            pass

    def _block_until_pressed(self):
        keyDetect.set_enter_key_listener()
        try:
            while not keyDetect.is_enter_pressed() and not self.manager.should_exit:
                self.update()
        except:
            return False

        keyDetect.clear_enter_pressed()
        return not self.manager.should_exit


def quit():
    manager.request_exit()
    keyDetect.cleanup()
    root.after(10, root.destroy)


if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("Dark")
    root.title("Flashcard App")
    root.geometry("1280x720")

    root.protocol("WM_DELETE_WINDOW", quit)

    manager = ScreenManager(root)
    manager.add_screen("home", HomeScreen)
    manager.add_screen("cards", CardScreen)
    manager.show_screen("home")

    root.mainloop()
