CREATE TABLE IF NOT EXISTS "word" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image TEXT NOT NULL DEFAULT '',
    explanation TEXT NOT NULL DEFAULT '',
    dict_source TEXT NULL DEFAULT NULL,
    dict_id TEXT NULL DEFAULT NULL 
);

CREATE TABLE IF NOT EXISTS "reading" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    kana TEXT NOT NULL DEFAULT '',
    audio TEXT NOT NULL DEFAULT '',
    reading_info TEXT NOT NULL DEFAULT '',
    pitch_accent INTEGER NULL DEFAULT NULL,
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS "spelling" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL,
    spelling TEXT NOT NULL DEFAULT '', -- using Anki's Ruby syntax for furigana
    kanji TEXT NOT NULL DEFAULT '', -- the actual kanji
    spelling_info TEXT NOT NULL DEFAULT '', -- additional information about the spelling, such as uncommon readings, etc.
    manual_related_readings TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "related_readings" (
    spelling_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    PRIMARY KEY (spelling_id, reading_id),
    FOREIGN KEY (spelling_id) REFERENCES spelling(id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "sense" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    sense TEXT NOT NULL DEFAULT '',
    parts_of_speech TEXT NOT NULL DEFAULT '',
    transitivity TEXT NULL CHECK (transitivity IN ('transitive', 'intransitive', 'both', 'none')) DEFAULT 'none',
    misc_info TEXT NOT NULL DEFAULT '', -- additional information about the sense, such as field of use, etc.
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "card_settings" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NULL DEFAULT NULL, -- card from definition to spelling 
    spelling_id INTEGER NULL DEFAULT NULL, -- card from spelling to definition 
    import_card_id INTEGER NULL DEFAULT NULL,
    import_deck_id INTEGER NULL DEFAULT NULL,
    tags TEXT NOT NULL DEFAULT '',
    note_type_id INTEGER NOT NULL,
    note_id INTEGER NULL DEFAULT NULL,
    card_id INTEGER NULL DEFAULT NULL,
    flag TEXT NOT NULL CHECK (flag IN ('red', 'orange', 'green', 'blue', 'pink', 'turquoise', 'purple','none')) DEFAULT 'none',
    generate_card BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE SET NULL, -- if word is deleted, card_settings are not deleted. This is to know which cards need to be deleted in Anki.
    FOREIGN KEY (spelling_id) REFERENCES spelling(id) ON DELETE SET NULL,
);

CREATE TABLE IF NOT EXISTS "additional_fields" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_name TEXT NOT NULL DEFAULT '',
    UNIQUE (field_name)
);

CREATE TABLE IF NOT EXISTS "word_additional_fields" (
    word_id INTEGER NOT NULL,
    field_id INTEGER NOT NULL,
    value TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (word_id, field_id),
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE,
    FOREIGN KEY (field_id) REFERENCES additional_fields(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "frequency" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 0,
    source TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "sentence" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    sentence TEXT NOT NULL DEFAULT '',
    translation TEXT NOT NULL DEFAULT '',
    audio TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "idx_reading_kana" ON "reading" (kana);
CREATE INDEX IF NOT EXISTS "idx_spelling_kanji" ON "spelling" (kanji);
CREATE INDEX IF NOT EXISTS "idx_reading_word_id" ON "reading" (word_id);
CREATE INDEX IF NOT EXISTS "idx_spelling_reading_id" ON "spelling" (reading_id);
CREATE INDEX IF NOT EXISTS "idx_related_readings_spelling_id" ON "related_readings" (spelling_id);
CREATE INDEX IF NOT EXISTS "idx_related_readings_reading_id" ON "related_readings" (reading_id);
CREATE INDEX IF NOT EXISTS "idx_sense_word_id" ON "sense" (word_id);
CREATE INDEX IF NOT EXISTS "idx_card_settings_word_id" ON "card_settings" (word_id);
CREATE INDEX IF NOT EXISTS "idx_card_settings_spelling_id" ON "card_settings" (spelling_id);
CREATE INDEX IF NOT EXISTS "idx_word_additional_fields_word_id" ON "word_additional_fields" (word_id);
CREATE INDEX IF NOT EXISTS "idx_word_additional_fields_field_id" ON "word_additional_fields" (field_id);
CREATE INDEX IF NOT EXISTS "idx_frequency_word_id" ON "frequency" (word_id);
CREATE INDEX IF NOT EXISTS "idx_sentence_word_id" ON "sentence" (word_id);


CREATE TRIGGER IF NOT EXISTS "add_related_readings_on_spelling_insert" AFTER INSERT ON "spelling"
BEGIN
-- think on whether this makes sense or not
    INSERT INTO related_readings (spelling_id, reading_id)
    SELECT new.id, reading.id
    FROM reading
    WHERE reading.kana = (SELECT reading.kana FROM reading WHERE id = new.reading_id)
    AND reading.id != new.reading_id;
END;