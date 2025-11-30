import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import json
import sys
import concurrent.futures

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
        "title": "Source 2 Batch Commander (Structure Saver)",
        "header_fmt": "1. SETTINGS & FORMATS:",
        "header_in": "2. INPUT FOLDERS:",
        "header_out": "3. OUTPUT DESTINATION:",
        "lbl_cli": "CLI Tool Path:",
        "chk_recursive": "Scan Subfolders (Keep Structure)",
        "chk_skip": "Skip Existing Files",
        "btn_add": "+ Add Folder",
        "btn_clear": "Clear All",
        "btn_browse": "Browse...",
        "btn_open": "Open Folder",
        "btn_start": "START CONVERSION",
        "btn_working": "PROCESSING...",
        "log_ready": "--- Ready. ---",
        "log_start_folder": ">>> Processing: {}",
        "log_skip_exists": "   [SKIP] Exists: {}",
        "log_done": "COMPLETED! Processed: {}. Skipped: {}. Errors: {}.",
        "msg_done": "Done!",
        "err_cli": "CLI Tool not found!",
        "err_no_in": "List is empty!",
        "err_no_out": "Select Output Folder."
    },
    "🇺🇦 Українська": {
        "title": "Source 2 Batch Commander (Збереження структури)",
        "header_fmt": "1. НАЛАШТУВАННЯ ТА ФОРМАТИ:",
        "header_in": "2. СПИСОК ПАПОК:",
        "header_out": "3. КУДИ ЗБЕРІГАТИ:",
        "lbl_cli": "Шлях до CLI:",
        "chk_recursive": "Сканувати підпапки (Структура)",
        "chk_skip": "Пропускати існуючі",
        "btn_add": "+ Додати папку",
        "btn_clear": "Очистити все",
        "btn_browse": "Огляд...",
        "btn_open": "Відкрити папку",
        "btn_start": "ПОЧАТИ ОБРОБКУ",
        "btn_working": "ОБРОБКА...",
        "log_ready": "--- Готовий. ---",
        "log_start_folder": ">>> Обробка: {}",
        "log_skip_exists": "   [SKIP] Вже є: {}",
        "log_done": "ЗАВЕРШЕНО! Оброблено: {}. Пропущено: {}. Помилок: {}.",
        "msg_done": "Готово!",
        "err_cli": "CLI не знайдено!",
        "err_no_in": "Список пустий!",
        "err_no_out": "Оберіть папку виводу."
    },
    "🇵🇱 Polski": {
        "title": "Source 2 Batch Commander",
        "header_fmt": "1. USTAWIENIA:",
        "header_in": "2. LISTA FOLDERÓW:",
        "header_out": "3. MIEJSCE DOCELOWE:",
        "lbl_cli": "Ścieżka CLI:",
        "chk_recursive": "Skanuj podfoldery",
        "chk_skip": "Pomiń istniejące",
        "btn_add": "+ Dodaj folder",
        "btn_clear": "Wyczyść",
        "btn_browse": "Przeglądaj...",
        "btn_open": "Otwórz folder",
        "btn_start": "ROZPOCZNIJ",
        "btn_working": "PRZETWARZANIE...",
        "log_ready": "--- Gotowy. ---",
        "log_start_folder": ">>> Przetwarzanie: {}",
        "log_skip_exists": "   [SKIP] Istnieje: {}",
        "log_done": "ZAKOŃCZONO! Przetworzono: {}. Pominięto: {}. Błędy: {}.",
        "msg_done": "Gotowe!",
        "err_cli": "Nie znaleziono CLI!",
        "err_no_in": "Lista pusta!",
        "err_no_out": "Wybierz folder wyjściowy."
    },
    "🇫🇷 Français": {
        "title": "Source 2 Batch Commander",
        "header_fmt": "1. PARAMÈTRES :",
        "header_in": "2. DOSSIERS :",
        "header_out": "3. DESTINATION :",
        "lbl_cli": "Chemin CLI :",
        "chk_recursive": "Sous-dossiers",
        "chk_skip": "Ignorer les existants",
        "btn_add": "+ Ajouter",
        "btn_clear": "Effacer",
        "btn_browse": "Parcourir...",
        "btn_open": "Ouvrir",
        "btn_start": "COMMENCER",
        "btn_working": "TRAITEMENT...",
        "log_ready": "--- Prêt. ---",
        "log_start_folder": ">>> Traitement : {}",
        "log_skip_exists": "   [SKIP] Existe : {}",
        "log_done": "TERMINÉ ! Traité : {}. Ignoré : {}. Erreurs : {}.",
        "msg_done": "Terminé !",
        "err_cli": "CLI introuvable !",
        "err_no_in": "Liste vide !",
        "err_no_out": "Sélectionnez la sortie."
    },
    "🇪🇸 Español": {
        "title": "Source 2 Batch Commander",
        "header_fmt": "1. AJUSTES:",
        "header_in": "2. CARPETAS:",
        "header_out": "3. DESTINO:",
        "lbl_cli": "Ruta CLI:",
        "chk_recursive": "Subcarpetas",
        "chk_skip": "Omitir existentes",
        "btn_add": "+ Añadir",
        "btn_clear": "Limpiar",
        "btn_browse": "Examinar...",
        "btn_open": "Abrir",
        "btn_start": "INICIAR",
        "btn_working": "PROCESANDO...",
        "log_ready": "--- Listo. ---",
        "log_start_folder": ">>> Procesando: {}",
        "log_skip_exists": "   [SKIP] Existe: {}",
        "log_done": "¡HECHO! Procesado: {}. Omitido: {}. Errores: {}.",
        "msg_done": "¡Hecho!",
        "err_cli": "¡Falta CLI!",
        "err_no_in": "¡Lista vacía!",
        "err_no_out": "Seleccione salida."
    },
    "🇩🇪 Deutsch": {
        "title": "Source 2 Batch Commander",
        "header_fmt": "1. EINSTELLUNGEN:",
        "header_in": "2. ORDNER:",
        "header_out": "3. ZIEL:",
        "lbl_cli": "CLI-Pfad:",
        "chk_recursive": "Unterordner",
        "chk_skip": "Existierende überspringen",
        "btn_add": "+ Hinzufügen",
        "btn_clear": "Leeren",
        "btn_browse": "Durchsuchen...",
        "btn_open": "Öffnen",
        "btn_start": "STARTEN",
        "btn_working": "VERARBEITUNG...",
        "log_ready": "--- Bereit. ---",
        "log_start_folder": ">>> Verarbeite: {}",
        "log_skip_exists": "   [SKIP] Existiert: {}",
        "log_done": "FERTIG! Verarbeitet: {}. Übersprungen: {}. Fehler: {}.",
        "msg_done": "Fertig!",
        "err_cli": "CLI fehlt!",
        "err_no_in": "Liste leer!",
        "err_no_out": "Ziel wählen."
    }
}

