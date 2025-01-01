-- Database schema --

CREATE TABLE IF NOT EXISTS "dictionary" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT '',
    url TEXT NOT NULL DEFAULT '',
);

CREATE TABLE IF NOT EXISTS "dictionary_entry" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dictionary_id INTEGER NOT NULL,
    sequence_number INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (dictionary_id) REFERENCES dictionary(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "reading" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dictionary_entry_id INTEGER NOT NULL,
    reading TEXT NOT NULL DEFAULT '', -- kana only
    FOREIGN KEY (dictionary_entry_id) REFERENCES dictionary_entry(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "reading_info" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL,
    info TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "reading_priority" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL,
    priority TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "kanji" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji TEXT NOT NULL DEFAULT '',
);

CREATE TABLE IF NOT EXISTS "kanji_info" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji_id INTEGER NOT NULL,
    info TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (kanji_id) REFERENCES kanji(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "kanji_priority" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji_id INTEGER NOT NULL,
    priority TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (kanji_id) REFERENCES kanji(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "kanji_reading" (
    kanji_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    furigana TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (kanji_id, reading_id),
    FOREIGN KEY (kanji_id) REFERENCES kanji(id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "sense" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (dictionary_entry_id) REFERENCES dictionary_entry(id) ON DELETE
);

CREATE TABLE IF NOT EXISTS "sense_reading" (
    sense_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    PRIMARY KEY (sense_id, reading_id),
    FOREIGN KEY (sense_id) REFERENCES sense(id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "sense_kanji" (
    sense_id INTEGER NOT NULL,
    kanji_id INTEGER NOT NULL,
    PRIMARY KEY (sense_id, kanji_id),
    FOREIGN KEY (sense_id) REFERENCES sense(id) ON DELETE CASCADE,
    FOREIGN KEY (kanji_id) REFERENCES kanji(id) ON DELETE CASCADE,
);