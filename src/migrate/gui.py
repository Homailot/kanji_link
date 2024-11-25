import typing
from typing import Optional

from anki.models import NotetypeNameId
from aqt import mw
from aqt.qt import *

from src.resources import get_icon, get_resource_path


class MigrateDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.resize(525, 587)

        self.deck_select = QComboBox(None)
        qconnect(self.deck_select.activated, self._deck_selected)

        self.deck_mapping = NoteTypeMapper()

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

        self.deck_selected = self.decks[index]


class NoteTypeListWidgetItem(QListWidgetItem):
    def __init__(self, note_type: NotetypeNameId, note_count: int):
        super().__init__(f"{note_type.name} ({note_count})", parent=None, type=1001)
        self.note_type = note_type

    def get_note_type(self):
        return self.note_type


def _take_selected_note_type(
    list_widget: QListWidget,
) -> Optional[NoteTypeListWidgetItem]:
    selected_note_types = list_widget.selectedIndexes()
    if len(selected_note_types) == 0:
        return None

    selected_note_type = selected_note_types[0]
    selected_item = list_widget.takeItem(selected_note_type.row())
    if selected_item is None:
        return None

    if not isinstance(selected_item, NoteTypeListWidgetItem):
        return None

    return typing.cast(NoteTypeListWidgetItem, selected_item)


class NoteTypeMapper(QGridLayout):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_events()
        self._load_data()

    def _setup_ui(self):
        self.note_types_list = QListWidget()
        self.migrate_types_list = QListWidget()
        self.keep_types_list = QListWidget()

        arrow_right = QIcon(get_icon("arrow_right.svg"))
        self.add_to_migrate_button = QPushButton("Migrate")
        self.add_to_migrate_button.setIcon(arrow_right)

        self.add_to_keep_button = QPushButton("Keep")
        self.add_to_keep_button.setIcon(arrow_right)

        self.addWidget(QLabel("Note Types"), 0, 0)
        self.addWidget(self.note_types_list, 1, 0, 3, 1)
        self.addWidget(self.add_to_migrate_button, 1, 1)
        self.addWidget(QLabel("Note Types to Migrate"), 0, 2)
        self.addWidget(self.migrate_types_list, 1, 2)
        self.addWidget(self.add_to_keep_button, 3, 1)
        self.addWidget(QLabel("Note Types to Keep"), 2, 2)
        self.addWidget(self.keep_types_list, 3, 2)

        self.setColumnStretch(0, 1)
        self.setColumnStretch(2, 1)

    def _setup_events(self):
        qconnect(self.add_to_migrate_button.released, self._on_add_to_migrate_released)
        pass

    def _load_data(self):
        self.note_types = mw.col.models.all_names_and_ids()

        for note_type in self.note_types:
            item = NoteTypeListWidgetItem(
                note_type, mw.col.models.use_count(mw.col.models.get(note_type.id))
            )
            self.note_types_list.addItem(item)

    def _on_add_to_migrate_released(self):
        selected_note_type_item = _take_selected_note_type(self.note_types_list)
        if selected_note_type_item is not None:
            self.migrate_types_list.addItem(selected_note_type_item)
