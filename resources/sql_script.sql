CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    vk_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255),
    city VARCHAR(255),
    age INTEGER,
    sex VARCHAR(10)
);

CREATE TABLE search_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vk_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(255),
    profile_url TEXT
);

CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    search_result_id INTEGER REFERENCES search_results(id) ON DELETE CASCADE,
    photo_url TEXT NOT NULL,
    likes INTEGER NOT NULL
);

CREATE TABLE favorite_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vk_id BIGINT NOT NULL,
    name VARCHAR(255),
    profile_url TEXT
);

CREATE TABLE blacklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vk_id BIGINT NOT NULL,
    name VARCHAR(255),
    profile_url TEXT
);
