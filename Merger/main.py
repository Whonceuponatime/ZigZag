import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
from tkinterdnd2 import TkinterDnD, DND_FILES


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("400x500")

        self.cover_page = None
        self.files = []

        self.cover_label = tk.Label(root, text="Drag and drop cover page here", width=40, height=2, bg="lightgray")
        self.cover_label.pack(pady=10)

        self.files_label = tk.Label(root, text="Drag and drop PDF files here", width=40, height=2, bg="lightgray")
        self.files_label.pack(pady=10)

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

        self.cover_label.drop_target_register(DND_FILES)
        self.cover_label.dnd_bind('<<Drop>>', self.drop_cover)

        self.files_label.drop_target_register(DND_FILES)
        self.files_label.dnd_bind('<<Drop>>', self.drop_files)

    def drop_cover(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            file = files[0]
            if file.lower().endswith(".pdf"):
                self.cover_page = file
                self.cover_label.config(text=f"Cover Page: {os.path.basename(file)}")

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith(".pdf"):
                self.files.append(file)
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.files:
            self.listbox.insert(tk.END, os.path.basename(file))

    def reset(self):
        self.cover_page = None
        self.files = []
        self.cover_label.config(text="Drag and drop cover page here")
        self.files_label.config(text="Drag and drop PDF files here")
        self.listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.cover_page:
            messagebox.showwarning("Warning", "Please add a cover page")
            return

        if len(self.files) < 2:
            messagebox.showwarning("Warning", "Please add at least two PDF files to merge")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        try:
            output_pdf = PdfFileWriter()

            # Add the cover page
            cover_reader = PdfFileReader(open(self.cover_page, "rb"))
            output_pdf.addPage(cover_reader.getPage(0))

            pdf_readers = [PdfFileReader(open(file, "rb")) for file in self.files]

            for i in range(max(reader.getNumPages() for reader in pdf_readers)):
                for reader in pdf_readers:
                    if i < reader.getNumPages():
                        output_pdf.addPage(reader.getPage(i))

            with open(output_path, "wb") as output_file:
                output_pdf.write(output_file)

            messagebox.showinfo("Success", f"PDFs merged successfully into {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging PDFs: {e}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
