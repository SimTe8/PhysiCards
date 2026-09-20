# PhysiCards - Physik & Mathe Karteikarten-Software ⚛️📐

<p align="center">
  <b>Ein spezialisiertes Lernsystem für Physik, höhere Mathematik und Naturwissenschaften.</b><br>
  Wissenschaftlich fundiertes Spaced Repetition (SuperMemo SM-2), gestochen scharfes LaTeX-Rendering (100% Offline), aktiver Formel-Kritzelblock und optionaler sokratischer KI-Tutor via Google AI Studio.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/KaTeX-100%25%20Offline-emerald.svg" alt="KaTeX Offline">
  <img src="https://img.shields.io/badge/Spaced%20Repetition-SuperMemo%20SM--2-orange.svg" alt="SM-2">
  <img src="https://img.shields.io/badge/AI%20Tutor-Gemini%203-purple.svg" alt="Gemini 3">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

---

## 🎯 Warum PhysiCards?

Formeln in der theoretischen und experimentalen Physik lernt man **nicht** durch passives Lesen oder einfaches Vokabelkarten-Abfragen. Echtes physikalisches Verständnis verlangt:
1. **Aktives handschriftliches Herleiten** vor dem Aufdecken der Lösung.
2. **Präzise mathematische Notation** mit Vektorpfeilen, Operatoren, Integralen und SI-Einheiten.
3. **Didaktische Tiefenschärfe**: Was bedeutet die Formel physikalisch? Wo liegen ihre Gültigkeitsgrenzen (z.B. $v \ll c$, $T \to 0$)?
4. **Wissenschaftliche Wiederholungsabstände** gegen die menschliche Vergessenskurve.

**PhysiCards** wurde von Grund auf entwickelt, um diese Anforderungen in einer modernen, ästhetischen Desktop- und Web-Applikation zu vereinen.

---

## ✨ Features im Überblick

### 1. Spaced Repetition nach SuperMemo SM-2
- **Wissenschaftlicher Algorithmus**: Berechnet für jede Karte individuelle Wiederholungsabstände basierend auf Wiederholungszähler ($n$), Intervall ($I$) und Leichtheitsfaktor ($EF$).
- **Live-Intervallvorhersage**: Auf den 4 Bewertungsbuttons (`[1] Nochmal`, `[2] Schwer`, `[3] Gut`, `[4] Einfach`) wird in Echtzeit angezeigt, wann die Karte bei der jeweiligen Bewertung wieder vorgelegt wird.
- **Laps-Handling**: Bei *„Nochmal“* wandert die Karte sofort ans Ende der aktuellen Lerneinheit, um sie im Kurzzeitgedächtnis zu festigen.

### 2. Aktiver Formel-Kritzelblock (Active Scratchpad / Whiteboard)
- **Keine Passivitäts-Falle**: Über die Taste `W` oder das Stift-Symbol blendest du direkt über der Karte eine transparente Zeichenfläche ein.
- Zeichne oder skizziere Formeln, Vektordiagramme oder Integrationswege per Maus, Stift oder Touchpad, **bevor** du die Antwort aufdeckst.

### 3. 100% Offline KaTeX-Formelrendering
- Mathematische Formeln inline (`$...$`) und abgesetzt (`$$...$$`).
- Sämtliche KaTeX-Bibliotheken und mathematischen Fonts sind **vollständig lokal gebündelt**. Die App funktioniert auch im Flugzeug, im Keller oder ohne Internetverbindung uneingeschränkt.

### 4. Strukturierte physikalische Vertiefung
Jede Karte ist didaktisch standardisiert in aufklappbare Bereiche gegliedert:
- **Exakte mathematische Formel**
- **Variablen, Naturkonstanten & SI-Einheiten** (z.B. $-\vec{E}$: Elektrisches Feld $[\mathrm{V/m}]$)
- **Physikalische Bedeutung & Intuition** (Alltags-Analogien, Gedankenexperimente)
- **Gültigkeitsbereich & Grenzfälle** (z.B. nicht-relativistischer Grenzfall, ideales Gas, $T \to 0$)

### 5. Sokratischer KI-Tutor (Google AI Studio & Gemini 3)
- **Interaktiver Chat-Drawer (Shortcut `T`)**: Diskutiere Karten live mit Gemini.
- **Stufenlos skalierbar**: Ziehe den linken Rand des Chatfensters mit der Maus nach links, um beliebig breite mathematische Herleitungen darzustellen. Die Wunschbreite wird automatisch gespeichert.
- **Didaktische Quick-Prompts**: *💡 Alltags-Analogie*, *❓ Sokratische Verständnisfrage*, *📐 Herleitung*, *⚠️ Typische Denkfallen*.
- **100% Privatsphäre & Offline**: Der KI-Tutor ist ein rein optionales Feature. Dein kostenloser Google AI Studio API-Key wird ausschließlich lokal auf deinem Rechner in SQLite gespeichert.

