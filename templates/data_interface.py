import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class DataStatisticsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Statistics GUI")

        # Create and place widgets
        self.label = ttk.Label(root, text="Data Statistics", font=("Arial", 16))
        self.label.pack(pady=10)

        self.load_button = ttk.Button(root, text="Load CSV File", command=self.load_file)
        self.load_button.pack(pady=5)

        self.plot_button = ttk.Button(root, text="Show Statistics", command=self.show_statistics)
        self.plot_button.pack(pady=5)
        self.plot_button.config(state=tk.DISABLED)

        self.file_path = ""

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.plot_button.config(state=tk.NORMAL)

    def show_statistics(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file loaded.")
            return
        
        data = pd.read_csv(self.file_path)
        
        fig, ax = plt.subplots()
        data.describe().plot(kind='bar', ax=ax)
        plt.title("Data Statistics")
        plt.xticks(rotation=45)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataStatisticsGUI(root)
    root.mainloop()
