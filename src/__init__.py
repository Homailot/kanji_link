from aqt import mw
from aqt.qt import *

from src.migrate.gui import MigrateDialog


def open_migrate() -> None:
    mw.dialog = MigrateDialog(mw.app.activeWindow())
    mw.dialog.exec()


action = QAction("Migrate Deck to KanjiLink", mw)
qconnect(action.triggered, open_migrate)

mw.form.menuTools.addAction(action)
