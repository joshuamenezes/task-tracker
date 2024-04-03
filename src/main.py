import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from util.db import TaskDAO
from datetime import datetime

# TODO we could probably abstract this further and separate menus into their own
# files


# class TaskManagerGUI:

#     def __init__(self, master):
#         self.master = master
#         master.title("Task Manager")
#         # Set the main window size and position
#         master.geometry("400x300+500+200")
#         self.view_tasks_window = None
#         self.add_task_window = None
#         self.edit_task_window = None
#         self.delete_task_window = None

#         self.label = tk.Label(master, text="Task Manager Application", font=("Arial", 16))
#         self.label.pack(pady=10)

#         # Add Task Button
#         self.add_task_btn = ttk.Button(master, text="Add Task", command=self.add_task)
#         self.add_task_btn.pack(pady=5)

#         # View Tasks Button
#         self.view_tasks_btn = ttk.Button(master, text="View Tasks", command=self.view_tasks)
#         self.view_tasks_btn.pack(pady=5)

#         # Edit Task Button
#         self.edit_task_btn = ttk.Button(master, text="Edit Task", command=self.edit_task)
#         self.edit_task_btn.pack(pady=5)

#         # Delete Task Button
#         self.delete_task_btn = ttk.Button(master, text="Delete Task", command=self.delete_task)
#         self.delete_task_btn.pack(pady=5)


#     def add_task(self):
#         if self.add_task_window is None or not self.add_task_window.winfo_exists():
#             self.add_task_window = tk.Toplevel(self.master)
#             self.add_task_window.title("Add New Task")
#             self.add_task_window.protocol("WM_DELETE_WINDOW", self.on_close_add_task)
#             self.add_task_window.geometry("300x300")  # Set the window size

#             # Ensure that the popup window has its own grid configuration
#             for i in range(5):
#                 self.add_task_window.rowconfigure(i, weight=1)
#             for j in range(2):
#                 self.add_task_window.columnconfigure(j, weight=1)

#             # Input fields
#             ttk.Label(self.add_task_window, text="Title:").grid(row=0, column=0, sticky='ew', padx=10, pady=10)
#             self.title_entry = ttk.Entry(self.add_task_window)
#             self.title_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)

#             ttk.Label(self.add_task_window, text="Description:").grid(row=1, column=0, sticky='ew', padx=10, pady=10)
#             self.description_entry = tk.Text(self.add_task_window, height=4, width=30)
#             self.description_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)

#             ttk.Label(self.add_task_window, text="Due Date:").grid(row=2, column=0, sticky='ew', padx=10, pady=10)
#             self.due_date_entry = DateEntry(self.add_task_window)
#             self.due_date_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

#             ttk.Label(self.add_task_window, text="Priority:").grid(row=3, column=0, sticky='ew', padx=10, pady=10)
#             self.priority_entry = ttk.Combobox(self.add_task_window, values=[1, 2, 3, 4, 5])
#             self.priority_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)

#             ttk.Label(self.add_task_window, text="Tag:").grid(row=4, column=0, sticky='ew', padx=10, pady=10)
#             self.tag_entry = ttk.Entry(self.add_task_window)
#             self.tag_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)

#             # Add Task Button
#             self.add_button = ttk.Button(self.add_task_window, text="Add Task", command=self.save_task)
#             self.add_button.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        
#         self.add_task_window.lift()





#     def save_task(self):
#         title = self.title_entry.get()
#         description = self.description_entry.get("1.0", tk.END).strip()
#         due_date = self.due_date_entry.get()
#         priority = self.priority_entry.get()
#         tag = self.tag_entry.get()

#         # Validate input
#         if not title:
#             messagebox.showerror("Error", "Title is required!")
#             return

#         # Insert into database
#         try:
#             # Using a with statement ensures the database connection is properly closed after the operation
#             with sqlite3.connect('task_db.sqlite') as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''INSERT INTO Tasks (title, description, due_date, priority, tag) 
#                                 VALUES (?, ?, ?, ?, ?)''', 
#                             (title, description, due_date, priority, tag))
#         except sqlite3.OperationalError as e:
#             messagebox.showerror("Database Error", str(e))
#             return
#         except sqlite3.IntegrityError as e:
#             messagebox.showerror("Integrity Error", "ID could not be auto-generated. Please check the database setup.")
#             return

