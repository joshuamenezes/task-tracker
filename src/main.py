import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

# TODO we could probably abstract this further and separate menus into their own
# files


class TaskManagerGUI:

    def __init__(self, master):
        self.master = master
        master.title("Task Manager")
        # Set the main window size and position
        master.geometry("400x300+500+200")

        self.label = tk.Label(master, text="Task Manager Application", font=("Arial", 16))
        self.label.pack(pady=10)

        # Add Task Button
        self.add_task_btn = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_task_btn.pack(pady=5)

        # View Tasks Button
        self.view_tasks_btn = ttk.Button(master, text="View Tasks", command=self.view_tasks)
        self.view_tasks_btn.pack(pady=5)

        # Edit Task Button
        self.edit_task_btn = ttk.Button(master, text="Edit Task", command=self.edit_task)
        self.edit_task_btn.pack(pady=5)

        # Delete Task Button
        self.delete_task_btn = ttk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_task_btn.pack(pady=5)


    def add_task(self):
        self.add_task_window = tk.Toplevel(self.master)
        self.add_task_window.title("Add New Task")
        self.add_task_window.geometry("300x300")  # Set the window size

        # Ensure that the popup window has its own grid configuration
        for i in range(5):
            self.add_task_window.rowconfigure(i, weight=1)
        for j in range(2):
            self.add_task_window.columnconfigure(j, weight=1)

        # Input fields
        ttk.Label(self.add_task_window, text="Title:").grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        self.title_entry = ttk.Entry(self.add_task_window)
        self.title_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(self.add_task_window, text="Description:").grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        self.description_entry = tk.Text(self.add_task_window, height=4, width=30)
        self.description_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(self.add_task_window, text="Due Date:").grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.due_date_entry = DateEntry(self.add_task_window)
        self.due_date_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(self.add_task_window, text="Priority:").grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.priority_entry = ttk.Combobox(self.add_task_window, values=[1, 2, 3, 4, 5])
        self.priority_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(self.add_task_window, text="Tag:").grid(row=4, column=0, sticky='ew', padx=10, pady=10)
        self.tag_entry = ttk.Entry(self.add_task_window)
        self.tag_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)

        # Add Task Button
        self.add_button = ttk.Button(self.add_task_window, text="Add Task", command=self.save_task)
        self.add_button.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=10)



    def save_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()
        tag = self.tag_entry.get()

        # Validate input
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return

        # Insert into database
        try:
            # Using a with statement ensures the database connection is properly closed after the operation
            with sqlite3.connect('task_db.sqlite') as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO Tasks (title, description, due_date, priority, tag) 
                                VALUES (?, ?, ?, ?, ?)''', 
                            (title, description, due_date, priority, tag))
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", str(e))
            return
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Integrity Error", "ID could not be auto-generated. Please check the database setup.")
            return

        messagebox.showinfo("Success", "Task added successfully")
        self.add_task_window.destroy()



    def view_tasks(self):
        print("View Tasks button clicked")

    def edit_task(self):
        print("Edit Task button clicked")

    def delete_task(self):
        print("Delete Task button clicked")


if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskManagerGUI(root)
    root.mainloop()