def get_text(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["🇬🇧 English"]).get(key, key)

class ConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config = self.load_config()
        saved_lang = self.config.get("language", "🇬🇧 English")
        self.current_lang = saved_lang if saved_lang in TRANSLATIONS else "🇬🇧 English"
        
        ctk.set_appearance_mode(self.config.get("theme", "System"))
        
        self.title("Source 2 Batch Commander")
        self.geometry("800x800")
        
        if os.path.exists("icon.ico"): self.iconbitmap("icon.ico")

        self.path_cli = ctk.StringVar(value=self.config.get("cli_path", ""))
        self.path_out = ctk.StringVar(value=self.config.get("output_path", ""))
        self.input_folders_list = self.config.get("input_folders_list", [])
        
        self.last_input = self.config.get("last_input", "/")
        self.last_output = self.config.get("last_output", "/")
        
        self.is_recursive = ctk.BooleanVar(value=self.config.get("recursive_scan", True))
        self.is_skip_existing = ctk.BooleanVar(value=self.config.get("skip_existing", False))
        
        self.format_vars = {}
        saved_formats = self.config.get("selected_formats", {})
        for ext in SUPPORTED_FORMATS_MAP.keys():
            self.format_vars[ext] = ctk.BooleanVar(value=saved_formats.get(ext, True))

        if not self.path_cli.get(): self.auto_detect_cli()
        
        self.setup_ui()
        self.refresh_folder_list_ui() 
        self.update_texts()

    def auto_detect_cli(self):
        base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        pot = os.path.join(base, DEFAULT_CLI_NAME)
        if os.path.exists(pot): self.path_cli.set(pot)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, sticky="ew", padx=20, pady=5)
        self.theme_sw = ctk.CTkSwitch(top, text="Mode", command=self.toggle_theme)
        self.theme_sw.pack(side="left")
        self.lang_cb = ctk.CTkComboBox(top, values=list(TRANSLATIONS.keys()), command=self.change_lang, width=140)
        self.lang_cb.set(self.current_lang)
        self.lang_cb.pack(side="right")

        cfg_fr = ctk.CTkFrame(self, fg_color="transparent")
        cfg_fr.grid(row=1, sticky="ew", padx=20, pady=5)
        
        cli_row = ctk.CTkFrame(cfg_fr, fg_color="transparent")
        cli_row.pack(fill="x", padx=10, pady=5)
        self.lbl_cli = ctk.CTkLabel(cli_row, text="CLI Path:", width=100, anchor="w")
        self.lbl_cli.pack(side="left")
        ctk.CTkEntry(cli_row, textvariable=self.path_cli).pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(cli_row, text="...", width=40, command=self.browse_cli).pack(side="right")

        self.lbl_fmt = ctk.CTkLabel(cfg_fr, text="FORMATS:", font=("Arial", 12, "bold"))
        self.lbl_fmt.pack(anchor="w", padx=10)
        
        opt_box = ctk.CTkFrame(cfg_fr)
        opt_box.pack(fill="x", padx=10, pady=(0, 10))
        
        for i, (ext, txt) in enumerate(SUPPORTED_FORMATS_MAP.items()):
            ctk.CTkCheckBox(opt_box, text=txt, variable=self.format_vars[ext], command=self.save_config).pack(side="left", padx=(10, 15), pady=10)
        
        ctk.CTkFrame(opt_box, width=2, height=20, fg_color="gray").pack(side="left", padx=5)
        
        self.chk_recursive = ctk.CTkCheckBox(opt_box, text="Scan Subfolders", variable=self.is_recursive, command=self.save_config, fg_color="#E0A800", hover_color="#C09000")
        self.chk_recursive.pack(side="left", padx=(10, 5), pady=10)
        self.chk_skip = ctk.CTkCheckBox(opt_box, text="Skip Existing", variable=self.is_skip_existing, command=self.save_config, fg_color="#00A2E8", hover_color="#007ACC")
        self.chk_skip.pack(side="left", padx=5, pady=10)

        in_fr = ctk.CTkFrame(self)
        in_fr.grid(row=2, sticky="nsew", padx=20, pady=5)
        head_row = ctk.CTkFrame(in_fr, fg_color="transparent")
        head_row.pack(fill="x", padx=10, pady=5)
        self.lbl_in = ctk.CTkLabel(head_row, text="INPUT LIST:", font=("Arial", 12, "bold"))
        self.lbl_in.pack(side="left")
        self.btn_add = ctk.CTkButton(head_row, text="+ Add", width=100, command=self.add_folder, fg_color="#2CC985", hover_color="#229965")
        self.btn_add.pack(side="right", padx=5)
        self.btn_clear = ctk.CTkButton(head_row, text="Clear", width=80, command=self.clear_list, fg_color="#C92C2C", hover_color="#992222")
        self.btn_clear.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(in_fr, height=150, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        out_fr = ctk.CTkFrame(self)
        out_fr.grid(row=3, sticky="ew", padx=20, pady=5)
        self.lbl_out = ctk.CTkLabel(out_fr, text="OUTPUT:", font=("Arial", 12, "bold"))
        self.lbl_out.pack(anchor="w", padx=10, pady=(5,0))
        out_row = ctk.CTkFrame(out_fr, fg_color="transparent")
        out_row.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkEntry(out_row, textvariable=self.path_out).pack(side="left", fill="x", expand=True)
        self.btn_out_browse = ctk.CTkButton(out_row, text="...", width=50, command=self.browse_out)
        self.btn_out_browse.pack(side="left", padx=5)
        self.btn_open_out = ctk.CTkButton(out_row, text="Open Folder", width=100, command=self.open_output_folder)
        self.btn_open_out.pack(side="left")

        bot = ctk.CTkFrame(self, fg_color="transparent")
        bot.grid(row=4, sticky="nsew", padx=20, pady=10)
        bot.rowconfigure(1, weight=1)
        bot.columnconfigure(0, weight=1)
        self.btn_start = ctk.CTkButton(bot, height=50, font=("Arial", 16, "bold"), command=self.start_thread)
        self.btn_start.grid(row=0, sticky="ew", pady=(0, 10))
        self.log_txt = ctk.CTkTextbox(bot, font=("Consolas", 11), state='disabled')
        self.log_txt.grid(row=1, sticky="nsew")

    def refresh_folder_list_ui(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        if not self.input_folders_list:
            ctk.CTkLabel(self.scroll_frame, text="(List is empty)", text_color="gray").pack(pady=10)
        else:
            for folder in self.input_folders_list:
                row = ctk.CTkFrame(self.scroll_frame)
                row.pack(fill="x", pady=2, padx=5)
                ctk.CTkLabel(row, text="📂", width=30).pack(side="left")
                ctk.CTkLabel(row, text=folder, anchor="w").pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkButton(row, text="✕", width=30, height=30, fg_color="#C92C2C", hover_color="#992222",
                              command=lambda f=folder: self.remove_folder(f)).pack(side="right", padx=5)

    def remove_folder(self, folder_path):
        if folder_path in self.input_folders_list:
            self.input_folders_list.remove(folder_path)
            self.save_config()
            self.refresh_folder_list_ui()

    def add_folder(self):
        d = filedialog.askdirectory(initialdir=self.last_input)
        if d:
            if d not in self.input_folders_list:
                self.input_folders_list.append(d)
                self.last_input = d
                self.save_config()
                self.refresh_folder_list_ui()

    def clear_list(self):
        self.input_folders_list = []
        self.save_config()
        self.refresh_folder_list_ui()

    def update_texts(self):
        t = lambda k: get_text(self.current_lang, k)
        self.lbl_fmt.configure(text=t("header_fmt"))
        self.lbl_in.configure(text=t("header_in"))
        self.lbl_out.configure(text=t("header_out"))
        self.lbl_cli.configure(text=t("lbl_cli"))
        self.chk_recursive.configure(text=t("chk_recursive"))
        self.chk_skip.configure(text=t("chk_skip"))
        self.btn_add.configure(text=t("btn_add"))
        self.btn_clear.configure(text=t("btn_clear"))
        self.btn_out_browse.configure(text=t("btn_browse"))
        self.btn_open_out.configure(text=t("btn_open"))
        self.btn_start.configure(text=t("btn_start"))
        self.log(t("log_ready"))

    def browse_cli(self):
        f = filedialog.askopenfilename(filetypes=[("EXE", "*.exe")])
        if f: self.path_cli.set(f); self.save_config()

    def browse_out(self):
        d = filedialog.askdirectory(initialdir=self.last_output)
        if d: self.path_out.set(d); self.last_output = d; self.save_config()

    def open_output_folder(self):
        path = self.path_out.get()
        if os.path.exists(path): os.startfile(path)
        else: messagebox.showerror("Error", "Folder not found.")

    def log(self, msg):
        self.log_txt.configure(state='normal')
        self.log_txt.insert(tk.END, msg + "\n")
        self.log_txt.see(tk.END)
        self.log_txt.configure(state='disabled')

    def toggle_theme(self):
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode()=="Dark" else "Dark")
        self.save_config()

    def change_lang(self, val):
        self.current_lang = val
        self.save_config()
        self.update_texts()

    def start_thread(self):
        threading.Thread(target=self.run_process, daemon=True).start()

    def convert_single(self, args):
        cli, fin, fout = args
        try:
            os.makedirs(os.path.dirname(fout), exist_ok=True)
            
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            res = subprocess.run([cli, "-i", fin, "-o", fout], capture_output=True, text=True, creationflags=flags)
            if res.returncode == 0: return True, os.path.basename(fin)
            else: return False, f"{os.path.basename(fin)} -> {res.stderr.strip() or res.stdout.strip() or 'Unknown'}"
        except Exception as e: return False, f"{os.path.basename(fin)}: {str(e)}"

    def run_process(self):
        t = lambda k: get_text(self.current_lang, k)
        cli = self.path_cli.get()
        out_root = self.path_out.get()
        folders = self.input_folders_list
        recursive = self.is_recursive.get()
        skip_existing = self.is_skip_existing.get()

        if not os.path.exists(cli): return messagebox.showerror("Err", t("err_cli"))
        if not folders: return messagebox.showerror("Err", t("err_no_in"))
        if not out_root: return messagebox.showerror("Err", t("err_no_out"))

        self.btn_start.configure(state='disabled', text=t("btn_working"))
        self.log("-" * 30)

        total_success = 0
        total_skipped = 0
        total_errors = 0
        exts = [e for e, v in self.format_vars.items() if v.get()]

        for idx, folder_path in enumerate(folders):
            if not os.path.exists(folder_path):
                self.log(f"[SKIP] Missing: {folder_path}")
                self.remove_folder(folder_path)
                continue

            folder_name = os.path.basename(folder_path.rstrip(os.sep))

            base_output_dir = os.path.join(out_root, folder_name)
            
            self.log(t("log_start_folder").format(folder_name))
            
            tasks = []
            for r, d, f in os.walk(folder_path):
                if not recursive: d.clear()

                rel_path = os.path.relpath(r, folder_path)
                
                current_out_dir = os.path.join(base_output_dir, rel_path)
                
                for file in f:
                    for ext in exts:
                        if file.endswith(ext):
                            fin = os.path.join(r, file)
                            name = os.path.splitext(file)[0] + TARGET_EXTENSIONS[ext]
                            
                            fout = os.path.join(current_out_dir, name)
                            
                            if skip_existing and os.path.exists(fout):
                                total_skipped += 1
                                continue
                                
                            tasks.append((cli, fin, fout))
                            break
            
            if not tasks:
                if total_skipped == 0: self.log("   -> No new files.")
                continue

            max_workers = min(32, (os.cpu_count() or 4) + 4)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self.convert_single, task) for task in tasks]
                for future in concurrent.futures.as_completed(futures):
                    ok, msg = future.result()
                    if ok: total_success += 1
                    else: 
                        total_errors += 1
                        self.log(f"   [ERR] {msg}")
            
            self.log(f"   -> Processed: {len(tasks)}")

        self.log("=" * 30)
        self.log(t("log_done").format(total_success, total_skipped, total_errors))
        messagebox.showinfo("Done", t("msg_done"))
        self.btn_start.configure(state='normal', text=t("btn_start"))

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f)
            except: pass
        return {}

    def save_config(self, event=None):
        data = {
            "theme": ctk.get_appearance_mode(),
            "language": self.current_lang,
            "cli_path": self.path_cli.get(),
            "output_path": self.path_out.get(),
            "input_folders_list": self.input_folders_list,
            "last_input": self.last_input,
            "last_output": self.last_output,
            "recursive_scan": self.is_recursive.get(),
            "skip_existing": self.is_skip_existing.get(),
            "selected_formats": {k: v.get() for k,v in self.format_vars.items()}
        }
        with open(CONFIG_FILE, "w") as f: json.dump(data, f, indent=4)

if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()