#         # messagebox.showinfo("Success", "Task added successfully")
#         self.add_task_window.destroy()



#     def view_tasks(self):
#         # Check if the window is already open
#         if self.view_tasks_window is None or not self.view_tasks_window.winfo_exists():

#             # Create a new window to view tasks
#             self.view_tasks_window = tk.Toplevel(self.master)
#             self.view_tasks_window.title("View Tasks")
#             self.view_tasks_window.geometry("750x400")  # Adjust the window size as needed

#             # Properly handle window close event
#             self.view_tasks_window.protocol("WM_DELETE_WINDOW", self.on_close_view_tasks)

#             # Sorting buttons
#             ttk.Button(self.view_tasks_window, text="Sort by Due Date", command=lambda: self.sort_tasks("due_date")).pack(pady=(5, 0))
#             ttk.Button(self.view_tasks_window, text="Sort by Priority", command=lambda: self.sort_tasks("priority")).pack(pady=5)

#             # Add a Treeview widget to the new window
#             self.tasks_treeview = ttk.Treeview(self.view_tasks_window, columns=("ID", "Title", "Description", "Due Date", "Priority", "Tag"), show='headings')
#             self.tasks_treeview.heading("ID", text="ID")
#             self.tasks_treeview.heading("Title", text="Title")
#             self.tasks_treeview.heading("Description", text="Description")
#             self.tasks_treeview.heading("Due Date", text="Due Date")
#             self.tasks_treeview.heading("Priority", text="Priority")
#             self.tasks_treeview.heading("Tag", text="Tag")
        
#             # Align text to the left (west) and define the column widths
#             self.tasks_treeview.column("ID", width=50, anchor='w')
#             self.tasks_treeview.column("Title", width=150, anchor='w')
#             self.tasks_treeview.column("Description", width=200, anchor='w')
#             self.tasks_treeview.column("Due Date", width=100, anchor='w')
#             self.tasks_treeview.column("Priority", width=70, anchor='w')
#             self.tasks_treeview.column("Tag", width=100, anchor='w')

#             # Connect to the database and fetch the tasks
#             try:
#                 conn = sqlite3.connect('task_db.sqlite')  # or the correct path to your sqlite file
#                 cursor = conn.cursor()
#                 cursor.execute("SELECT * FROM Tasks")
#                 rows = cursor.fetchall()
#                 for row in rows:
#                     self.tasks_treeview.insert("", tk.END, values=row)
#                 conn.close()
#             except sqlite3.Error as e:
#                 messagebox.showerror("Database Error", str(e))
#                 return

#             # Add a scrollbar to the Treeview
#             scrollbar = ttk.Scrollbar(self.view_tasks_window, orient=tk.VERTICAL, command=self.tasks_treeview.yview)
#             self.tasks_treeview.configure(yscroll=scrollbar.set)
#             scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#             self.tasks_treeview.pack(expand=True, fill='both', padx=10, pady=10)

#             self.populate_tasks()
        
#         self.view_tasks_window.lift()


#     def populate_tasks(self, sort_by="due_date"):
#         # Clear existing entries
#         for i in self.tasks_treeview.get_children():
#             self.tasks_treeview.delete(i)
#         # Fetch and display tasks sorted by the specified attribute
#         try:
#             conn = sqlite3.connect('task_db.sqlite')  # Adjust path as needed
#             cursor = conn.cursor()
#             cursor.execute(f"SELECT * FROM Tasks ORDER BY {sort_by}")
#             rows = cursor.fetchall()
#             for row in rows:
#                 self.tasks_treeview.insert("", tk.END, values=row)
#             conn.close()
#         except sqlite3.Error as e:
#             messagebox.showerror("Database Error", str(e))


#     def sort_tasks(self, attribute):
#         self.populate_tasks(sort_by=attribute)


