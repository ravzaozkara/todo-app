CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,

    text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO todos (text) VALUES ('İlk task');
INSERT INTO todos (text) VALUES ('İkinci task');

\d todos;

SELECT * FROM todos;




