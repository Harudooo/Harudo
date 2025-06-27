import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SmartSchedulerApp:
    def __init__(self, master):
        self.master = master
        master.title("Smart Scheduler")
        master.geometry("1000x700") # Increased window size for better layout
        master.resizable(True, True)
        master.config(bg="#e8edf2") # Lighter, modern background

        self.exams = [] # List to store exam dictionaries

        # --- ttk Style Configuration ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use 'clam' or 'alt' for a flatter look

        # General frame/background style
        self.style.configure('TFrame', background='#e8edf2')
        self.style.configure('TLabelframe', background='#ffffff', bordercolor='#d0d6df', relief='flat')
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 14, 'bold'), foreground='#334155')

        # Label styles
        self.style.configure('TLabel', background='white', foreground='#334155', font=('Segoe UI', 11))
        self.style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#1e3a8a', background='#e8edf2')

        # Entry styles
        self.style.configure('TEntry', fieldbackground='#f8fafc', bordercolor='#cbd5e1', foreground='#334155', font=('Segoe UI', 11))
        self.style.map('TEntry',
                       fieldbackground=[('focus', '#e0f2fe')],
                       bordercolor=[('focus', '#2563eb')])

        # Button styles
        self.style.configure('TButton',
                             font=('Segoe UI', 11, 'bold'),
                             background='#4f46e5', # Indigo
                             foreground='white',
                             relief='flat',
                             padding=10,
                             focusthickness=0,
                             focuscolor='none') # No focus border
        self.style.map('TButton',
                       background=[('active', '#4338ca')],
                       foreground=[('active', 'white')])

        # Special button styles
        self.style.configure('Add.TButton', background='#22c55e', foreground='white') # Green
        self.style.map('Add.TButton', background=[('active', '#16a34a')])

        self.style.configure('Clear.TButton', background='#64748b', foreground='white') # Gray
        self.style.map('Clear.TButton', background=[('active', '#475569')])

        self.style.configure('Edit.TButton', background='#0ea5e9', foreground='white') # Sky Blue
        self.style.map('Edit.TButton', background=[('active', '#0284c7')])

        self.style.configure('Delete.TButton', background='#ef4444', foreground='white') # Red
        self.style.map('Delete.TButton', background=[('active', '#dc2626')])

        # Treeview (Table) styles
        self.style.configure("Treeview.Heading", font=('Segoe UI', 12, 'bold'), background='#64748b', foreground='white') # Slate
        self.style.configure("Treeview", font=('Segoe UI', 11), rowheight=28, background='#ffffff', foreground='#334155', fieldbackground='#ffffff')
        self.style.map('Treeview', background=[('selected', '#a3e635')], foreground=[('selected', '#1f2937')]) # Lime green selection

        # --- Main Frame for layout ---
        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.pack(expand=True, fill="both")

        # --- Title ---
        self.title_label = ttk.Label(self.main_frame, text="Smart Exam Scheduler", style='Header.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="n")

        # --- Input Frame ---
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Exam Details", padding="20 20 20 20")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # Grid configuration for input frame
        self.input_frame.columnconfigure(1, weight=1) # Make entry columns expandable

        # Labels and Entry fields
        self.create_input_row(self.input_frame, 0, "Exam Name:", "name_entry")
        self.create_input_row(self.input_frame, 1, "Date (YYYY-MM-DD):", "date_entry")
        self.create_input_row(self.input_frame, 2, "Time (HH:MM):", "time_entry")
        self.create_input_row(self.input_frame, 3, "Room:", "room_entry")

        # --- Buttons Frame (Add/Clear Form) ---
        self.button_form_actions_frame = ttk.Frame(self.main_frame)
        self.button_form_actions_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))

        self.add_update_button = ttk.Button(self.button_form_actions_frame, text="Add Exam", command=self.add_exam, style='Add.TButton')
        self.add_update_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(self.button_form_actions_frame, text="Clear Form", command=self.clear_form, style='Clear.TButton')
        self.clear_button.pack(side="left", padx=10)

        # --- Exam List Frame (using Treeview) ---
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Scheduled Exams", padding="15 15 15 15")
        self.list_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        self.main_frame.rowconfigure(3, weight=1) # Make list frame expand vertically

        # Define Treeview columns
        columns = ("Name", "Date", "Time", "Room")
        self.exam_treeview = ttk.Treeview(self.list_frame, columns=columns, show="headings")

        # Configure column headings
        self.exam_treeview.heading("Name", text="Exam Name", anchor="w")
        self.exam_treeview.heading("Date", text="Date", anchor="w")
        self.exam_treeview.heading("Time", text="Time", anchor="w")
        self.exam_treeview.heading("Room", text="Room", anchor="w")

        # Configure column widths (adjust as needed)
        self.exam_treeview.column("Name", width=200, minwidth=150, stretch=tk.YES)
        self.exam_treeview.column("Date", width=120, minwidth=100, stretch=tk.NO)
        self.exam_treeview.column("Time", width=100, minwidth=80, stretch=tk.NO)
        self.exam_treeview.column("Room", width=150, minwidth=100, stretch=tk.YES)


        self.exam_treeview.pack(side="left", fill="both", expand=True)

        # Scrollbar for Treeview
        self.tree_scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.exam_treeview.yview)
        self.tree_scrollbar.pack(side="right", fill="y")
        self.exam_treeview.config(yscrollcommand=self.tree_scrollbar.set)

        # Bind selection event to Treeview
        self.exam_treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # --- Action Buttons Frame (Edit/Delete for selected item) ---
        self.action_button_frame = ttk.Frame(self.main_frame)
        self.action_button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 0))

        self.edit_button = ttk.Button(self.action_button_frame, text="Edit Selected Exam", command=self.edit_selected_exam, style='Edit.TButton')
        self.edit_button.pack(side="left", padx=10)

        self.delete_button = ttk.Button(self.action_button_frame, text="Delete Selected Exam", command=self.delete_selected_exam, style='Delete.TButton')
        self.delete_button.pack(side="left", padx=10)

        # Track the exam currently being edited (its original data)
        self.current_editing_exam_data = None

        # Initially populate the treeview
        self.update_exam_treeview()

    def create_input_row(self, parent_frame, row_idx, label_text, entry_attr_name):
        """Helper to create a label and ttk.Entry field pair using grid."""
        label = ttk.Label(parent_frame, text=label_text)
        label.grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")

        entry = ttk.Entry(parent_frame, width=40)
        entry.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        setattr(self, entry_attr_name, entry) # Assign entry widget to an attribute

    def clear_form(self):
        """Clears all input fields in the form and resets the add/update button."""
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.room_entry.delete(0, tk.END)
        self.add_update_button.config(text="Add Exam", command=self.add_exam, style='Add.TButton')
        self.current_editing_exam_data = None # Reset editing state
        self.exam_treeview.selection_remove(self.exam_treeview.selection()) # Deselect any item in treeview


    def add_exam(self):
        """Adds a new exam entry from the form fields."""
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        room = self.room_entry.get().strip()

        if not all([name, date_str, time_str, room]):
            messagebox.showerror("Input Error", "All fields must be filled!")
            return

        try:
            exam_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            exam_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format. Please use HH:MM (24-hour).")
            return

        exam = {
            "name": name,
            "date": exam_date,
            "time": exam_time,
            "room": room
        }
        self.exams.append(exam)
        self.clear_form()
        self.update_exam_treeview()
        messagebox.showinfo("Success", f"Exam '{name}' added successfully!")

    def update_exam(self):
        """Updates the exam that was previously loaded into the form for editing."""
        if self.current_editing_exam_data is None:
            messagebox.showwarning("No Exam Selected", "No exam is selected for update. Please select an exam from the list or add a new one.")
            self.clear_form() # Reset the button in case it's stuck in "Update" mode
            return

        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        room = self.room_entry.get().strip()

        if not all([name, date_str, time_str, room]):
            messagebox.showerror("Input Error", "All fields must be filled for update!")
            return

        try:
            exam_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            exam_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format. Please use HH:MM (24-hour).")
            return

        # Find the actual index of the old_exam_data in the unsorted 'exams' list
        try:
            original_index = -1
            for i, exam in enumerate(self.exams):
                # Compare all fields to find the exact original exam object
                if (exam['name'] == self.current_editing_exam_data['name'] and
                    exam['date'] == self.current_editing_exam_data['date'] and
                    exam['time'] == self.current_editing_exam_data['time'] and
                    exam['room'] == self.current_editing_exam_data['room']):
                    original_index = i
                    break

            if original_index != -1:
                self.exams[original_index] = {
                    "name": name,
                    "date": exam_date,
                    "time": exam_time,
                    "room": room
                }
                self.clear_form()
                self.update_exam_treeview()
                messagebox.showinfo("Success", f"Exam '{name}' updated successfully!")
                self.current_editing_exam_data = None # Reset editing state
            else:
                messagebox.showerror("Error", "Could not find the original exam to update. It might have been deleted or modified externally.")
                self.clear_form() # Clear form and reset button
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during update: {e}")
            self.clear_form()


    def update_exam_treeview(self):
        """Clears and repopulates the Treeview with current exams, sorted."""
        # Clear existing items in Treeview
        for iid in self.exam_treeview.get_children():
            self.exam_treeview.delete(iid)

        # Sort exams by date, then by time
        sorted_exams = sorted(self.exams, key=lambda x: (x["date"], x["time"]))

        for exam in sorted_exams:
            # Insert data into Treeview
            self.exam_treeview.insert("", tk.END, values=(
                exam['name'],
                exam['date'].strftime('%Y-%m-%d'),
                exam['time'].strftime('%H:%M'),
                exam['room']
            ), tags=('exam_row',)) # Assign a tag for potential future styling

    def on_treeview_select(self, event):
        """Fills the form with details of the selected exam when an item is clicked in the Treeview."""
        selected_item_id = self.exam_treeview.focus() # Get the ID of the selected item
        if selected_item_id:
            # Get the values from the selected row in the Treeview
            values = self.exam_treeview.item(selected_item_id, 'values')

            # Reconstruct the exam dictionary based on values from Treeview
            # Note: Dates/times from Treeview are strings, convert back to datetime objects if needed for logic
            # For this context, we're just populating the form for display/editing
            selected_exam_from_display = {
                "name": values[0],
                "date": datetime.strptime(values[1], "%Y-%m-%d").date(),
                "time": datetime.strptime(values[2], "%H:%M").time(),
                "room": values[3]
            }

            self.clear_form() # Clear form before populating
            self.name_entry.insert(0, selected_exam_from_display["name"])
            self.date_entry.insert(0, selected_exam_from_display["date"].strftime("%Y-%m-%d"))
            self.time_entry.insert(0, selected_exam_from_display["time"].strftime("%H:%M"))
            self.room_entry.insert(0, selected_exam_from_display["room"])

            self.current_editing_exam_data = selected_exam_from_display # Store the reference to the original exam data

            # Change Add button to Update button
            self.add_update_button.config(text="Update Exam", command=self.update_exam, style='Edit.TButton')
        else:
            self.clear_form() # If selection is cleared, reset form


    def edit_selected_exam(self):
        """Handles the 'Edit Selected Exam' button click."""
        selected_item_id = self.exam_treeview.focus()
        if selected_item_id:
            # If an item is selected, trigger the selection event to populate the form
            self.on_treeview_select(None) # Pass None as event argument
        else:
            messagebox.showwarning("No Selection", "Please select an exam from the list to edit.")


    def delete_selected_exam(self):
        """Deletes the currently selected exam from the list."""
        selected_item_id = self.exam_treeview.focus()
        if selected_item_id:
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this exam?")
            if response:
                # Get the values from the selected row in the Treeview
                values = self.exam_treeview.item(selected_item_id, 'values')
                # Reconstruct the exam dictionary to find the exact one in self.exams
                exam_to_delete_from_display = {
                    "name": values[0],
                    "date": datetime.strptime(values[1], "%Y-%m-%d").date(),
                    "time": datetime.strptime(values[2], "%H:%M").time(),
                    "room": values[3]
                }

                # Find and remove the exact exam object from the original list
                try:
                    # Find the index of the object matching the reconstructed data
                    found_index = -1
                    for i, exam in enumerate(self.exams):
                        if (exam['name'] == exam_to_delete_from_display['name'] and
                            exam['date'] == exam_to_delete_from_display['date'] and
                            exam['time'] == exam_to_delete_from_display['time'] and
                            exam['room'] == exam_to_delete_from_display['room']):
                            found_index = i
                            break
                    if found_index != -1:
                        del self.exams[found_index]
                        self.exam_treeview.delete(selected_item_id) # Remove from Treeview
                        self.clear_form()
                        self.update_exam_treeview() # Re-render to ensure sorting/indices are correct
                        messagebox.showinfo("Deleted", "Exam deleted successfully!")
                    else:
                        messagebox.showerror("Error", "Exam not found in list. It might have been deleted already.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during deletion: {e}")

        else:
            messagebox.showwarning("No Selection", "Please select an exam from the list to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartSchedulerApp(root)
    root.mainloop()
