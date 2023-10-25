/* Создание схемы content */
CREATE SCHEMA IF NOT EXISTS content;

/* Создание  таблицы film_work в схеме content */
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    modified timestamp with time zone DEFAULT CURRENT_TIMESTAMP
); /*PARTITION BY RANGE (creation_date);*/


CREATE OR REPLACE  FUNCTION update_updated_at_movie() RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        SET TIMEZONE TO 'Europe/Moscow';
        NEW.modified = now();
        RETURN NEW;
    END;
$$;

CREATE TRIGGER update_user_task_updated_on
    BEFORE UPDATE
    ON
        content.film_work
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_movie();


/* Создание  индекса film_work_creation_date_idx так,
    чтобы ускорять поиск с фильтром по  creation_date */
CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work(creation_date);


/* Создание таблицы genre в схеме content */
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    modified timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


/* Создание  индекса genre_name_idx так,
    чтобы ускорять поиск с фильтром по наименованию жанра */
CREATE INDEX IF NOT EXISTS genre_name_idx ON content.genre(name);


/* Создание таблицы person в схеме content */
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    modified timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


/* Создание таблицы person_film_work в схеме content */
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE
);


/* Создание композитный индекса film_work_person_idx так,
    чтобы нельзя было добавить одного актёра несколько раз к одному фильму. */
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);


/* Создание таблицы genre_film_work в схеме content */
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE
);

/* Создание композитный индекса film_work_genre_idx так,
    чтобы нельзя было добавить один жанр несколько раз к одному фильму. */
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);