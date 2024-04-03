import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from util.db import TaskDAO
from datetime import datetime

# TODO we could probably abstract this further and separate menus into their own
# files

class TaskManagerGUI:
    def __init__(self, master):
        """
        Initialize the main GUI window.

        Parameters:
        - master: The parent Tkinter widget.
        """

        self.master = master
        master.title("Task Manager")
        master.geometry("800x400")

        # Track open windows
        self.add_task_window = None

        # Create a frame for the buttons
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))

        # Add Task Button
        self.add_task_btn = tk.Button(button_frame, text="Add Task", command=self.add_task)
        self.add_task_btn.pack(side=tk.LEFT, padx=5)

        # Edit Task Button
        self.edit_task_btn = tk.Button(button_frame, text="Edit Selected Task", command=self.edit_selected_task)
        self.edit_task_btn.pack(side=tk.LEFT, padx=5)

        # Delete Task Button
        self.delete_task_btn = tk.Button(button_frame, text="Delete Selected Task", command=self.delete_selected_task)
        self.delete_task_btn.pack(side=tk.LEFT, padx=5)

        # Sort Tasks Button
        self.sort_tasks_btn = tk.Button(button_frame, text="Sort by Due Date", command=lambda: self.populate_tasks(sort_by="due_date"))
        self.sort_tasks_btn.pack(side=tk.LEFT, padx=5)

        # Sort Tasks Button
        self.sort_tasks_btn = tk.Button(button_frame, text="Sort by Priority", command=lambda: self.populate_tasks(sort_by="priority", descending=True))
        self.sort_tasks_btn.pack(side=tk.LEFT, padx=5)
        

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
        """
        Populate the Treeview with tasks sorted according to the specified attribute.

        Parameters:
        - sort_by: The attribute to sort the tasks by. Defaults to "due_date".
        - descending: Boolean indicating whether to sort in descending order. Defaults to False.
        """

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
        """
        Open a window to add a new task. If the window is already open, bring it to focus.
        """

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
                conn = sqlite3.connect('task_db.sqlite')
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
            self.add_task_window.destroy()
        

        if not self.add_task_window or not self.add_task_window.winfo_exists():
            self.add_task_window = tk.Toplevel(self.master)
            self.add_task_window.title("Add New Task")
            
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
            
            save_button = tk.Button(self.add_task_window, text="Save", command=save_new_task)
            save_button.grid(row=5, column=0, columnspan=2)
        else:
            self.add_task_window.focus()


    def edit_selected_task(self):
        """
        Open a window to edit the currently selected task. If no task is selected, show an error.
        """

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
        due_date_entry = tk.Entry(edit_window)
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
            # Collect the updated task details from the input fields
            updated_title = title_entry.get()
            updated_description = description_entry.get("1.0", tk.END).strip()
            updated_due_date = due_date_entry.get()
            updated_priority = priority_entry.get()
            updated_tag = tag_entry.get()

            # Connect to the database and update the task
            try:
                conn = sqlite3.connect('task_db.sqlite') 
                cursor = conn.cursor()
                
                # Execute the UPDATE SQL statement
                cursor.execute('''UPDATE Tasks SET title=?, description=?, due_date=?, priority=?, tag=? WHERE id=?''',
                            (updated_title, updated_description, updated_due_date, updated_priority, updated_tag, task_id))
                
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

            self.populate_tasks()  # Refresh the tasks list
            edit_window.destroy()  # Close the edit window

        save_button = tk.Button(edit_window, text="Update", command=update_task)
        save_button.grid(row=5, column=0, columnspan=2)


    def delete_selected_task(self):
        """
        Delete the currently selected task(s) after confirming with the user. If no task is selected, show an info message.
        """
        selected_items = self.tasks_treeview.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No tasks selected.")
            return

        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected tasks?")
        if response:
            self.perform_deletion(selected_items)


    def perform_deletion(self, selected_items):
        """
        Perform the deletion of selected tasks from the database.

        Parameters:
        - selected_items: A list of Treeview item identifiers for the selected tasks.
        """
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

