from aqt import mw
from aqt.qt import *
from pathlib import Path

ADDON_DIR = Path(__file__).resolve().parent
sys.path.append(str(ADDON_DIR / "vendor"))

from .migrate.gui.deckselect import MigrateDialog

def open_migrate() -> None:
    mw.dialog = MigrateDialog(mw.app.activeWindow())
    mw.dialog.exec()



action = QAction("Migrate Deck to Structured Kanji", mw)
qconnect(action.triggered, open_migrate)

mw.form.menuTools.addAction(action)