### 6. Automatisierte Kartenerstellung
- Lasse Gemini direkt im Chat neue Karten im standardisierten Format entwerfen.
- Neuer Dashboard-Button **„🪄 KI-Karte generieren“**: Thema eingeben $\to$ didaktisch strukturierte Karte mit Variablen und LaTeX wird automatisch generiert und im Editor vorausgefüllt.

### 7. Live Split-Screen Editor & Deck-Verwaltung
- Links Eingabe in Markdown/LaTeX, rechts gerenderte KaTeX-Vorschau in Echtzeit.
- Toolbar für häufige Physik-Symbole ($\nabla$, $\vec{E}$, $\int$, $\oiint$, $\hbar$, $\ket{\psi}$, etc.).
- Vollständige Deck-Bearbeitung: Benenne Decks um, wähle Akzentfarben über Farbwähler/Paletten und wähle Symbole ($\sum, f(x), \infty, \⚛, \⚡, \🔥, \🪐, \🧭, \📐, \🔬$).

### 8. Datensicherung & Anki-Kompatibilität
- **1-Klick JSON-Backup**: Sichert den kompletten Datenbestand inklusive aller Lernstände und SM-2 Statistiken.
- **Anki-Export (TSV)**: Exportiere deine Karten mit sauber formatiertem HTML/LaTeX für Anki.

---

## 🚀 Schnellstart & Installation

### Voraussetzungen
- Python 3.10 oder neuer

### 1. Repository klonen
```bash
git clone https://github.com/DEIN-BENUTZERNAME/PhysiCards.git
cd PhysiCards
```

### 2. Abhängigkeiten installieren
PhysiCards hat minimale Abhängigkeiten (der gesamte KI-Client und KaTeX laufen ohne externe Großbibliotheken):
```bash
pip install -r requirements.txt
```

### 3. Anwendung starten

**Unter Windows:**
Einfach die Datei **`start.bat`** per Doppelklick ausführen.

**Über das Terminal (Desktop-Fenster via PyWebView):**
```bash
python main.py
```

**Direkt im Standard-Webbrowser öffnen:**
```bash
python main.py --browser
```
Die App läuft lokal unter: `http://127.0.0.1:5055`

---

## 📚 Enthaltene Standard-Decks (8 Decks & 95 Fachkarten)

Beim ersten Start initialisiert die Software automatisch eine frische SQLite-Datenbank mit 95 kuratierten Fachkarten:

1. **Reine Mathematik & Analysis** ($\sum$):
   $L^2$-Raum & Norm, Skalarprodukt $\langle f, g \rangle$, Vollständigkeit & Satz von Riesz-Fischer, Cauchy-Schwarz-Ungleichung, Minkowski-Dreiecksungleichung, Geometrische Reihe, Harmonische Reihe (logarithmische Divergenz & Euler-Mascheroni $\gamma$), Basler Problem ($\sum 1/n^2 = \pi^2/6$), Leibniz-Kriterium & alternierende Reihen, Taylor-Reihen ($e^x, \sin x, \cos x$), Cauchy-Hadamard-Konvergenzradius, Parsevalsche Identität in $L^2$, Spektralsatz für selbstadjungierte Operatoren.
2. **Naturkonstanten & Größenordnungen** (📐):
   Fundamentale Konstanten ($c, h, \hbar, e, m_e, m_p, k_B, N_A, R, G, g, \varepsilon_0, \mu_0, a_0, \alpha \approx 1/137, \sigma$), Fermi-Faustregeln (Sekunden im Jahr $\approx \pi \times 10^7\,\text{s}$, $k_B T \approx 25\,\text{meV}$, Schallgeschwindigkeit $c_s$, Sonnen- & Erdmassen, Wellenlängen sichtbaren Lichts).
3. **Quantenmechanik** (⚛):
   Die 5 Postulate, Schrödinger-Gleichung, Heisenbergsche Unschärferelation ($\Delta x \Delta p$ und $\Delta E \Delta t$ mit Zerfallsbreite $\Gamma = \hbar/\tau$), De-Broglie-Wellenlänge, Impuls-Wellenvektor-Beziehung ($p = \hbar k$), Planck-Einstein-Relation ($E = \hbar\omega$), harmonischer Oszillator & Leiteroperatoren $\hat{a}, \hat{a}^\dagger$, Pauli-Spinmatrizen.
4. **Klassische Mechanik** (🧭):
   Die 3 Newtonschen Axiome, Lagrange-Gleichungen 2. Art, Hamiltonsche Gleichungen, Harmonischer Oszillator, Noether-Theorem, Fluchtgeschwindigkeit, Fadenpendel, Zentripetalkraft, Drehimpulserhaltung & Pirouetteneffekt.
5. **Elektrodynamik & Optik** (⚡):
   Alle 4 Maxwell-Gleichungen (differentiell & integral), Lorentzkraft, Kontinuitätsgleichung, Poynting-Vektor, Ohmsches Gesetz & Verlustleistung ($P=UI=I^2R$), Kondensator- und Spulenenergie, Thomson-Schwingkreis, Snelliussches Brechungsgesetz, Lichtgeschwindigkeit $c = 1/\sqrt{\varepsilon_0\mu_0}$.
