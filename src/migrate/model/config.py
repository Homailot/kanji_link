from dataclasses import dataclass

from anki.decks import DeckNameId
from anki.models import NotetypeNameId


@dataclass
class DeckConfig:
    selected_deck: DeckNameId
    note_types_to_migrate: list[NotetypeNameId]
    note_types_to_keep: list[NotetypeNameId]