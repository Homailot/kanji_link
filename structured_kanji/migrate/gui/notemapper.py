from typing import Optional

from aqt.qt import *

from structured_kanji.migrate.model.config import DeckConfig


class NoteMapper(QDialog):
    def __init__(self, deck_config: DeckConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.deck_config = deck_config
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        super().setWindowTitle("Map Note Types")
        self.resize(525, 587)

        self.layout = QVBoxLayout()
        self.layout.addLayout(WordTabs(self.deck_config, self))
        self.setLayout(self.layout)

    def _load_data(self):
        pass


class WordTabs(QVBoxLayout):
    def __init__(self, deck_config: DeckConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.deck_config = deck_config
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.tab_view = QTabWidget(self.parent())
        for note_type in self.deck_config.note_types_to_migrate:
            self.tab_view.addTab(WordMapper(self.parent()), note_type.name)

        self.addWidget(QLabel("Nouns"))
        self.addWidget(self.tab_view)

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
