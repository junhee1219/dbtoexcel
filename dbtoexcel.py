import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import dbselector as db
import json

def read_json():
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
            print(config_data)
            entry_host.insert(0, config_data["host"])
            entry_port.insert(0, config_data["port"])
            entry_username.insert(0, config_data["user"])
            entry_password.insert(0, config_data["password"])
            entry_db.insert(0, config_data["database"])
        return
    except:
        return
    

## 패딩설정
padx = 10
pady = 5

def browse_folder():
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("xlsx files", "*.xlsx")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, save_path)
    

def execute_query():
     # Host
    dbinfo = {
        "host" : entry_host.get(),
        "port" : entry_port.get(),
        "user" : entry_username.get(),
        "password" : entry_password.get(),
        "database" : entry_db.get()
    }

    query = text_query.get("1.0", tk.END)
    file_path = entry_file_path.get()
    
    result = db.fetch_data(query, dbinfo ,file_path)
    
    if result is not None:
        messagebox.showinfo("결과", result)


root = tk.Tk()
root.title("db셀렉터")
root.geometry("600x400")  # 초기 창 크기 설정

## ROW 1 ##

# 호스트 입력
tk.Label(root, text="Host").grid(row=0, column=0, sticky="w", padx=padx, pady=pady)
entry_host = tk.Entry(root)
entry_host.grid(row=0, column=1, sticky="ew", padx=padx, pady=pady, columnspan=2)

# 포트 입력
tk.Label(root, text="Port").grid(row=0, column=3, sticky="w", padx=padx)
entry_port = tk.Entry(root)
entry_port.grid(row=0, column=4, sticky="ew", padx=padx, pady=pady, columnspan=2)

## ROW 2 ##
# 데이터베이스 입력
tk.Label(root, text="Database").grid(row=1, column=0, sticky="w", padx=padx, pady=pady)
entry_db = tk.Entry(root)
entry_db.grid(row=1, column=1, sticky="ew", padx=padx, pady=pady,columnspan=2)

## ROW 3 ##
# 사용자 이름 입력
tk.Label(root, text="ID").grid(row=2, column=0, sticky="w", padx=padx, pady=pady)
entry_username = tk.Entry(root)
entry_username.grid(row=2, column=1, sticky="ew", padx=padx, pady=pady,columnspan=2)

# 비밀번호 입력
tk.Label(root, text="PW").grid(row=2, column=3, sticky="w", padx=padx, pady=pady)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=4, sticky="ew", padx=padx, pady=pady,columnspan=2)


# 쿼리 입력 (스크롤 가능한 텍스트 영역)
tk.Label(root, text="쿼리").grid(row=3, column=0, sticky="w", padx=padx, pady=pady)
text_query = scrolledtext.ScrolledText(root, height=5)
text_query.grid(row=3, column=1, sticky="nsew", padx=padx, pady=pady,columnspan=5)  # n, s, e, w 붙여서 모든 방향으로 늘어나도록 설정


# 파일 경로 입력
tk.Label(root, text="파일경로").grid(row=4, column=0, sticky="w", padx=padx, pady=pady)
entry_file_path = tk.Entry(root)
entry_file_path.grid(row=4, column=1, sticky="ew", padx=padx, pady=pady, columnspan=4)
button_browse = tk.Button(root, text="찾기", command=browse_folder)
button_browse.grid(row=4, column=5, sticky="ew", padx=padx, pady=pady)


# 실행 버튼
execute_button = tk.Button(root, text="데이터 추출",  command=execute_query)
execute_button.grid(row=5, column=0, sticky="s", padx=padx, pady=pady*2,columnspan=6)

root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(4, weight=1)
root.grid_rowconfigure(3, weight=1)   # 쿼리 입력란이 세로로 늘어나도록 설정
read_json()
root.mainloop()
