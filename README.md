# The GLogger

The GLogger ist ein Toolkit zur Erstellung von Datenerfassungs-Anwendungen für Windows. Es bietet eine einfache Kommandozeilen-Oberfläche, um Python-Skripte zu generieren und sie in eigenständige `.exe`-Dateien zu kompilieren. Die Hauptanwendung `Graber` sammelt eine Vielzahl von Benutzer- und Systemdaten und lädt sie zur Analyse in ein privates Dropbox-Konto hoch.

**Wichtiger Hinweis:** Der Name des hochgeladenen Archivs in Dropbox ist `FScriptExport.zip`.

---

## ⚠️ Disclaimer / Haftungsausschluss

Dieses Tool ist ausschließlich für Bildungs-, Forschungs- und autorisierte Testzwecke vorgesehen. Das Ausführen dieses Programms auf einem Computer ohne die ausdrückliche Zustimmung des Eigentümers ist illegal und unethisch. Die Autoren dieses Projekts übernehmen keine Verantwortung für Missbrauch oder Schäden, die durch dieses Programm verursacht werden. **Verwenden Sie es verantwortungsbewusst.**

---

## ✨ Features von `Graber.exe`

Die generierte `Graber.exe` führt die folgenden Aktionen auf dem Zielsystem aus:

-   **Log-Erstellung**: Führt eine Log-Datei über seine Aktivitäten.
-   **Dokumenten-Kopie**: Kopiert `.docx`, `.pdf`, und `.txt` Dateien aus dem `Dokumente`-Ordner des Benutzers.
-   **Bilder-Kopie**: Kopiert `.jpg`, `.jpeg`, und `.png` Dateien aus dem `Bilder`-Ordner des Benutzers.
-   **Screenshot**: Erstellt einen Screenshot des aktuellen Desktops.
-   **Chrome-Daten**: Versucht, die `Login Data`-Datenbank von Google Chrome zu kopieren und die darin enthaltenen (unverschlüsselten) Daten auszulesen.
-   **Systeminformationen**: Sammelt umfassende System- und Netzwerkinformationen:
    -   Betriebssystem, Architektur, Hostname
    -   CPU- und RAM-Details
    -   Liste der laufenden Prozesse
    -   Aktive Netzwerkverbindungen und IP-Adressen
    -   Liste der installierten Programme (aus der Windows-Registry)
-   **Archivierung & Upload**: Fasst alle gesammelten Daten in einer `FScriptExport.zip`-Datei zusammen.
-   **Dropbox-Upload**: Lädt die ZIP-Datei in das Stammverzeichnis des konfigurierten Dropbox-Kontos hoch.
-   **Säuberung**: Löscht nach erfolgreichem Upload alle lokal gesammelten Dateien und das ZIP-Archiv, um Spuren zu minimieren.

---

## 🛠️ Setup & Konfiguration

Folgen Sie diesen Schritten, um das Projekt einzurichten und zu konfigurieren.

### Schritt 1: Installation der Abhängigkeiten

1.  **Repository klonen**:
    ```bash
    git clone <repository-url>
    cd The-GLogger
    ```

2.  **Virtuelle Umgebung erstellen**:
    ```bash
    python -m venv venv
    ```

3.  **Virtuelle Umgebung aktivieren**:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    Oder in CMD:
    ```cmd
    .\venv\Scripts\activate.bat
    ```

4.  **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    ```

### Schritt 2: Dropbox-Token erstellen

Um Daten in Ihr Dropbox-Konto hochladen zu können, benötigen Sie einen Access Token.

1.  **Dropbox App erstellen**:
    -   Gehen Sie zu [Dropbox App Console](https://www.dropbox.com/developers/apps).
    -   Klicken Sie auf **"Create app"**.

2.  **App-Konfiguration**:
    -   **API wählen**: Wählen Sie **"Scoped access"**.
    -   **Zugriffsart**: Wählen Sie **"App folder"** – dies beschränkt den Zugriff der App auf einen einzigen Ordner in Ihrem Dropbox-Konto.
    -   **App-Namen wählen**: Geben Sie Ihrer App einen eindeutigen Namen (z.B. `GLoggerData`) und klicken Sie auf **"Create app"**.

3.  **Berechtigungen (Permissions) festlegen**:
    -   Navigieren Sie zum Tab **"Permissions"**.
    -   Geben Sie der App die Berechtigung **`files.content.write`**. Stellen Sie sicher, dass das Kästchen markiert ist. Klicken Sie oben rechts auf **"Submit"**.

4.  **Access Token generieren**:
    -   Gehen Sie zurück zum Tab **"Settings"**.
    -   Im Abschnitt **"Generated access token"** klicken Sie auf den Button **"Generate"**.
    -   **Kopieren Sie den angezeigten Token.** Dies ist Ihr `DROPBOX_ACCESS_TOKEN`.

### Schritt 3: Token im Projekt speichern

Führen Sie das `update_token.py`-Skript aus, um den Token sicher in die Build-Konfiguration einzufügen.

```bash
python update_token.py
```

Das Skript fordert Sie auf, den kopierten Token einzufügen.

---

## 🚀 Anwendung

Nachdem die Konfiguration abgeschlossen ist, können Sie die ausführbare Datei generieren.

1.  **Hauptmenü starten**:
    Führen Sie das UI-Skript aus, um das Hauptmenü anzuzeigen.
    ```bash
    python glogger_ui.py
    ```

2.  **Graber generieren**:
    -   Wählen Sie im Menü die Option **"2. Graber"**.
    -   Das Skript generiert nun die `Graber.py`-Datei und kompiliert sie mit PyInstaller zu einer einzigen `.exe`-Datei.

3.  **Ergebnis finden**:
    -   Die fertige ausführbare Datei befindet sich im `dist/`-Ordner: `dist/Graber.exe`.

Diese `Graber.exe` ist die eigenständige Anwendung, die auf einem Ziel-Windows-System ausgeführt werden kann. Beim Ausführen arbeitet sie unsichtbar im Hintergrund und lädt am Ende die `FScriptExport.zip` in Ihr Dropbox-Konto hoch.
