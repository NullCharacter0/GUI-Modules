import tkinter as tk
from tkinter import ttk

class TreeViewManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Treeview Manager")

        # Create Treeview
        self.tree = ttk.Treeview(root, columns=('Name', 'Description'))

        # Add headings
        self.tree.heading('#0', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Description', text='Description')

        # Add items with checkboxes
        self.items = {}

        # Add some initial items
        self.add_item('Item 1', 'Description 1')
        self.add_item('Item 2', 'Description 2')

        # Bind a callback to toggle checkboxes
        self.tree.tag_bind('unchecked', '<ButtonRelease-1>', self.toggle_checkbox)
        self.tree.tag_bind('checked', '<ButtonRelease-1>', self.toggle_checkbox)

        # Add buttons
        add_button = tk.Button(root, text='Add Item', command=self.add_item_prompt)
        add_button.pack(side=tk.LEFT, padx=5)
        remove_button = tk.Button(root, text='Remove Item', command=self.remove_selected_item)
        remove_button.pack(side=tk.LEFT, padx=5)

        # Pack the Treeview
        self.tree.pack()

    def toggle_checkbox(self, event):
        item_id = self.tree.selection()[0]
        current_state = self.tree.item(item_id, 'tags')
        new_state = ('unchecked',) if 'checked' in current_state else ('checked',)
        self.tree.item(item_id, tags=new_state)

    def add_item(self, name, description):
        item_id = self.tree.insert('', 'end', text=len(self.items) + 1, values=(name, description), tags=('unchecked',))
        self.items[item_id] = {'name': name, 'description': description}

    def remove_selected_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            del self.items[selected_item[0]]

    def add_item_prompt(self):
        add_item_window = tk.Toplevel(self.root)
        add_item_window.title('Add Item')

        name_label = tk.Label(add_item_window, text='Name:')
        name_label.pack()
        name_entry = tk.Entry(add_item_window)
        name_entry.pack()

        description_label = tk.Label(add_item_window, text='Description:')
        description_label.pack()
        description_entry = tk.Entry(add_item_window)
        description_entry.pack()

        add_button = tk.Button(add_item_window, text='Add', command=lambda: self.add_item(
            name_entry.get(), description_entry.get()))
        add_button.pack()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeViewManager(root)
    app.run()
