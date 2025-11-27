import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import json
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"
DEFAULT_CLI_NAME = "Source2Viewer-CLI.exe"

SUPPORTED_FORMATS_MAP = {
    ".vtex_c": "Textures (.vtex_c -> .png)",
    ".vsnd_c": "Sounds (.vsnd_c -> .wav)",
    ".vmdl_c": "Models (.vmdl_c -> .gltf)",
}

TARGET_EXTENSIONS = {
    ".vtex_c": ".png",
    ".vsnd_c": ".wav",
    ".vmdl_c": ".gltf",
    ".vpcf_c": ".txt",
}

TRANSLATIONS = {
    "🇬🇧 English": {
        "title": "Source 2 Universal Converter",
        "header_formats": "SELECT FILE TYPES TO CONVERT:",
        "header_paths": "PATHS CONFIGURATION:",
        "lbl_cli": "Path to Source2Viewer-CLI.exe:",
        "lbl_input": "Input Folder:",
        "lbl_output": "Output Folder:",
        "btn_browse": "Browse...",
        "btn_start": "START CONVERSION",
        "btn_start_working": "PROCESSING...",
        "log_start": "--- Ready. Select formats and paths. ---",
        "log_searching": "Searching for files...",
        "log_not_found": "No matching files found!",
        "log_done": "Done! Processed: {}/{} files.",
        "err_no_cli": "CLI tool missing!",
        "err_no_input": "Select Input Folder.",
        "err_no_formats": "Select at least one format!",
        "msg_done": "Finished!",
        "status_ready": "Ready",
        "help_title": "Help",
        "help_text": "1. Select Source2Viewer-CLI.exe\n2. Select Input/Output folders\n3. Choose formats\n4. Click START"
    },
    "🇺🇦 Українська": {
        "title": "Універсальний Конвертер Source 2",
        "header_formats": "ОБЕРІТЬ ТИПИ ФАЙЛІВ:",
        "header_paths": "НАЛАШТУВАННЯ ШЛЯХІВ:",
        "lbl_cli": "Шлях до Source2Viewer-CLI.exe:",
        "lbl_input": "Вхідна папка:",
        "lbl_output": "Вихідна папка:",
        "btn_browse": "Огляд...",
        "btn_start": "ПОЧАТИ КОНВЕРТАЦІЮ",
        "btn_start_working": "ОБРОБКА...",
        "log_start": "--- Готовий. Оберіть формати та шляхи. ---",
        "log_searching": "Пошук файлів...",
        "log_not_found": "Файлів не знайдено!",
        "log_done": "Готово! Оброблено: {}/{} файлів.",
        "err_no_cli": "Інструмент CLI відсутній!",
        "err_no_input": "Оберіть вхідну папку.",
        "err_no_formats": "Оберіть хоча б один формат!",
        "msg_done": "Завершено!",
        "status_ready": "Готово",
        "help_title": "Допомога",
        "help_text": "1. Оберіть Source2Viewer-CLI.exe\n2. Вкажіть вхідну/вихідну папки\n3. Поставте галочки на форматах\n4. Тисніть ПОЧАТИ"
    },
    "🇵🇱 Polski": {
        "title": "Uniwersalny Konwerter Source 2",
        "header_formats": "WYBIERZ TYPY PLIKÓW:",
        "header_paths": "KONFIGURACJA ŚCIEŻEK:",
        "lbl_cli": "Ścieżka do Source2Viewer-CLI.exe:",
        "lbl_input": "Folder wejściowy:",
        "lbl_output": "Folder wyjściowy:",
        "btn_browse": "Przeglądaj...",
        "btn_start": "ROZPOCZNIJ",
        "btn_start_working": "PRZETWARZANIE...",
        "log_start": "--- Gotowy. Wybierz formaty i ścieżki. ---",
        "log_searching": "Szukanie plików...",
        "log_not_found": "Nie znaleziono plików!",
        "log_done": "Gotowe! Przetworzono: {}/{}",
        "err_no_cli": "Brak narzędzia CLI!",
        "err_no_input": "Wybierz folder wejściowy.",
        "err_no_formats": "Wybierz co najmniej jeden format!",
        "msg_done": "Zakończono!",
        "status_ready": "Gotowy",
        "help_title": "Pomoc",
        "help_text": "1. Wybierz Source2Viewer-CLI.exe\n2. Wybierz foldery\n3. Zaznacz formaty\n4. Kliknij START"
    },
    "🇫🇷 Français": {
        "title": "Convertisseur Universel Source 2",
        "header_formats": "TYPES DE FICHIERS :",
        "header_paths": "CHEMINS :",
        "lbl_cli": "Chemin vers Source2Viewer-CLI.exe :",
        "lbl_input": "Dossier d'entrée :",
        "lbl_output": "Dossier de sortie :",
        "btn_browse": "Parcourir...",
        "btn_start": "DÉMARRER",
        "btn_start_working": "TRAITEMENT...",
        "log_start": "--- Prêt. Sélectionnez les formats. ---",
        "log_searching": "Recherche de fichiers...",
        "log_not_found": "Aucun fichier trouvé !",
        "log_done": "Terminé ! Traité : {}/{}",
        "err_no_cli": "Outil CLI manquant !",
        "err_no_input": "Sélectionnez le dossier d'entrée.",
        "err_no_formats": "Sélectionnez un format !",
        "msg_done": "Terminé !",
        "status_ready": "Prêt",
        "help_title": "Aide",
        "help_text": "1. Sélectionnez Source2Viewer-CLI.exe\n2. Choisissez les dossiers\n3. Cochez les formats\n4. Cliquez sur DÉMARRER"
    },
    "🇪🇸 Español": {
        "title": "Conversor Universal Source 2",
        "header_formats": "TIPOS DE ARCHIVO:",
        "header_paths": "RUTAS:",
        "lbl_cli": "Ruta a Source2Viewer-CLI.exe:",
        "lbl_input": "Carpeta de entrada:",
        "lbl_output": "Carpeta de salida:",
        "btn_browse": "Examinar...",
        "btn_start": "INICIAR",
        "btn_start_working": "PROCESANDO...",
        "log_start": "--- Listo. Seleccione formatos. ---",
        "log_searching": "Buscando archivos...",
        "log_not_found": "¡No se encontraron archivos!",
        "log_done": "¡Hecho! Procesado: {}/{}",
        "err_no_cli": "¡Falta herramienta CLI!",
        "err_no_input": "Seleccione carpeta de entrada.",
        "err_no_formats": "¡Seleccione un formato!",
        "msg_done": "¡Finalizado!",
        "status_ready": "Listo",
        "help_title": "Ayuda",
        "help_text": "1. Seleccione Source2Viewer-CLI.exe\n2. Elija carpetas\n3. Marque formatos\n4. Clic en INICIAR"
    },
    "🇩🇪 Deutsch": {
        "title": "Universeller Source 2 Konverter",
        "header_formats": "DATEITYPEN WÄHLEN:",
        "header_paths": "PFADE KONFIGURIEREN:",
        "lbl_cli": "Pfad zu Source2Viewer-CLI.exe:",
        "lbl_input": "Eingabeordner:",
        "lbl_output": "Ausgabeordner:",
        "btn_browse": "Durchsuchen...",
        "btn_start": "STARTEN",
        "btn_start_working": "VERARBEITUNG...",
        "log_start": "--- Bereit. Formate wählen. ---",
        "log_searching": "Suche nach Dateien...",
        "log_not_found": "Keine Dateien gefunden!",
        "log_done": "Fertig! Verarbeitet: {}/{}",
        "err_no_cli": "CLI-Tool fehlt!",
        "err_no_input": "Eingabeordner wählen.",
        "err_no_formats": "Mindestens ein Format wählen!",
        "msg_done": "Abgeschlossen!",
        "status_ready": "Bereit",
        "help_title": "Hilfe",
        "help_text": "1. Wähle Source2Viewer-CLI.exe\n2. Wähle Ordner\n3. Formate ankreuzen\n4. Klicke STARTEN"
    }
}

class ConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config = self.load_config()
        current_theme = self.config.get("theme", "System")
        ctk.set_appearance_mode(current_theme)

        self.title("Source 2 Converter Pro")
        self.geometry("750x650")

        if os.path.exists("icon.ico"):
            self.iconbitmap("icon.ico")
        
        loaded_lang = self.config.get("language", "🇬🇧 English")
        if loaded_lang in TRANSLATIONS:
            self.current_lang = loaded_lang
        else:
            self.current_lang = "🇬🇧 English"
        
        self.path_cli = ctk.StringVar(value=self.config.get("cli_path", ""))
        self.path_in = ctk.StringVar(value=self.config.get("input_path", ""))
        self.path_out = ctk.StringVar(value=self.config.get("output_path", ""))
        
        self.format_vars = {}
        saved_formats = self.config.get("selected_formats", {})
        for ext in SUPPORTED_FORMATS_MAP.keys():
            is_checked = saved_formats.get(ext, True) 
            self.format_vars[ext] = ctk.BooleanVar(value=is_checked)

        if not self.path_cli.get():
            self.auto_detect_cli()

        self.setup_ui()
        self.update_texts()

    def auto_detect_cli(self):
        if getattr(sys, 'frozen', False): base_path = os.path.dirname(sys.executable)
        else: base_path = os.path.dirname(os.path.abspath(__file__))
        potential_path = os.path.join(base_path, DEFAULT_CLI_NAME)
        if os.path.exists(potential_path): self.path_cli.set(potential_path)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        
        self.switch_theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        self.switch_theme = ctk.CTkSwitch(top_frame, text="Dark Mode", command=self.toggle_theme,
                                          variable=self.switch_theme_var, onvalue="Dark", offvalue="Light")
        self.switch_theme.pack(side="left")
        
        self.lang_combo = ctk.CTkComboBox(top_frame, values=list(TRANSLATIONS.keys()), 
                                          command=self.change_language, width=160)
        self.lang_combo.set(self.current_lang)
        self.lang_combo.pack(side="right")
        
        self.btn_help = ctk.CTkButton(top_frame, text="?", width=40, height=30, command=self.show_help)
        self.btn_help.pack(side="right", padx=10)

        self.fmt_frame = ctk.CTkFrame(self)
        self.fmt_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.lbl_header_fmt = ctk.CTkLabel(self.fmt_frame, text="FORMATS", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_header_fmt.pack(anchor="w", padx=15, pady=(10, 5))
        
        checkbox_container = ctk.CTkFrame(self.fmt_frame, fg_color="transparent")
        checkbox_container.pack(fill="x", padx=15, pady=(0, 10))
        
        for i, (ext, text) in enumerate(SUPPORTED_FORMATS_MAP.items()):
            cb = ctk.CTkCheckBox(checkbox_container, text=text, variable=self.format_vars[ext], command=self.save_config)
            cb.grid(row=0, column=i, padx=(0, 15), sticky="w")

        self.paths_frame = ctk.CTkFrame(self)
        self.paths_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        self.lbl_header_paths = ctk.CTkLabel(self.paths_frame, text="PATHS", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_header_paths.pack(anchor="w", padx=15, pady=(10, 5))

        def create_path_row(parent, label_attr, entry_var, btn_attr, browse_cmd):
            fr = ctk.CTkFrame(parent, fg_color="transparent")
            fr.pack(fill="x", padx=15, pady=(5, 0))
            lbl = ctk.CTkLabel(fr, text="Label", anchor="w", width=180)
            lbl.pack(side="left")
            setattr(self, label_attr, lbl)
            entry = ctk.CTkEntry(fr, textvariable=entry_var, height=35)
            entry.pack(side="left", fill="x", expand=True, padx=10)
            btn = ctk.CTkButton(fr, text="...", width=60, height=35, command=browse_cmd)
            btn.pack(side="right")
            setattr(self, btn_attr, btn)

        create_path_row(self.paths_frame, "lbl_cli", self.path_cli, "btn_browse_cli", lambda: self.browse_file(self.path_cli))
        create_path_row(self.paths_frame, "lbl_input", self.path_in, "btn_browse_in", lambda: self.browse_folder(self.path_in, True))
        create_path_row(self.paths_frame, "lbl_output", self.path_out, "btn_browse_out", lambda: self.browse_folder(self.path_out))
        
        ctk.CTkLabel(self.paths_frame, text="", height=10).pack()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(10, 20))
        bottom_frame.grid_rowconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.btn_start = ctk.CTkButton(bottom_frame, text="START", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.start_thread)
        self.btn_start.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.log_area = ctk.CTkTextbox(bottom_frame, state='disabled', font=ctk.CTkFont(family="Consolas", size=12))
        self.log_area.grid(row=1, column=0, sticky="nsew")

    def update_texts(self):
        t = TRANSLATIONS[self.current_lang]
        self.title(t["title"])
        self.lbl_header_fmt.configure(text=t["header_formats"])
        self.lbl_header_paths.configure(text=t["header_paths"])
        self.lbl_cli.configure(text=t["lbl_cli"])
        self.lbl_input.configure(text=t["lbl_input"])
        self.lbl_output.configure(text=t["lbl_output"])
        self.btn_browse_cli.configure(text=t["btn_browse"])
        self.btn_browse_in.configure(text=t["btn_browse"])
        self.btn_browse_out.configure(text=t["btn_browse"])
        self.btn_start.configure(text=t["btn_start"])
        
        current_mode = ctk.get_appearance_mode()
        self.switch_theme.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")
        
        self.log_clear()
        self.log(t["log_start"])

    def toggle_theme(self):
        new_mode = self.switch_theme_var.get()
        ctk.set_appearance_mode(new_mode)
        self.update_texts()
        self.save_config()

    def change_language(self, choice):
        self.current_lang = choice
        self.save_config()
        self.update_texts()

    def show_help(self):
        t = TRANSLATIONS[self.current_lang]
        help_window = ctk.CTkToplevel(self)
        help_window.title(t["help_title"])
        help_window.geometry("400x300")
        help_window.attributes("-topmost", True)
        
        help_window.grab_set()
        
        textbox = ctk.CTkTextbox(help_window, font=ctk.CTkFont(size=14))
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        textbox.insert("0.0", t["help_text"])
        textbox.configure(state="disabled")

    def browse_file(self, var):
        f = filedialog.askopenfilename(filetypes=[("Executables", "*.exe")])
        if f: 
            var.set(f)
            self.save_config()

    def browse_folder(self, var, auto_set_output=False):
        d = filedialog.askdirectory()
        if d: 
            var.set(d)
            if auto_set_output and not self.path_out.get():
                self.path_out.set(os.path.join(d, "converted_files"))
            self.save_config()

    def log(self, msg):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')
        
    def log_clear(self):
        self.log_area.configure(state='normal')
        self.log_area.delete("0.0", tk.END)
        self.log_area.configure(state='disabled')

    def start_thread(self):
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        t = TRANSLATIONS[self.current_lang]
        cli = self.path_cli.get()
        inp = self.path_in.get()
        outp = self.path_out.get()

        if not os.path.exists(cli):
            messagebox.showerror("Error", t["err_no_cli"])
            return
        if not os.path.exists(inp):
            messagebox.showerror("Error", t["err_no_input"])
            return
            
        active_extensions = []
        for ext, var in self.format_vars.items():
            if var.get():
                active_extensions.append(ext)
                
        if not active_extensions:
             messagebox.showwarning("Warning", t["err_no_formats"])
             return

        self.btn_start.configure(state='disabled', text=t["btn_start_working"])
        self.log("-" * 30)
        self.log(t["log_searching"])

        files_to_process = []
        for r, d, f in os.walk(inp):
            for file in f:
                for ext in active_extensions:
                    if file.endswith(ext):
                        files_to_process.append((os.path.join(r, file), ext))
                        break

        if not files_to_process:
            self.log(t["log_not_found"])
            self.btn_start.configure(state='normal', text=t["btn_start"])
            return

        os.makedirs(outp, exist_ok=True)
        count = 0
        
        for i, (fpath, ext) in enumerate(files_to_process):
            fname = os.path.basename(fpath)
            name_only = os.path.splitext(fname)[0]
            target_ext = TARGET_EXTENSIONS[ext]
            final_out = os.path.join(outp, name_only + target_ext)

            try:
                creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                subprocess.run(
                    [cli, "-i", fpath, "-o", final_out], 
                    check=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL,
                    creationflags=creation_flags
                )
                self.log(f"[{i+1}/{len(files_to_process)}] OK: {fname}")
                count += 1
            except Exception as e:
                self.log(f"[ERR] {fname}: {e}")

        self.log("-" * 30)
        self.log(t["log_done"].format(count, len(files_to_process)))
        messagebox.showinfo("Success", t["msg_done"])
        self.btn_start.configure(state='normal', text=t["btn_start"])

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f)
            except: pass
        return {}

    def save_config(self, event=None):
        selected_formats_state = {ext: var.get() for ext, var in self.format_vars.items()}
        data = {
            "theme": ctk.get_appearance_mode(),
            "language": self.current_lang,
            "cli_path": self.path_cli.get(),
            "input_path": self.path_in.get(),
            "output_path": self.path_out.get(),
            "selected_formats": selected_formats_state
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()