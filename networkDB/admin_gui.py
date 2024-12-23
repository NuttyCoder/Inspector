import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Network Admin Panel")

        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set up the users section
        self.users_label = ttk.Label(self.main_frame, text="Users")
        self.users_label.grid(row=0, column=0, padx=5, pady=5)
        self.users_listbox = tk.Listbox(self.main_frame, height=10)
        self.users_listbox.grid(row=1, column=0, padx=5, pady=5)
        self.refresh_users_list()

        # Set up the logs section
        self.logs_label = ttk.Label(self.main_frame, text="Device Logs")
        self.logs_label.grid(row=0, column=1, padx=5, pady=5)
        self.logs_treeview = ttk.Treeview(self.main_frame, columns=("User ID", "Device", "Date", "Time"), show='headings')
        self.logs_treeview.heading("User ID", text="User ID")
        self.logs_treeview.heading("Device", text="Device")
        self.logs_treeview.heading("Date", text="Date")
        self.logs_treeview.heading("Time", text="Time")
        self.logs_treeview.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_logs_list()

        # Set up add user section
        self.add_user_frame = ttk.Frame(root, padding="10")
        self.add_user_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.new_user_label = ttk.Label(self.add_user_frame, text="Add User:")
        self.new_user_label.grid(row=0, column=0, padx=5, pady=5)
        self.new_user_entry = ttk.Entry(self.add_user_frame)
        self.new_user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_user_button = ttk.Button(self.add_user_frame, text="Add", command=self.add_user)
        self.add_user_button.grid(row=0, column=2, padx=5, pady=5)

    def refresh_users_list(self):
        self.users_listbox.delete(0, tk.END)
        users = database.get_users()
        for user in users:
            self.users_listbox.insert(tk.END, f"{user[0]}: {user[1]}")

    def refresh_logs_list(self):
        for row in self.logs_treeview.get_children():
            self.logs_treeview.delete(row)
        logs = database.get_logs()
        for log in logs:
            self.logs_treeview.insert("", tk.END, values=log)

    def add_user(self):
        username = self.new_user_entry.get()
        if username:
            database.add_user(username)
            self.refresh_users_list()
            self.new_user_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Username cannot be empty")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
