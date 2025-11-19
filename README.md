# The G Logger – Security-Demo

**Hinweis:** Dieses Projekt demonstriert, wie Keylogging- und Datensammlungs-Skripte technisch aufgebaut sein können. Es ist **ausschließlich** für Lern-, Analyse- und Forensik-Zwecke auf deinen **eigenen Systemen** gedacht.

## ⚠️ Rechtlicher Hinweis & Ethik

- **Nur auf eigenen Systemen:** Führe die erzeugten Skripte ausschließlich auf Rechnern aus, die dir gehören oder auf denen du explizit die Zustimmung hast.
- **Keine Überwachung Dritter:** Der Einsatz von Keyloggern oder Datensammlern ohne klare Einwilligung der betroffenen Person(en) ist in vielen Ländern strafbar.
- **Verantwortungsvoller Umgang:** Nutze den Code, um zu verstehen, wie solche Tools funktionieren, damit du dich und andere besser davor schützen kannst (z.B. Erkennung, Forensik), **nicht** um andere heimlich auszuspionieren.

Wenn du dir unsicher bist, welche Nutzung rechtlich zulässig ist, **hole rechtlichen Rat ein**, bevor du irgendetwas außerhalb deiner eigenen Testumgebung einsetzt.

## Überblick

**The G Logger** stellt eine einfache Konsolenoberfläche bereit, über die du:

- einen **Keylogger** als Python-Skript  generieren kannst und dann automatisch in eine Exe umgewandelt wird.
- ein **Graber-Skript** generieren kannst, das lokal Dokumente/Bilder/Systeminformationen einsammelt und in ein ZIP packt, und dann per Dropbox an deine Dropbox-Konto hochgeladen wird.

## Projektstruktur & wichtige Dateien

- **`glogger_ui.py`**
  - Startskript mit einem einfachen Textmenü.
  - Bietet Optionen zum Erzeugen des Keylogger-Skripts und des Graber-Skripts.
  - Leitet die Aktionen an die Funktionen in `tools/generate_keylogger.py` und `tools/generate_Graber.py` weiter.

- **`tools/generate_keylogger.py`**
  - Funktion `create_file()` erzeugt ein `Keylogger.py`-Skript.
  - Der erzeugte Keylogger protokolliert Tastatureingaben in eine Logdatei.
  - Versucht, das Skript mit **PyInstaller** zu einer ausführbaren Datei zu bauen, falls PyInstaller installiert ist.

- **`tools/generate_Graber.py`**
  - Funktion `create_file()` erzeugt ein Skript `Graber.py`.
  - Das generierte Skript sammelt auf dem lokalen System u.a.:
    - ausgewählte Dokumente und Bilder,
    - einfache Browser-Login-Daten (zur Demonstration des Zugriffs auf lokale Datenbanken),
    - System- und Hardwareinformationen,
    - laufende Prozesse und Netzwerkdaten.
  - Es legt alles in einem Exportordner unter deinem Benutzerprofil ab und erstellt daraus ein ZIP-Archiv.
  - Optional: Upload des ZIP-Archivs zu **Dropbox** mithilfe eines Access Tokens (siehe Abschnitt „Dropbox-Token“).
  - Versucht ebenfalls, mit **PyInstaller** eine ausführbare Datei aus dem generierten Skript zu bauen.

- **`update_token.py`**
  - Bietet eine Hilfsfunktion `update_dropbox_token()`, die dich in der Konsole nach einem neuen Dropbox-Access-Token fragt.
  - Sucht in `tools/generate_Graber.py` nach der Zeile mit `DROPBOX_ACCESS_TOKEN =` und ersetzt den dort hinterlegten Wert durch den neuen Token.
  - Wird für **Testzwecke** genutzt, um das Dropbox-Beispiel mit deinem eigenen Konto zu verknüpfen (nur für Backups/Analysen deiner eigenen Systeme).

- **`clean_pyinstaller.py`**
  - Entfernt typische **PyInstaller-Artefakte** (`dist/`, `build/`, `*.spec`).
  - Löscht den lokalen Exportordner des Graber-Demos (`G_LoggerExport` im Benutzerverzeichnis) und das zugehörige ZIP, falls vorhanden.
  - Kann genutzt werden, um deine Umgebung nach Tests wieder aufzuräumen.

- **`requirements.txt`**
  - Listet die benötigten Python-Abhängigkeiten für die Demo (u.a. `pynput`, `psutil`, `Pillow`, `py-cpuinfo`, `dropbox`).

## Voraussetzungen

- **Betriebssystem:** Windows (einige Teile nutzen Windows-spezifische Pfade/Registry-Befehle).
- **Python:** Empfohlen wird eine aktuelle Python-3-Version.
- **Paketverwaltung:** `pip` zum Installieren der Abhängigkeiten.
- Optional: **PyInstaller**, falls du die generierten Skripte als EXE bauen willst.

## Projekt herunterladen & installieren

1. **Repository klonen**

   ```bash
   git clone https://github.com/M0x37/The-G-Logger.git
   cd "The GLogger"
   ```

   Alternativ kannst du das Repository als ZIP von GitHub herunterladen und entpacken.

2. **Virtuelle Umgebung anlegen (empfohlen):**

   ```bash
   python -m venv venv
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

3. **Abhängigkeiten installieren:**

   ```bash
   pip install -r requirements.txt
   ```

4. Optional: **PyInstaller** installieren (für EXE-Builds):

   ```bash
   pip install pyinstaller
   ```

## Nutzung (nur zu Test-/Lernzwecken auf eigenen Systemen)

> **Wichtig:** Die folgenden Hinweise dienen dazu, das Verhalten solcher Tools nachzuvollziehen. Setze sie nicht gegen andere Personen ein.

1. **UI starten:**

   ```bash
   python glogger_ui.py
   ```

2. Im Menü kannst du dann Skripte generieren lassen (Keylogger oder Graber). Die Details der Ausführung entnimmst du am besten direkt dem Quellcode – er ist bewusst einfach gehalten, damit du ihn nachvollziehen und analysieren kannst.

3. Die generierten Skripte legen ihre Ausgaben (Logs, Exportordner etc.) lokal auf deinem System ab. Lies diese Dateien bewusst und analysiere, **welche Informationen in welcher Form erfasst werden**.

> **Sicherheitshinweis:** Das Speichern eines Access Tokens im Klartext im Quellcode ist unsicher. Für produktive Szenarien solltest du stattdessen z.B. Umgebungsvariablen oder einen sicheren Secret-Store verwenden. Hier geschieht es nur aus didaktischen Gründen, um die Funktionsweise leicht nachvollziehbar zu machen.

## Aufräumen von Build- und Export-Artefakten

Nach Tests kannst du mit folgendem Skript die wichtigsten Artefakte entfernen:

```bash
python clean_pyinstaller.py
```

Das Skript entfernt u.a.:

- `dist/` und `build/` (PyInstaller-Ausgaben),
- `.spec`-Dateien,
- den Exportordner `G_LoggerExport` im Benutzerverzeichnis und das zugehörige ZIP.

