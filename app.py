import json
import logging
import time
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter.font import Font
import threading

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)

# Logging-Konfiguration
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger_error = logging.getLogger(__name__)

class DoclingConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 Docling Converter 📊")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        # Emojis für verschiedene Dateitypen
        self.file_emojis = {
            "pdf": "📑",
            "docx": "📝",
            "html": "🌐",
            "jpg": "🖼️",
            "png": "🖼️",
            "default": "📄"
        }

        self.setup_ui()
        self.filenames = []

    def setup_ui(self):
        # Hauptüberschrift
        title_font = Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(self.root, text="📄 Dokument-Konvertierung 📊",
                              font=title_font, bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=15)

        # Beschreibung
        desc_font = Font(family="Arial", size=10)
        desc_label = tk.Label(self.root,
                             text="Konvertiere PDF, Word und andere Dokumente mit intelligenter Texterkennung",
                             font=desc_font, bg="#f0f0f0", fg="#555555")
        desc_label.pack(pady=5)

        # Dateiauswahl-Frame
        file_frame = tk.Frame(self.root, bg="#f0f0f0")
        file_frame.pack(pady=15, fill=tk.X, padx=20)

        # Dateiauswahl-Button
        select_btn = tk.Button(file_frame, text="📂 Dateien auswählen",
                              command=self.select_files, bg="#4a86e8", fg="white",
                              font=("Arial", 10, "bold"), padx=15, pady=8)
        select_btn.pack(side=tk.LEFT, padx=5)

        # Start-Button
        self.process_btn = tk.Button(file_frame, text="▶️ Verarbeitung starten",
                                   command=self.process_files, bg="#43a047", fg="white",
                                   font=("Arial", 10, "bold"), padx=15, pady=8, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=5)

        # Dateien-Liste Frame
        list_frame = tk.Frame(self.root, bg="white", relief=tk.GROOVE, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Überschrift für die Liste
        list_label = tk.Label(list_frame, text="Ausgewählte Dateien", bg="white", fg="#333333",
                             font=("Arial", 10, "bold"))
        list_label.pack(anchor=tk.W, padx=10, pady=5)

        # Scrollbar und Listbox für Dateien
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED,
                                     bg="white", fg="#333333", font=("Arial", 9),
                                     height=10, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=self.file_listbox.yview)

        # Status-Frame
        self.status_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.status_frame.pack(fill=tk.X, padx=20, pady=10)

        # Status-Label
        self.status_label = tk.Label(self.status_frame, text="✅ Bereit zur Auswahl von Dateien",
                                   bg="#f0f0f0", fg="#555555", font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT)

        # Fortschrittsbalken
        self.progress = ttk.Progressbar(self.status_frame, orient=tk.HORIZONTAL,
                                      length=200, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=10)

        # Footer
        footer_label = tk.Label(self.root, text="🔍 Powered by Docling Converter",
                               bg="#f0f0f0", fg="#999999", font=("Arial", 8))
        footer_label.pack(side=tk.BOTTOM, pady=5)

    def select_files(self):
        filetypes = (
            ('PDF-Dateien', '*.pdf'),
            ('Word-Dateien', '*.docx'),
            ('HTML-Dateien', '*.html'),
            ('Bild-Dateien', '*.jpg *.jpeg *.png'),
            ('Alle Dateien', '*.*')
        )

        self.filenames = filedialog.askopenfilenames(
            title='Dateien zur Verarbeitung auswählen',
            initialdir=Path.home(),
            filetypes=filetypes
        )

        if self.filenames:
            self.file_listbox.delete(0, tk.END)
            for filename in self.filenames:
                file_path = Path(filename)
                file_ext = file_path.suffix.lower()[1:]
                emoji = self.file_emojis.get(file_ext, self.file_emojis["default"])
                self.file_listbox.insert(tk.END, f"{emoji} {file_path.name}")

            self.status_label.config(text=f"✅ {len(self.filenames)} Dateien ausgewählt")
            self.process_btn.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="⚠️ Keine Dateien ausgewählt")
            self.process_btn.config(state=tk.DISABLED)

    def process_files(self):
        if not self.filenames:
            messagebox.showinfo("Information", "Bitte wähle zuerst Dateien aus!")
            return

        # UI vor Verarbeitung aktualisieren
        self.process_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⏳ Verarbeitung läuft...")
        self.progress.start(10)

        # Starte Verarbeitung in einem Thread, um UI nicht zu blockieren
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()

    def run_conversion(self):
        logger_info = logging.getLogger(__name__)

        # Pipeline-Optionen konfigurieren
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        doc_converter = DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.IMAGE
            ],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                )
            },
        )

        output_dir = Path("Scratch")
        output_dir.mkdir(parents=True, exist_ok=True)

        processed_files = 0
        total_files = len(self.filenames)

        for idx, filename in enumerate(self.filenames):
            try:
                # UI-Update im Hauptthread
                self.root.after(0, lambda idx=idx, total=total_files:
                               self.status_label.config(text=f"⏳ Verarbeite Datei {idx+1}/{total}..."))

                input_doc_path = filename
                start_time = time.time()
                logger_info.info(f"Verarbeite Datei: {input_doc_path}")

                converter = doc_converter.convert(input_doc_path)
                processing_time = time.time() - start_time

                doc_filename = converter.input.file.stem

                # Export nach TXT
                with open(output_dir / f"{doc_filename}.txt", "w", encoding="utf-8") as text_file:
                    text_file.write(json.dumps(converter.document.export_to_dict()))

                logger_info.info(f"Konvertierung abgeschlossen in {processing_time:.2f} Sekunden.")
                processed_files += 1

                # Listbox-Eintrag aktualisieren
                self.root.after(0, lambda idx=idx:
                               self.file_listbox.itemconfig(idx, fg="green"))

            except Exception as e:
                logger_error.error(f"Fehler bei der Verarbeitung von {filename}: {str(e)}")
                # Listbox-Eintrag aktualisieren
                self.root.after(0, lambda idx=idx:
                               self.file_listbox.itemconfig(idx, fg="red"))

        # UI nach Verarbeitung zurücksetzen
        self.root.after(0, self.finish_processing, processed_files, total_files)

    def finish_processing(self, processed_files, total_files):
        self.progress.stop()
        if processed_files == total_files:
            self.status_label.config(text=f"✅ {processed_files} Dateien erfolgreich verarbeitet!")
            messagebox.showinfo("Erfolg", f"{processed_files} Dateien wurden erfolgreich verarbeitet und in den 'Scratch'-Ordner exportiert.")
        else:
            self.status_label.config(text=f"⚠️ {processed_files}/{total_files} Dateien verarbeitet. Einige Fehler aufgetreten.")
            messagebox.showwarning("Warnung", f"Es wurden {processed_files} von {total_files} Dateien verarbeitet. Prüfe das Log für Details zu Fehlern.")

        self.process_btn.config(state=tk.NORMAL if self.filenames else tk.DISABLED)

def main():
    root = tk.Tk()
    DoclingConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
