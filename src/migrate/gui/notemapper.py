import typing
from typing import Optional

import aqt.tagedit
from anki.decks import DeckNameId
from anki.models import NotetypeNameId
from aqt import mw, colors
from aqt.qt import *
from aqt.theme import theme_manager
from aqt.utils import (
    tr,
    shortcut
)

from src.resources import get_icon

class NoteMapper(QDialog):
    def __init__(self, selected_deck: DeckNameId, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.selected_deck = selected_deck
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        pass

    def _load_data(self):
        pass