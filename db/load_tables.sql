COPY Questions (id_question, text_question) 
FROM '/docker-entrypoint-initdb.d/static_data/questions.csv'
DELIMITER ','
CSV HEADER;

COPY Answers (id_answer, foreign_question, text_answer, bool_correct)
FROM '/docker-entrypoint-initdb.d/static_data/answers.csv'
DELIMITER ','
CSV HEADER;
