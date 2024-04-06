import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes
import sqlite3
from datetime import datetime


class TaskManagerGUI:
    def __init__(self, master):
        # Main window setup
        self.master = master
        master.title("Task Manager")
        master.geometry("1100x850")

        # Apply a style to the calendar
        style = ttk.Style(master)
        style.theme_use('clam') 
        style.configure('my.Calendar.TButton', font=('Arial', 10, 'bold'), foreground='dark blue')
        style.configure('my.Calendar.TLabel', font=('Arial', 12, 'bold'), foreground='dark red')
        style.configure('my.Calendar.TFrame', background='light blue')

        # Main layout frames
        left_frame = tk.Frame(master)
        right_frame = tk.Frame(master, bg='light grey')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize add_task_window attribute
        self.add_task_window = None

        # Calendar frame on the left
        calendar_frame = tk.Frame(left_frame)
        calendar_frame.grid(row=0, column=0, sticky='nsew')
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)

        self.calendar = Calendar(calendar_frame, font=("Arial", 14), selectmode='day', 
                                 style='my.Calendar', locale='en_US')
        self.calendar.pack(expand=True, fill=tk.BOTH)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_date_select)

        # Filter frame on the left
        filter_frame = tk.Frame(left_frame)
        filter_frame.grid(row=1, column=0, sticky='ew')

        self.tag_filter_entry = tk.Entry(filter_frame)
        self.tag_filter_entry.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)
        self.tag_filter_entry.bind('<KeyRelease>', self.on_keyrelease)  # Bind the key release event
        self.filter_button = tk.Button(filter_frame, text="Filter by Tag", command=self.filter_by_tag)
        self.filter_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Treeview for displaying tasks on the left, under the filter frame
        self.tasks_treeview = self.create_task_treeview(left_frame)
        self.tasks_treeview.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        left_frame.rowconfigure(2, weight=5)

        # Treeview for displaying tasks for the selected day on the right
        self.selected_day_tasks_treeview = self.create_task_treeview(right_frame)
        self.selected_day_tasks_treeview.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons frame on the left, below the filter frame
        button_frame = tk.Frame(left_frame)
        button_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        self.add_task_btn = tk.Button(button_frame, text="Add Task", command=self.add_task)
        self.edit_task_btn = tk.Button(button_frame, text="Edit Selected Task", command=self.edit_selected_task)
        self.delete_task_btn = tk.Button(button_frame, text="Delete Selected Task", command=self.delete_selected_task)
        self.sort_by_date_btn = tk.Button(button_frame, text="Sort by Due Date", command=lambda: self.populate_tasks(sort_by="due_date"))
        self.sort_by_priority_btn = tk.Button(button_frame, text="Sort by Priority", command=lambda: self.populate_tasks(sort_by="priority", descending=True))

        # Pack buttons in order
        for button in [self.add_task_btn, self.edit_task_btn, self.delete_task_btn, self.sort_by_date_btn, self.sort_by_priority_btn]:
            button.pack(side=tk.LEFT, padx=5)

        # Initial population of tasks
        self.populate_tasks()


    def create_task_treeview(self, parent):
        columns = ("ID", "Title", "Description", "Due Date", "Priority", "Tag")
        treeview = ttk.Treeview(parent, columns=columns, show='headings')
        treeview.column("ID", width=0, stretch=tk.NO, anchor='w')
        treeview.heading("Title", text="Title")
        treeview.heading("Description", text="Description")
        treeview.heading("Due Date", text="Due Date")
        treeview.heading("Priority", text="Priority")
        treeview.heading("Tag", text="Tag")
        for col in ["Title", "Description", "Due Date", "Priority", "Tag"]:
            treeview.column(col, width=100, anchor='w')
        return treeview

    def on_calendar_date_select(self, event):
        selected_date = self.calendar.selection_get()
        self.populate_tasks_for_date(selected_date)

    def populate_tasks_for_date(self, date):
        self.selected_day_tasks_treeview.delete(*self.selected_day_tasks_treeview.get_children())
        # Call get_tasks_by_date with only the date parameter
        filtered_tasks = self.get_tasks_by_date(date)
        for task in filtered_tasks:
            self.selected_day_tasks_treeview.insert('', 'end', values=(task['id'], task['title'], task['description'], task['due_date'], task['priority'], task['tag']))



    def populate_tasks(self, sort_by="due_date", descending=False):
        self.tasks_treeview.delete(*self.tasks_treeview.get_children())
        order = "DESC" if descending else "ASC"
        sql_query = f"SELECT * FROM Tasks ORDER BY {sort_by} {order}"
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

    def on_keyrelease(self, event):
        self.filter_by_tag()

    def filter_by_tag(self):
        tag = self.tag_filter_entry.get()
        self.populate_tasks_with_tag(tag)

    def populate_tasks_with_tag(self, tag):
        # Clear the treeview
        for item in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(item)
        
        # Filter tasks by tag and update the treeview
        # Fetch the tasks from the database with the matching tag
        conn = sqlite3.connect('task_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tasks WHERE tag LIKE ?", ('%' + tag + '%',))
        rows = cursor.fetchall()
        conn.close()
        
        # Populate the treeview with the filtered tasks
        for row in rows:
            self.tasks_treeview.insert("", tk.END, values=row)

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
            time_tuple = self.time_picker.time()
            due_time = f"{time_tuple[0]:02d}:{time_tuple[1]:02d}"
            priority = self.priority_entry.get()
            tag = self.tag_entry.get()

            # Validate input (simple validation)
            if not title or not due_date or not priority:
                messagebox.showerror("Error", "Title, due date, and priority are required.")
                return
            
            # Combine the date and time into a single datetime object
            due_datetime = datetime.strptime(f'{due_date} {due_time}', '%Y-%m-%d %H:%M')

                # Connect to the database and insert the new task
            try:
                conn = sqlite3.connect('task_db.sqlite')
                cursor = conn.cursor()
                
                # Insert the new task into the database
                cursor.execute('''INSERT INTO Tasks (title, description, due_date, priority, tag)
                                VALUES (?, ?, ?, ?, ?)''',
                            (title, description, due_datetime, priority, tag))
                
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

            ttk.Label(self.add_task_window, text="Time:").grid(row=2, column=0, sticky='ew', padx=10, pady=10)
            self.time_picker = AnalogPicker(self.add_task_window)
            self.time_picker.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

            ttk.Label(self.add_task_window, text="Due Date:").grid(row=3, column=0, sticky='ew', padx=10, pady=10)
            self.due_date_entry = DateEntry(self.add_task_window)
            self.due_date_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)

            ttk.Label(self.add_task_window, text="Priority:").grid(row=4, column=0, sticky='ew', padx=10, pady=10)
            self.priority_entry = ttk.Combobox(self.add_task_window, values=[1, 2, 3, 4, 5])
            self.priority_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)

            ttk.Label(self.add_task_window, text="Tag:").grid(row=5, column=0, sticky='ew', padx=10, pady=10)
            self.tag_entry = ttk.Entry(self.add_task_window)
            self.tag_entry.grid(row=5, column=1, sticky='ew', padx=10, pady=10)
            
            save_button = tk.Button(self.add_task_window, text="Save", command=save_new_task)
            save_button.grid(row=6, column=0, columnspan=2)
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



    def get_tasks_by_date(self, date):
        """
        Fetch tasks from the database for the given date.

        Parameters:
        - date: The date for which to fetch tasks. Expected to be a datetime.date instance.
        """
        tasks = []
        # Format the date as a string in YYYY-MM-DD format for the SQL query
        date_str = date.strftime('%Y-%m-%d')

        try:
            conn = sqlite3.connect('task_db.sqlite')
            cursor = conn.cursor()

            # Select tasks where the due date matches the date provided
            cursor.execute("SELECT * FROM Tasks WHERE due_date = ?", (date_str,))
            rows = cursor.fetchall()

            # Assuming your task data is stored in a dictionary format
            for row in rows:
                task = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'due_date': row[3],
                    'priority': row[4],
                    'tag': row[5]
                }
                tasks.append(task)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if conn:
                conn.close()

        return tasks


if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskManagerGUI(root)
    root.mainloop()