6. **Thermodynamik & Statistische Physik** (🔥):
   Die 4 Hauptsätze der Thermodynamik, Gaußsche Normalverteilung, Maxwell-Boltzmann-Geschwindigkeitsverteilung, Boltzmann-Entropie $S = k_B \ln \Omega$, Äquipartitionstheorem, Ideale Gasgleichung, Carnot-Wirkungsgrad, Stefan-Boltzmann-Gesetz, Bernoulli-Gleichung & hydrostatischer Druck.
7. **Mathematische Methoden der Physik** (📐):
   Gaußscher Integralsatz, Stokesscher Integralsatz, Dirac-Delta-Distribution, Fourier-Transformation, Taylor-Entwicklungen & Kleinwinkelnäherungen, Gaußsches Fehlerintegral.
8. **Relativitätstheorie** (🪐):
   Lorentz-Transformation, Zeitdilatation, Längenkontraktion, Relativistische Energie-Impuls-Beziehung $E^2 = (pc)^2 + (m_0 c^2)^2$.

---

## 🕹️ Tastaturkürzel

| Taste | Funktion |
|---|---|
| `Leertaste` | Karte umdrehen (Antwort aufdecken) |
| `1` | Bewertung: **Nochmal** (< 10 min) |
| `2` | Bewertung: **Schwer** |
| `3` | Bewertung: **Gut** |
| `4` | Bewertung: **Einfach** |
| `W` | Formel-Kritzelblock (Whiteboard) ein-/ausblenden |
| `E` | Aktuelle Karte im Live-Editor bearbeiten |
| `T` | Sokratischen KI-Tutor öffnen/schließen |
| `Esc` | Modals / Chat schließen bzw. zurück zum Dashboard |

---

## 📁 Projektstruktur

```
PhysiCards/
├── app.py                  # Flask REST-API & Routen
├── main.py                 # Desktop-Window Launcher (PyWebView & Browser-Fallback)
├── start.bat               # 1-Klick Windows-Starter
├── requirements.txt        # Python-Abhängigkeiten
├── .gitignore              # Git-Ausschlussregeln (schützt cards.db und API-Keys)
├── core/
│   ├── models.py           # Dataclasses für Decks, Cards, ReviewState
│   ├── sm2.py              # Wissenschaftlicher SuperMemo SM-2 Algorithmus
│   ├── storage.py          # SQLite-Persistenzschicht & Stats
│   ├── default_decks.py    # 8 Standard-Decks & 95 Fachkarten
│   └── gemini_service.py   # Google AI Studio / Gemini 3 SSE-Streaming & Tutor
├── data/
│   └── .gitkeep            # Lokales Datenverzeichnis (cards.db wird lokal erzeugt)
├── static/
│   ├── index.html          # Single-Page Frontend GUI
│   ├── css/style.css       # Responsive Dark/Light Design & Animationen
│   ├── js/
│   │   ├── app.js          # Hauptanwendungslogik, SM-2 Schleife & UI
│   │   ├── scratchpad.js   # HTML5 Canvas Formel-Kritzelblock
│   │   └── audio.js        # Web Audio API Soundeffekte
│   └── vendor/katex/       # 100% Offline KaTeX Engine & Schriften
└── tests/
    ├── test_sm2.py         # SM-2 Intervall- und Progressions-Tests
    ├── test_storage.py     # SQLite CRUD-, Seed- & Reset-Tests
    ├── test_api.py         # REST-API Integrationstests
    ├── test_gemini.py      # Prompt-Builder, LaTeX-Sanitizer & Mock-Tests
    └── test_system.py      # KaTeX-Fonts & Offline-Asset Tests
```

---

## 🔒 Datenschutz & Sicherheit

- **100% Lokal**: Deine persönliche Lernhistorie, Wiederholungszeiten und Kartennotizen werden ausschließlich in deiner lokalen SQLite-Datei (`data/cards.db`) gespeichert.
- **Keine Telemetrie**: Es werden keinerlei Analysedaten oder Tracking-Cookies übertragen.
- **API-Key Schutz**: Dein Google AI Studio API-Key wird nur lokal abgelegt und verlässt deinen Rechner ausschließlich als Autorisierungs-Header direkt zu den offiziellen Endpunkten von Google (`generativelanguage.googleapis.com`). Durch die beiliegende `.gitignore` wird die Datenbank niemals versehentlich in öffentliche Repositories hochgeladen.

---

## 🧪 Tests ausführen

Die gesamte Testsuite (24 automatisierte Tests) lässt sich ohne externe Testrunner mit Pythons Standard-Unittest ausführen:

```bash
python -m unittest discover tests
```

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Frei zur Nutzung, Modifikation und Weitergabe für Studium, Forschung und Lehre.
