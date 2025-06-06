
CREATE TABLE Groups (
    group_id BIGINT PRIMARY KEY,
    period BIGINT NOT NULL DEFAULT 3600,
    last_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    send_after BIGINT
);

CREATE TABLE User_info (
    user_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL REFERENCES Groups(group_id) ON DELETE CASCADE,
    tag_name TEXT NOT NULL,
    points BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE Questions (
    id_question BIGINT PRIMARY KEY,
    text_question TEXT NOT NULL
);

CREATE TABLE Answers (
    id_answer BIGINT PRIMARY KEY,
    foreign_question BIGINT NOT NULL,
    text_answer TEXT NOT NULL,
    bool_correct BOOLEAN NOT NULL,
    CONSTRAINT fk_question
        FOREIGN KEY (foreign_question)
        REFERENCES Questions(id_question)
        ON DELETE CASCADE
);

CREATE TABLE User_answered_questions (
    user_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL REFERENCES Groups(group_id) ON DELETE CASCADE,
    question_id BIGINT NOT NULL REFERENCES Questions(id_question) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id, question_id)
)