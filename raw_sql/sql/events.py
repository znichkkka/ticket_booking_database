import datetime
import os

from dotenv import load_dotenv
from psycopg.rows import dict_row
import psycopg


def list_events(database_url: str) -> list[dict]:
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, title, venue, starts_at FROM events ORDER BY id' )
            return cursor.fetchall()


def search_events(database_url: str, title_part: str = "", venue_part: str = "") -> list[dict]:
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, title, venue, starts_at FROM events '
                'WHERE title ILIKE %s AND venue ILIKE %s ORDER BY starts_at, id',
                (f'%{title_part}%', f'%{venue_part}%'),
            )
            return cursor.fetchall()


def add_event(database_url: str, event_title: str, event_venue: str, starts_at: datetime) -> None:
    with psycopg.connect(database_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO events (title, venue, starts_at) VALUES (%s, %s, %s)',
                (event_title, event_venue, starts_at)
            )


def delete_event(database_url: str, event_id: int) -> None:
    with psycopg.connect(database_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM events WHERE id = %s',
                (event_id,)
            )


def find_events_by_seat(database_url: str, row_number: int, seat_number: int) -> list[dict]:
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT events.id, events.title, events.venue, events.starts_at FROM events '
                'JOIN seats ON seats.event_id = events.id '
                'WHERE seats.row_number = %s AND seats.seat_number = %s ',
                (row_number, seat_number)
            )
            return cursor.fetchall()


if __name__ == '__main__':
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')

    print(list_events(db_url))
    print(search_events(db_url, title_part='Джазовый', venue_part='мал'))

    add_event(db_url, 'Импровизация', 'Дворец спорта', '2026-11-28 19:00:00')
    print(list_events(db_url))

    delete_event(db_url, 2)
    print(list_events(db_url))

    print(find_events_by_seat(db_url, 1, 1))
