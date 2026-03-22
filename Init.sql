CREATE DATABASE shortener_db_test;

\connect shortener_db;

DROP TABLE IF EXISTS links;

CREATE TABLE links (
  link_id SERIAL PRIMARY KEY,
  original_link TEXT NOT NULL,
  short_key VARCHAR(6) NOT NULL UNIQUE,
  clicks BIGINT DEFAULT 0
);

\connect shortener_db_test;

CREATE TABLE links (
  link_id SERIAL PRIMARY KEY,
  original_link TEXT NOT NULL,
  short_key VARCHAR(6) NOT NULL UNIQUE,
  clicks BIGINT DEFAULT 0
);