#     def edit_task(self):
#         print("Edit Task button clicked")
#         if self.edit_task_window is None or not self.edit_task_window.winfo_exists():
#             self.edit_task_window = tk.Toplevel(self.master)
#             self.edit_task_window.title("Edit Task")
#             self.edit_task_window.protocol("WM_DELETE_WINDOW", self.on_close_edit_task)


#     def delete_task(self):
#         print("Delete Task button clicked")
#         if self.delete_task_window is None or not self.delete_task_window.winfo_exists():
#             self.delete_task_window = tk.Toplevel(self.master)
#             self.delete_task_window.title("Delete Task")
#             self.delete_task_window.protocol("WM_DELETE_WINDOW", self.on_close_delete_task)


#     def on_close_add_task(self):
#         self.add_task_window.destroy()
#         self.add_task_window = None

#     def on_close_view_tasks(self):
#         self.view_tasks_window.destroy()
#         self.view_tasks_window = None

#     def on_close_edit_task(self):
#         self.edit_task_window.destroy()
#         self.edit_task_window = None

#     def on_close_delete_task(self):
#         self.delete_task_window.destroy()
#         self.delete_task_window = None


class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager")
        master.geometry("800x400")

        # Button for adding a new task
        ttk.Button(master, text="Add Task", command=self.add_task).pack(pady=(5, 0))

        # Buttons for task operations
        ttk.Button(master, text="Edit Selected Task", command=self.edit_selected_task).pack(pady=3)
        ttk.Button(master, text="Delete Selected Task", command=self.delete_selected_task).pack(pady=3)

        # Sorting options
        ttk.Button(master, text="Sort by Due Date", command=lambda: self.populate_tasks("due_date")).pack(pady=3)
        ttk.Button(master, text="Sort by Priority", command=lambda: self.populate_tasks("priority", True)).pack(pady=3)

        # Treeview for displaying tasks
        self.tasks_treeview = ttk.Treeview(master, columns=("ID", "Title", "Description", "Due Date", "Priority", "Tag"), show='headings')
        self.tasks_treeview.column("ID", width=0, stretch=tk.NO, anchor='w')
        self.tasks_treeview.heading("Title", text="Title")
        self.tasks_treeview.heading("Description", text="Description")
        self.tasks_treeview.heading("Due Date", text="Due Date")
        self.tasks_treeview.heading("Priority", text="Priority")
        self.tasks_treeview.heading("Tag", text="Tag")
        

        self.tasks_treeview.column("Title", width=150, anchor='w')
        self.tasks_treeview.column("Description", width=200, anchor='w')
        self.tasks_treeview.column("Due Date", width=100, anchor='w')
        self.tasks_treeview.column("Priority", width=70, anchor='w')
        self.tasks_treeview.column("Tag", width=100, anchor='w')

        self.tasks_treeview.pack(expand=True, fill='both', padx=10, pady=20)

        self.populate_tasks()

    def populate_tasks(self, sort_by="due_date", descending=False):
        # Clear existing entries
        for i in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(i)

        # Adjust the SQL query based on the desired sort order
        order = "DESC" if descending else "ASC"
        sql_query = f"SELECT * FROM Tasks ORDER BY {sort_by} {order}"
        
        # Fetch and display tasks sorted by the specified attribute and order
        try:
            conn = sqlite3.connect('task_db.sqlite')
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            for row in rows:
                self.tasks_treeview.insert("", tk.END, values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def add_task(self):
        def save_new_task():
            # Gather task details from input fields
            title = self.title_entry.get()
            description = self.description_entry.get("1.0", tk.END).strip()
            due_date = self.due_date_entry.get()
            due_date = datetime.strptime(due_date, '%m/%d/%y').strftime('%Y-%m-%d')
            priority = self.priority_entry.get()
            tag = self.tag_entry.get()

            # Validate input (simple validation)
            if not title or not due_date or not priority:
                messagebox.showerror("Error", "Title, due date, and priority are required.")
                return

            # Connect to the database and insert the new task
            try:
                conn = sqlite3.connect('task_db.sqlite')  # Adjust the path as needed
                cursor = conn.cursor()
                
                # Insert the new task into the database
                cursor.execute('''INSERT INTO Tasks (title, description, due_date, priority, tag)
                                VALUES (?, ?, ?, ?, ?)''',
                            (title, description, due_date, priority, tag))
                
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

            # Refresh the task list to show the newly added task
            self.populate_tasks()
            # Close the add task window
            add_window.destroy()
        
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Task")
        
        # Input fields
        ttk.Label(add_window, text="Title:").grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        self.title_entry = ttk.Entry(add_window)
        self.title_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(add_window, text="Description:").grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        self.description_entry = tk.Text(add_window, height=4, width=30)
        self.description_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(add_window, text="Due Date:").grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.due_date_entry = DateEntry(add_window)
        self.due_date_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(add_window, text="Priority:").grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.priority_entry = ttk.Combobox(add_window, values=[1, 2, 3, 4, 5])
        self.priority_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)

        ttk.Label(add_window, text="Tag:").grid(row=4, column=0, sticky='ew', padx=10, pady=10)
        self.tag_entry = ttk.Entry(add_window)
        self.tag_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)
        
        save_button = tk.Button(add_window, text="Save", command=save_new_task)
        save_button.grid(row=5, column=0, columnspan=2)


    def edit_selected_task(self):
        selected_item = self.tasks_treeview.focus()
        if not selected_item:  # No selection made
            messagebox.showerror("Error", "No task selected")
            return

        task_details = self.tasks_treeview.item(selected_item, 'values')
        if not task_details:
            messagebox.showerror("Error", "No task found")
            return

        # Extracting task details
        task_id, title, description, due_date, priority, tag = task_details

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Title").grid(row=0, column=0)
        title_entry = tk.Entry(edit_window)
        title_entry.grid(row=0, column=1)
        title_entry.insert(0, title)  # Pre-populate field

        tk.Label(edit_window, text="Description").grid(row=1, column=0)
        description_entry = tk.Text(edit_window, height=4, width=30)
        description_entry.grid(row=1, column=1)
        description_entry.insert('1.0', description)  # Pre-populate field

        tk.Label(edit_window, text="Due Date").grid(row=2, column=0)
        due_date_entry = tk.Entry(edit_window)  # Consider using a DateEntry widget for better date selection
        due_date_entry.grid(row=2, column=1)
        due_date_entry.insert(0, due_date)  # Pre-populate field

        tk.Label(edit_window, text="Priority").grid(row=3, column=0)
        priority_entry = tk.Entry(edit_window)
        priority_entry.grid(row=3, column=1)
        priority_entry.insert(0, priority)  # Pre-populate field

        tk.Label(edit_window, text="Tag").grid(row=4, column=0)
        tag_entry = tk.Entry(edit_window)
        tag_entry.grid(row=4, column=1)
        tag_entry.insert(0, tag)  # Pre-populate field

        def update_task():
            # Update the task details in the database
            updated_title = title_entry.get()
            updated_description = description_entry.get("1.0", tk.END).strip()
            updated_due_date = due_date_entry.get()
            updated_priority = priority_entry.get()
            updated_tag = tag_entry.get()

            # Here you would execute an UPDATE SQL statement using these values
            # For simplicity, I'm omitting direct database operations
            
            # Assume a function update_task_by_id exists to handle database update
            # update_task_by_id(task_id, updated_title, updated_description, updated_due_date, updated_priority, updated_tag)

            self.populate_tasks()  # Refresh the tasks list
            edit_window.destroy()  # Close the edit window

        save_button = tk.Button(edit_window, text="Update", command=update_task)
        save_button.grid(row=5, column=0, columnspan=2)




    def delete_selected_task(self):
        selected_items = self.tasks_treeview.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No tasks selected.")
            return

        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected tasks?")
        if response:
            self.perform_deletion(selected_items)


    def perform_deletion(self, selected_items):
        # Assuming task ID is the first value in the Treeview row
        for item in selected_items:
            task_id = self.tasks_treeview.item(item, 'values')[0]
            try:
                conn = sqlite3.connect('task_db.sqlite')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
                return
            finally:
                conn.close()
        
        self.populate_tasks()  # Refresh the task list




if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskManagerGUI(root)
    root.mainloop()

