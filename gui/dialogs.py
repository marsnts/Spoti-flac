from tkinter import filedialog

class DialogMixin:

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)