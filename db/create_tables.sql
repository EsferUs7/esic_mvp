CREATE TABLE User_info (
    user_id SERIAL PRIMARY KEY,
    tag_name TEXT,
    points INTEGER NOT NULL DEFAULT 0,
    group_id INTEGER REFERENCES Group(group_id) ON DELETE CASCADE
);

CREATE TABLE Questions (
    id_question SERIAL PRIMARY KEY,
    text_question TEXT NOT NULL
);

CREATE TABLE Answers (
    id_answer SERIAL PRIMARY KEY,
    foreign_question INTEGER NOT NULL,
    text_answer TEXT NOT NULL,
    bool_correct BOOLEAN NOT NULL,
    CONSTRAINT fk_question
        FOREIGN KEY (foreign_question)
        REFERENCES Questions(id_question)
        ON DELETE CASCADE
);

CREATE TABLE Groups (
    group_id SERIAL PRIMARY KEY,
    period INT NOT NULL DEFAULT 3600,
    last_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    send_after INT
)