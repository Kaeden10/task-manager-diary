# Запросы базе данных
import sqlite3
cursor = None
conn = None


def connect():
    global cursor, conn
    conn = sqlite3.connect("task_manager_data.db")
    cursor = conn.cursor()



def add_events(name):
    cursor.execute('INSERT INTO EVENTS (name) VALUES (?)', (name,))
    conn.commit()


def del_events(name):
    cursor.execute('DELETE FROM EVENTS WHERE name=?', (name,))
    conn.commit()


def add_homework(id):
    cursor.execute('INSERT INTO HOMEWORK (schedule_id, text) VALUES (?, ?)', (id, ''))
    conn.commit()


def add_schedule(event_id, name):
    cursor.execute('INSERT INTO SCHEDULE (event_id, name) VALUES (?, ?)', (event_id, name))
    conn.commit()


def get_lessons(date):
    lessons = list(map(lambda x: x[0], cursor.execute('''SELECT s.name FROM EVENTS e 
                             INNER JOIN SCHEDULE s
                             ON e.id = s.event_id
                             WHERE s.event_id=?''', (date, )).fetchall()))
    lessons = list(reversed(lessons))
    while len(lessons) != 9:
        lessons.insert(0, '')
    return lessons


def get_day(day):
    return cursor.execute('SELECT name FROM EVENTS WHERE id=?', (day, )).fetchone()[0]


def get_lessons_count(day):
    return len(cursor.execute('SELECT id FROM SCHEDULE WHERE event_id=?', (day, )).fetchall()) + 1


def get_homework_lesson(day):
    hm = list(map(lambda x: x[0], cursor.execute('''SELECT hm.text FROM EVENTS e 
    INNER JOIN SCHEDULE s ON e.id = s.event_id INNER JOIN HOMEWORK hm ON s.id = hm.schedule_id
                             WHERE e.id=?''', (day, )).fetchall()))
    hm = list(reversed(hm))
    while len(hm) != 9:
        hm.insert(0, '')
    return hm

def take_lesson(day):
    return cursor.execute('SELECT * FROM SCHEDULE WHERE event_id=?', (day, )).fetchall()[-1][0]


def get_id_lesson(date):
        lessons = list(map(lambda x: x[0], cursor.execute('''SELECT s.id FROM EVENTS e 
                                 INNER JOIN SCHEDULE s
                                 ON e.id = s.event_id
                                 WHERE s.event_id=?''', (date,)).fetchall()))
        lessons = list(reversed(lessons))
        while len(lessons) != 9:
            lessons.insert(0, '')
        return lessons

def reset_homework(id, text):
    cursor.execute(f'UPDATE HOMEWORK SET text="{text}" WHERE schedule_id=?', (id, )).fetchall()
    conn.commit()

def all_homework_day(day):
    homework = list(map(lambda x: x[0], cursor.execute('''SELECT h.text FROM HOMEWORK hm 
                                 INNER JOIN SCHEDULE s
                                 ON s.id = hm.schedule_id
                                 INNER JOIN EVENTS e
                                 ON e.id = s.event_id
                                 WHERE s.event_id=?''', (day,)).fetchall()))
    homework = list(reversed(homework))
    while len(homework) != 9:
        homework.insert(0, '')
    return homework


def add_comment(lesson):
    cursor.execute('INSERT INTO COMMENTS (schedule_id, comment) VALUES (?, ?)', (lesson, ''))
    conn.commit()
#///////////
def get_comment_lesson(day):
    hm = list(map(lambda x: x[0], cursor.execute('''SELECT cm.comment FROM EVENTS e 
    INNER JOIN SCHEDULE s ON e.id = s.event_id INNER JOIN COMMENTS cm ON s.id = cm.schedule_id
                             WHERE e.id=?''', (day, )).fetchall()))
    hm = list(reversed(hm))
    while len(hm) != 9:
        hm.insert(0, '')
    return hm


def reset_comment(id, text):
    cursor.execute(f'UPDATE COMMENTS SET comment="{text}" WHERE schedule_id=?', (id, )).fetchall()
    conn.commit()

def reset_lesson(id, text):
    cursor.execute(f'UPDATE SCHEDULE SET name="{text}" WHERE id=?', (id,)).fetchall()
    conn.commit()