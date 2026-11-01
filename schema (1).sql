-- Run once inside the "library" database.
-- Create the database first with:  CREATE DATABASE library;

CREATE TABLE IF NOT EXISTS books (
    id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title  TEXT    NOT NULL,
    author TEXT    NOT NULL,
    year   INTEGER NOT NULL
);

-- Optional sample data (run only once, or you will get duplicates):
-- INSERT INTO books (title, author, year) VALUES
--     ('Clean Code', 'Robert C. Martin', 2008),
--     ('The Pragmatic Programmer', 'Andrew Hunt and David Thomas', 1999),
--     ('Fluent Python', 'Luciano Ramalho', 2015);
