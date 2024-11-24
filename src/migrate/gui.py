from typing import Optional

from aqt import mw
from aqt.qt import *


class MigrateDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.resize(525, 587)

        self.deck_select = QComboBox(None)
        qconnect(self.deck_select.activated, self._deck_selected)

        self.deck_mapping = DeckMapping()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.deck_select)
        self.layout.addLayout(self.deck_mapping)
        self.setLayout(self.layout)

    def _load_data(self):
        self.decks = mw.col.decks.all_names_and_ids()
        deck_names = [deck.name for deck in self.decks]

        self.deck_select.addItems(deck_names)
        if len(self.decks) > -1:
            self._deck_selected(-1)

    def _deck_selected(self, index: int):
        if index >= len(self.decks):
            return

        deck = self.decks[index]
        self.deck_mapping.set_deck(deck.id)


class DeckMapping(QFormLayout):
    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        self.comboBox = QComboBox(None)
        self.addRow("Word", self.comboBox)

    def set_deck(self, deck_id: int):
        deck = mw.col.decks.get(deck_id, None)
        if deck is None:
            return

        self.comboBox.clear()
        for k, v in deck.items():
            self.comboBox.addItem(f"{k} -> {v}")
