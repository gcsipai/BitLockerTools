import subprocess
import re
import sys
import os
from threading import Thread
import platform
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
# >>> CustomTkinter importálása
import customtkinter as ctk

# A célezni kívánt meghajtó alapértelmezett értéke
DEFAULT_DRIVE = "C:"

# Színkonstansok a naplózáshoz (A CTk színeihez igazítva)
COLOR_SUCCESS = ctk.ThemeManager.theme["CTkButton"]["fg_color"][0]
COLOR_WARNING = "#FF8C00"
COLOR_ERROR = "#DC3545"
COLOR_INFO = "#1E90FF"
COLOR_DEFAULT = "black"


# ----------------------------------------------------------------------
# SEGÉDFÜGGVÉNYEK ÉS LOGIKA
# ----------------------------------------------------------------------

def is_windows():
    return platform.system() == "Windows"


def is_admin():
    if not is_windows(): return False
    try:
        # Ellenőrzés, hogy a szkript admin joggal fut-e
        os.listdir(os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32\\config'))
        return True
    except PermissionError:
        return False
    except Exception:
        return False


def check_drive_validity(drive_letter: str) -> bool:
    if not re.match(r"^[A-Za-z]:$", drive_letter):
        return False
    return os.path.exists(drive_letter + os.sep)


def futtat_parancsot(parancs: str, emelt_jogot_igenyel: bool):
    """
    Parancs futtatása a Python subprocess modulján keresztül (shell=False)
    a teljes elérési útvonal használatával a legnagyobb megbízhatóság érdekében.
    """
    if not is_windows():
        return None, "❌ Hiba: A BitLocker parancsok csak Windows operációs rendszeren futtathatók."

    if emelt_jogot_igenyel and not is_admin():
        return None, "❌ A művelethez RENDSZERGAZDAI JOGOSULTSÁG szükséges! Futtassa a programot emelt joggal."

    # Készítjük a parancs listáját a subprocess.run számára
    system32_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')
    manage_bde_path = os.path.join(system32_path, 'manage-bde.exe')

    # A parancs szétválasztása listára.
    parancs_lista = parancs.split()
    # manage-bde lecserélése a teljes útvonalra a shell=False futtatáshoz
    try:
        if parancs_lista[0].lower() == 'manage-bde':
            parancs_lista[0] = manage_bde_path
    except IndexError:
        return None, "❌ HIBA: Üres parancsot próbált futtatni."

    try:
        # Futtatás shell=False beállítással (a legmegbízhatóbb módszer)
        eredmeny = subprocess.run(
            parancs_lista,
            capture_output=True,
            text=True,
            encoding='cp852',
            check=True,
            shell=False
        )
        return eredmeny.stdout.strip(), None
    except FileNotFoundError:
        # Ez a hiba jelzi, hogy a manage-bde.exe valóban hiányzik a System32 mappából.
        return None, (
            "❌ Hiba: A 'manage-bde' eszköz nem található a rendszerén.\n\n"
            "⚠️ Ez a program csak a Windows 10/11 alábbi kiadásaival kompatibilis:\n"
            "   - **Professional** (Pro)\n"
            "   - **Enterprise**\n"
            "   - **Education**\n\n"
            "Kérjük, ellenőrizze, hogy a Windows kiadása támogatja-e a BitLockert!"
        )
    except subprocess.CalledProcessError as e:
        hiba_kimenet = e.stderr.strip() or e.stdout.strip()
        return None, f"❌ Hiba történt a BitLocker parancs futtatása során:\n{hiba_kimenet}"
    except Exception as e:
        return None, f"❌ Ismeretlen futási hiba: {e}"


# --- BitLocker Műveletek (manage-bde parancsok) ---
def get_status(meghajto_betu: str):
    parancs = f'manage-bde -status {meghajto_betu}'
    return futtat_parancsot(parancs, emelt_jogot_igenyel=False)


def export_recovery_key(meghajto_betu: str, fajl_eleresi_ut: str):
    parancs = f'manage-bde -protectors -get {meghajto_betu}'
    kimenet, hiba = futtat_parancsot(parancs, emelt_jogot_igenyel=False)

    if hiba or not kimenet:
        return None, hiba or "Nem sikerült lekérni a kulcsvédőket."

    kulcs_minta = r"Recovery Password:\s*([\d\s]+)"
    egyezesek = re.findall(kulcs_minta, kimenet, re.MULTILINE)

    if egyezesek:
        kulcsok = [kulcs.replace(" ", "") for kulcs in egyezesek]
        try:
            with open(fajl_eleresi_ut, 'w', encoding='utf-8') as f:
                f.write(f"*** BitLocker Helyreállítási Kulcsok a(z) {meghajto_betu} meghajtóhoz ***\n\n")
                for kulcs in kulcsok:
                    formazott_kulcs = ' '.join(kulcs[i:i + 6] for i in range(0, len(kulcs), 6))
                    f.write(f"Kulcs: {formazott_kulcs}\n")

            return f"✅ Sikeres mentés ide: {os.path.abspath(fajl_eleresi_ut)}. Mentett kulcsok száma: {len(kulcsok)}", None
        except IOError as e:
            return None, f"❌ Hiba a fájl írásakor: {e}"
    else:
        return None, "❌ Nem találtam 'Recovery Password' típusú kulcsot. (Lehet, hogy csak TPM védi.)"


def pause_bitlocker(meghajto_betu: str):
    parancs = f'manage-bde -pause {meghajto_betu}'
    return futtat_parancsot(parancs, emelt_jogot_igenyel=True)


def resume_bitlocker(mehajto_betu: str):
    parancs = f'manage-bde -resume {mehajto_betu}'
    return futtat_parancsot(parancs, emelt_jogot_igenyel=True)


def disable_bitlocker(meghajto_betu: str):
    parancs = f'manage-bde -off {meghajto_betu}'
    return futtat_parancsot(parancs, emelt_jogot_igenyel=True)


# ----------------------------------------------------------------------
# GRAFIKUS FELÜLET (GUI) OSZTÁLY - CUSTOMTKINTERREL
# ----------------------------------------------------------------------

class BitLockerTools(ctk.CTk):
    VERSION = "v7.1 (Béta kiadás!!!)"

    def __init__(self):
        super().__init__()

        # CTk Beállítások
        self.title(f"BitLockerTools {self.VERSION} (Citk 2025)")
        self.geometry("750x750")
        self.resizable(False, False)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.drive_var = ctk.StringVar(value=DEFAULT_DRIVE)
        self.Thread = Thread

        self._setup_ui()
        self._initial_system_check()

    def _setup_ui(self):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text=f"🔐 BitLockerTools", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 5))

        # >>> VERZIÓ KIÍRÁS <<<
        ctk.CTkLabel(main_frame, text=f"{self.VERSION} (Citk 2025)", font=ctk.CTkFont(size=12, slant="italic")).pack(
            pady=(0, 15))

        self.admin_status_var = ctk.StringVar()
        self.os_status_var = ctk.StringVar()

        self.admin_label = ctk.CTkLabel(main_frame, textvariable=self.admin_status_var,
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.admin_label.pack(pady=(5, 2))
        self.os_label = ctk.CTkLabel(main_frame, textvariable=self.os_status_var,
                                     font=ctk.CTkFont(size=12, weight="bold"))
        self.os_label.pack(pady=(2, 10))

        drive_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        drive_frame.pack(pady=10)
        ctk.CTkLabel(drive_frame, text="Meghajtó Betűjele (pl. C:):", font=ctk.CTkFont(size=12, weight="bold")).pack(
            side=tk.LEFT, padx=(0, 10))
        ctk.CTkEntry(drive_frame, textvariable=self.drive_var, width=50, font=ctk.CTkFont(size=12),
                     justify='center').pack(side=tk.LEFT, padx=5)

        # ----------------------------------------------
        # >>> ÚJ MENÜ ELRENDEZÉS - KÉT KERETBEN <<<
        # ----------------------------------------------

        # 1. ÁLTALÁNOS MŰVELETEK (Normál jogosultsággal)
        ctk.CTkLabel(main_frame, text="1. Általános Műveletek (Normál Jog)",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), padx=10, anchor='w')
        self.general_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.general_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.general_frame.grid_columnconfigure(0, weight=1)
        self.general_frame.grid_columnconfigure(1, weight=1)

        self._create_button_widget(self.general_frame, "Állapot Lekérdezése 🔍", self._start_check_status, 0, 0, False,
                                   "#007BFF")
        self._create_button_widget(self.general_frame, "Kulcs Exportálása 💾", self._start_export_key, 0, 1, False,
                                   ctk.ThemeManager.theme["CTkButton"]["fg_color"][0])

        # 2. ADMINISZTRÁCIÓS MŰVELETEK (Rendszergazdai jog kell)
        ctk.CTkLabel(main_frame, text="2. Adminisztrációs Műveletek (Rendszergazdai Jog KELL)",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), padx=10, anchor='w')
        self.admin_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.admin_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.admin_frame.grid_columnconfigure(0, weight=1)
        self.admin_frame.grid_columnconfigure(1, weight=1)

        self._create_button_widget(self.admin_frame, "Felfüggesztés ⏸️", self._start_pause, 0, 0, True, COLOR_WARNING)
        self._create_button_widget(self.admin_frame, "Folytatás ▶️", self._start_resume, 0, 1, True, "#17A2B8")
        self._create_button_widget(self.admin_frame, "KIKAPCSOLÁS (Dekódolás) ⛔", self._start_disable, 1, 0, True,
                                   COLOR_ERROR)

        # ----------------------------------------------
        # >>> NAPLÓ ÉS KILÉPÉS <<<
        # ----------------------------------------------
        ctk.CTkLabel(main_frame, text="Kimeneti Napló (Műveletek):", font=ctk.CTkFont(size=12, weight="bold")).pack(
            pady=(10, 5), padx=10, anchor='w')

        ctk_bg_color = self._get_ctk_color_for_widget("CTkFrame")
        ctk_fg_color = self._get_ctk_color_for_widget("CTkLabel", "text_color")

        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD, font=("Consolas", 10),
                                                     bg=ctk_bg_color,
                                                     fg=ctk_fg_color,
                                                     insertbackground=ctk_fg_color,
                                                     relief=tk.FLAT)
        self.output_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        self._log_output("Üdvözlöm! Induláskor rendszer- és jogosultság ellenőrzés történt.", COLOR_INFO)

        ctk.CTkButton(main_frame, text="Kilépés", command=self.destroy, fg_color="#DC3545", hover_color="#C82333").pack(
            pady=10)

    def _get_ctk_color_for_widget(self, widget_name, color_key="fg_color"):
        try:
            color = ctk.ThemeManager.theme[widget_name][color_key]
            if isinstance(color, list):
                return color[0] if ctk.get_appearance_mode() == "Light" else color[1]
            return color
        except Exception:
            return "white"

    def _create_button_widget(self, parent, text, command, row, col, needs_admin, color):
        btn = ctk.CTkButton(parent, text=text, command=command, fg_color=color,
                            hover_color=self._adjust_color(color, 0.8))

        if needs_admin and not is_admin():
            # Ha nincs admin jog, inaktiváljuk az admin gombokat
            btn.configure(text=f"{text} (INAKTÍV - ADMIN JOG KELL)", state="disabled", fg_color="#6C757D")

        btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        return btn

    def _adjust_color(self, color, factor):
        if isinstance(color, list):
            color = color[0]

        if color.startswith('#'):
            hex_color = color[1:]
        else:
            return color

        rgb = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
        rgb = [min(255, max(0, int(c * factor))) for c in rgb]
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def _initial_system_check(self):
        if is_windows():
            self.os_status_var.set("OS: ✅ Windows (BitLocker Támogatott)")
            self.os_label.configure(text_color=COLOR_SUCCESS)
        else:
            self.os_status_var.set(f"OS: ❌ Nem Windows ({platform.system()}) - BitLocker Parancsok NEM fognak működni!")
            self.os_label.configure(text_color=COLOR_ERROR)

        if is_admin():
            self.admin_status_var.set("Admin Jog: ✅ Igen (Minden funkció elérhető)")
            self.admin_label.configure(text_color=COLOR_SUCCESS)
        else:
            self.admin_status_var.set(
                "Admin Jog: ⚠️ Nem (Rendszergazdaként való indítás szükséges az admin funkciókhoz!)")
            self.admin_label.configure(text_color=COLOR_WARNING)

    def _log_output(self, message: str, color="black"):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")

        self.output_text.tag_config(COLOR_SUCCESS, foreground=COLOR_SUCCESS)
        self.output_text.tag_config(COLOR_ERROR, foreground=COLOR_ERROR)
        self.output_text.tag_config(COLOR_WARNING, foreground=COLOR_WARNING)
        self.output_text.tag_config(COLOR_INFO, foreground=COLOR_INFO)
        self.output_text.tag_config("timestamp", foreground='#6C757D')

        self.output_text.insert(tk.END, f"[{time_str}] ", "timestamp")
        self.output_text.insert(tk.END, f"{message}\n", color)
        self.output_text.yview(tk.END)

    def _set_buttons_state(self, state):
        # A gombok állapotát a két keretben állítjuk
        state_str = "disabled" if state == tk.DISABLED else "normal"

        for frame in [self.general_frame, self.admin_frame]:
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(state=state_str)

                    # Visszaállításnál ellenőrizzük az admin jogot az admin_frame gombjainál
                    if state == tk.NORMAL and frame == self.admin_frame and not is_admin():
                        child.configure(state="disabled")

    def _run_function_in_thread(self, func, *args, **kwargs):
        drive = self.drive_var.get().upper()
        if not check_drive_validity(drive):
            self._log_output(f"❌ HIBA: Érvénytelen vagy nem elérhető meghajtó: {drive}", COLOR_ERROR)
            messagebox.showerror("Hiba",
                                 f"Érvénytelen vagy nem elérhető meghajtó betűjel: {drive}. Kérjük, ellenőrizze!")
            return

        self._set_buttons_state(tk.DISABLED)

        def worker():
            kimenet, hiba = func(drive, *args, **kwargs)
            self.after(0, lambda: self._handle_result(kimenet, hiba))

        self.Thread(target=worker).start()

    def _handle_result(self, kimenet: str | None, hiba: str | None):
        if hiba:
            # Csak az első hibaüzenet sort mutatjuk meg a popup-ban
            messagebox.showerror("Művelet Hiba", hiba.splitlines()[0])
            self._log_output(f"❌ HIBA (Részletek a következőkben):", COLOR_ERROR)
            self._log_output(hiba, COLOR_ERROR)
        else:
            self._log_output("✅ SIKERES MŰVELET! Részletek a következőkben:", COLOR_SUCCESS)
            self._log_output(kimenet, COLOR_DEFAULT)

        self._set_buttons_state(tk.NORMAL)

    # --- Fő Műveletek Fül Gombfunkciói ---
    def _start_check_status(self):
        self._log_output(f"\n[FUT] Állapot lekérdezése: {self.drive_var.get()}", COLOR_INFO)
        self._run_function_in_thread(get_status)

    def _start_export_key(self):
        fajl_eleresi_ut = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"BitLocker_Recovery_Key_{self.drive_var.get().replace(':', '')}_{datetime.date.today()}.txt",
            filetypes=[("Szöveges fájlok", "*.txt"), ("Minden fájl", "*.*")],
            title="Válaszd ki a kulcsfájl mentési helyét"
        )
        if fajl_eleresi_ut:
            self._log_output(f"\n[FUT] Kulcs exportálása: {self.drive_var.get()} (Normál Jog)", COLOR_INFO)
            # A lambda a meghajtó betűjét adja át, a fájl elérési utat külön kwargs-ban kapja
            self._run_function_in_thread(lambda d: export_recovery_key(d, fajl_eleresi_ut))
        else:
            self._log_output("Művelet megszakítva (Kulcs Exportálás).", COLOR_WARNING)

    def _start_pause(self):
        if is_admin() and messagebox.askyesno("Megerősítés",
                                              "Biztosan felfüggeszted a BitLockert? (Újraindításkor folytatja)"):
            self._log_output(f"\n[FUT] BitLocker felfüggesztése: {self.drive_var.get()} (Admin Jog Kell)",
                             COLOR_WARNING)
            self._run_function_in_thread(pause_bitlocker)

    def _start_resume(self):
        if is_admin() and messagebox.askyesno("Megerősítés",
                                              "Biztosan folytatod (bekapcsolod) a felfüggesztett BitLockert?"):
            self._log_output(f"\n[FUT] BitLocker folytatása: {self.drive_var.get()} (Admin Jog Kell)", COLOR_WARNING)
            self._run_function_in_thread(resume_bitlocker)

    def _start_disable(self):
        if is_admin() and messagebox.askyesno("VÉGLEGES KIKAPCSOLÁS",
                                              "!!! Veszélyes művelet !!! Biztosan VÉGLEGESEN kikapcsolod a BitLockert (dekódolás)? Ez időigényes!"):
            self._log_output(f"\n[FUT] BitLocker KIKAPCSOLÁSA (Dekódolás): {self.drive_var.get()} (Admin Jog Kell)",
                             COLOR_ERROR)
            self._run_function_in_thread(disable_bitlocker)


# ----------------------------------------------------------------------
# PROGRAM INDÍTÁSA
# ----------------------------------------------------------------------

if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            import ctypes

            # DPI skálázás javítása magas felbontású monitorokon
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = BitLockerTools()
    app.mainloop()
