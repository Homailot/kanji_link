import typing
from typing import Optional

import aqt.tagedit
from anki.decks import DeckNameId
from anki.models import NotetypeNameId, NotetypeId
from aqt import mw, colors
from aqt.notetypechooser import NotetypeChooser
from aqt.qt import *
from aqt.theme import theme_manager
from aqt.utils import (
    tr,
    shortcut
)

from src.migrate.model.config import DeckConfig
from src.resources import get_icon

class NoteMapper(QDialog):
    def __init__(self, deck_config: DeckConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.deck_config = deck_config
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        super().setWindowTitle("Map Note Types")
        self.resize(525, 587)
        self.noun_tab_view = QTabWidget(self)
        self.noun_tab_view.addTab(WordMapper(self.noun_tab_view), "Vocabulary (and Reversed)")
        self.noun_tab_view.addTab(WordMapper(self.noun_tab_view), "Vocabulary")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Nouns"))
        self.layout.addWidget(self.noun_tab_view)
        self.setLayout(self.layout)


    def _load_data(self):
        pass

class WordMapper(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Word"))
        self.layout.addWidget(QLabel("Furigana"))
        self.layout.addWidget(QLabel("Meanings"))
        self.setLayout(self.layout)

    def _load_data(self):
        pass
