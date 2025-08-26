# 📄 Docling Converter 📊

Eine elegante GUI-Anwendung zum Konvertieren und Verarbeiten von Dokumenten mit Textextraktion, OCR und Tabellenerkennung.

![Docling Converter](https://img.shields.io/badge/Docling-Converter-blue?style=for-the-badge&logo=python)

## 🌟 Funktionen

- 📑 **Multi-Format-Unterstützung**: Verarbeitet PDF, DOCX, HTML und Bild-Dateien
- 🔍 **Intelligente Texterkennung**: OCR-Technologie für Texterkennung in Bildern und Scans
- 📊 **Tabellenerkennung**: Erkennt und extrahiert tabellarische Daten
- 🖼️ **Benutzerfreundliche Oberfläche**: Moderne GUI mit Emojis und intuitivem Design
- 🔄 **Batch-Verarbeitung**: Verarbeite mehrere Dokumente gleichzeitig
- 📋 **Fortschrittsanzeige**: Visuelles Feedback zum Verarbeitungsfortschritt

## 🚀 Schnellstart

1. Stelle sicher, dass Python (Version 3.6 oder höher) installiert ist
2. Installiere die erforderlichen Abhängigkeiten:
   ```
   pip install docling tkinter
   ```
3. Starte die Anwendung:
   ```
   python app.py
   ```

## 📋 Verwendung

1. **Dateien auswählen**: Klicke auf "📂 Dateien auswählen" und wähle deine Dokumente aus
2. **Verarbeitung starten**: Klicke auf "▶️ Verarbeitung starten"
3. **Ergebnisse**: Die verarbeiteten Dateien werden im "Scratch"-Ordner gespeichert
4. **Status**: Erfolgreich verarbeitete Dateien werden grün markiert, fehlerhafte rot

## 🛠️ Technische Details

Die Anwendung basiert auf:
- **Docling**: Framework für Dokumentenverarbeitung
- **PyPdfium2**: PDF-Verarbeitungsbibliothek
- **Tkinter**: GUI-Framework für Python
- **Threading**: Nicht-blockierende Verarbeitung für eine reaktionsschnelle Benutzeroberfläche

### Unterstützte Dateiformate

| Format | Emoji | Beschreibung |
|--------|-------|--------------|
| PDF    | 📑    | Portable Document Format |
| DOCX   | 📝    | Microsoft Word Dokument |
| HTML   | 🌐    | Webseiten-Dokument |
| JPG/PNG| 🖼️    | Bilddateien (mit OCR) |

## 📝 Beispielausgabe

Die Anwendung generiert strukturierte Textdateien, die den extrahierten Inhalt und erkannte Strukturen enthalten. Diese Dateien können für weitere Analyse oder Datenextraktionsaufgaben verwendet werden.


## 📜 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

---
