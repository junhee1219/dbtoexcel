import pandas as pd
import mysql.connector
import sqlparse
import os
from tkinter import messagebox


def connect_to_db(dbinfo):
    return mysql.connector.connect(
        host=dbinfo["host"],
        port=dbinfo["port"], 
        user=dbinfo["user"],
        password=dbinfo["password"],
        database=dbinfo["database"]
    )

def fetch_data(query, dbinfo ,filepath):
    if not is_only_select_query(query):
        return "select 쿼리만 추출가능합니다."
    try:
        connection = connect_to_db(dbinfo)
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] 
        cursor.close()
        connection.close()
        df = pd.DataFrame(data, columns=column_names)
        df.columns = [col.upper() for col in df.columns]
        answer = True
        if os.path.exists(filepath):
            answer = messagebox.askokcancel("파일경로 중복", "해당 경로에 이미 파일이 있습니다. 덮어쓰기 하시겠습니까?")
        if answer :
            df.to_excel(filepath, index=False)
            return "저장 완료했습니다."
        else:
            return None
    except Exception as e:
        messagebox.showerror("오류", str(e))
        return None


def is_only_select_query(query):
    statements = sqlparse.parse(query)
    for statement in statements:
        if statement.get_type() != "SELECT" :
            return False
    return True