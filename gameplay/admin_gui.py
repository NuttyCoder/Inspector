import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Xbox Usage Admin Panel")

        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set up the users section
        self.users_label = ttk.Label(self.main_frame, text="Users")
        self.users_label.grid(row=0, column=0, padx=5, pady=5)
        self.users_listbox = tk.Listbox(self.main_frame, height=10)
        self.users_listbox.grid(row=1, column=0, padx=5, pady=5)
        self.refresh_users_list()

        # Set up the gameplay logs section
        self.gameplay_label = ttk.Label(self.main_frame, text="Gameplay Logs")
        self.gameplay_label.grid(row=0, column=1, padx=5, pady=5)
        self.gameplay_treeview = ttk.Treeview(self.main_frame, columns=("User ID", "Game Title", "Duration", "Timestamp"), show='headings')
        self.gameplay_treeview.heading("User ID", text="User ID")
        self.gameplay_treeview.heading("Game Title", text="Game Title")
        self.gameplay_treeview.heading("Duration", text="Duration")
        self.gameplay_treeview.heading("Timestamp", text="Timestamp")
        self.gameplay_treeview.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_gameplay_logs()

        # Set up the chat logs section
        self.chat_label = ttk.Label(self.main_frame, text="Chat Logs")
        self.chat_label.grid(row=0, column=2, padx=5, pady=5)
        self.chat_treeview = ttk.Treeview(self.main_frame, columns=("User ID", "Message", "Timestamp"), show='headings')
        self.chat_treeview.heading("User ID", text="User ID")
        self.chat_treeview.heading("Message", text="Message")
        self.chat_treeview.heading("Timestamp", text="Timestamp")
        self.chat_treeview.grid(row=1, column=2, padx=5, pady=5)
        self.refresh_chat_logs()

        # Set up add user section
        self.add_user_frame = ttk.Frame(root, padding="10")
        self.add_user_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

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

    def refresh_gameplay_logs(self):
        for row in self.gameplay_treeview.get_children():
            self.gameplay_treeview.delete(row)
        logs = database.get_gameplay_logs()
        for log in logs:
            self.gameplay_treeview.insert("", tk.END, values=log)

    def refresh_chat_logs(self):
        for row in self.chat_treeview.get_children():
            self.chat_treeview.delete(row)
        logs = database.get_chat_logs()
        for log in logs:
            self.chat_treeview.insert("", tk.END, values=log)

    def add_user(self):
        username = self.new_user_entry.get()
        if username:
            user_id = self.generate_user_id(username)
            database.add_user(user_id, username)
            self.refresh_users_list()
            self.new_user_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Username cannot be empty")

    def generate_user_id(self, username):
        # Placeholder for generating unique user ID
        return username.lower().replace(" ", "_")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
