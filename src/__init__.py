from typing import Optional

import aqt.forms.filtered_deck
from aqt import mw
from aqt.qt import *


class ImportDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.resize(526, 587)

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
        if len(self.decks) > 0:
            self._deck_selected(0)

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


def test_function() -> None:
    mw.dialog = ImportDialog(mw.app.activeWindow())
    mw.dialog.exec()


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, test_function)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
