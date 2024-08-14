# utils/database_utils.py

import pypyodbc as odbc
import logging
from datetime import datetime, timezone
from config.config import DATABASE_CONFIG

def connect_to_database():
    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{DATABASE_CONFIG['server']},1433;"
        f"Database={DATABASE_CONFIG['database']};Uid={DATABASE_CONFIG['username']};Pwd={DATABASE_CONFIG['password']};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    
    try:
        conn = odbc.connect(connection_string)
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")

def fetch_the_queue(conn):
    try:
        cursor = conn.cursor()
        query = "SELECT jobID, email, selectedResume, timeOfArrival FROM applyQueue ORDER BY timeOfArrival ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        job_queue = [{'id': row[0], 'email': row[1], 'selectedResume': row[2], 'timeOfArrival': str(row[3])} for row in rows]
        cursor.close()
        return job_queue if job_queue else False
    except Exception as e:
        logging.error(f"Error fetching queue: {e}")

def remove_from_queue(conn, job_id, email):
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM applyQueue WHERE jobID = '{job_id}' AND email = '{email}'"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        logging.info(f"Job {job_id} removed from apply queue.")
    except Exception as e:
        logging.error(f"Error removing job from queue: {e}")

def update_the_job(conn, job_id, apply_status):
    try:
        cursor = conn.cursor()
        timestamp = int(datetime.now(timezone.utc).timestamp())
        query = f"UPDATE allData SET myStatus = '{apply_status}', decisionTime = {timestamp} WHERE id = '{job_id}'"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        logging.info(f"Job {job_id} updated with status {apply_status}.")
    except Exception as e:
        logging.error(f"Error updating job: {e}")

def fetch_resume_list(conn):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM resumeList"
        cursor.execute(query)
        rows = cursor.fetchall()
        emailDict = {}
        for id, name, email in rows:
            if email not in emailDict:
                emailDict[email] = []
            emailDict[email].append([id, name])
        cursor.close()
        return emailDict
    except Exception as e:
        logging.error(f"Error fetching resume list: {e}")

def fetchTheScore(conn):
    try:
        cursor = conn.cursor()
        query = "SELECT score FROM scoreBoard WHERE contender = 'theMachine'"
        cursor.execute(query)
        result = cursor.fetchall()
        if not result or type(result[0][0]) != int:
            result = 0
        else:
            result = result[0][0]
        cursor.close()
        return result
    except Exception as e:
        logging.error(f"Error fetching score: {e}")

def setTheScore(conn, new_score):
    try:
        cursor = conn.cursor()
        query = f"UPDATE scoreBoard SET score = {new_score} WHERE contender = 'theMachine'"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        logging.info(f"Score updated to {new_score}.")
    except Exception as e:
        logging.error(f"Error setting score: {e}")

def fetchDiceCreds(email):
    tempConn = connect_to_database()
    try:
        cursor = tempConn.cursor()
        query = f"SELECT dice_password FROM users WHERE email = '{email}'"
        cursor.execute(query)
        rows = cursor.fetchall() or None
        cursor.close()
        tempConn.close()
        return rows[0][0] or None
    except Exception as e:
        logging.error(f"Error fetching queue: {e}")