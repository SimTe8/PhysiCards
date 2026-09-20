"""
Curated, high-yield starter decks for physics and mathematical methods.
Covers core physical laws, formulas, postulates, variable breakdowns, and physical interpretations.
"""

from core.models import Card, Deck


def get_default_decks() -> list[Deck]:
    return [
        Deck(
            id="elektrodynamik",
            name="Elektrodynamik & Optik",
            description="Maxwell-Gleichungen (diff. & int.), Lorentzkraft, Potenziale, Wellenausbreitung",
            icon="zap",
            color="#3b82f6",
        ),
        Deck(
            id="quantenmechanik",
            name="Quantenmechanik",
            description="Die 5 Postulate, Schrödinger-Gleichung, Unschärfe, Operatoren & Dirac-Notation",
            icon="atom",
            color="#8b5cf6",
        ),
        Deck(
            id="mechanik",
            name="Klassische Mechanik",
            description="Newton-Axiome, Lagrange- und Hamilton-Formalismus, Oszillatoren, Erhaltungssätze",
            icon="compass",
            color="#10b981",
        ),
        Deck(
            id="thermodynamik",
            name="Thermodynamik & Statistik",
            description="Hauptsätze, Gauß- & Maxwell-Boltzmann-Verteilung, Entropie, Phasenübergänge",
            icon="flame",
            color="#f59e0b",
        ),
        Deck(
            id="relativitaet",
            name="Relativitätstheorie",
            description="Lorentz-Transformation, Raumzeit, 4er-Vektoren, Energie-Impuls-Relation",
            icon="orbit",
            color="#ec4899",
        ),
        Deck(
            id="mathe_physik",
            name="Mathematische Methoden",
            description="Integralsätze (Gauß, Stokes), Fourier-Transformation, Dirac-Delta, Differentialoperatoren",
            icon="calculator",
            color="#06b6d4",
        ),
        Deck(
            id="konstanten",
            name="Naturkonstanten & Größenordnungen",
            description="Fundamentale Naturkonstanten (c, h, k_B, N_A, e, G), Fermi-Abschätzungen und physikalische Faustregeln",
            icon="calculator",
            color="#f43f5e",
        ),
        Deck(
            id="reine_mathematik",
            name="Reine Mathematik & Analysis",
            description="Funktionenräume (L²-Raum, Hilbertraum), Reihen & Grenzwerte (Basler Problem, geometrische Reihe), Konvergenzkriterien, Spektralsatz",
            icon="sigma",
            color="#6366f1",
        ),
    ]


def get_default_cards() -> list[Card]:
    cards = [
        # ==========================================
        # ELEKTRODYNAMIK
        # ==========================================
        Card(
            id="em_maxwell_1",
            deck_id="elektrodynamik",
            title="1. Maxwell-Gleichung (Gaußsches Gesetz)",
            front="Wie lautet die **1. Maxwell-Gleichung (Gaußsches Gesetz für das elektrische Feld)** in **differentieller** und **integraler** Form?",
            back="""**Differentielle Form:**
$$\\nabla \\cdot \\vec{E} = \\frac{\\rho}{\\varepsilon_0}$$

**Integrale Form:**
$$\\oiint_{\\partial V} \\vec{E} \\cdot d\\vec{A} = \\frac{Q_{\\text{innen}}}{\\varepsilon_0} = \\frac{1}{\\varepsilon_0} \\iiint_V \\rho \\, dV$$""",
            hint="Quellen des E-Feldes sind elektrische Ladungen.",
            formula_breakdown="""- $\\vec{E}$: Elektrische Feldstärke $[\\mathrm{V/m} = \\mathrm{N/C}]$
- $\\rho$: Raumladungsdichte $[\\mathrm{C/m^3}]$
- $\\varepsilon_0$: Elektrische Feldkonstante (Vakuum-Permittivität) $\\approx 8{,}854 \\times 10^{-12} \\, \\mathrm{A\\cdot s / (V\\cdot m)}$
- $d\\vec{A}$: Nach außen gerichtetes Flächenelement $[\\mathrm{m^2}]$
- $Q_{\\text{innen}}$: Im Volumen $V$ eingeschlossene Gesamtladung $[\\mathrm{C}]$""",
            physical_meaning="Elektrische Feldlinien beginnen auf positiven Ladungen und enden auf negativen Ladungen. Das elektrische Feld besitzt echte Quellen und Senken.",
            validity_domain="Allgemein gültig in der klassischen Elektrodynamik im Vakuum (in Medien: $\\nabla \\cdot \\vec{D} = \\rho_{\\text{frei}}$).",
            tags=["Maxwell", "Elektrostatik", "Vektoranalysis", "Grundgleichung"],
            difficulty=2,
        ),
        Card(
            id="em_maxwell_2",
            deck_id="elektrodynamik",
            title="2. Maxwell-Gleichung (Gauß für Magnetfelder)",
            front="Wie lautet die **2. Maxwell-Gleichung (Quellenfreiheit des Magnetfeldes)** in **differentieller** und **integraler** Form?",
            back="""**Differentielle Form:**
$$\\nabla \\cdot \\vec{B} = 0$$

**Integrale Form:**
$$\\oiint_{\\partial V} \\vec{B} \\cdot d\\vec{A} = 0$$""",
            hint="Gibt es isolierte magnetische Monopole?",
            formula_breakdown="""- $\\vec{B}$: Magnetische Flussdichte (Induktion) $[\\mathrm{T} = \\mathrm{V\\cdot s / m^2}]$
- $\\nabla \\cdot \\vec{B}$: Divergenz des Magnetfeldes
- $\\oiint$: Geschlossenes Hüllenintegral über Randfläche $\\partial V$""",
            physical_meaning="Es gibt keine isolierten magnetischen Ladungen (Monopole). Magnetische Feldlinien sind stets geschlossen (wirbelförmig). Der magnetische Nettofluss durch jede geschlossene Fläche ist null.",
            validity_domain="Gilt ausnahmslos in der klassischen Physik. (Hypothetische Dirac-Monopole wurden bisher experimentell nicht nachgewiesen).",
            tags=["Maxwell", "Magnetismus", "Monopole"],
            difficulty=2,
        ),
        Card(
            id="em_maxwell_3",
            deck_id="elektrodynamik",
            title="3. Maxwell-Gleichung (Faradaysches Induktionsgesetz)",
            front="Wie lautet die **3. Maxwell-Gleichung (Faradaysches Induktionsgesetz)** in **differentieller** und **integraler** Form?",
            back="""**Differentielle Form:**
$$\\nabla \\times \\vec{E} = -\\frac{\\partial \\vec{B}}{\\partial t}$$

**Integrale Form:**
$$\\oint_{\\partial S} \\vec{E} \\cdot d\\vec{r} = -\\frac{d}{dt} \\iint_S \\vec{B} \\cdot d\\vec{A} = -\\frac{d\\Phi_B}{dt}$$""",
            hint="Ein zeitlich veränderliches Magnetfeld erzeugt ein elektrisches Wirbelfeld. Achte auf das Vorzeichen (Lenzsche Regel)!",
            formula_breakdown="""- $\\nabla \\times \\vec{E}$: Rotation des elektrischen Feldes (Wirbelstärke)
- $\\frac{\\partial \\vec{B}}{\\partial t}$: Zeitliche Änderung der magnetischen Flussdichte $[\\mathrm{T/s}]$
- $\\Phi_B = \\iint_S \\vec{B} \\cdot d\\vec{A}$: Magnetischer Fluss $[\\mathrm{Wb} = \\mathrm{V\\cdot s}]$
- Minuszeichen: Lenzsche Regel (Induktionswirkung wirkt ihrer Ursache entgegen)""",
            physical_meaning="Zeitliche Änderungen des Magnetfeldes treiben geschlossene elektrische Wirbel an. Grundlage von Transformatoren, Generatoren und Induktionsspulen.",
            validity_domain="Universell gültig (auch relativistisch kovariant).",
            tags=["Maxwell", "Induktion", "Lenz", "Wirbelfeld"],
            difficulty=3,
        ),
        Card(
            id="em_maxwell_4",
            deck_id="elektrodynamik",
            title="4. Maxwell-Gleichung (Ampère-Maxwell-Gesetz)",
            front="Wie lautet die **4. Maxwell-Gleichung (Durchflutungsgesetz mit Maxwellschem Verschiebungsstrom)** in differentieller Form?",
            back="""$$\\nabla \\times \\vec{B} = \\mu_0 \\vec{j} + \\mu_0 \\varepsilon_0 \\frac{\\partial \\vec{E}}{\\partial t}$$

Oder mit $c = \\frac{1}{\\sqrt{\\varepsilon_0 \\mu_0}}$:
$$\\nabla \\times \\vec{B} = \\mu_0 \\vec{j} + \\frac{1}{c^2} \\frac{\\partial \\vec{E}}{\\partial t}$$""",
            hint="Welchen Term fügte Maxwell dem ursprünglichen Ampère-Gesetz hinzu, um die Ladungserhaltung zu gewährleisten?",
            formula_breakdown="""- $\\vec{B}$: Magnetische Flussdichte $[\\mathrm{T}]$
- $\\vec{j}$: Elektrische Stromdichte $[\\mathrm{A/m^2}]$
- $\\mu_0$: Magnetische Feldkonstante (Vakuum-Permeabilität) $= 4\\pi \\times 10^{-7} \\, \\mathrm{N/A^2}$
- $\\vec{j}_D = \\varepsilon_0 \\frac{\\partial \\vec{E}}{\\partial t}$: Maxwellscher Verschiebungsstrom
- $c$: Vakuum-Lichtgeschwindigkeit $\\approx 3 \\times 10^8 \\, \\mathrm{m/s}$""",
            physical_meaning="Magnetische Wirbelfelder entstehen sowohl durch echte elektrische Ströme $\\vec{j}$ als auch durch zeitlich veränderliche elektrische Felder (Verschiebungsstrom). Erst dieser Term ermöglicht die Existenz elektromagnetischer Wellen!",
            validity_domain="Klassische Elektrodynamik im Vakuum.",
            tags=["Maxwell", "Verschiebungsstrom", "Ampere", "Licht"],
            difficulty=3,
        ),
        Card(
            id="em_lorentz_force",
            deck_id="elektrodynamik",
            title="Lorentzkraft",
            front="Wie lautet die Formel für die **Lorentzkraft** auf eine Punktladung $q$ im elektromagnetischen Feld?",
            back="""$$\\vec{F}_L = q \\left( \\vec{E} + \\vec{v} \\times \\vec{B} \\right)$$""",
            hint="Setzt sich aus elektrischem Anteil und geschwindigkeitsabhängigem magnetischem Kreuzprodukt zusammen.",
            formula_breakdown="""- $\\vec{F}_L$: Kraft auf die Ladung $[\\mathrm{N}]$
- $q$: Elektrische Ladung $[\\mathrm{C}]$
- $\\vec{E}$: Elektrisches Feld $[\\mathrm{V/m}]$
- $\\vec{v}$: Geschwindigkeit des Teilchens $[\\mathrm{m/s}]$
- $\\vec{B}$: Magnetische Flussdichte $[\\mathrm{T}]$""",
            physical_meaning="Der magnetische Teil $q(\\vec{v} \\times \\vec{B})$ steht stets senkrecht auf der Bewegungsrichtung $\\vec{v}$ und leistet daher keine Arbeit (verändert nur die Richtung, nicht die kinetische Energie).",
            validity_domain="Gilt für beliebige Teilchengeschwindigkeiten $v < c$ (bei relativistischer Mechanik ist $\\vec{F} = \\frac{d\\vec{p}}{dt}$ mit relativistischem Impuls $\\vec{p} = \\gamma m \\vec{v}$).",
            tags=["Kräfte", "Lorentz", "Elektrodynamik"],
            difficulty=1,
        ),
        Card(
            id="em_continuity",
            deck_id="elektrodynamik",
            title="Kontinuitätsgleichung der elektrischen Ladung",
            front="Wie lautet die **Kontinuitätsgleichung** für Ladungs- und Stromdichte in differentieller Form?",
            back="""$$\\nabla \\cdot \\vec{j} + \\frac{\\partial \\rho}{\\partial t} = 0$$

In 4er-Schreibweise:
$$\\partial_\\mu j^\\mu = 0$$""",
            hint="Ausdruck der lokalen Ladungserhaltung.",
            formula_breakdown="""- $\\vec{j}$: Elektrische Stromdichte $[\\mathrm{A/m^2}]$
- $\\nabla \\cdot \\vec{j}$: Divergenz (Nettoausstrom von Strom pro Volumeneinheit)
- $\\rho$: Raumladungsdichte $[\\mathrm{C/m^3}]$
- $\\partial_\\mu j^\\mu$: 4er-Divergenz des 4er-Stroms $j^\\mu = (c\\rho, \\vec{j})$""",
            physical_meaning="Ladung kann weder aus dem Nichts entstehen noch vernichtet werden. Eine Änderung der Ladung in einem Volumen erfordert zwingend einen messbaren Strom durch dessen Rand.",
            validity_domain="Exakt und fundamental in der gesamten Physik.",
            tags=["Ladungserhaltung", "Kontinuität", "Erhaltungssatz"],
            difficulty=2,
        ),
        Card(
            id="em_poynting",
            deck_id="elektrodynamik",
            title="Poynting-Vektor",
            front="Wie lautet die Definition des **Poynting-Vektors** $\\vec{S}$ und was beschreibt er physikalisch?",
            back="""$$\\vec{S} = \\frac{1}{\\mu_0} \\left( \\vec{E} \\times \\vec{B} \\right)$$

In Medien: $\\vec{S} = \\vec{E} \\times \\vec{H}$""",
            hint="Kreuzprodukt aus E- und B-Feld.",
            formula_breakdown="""- $\\vec{S}$: Poynting-Vektor (Energiejoule pro Sekunde und Fläche) $[\\mathrm{W/m^2}]$
- $\\vec{E}$: Elektrisches Feld $[\\mathrm{V/m}]$
- $\\vec{B}$: Magnetische Flussdichte $[\\mathrm{T}]$
- $\\mu_0$: Vakuum-Permeabilität $[\\mathrm{N/A^2}]$""",
            physical_meaning="Gibt die Richtung und den Betrag des elektromagnetischen Energietransports (Energieflussdichte) an. Die Strahlungsintensität einer Welle ist der zeitliche Mittelwert $\\langle |\\vec{S}| \\rangle$.",
            validity_domain="Klassische Elektrodynamik.",
            tags=["Energiefluss", "Optik", "Strahlung"],
            difficulty=2,
        ),
        # ==========================================
        # QUANTENMECHANIK
        # ==========================================
        Card(
            id="qm_postulate_1",
            deck_id="quantenmechanik",
            title="1. Postulat der Quantenmechanik: Der Zustandsraum",
            front="Wie lautet das **1. Postulat der Quantenmechanik (Zustandsraum)**?",
            back="""Der Zustand eines physikalischen Systems wird vollständig beschrieben durch einen normierten Zustandsvektor (Strahl) $\\ket{\\psi}$ in einem komplexen Hilbertraum $\\mathcal{H}$:

$$\\ket{\\psi} \\in \\mathcal{H}, \\quad \\langle \\psi | \\psi \\rangle = 1$$

Zwei Vektoren, die sich nur um einen globalen Phasenfaktor $e^{i\\alpha}$ unterscheiden, beschreiben denselben physikalischen Zustand.""",
            hint="Hilbertraum, Superpositionsprinzip, Bra-Ket-Notation.",
            formula_breakdown="""- $\\mathcal{H}$: Vollständiger Vektorraum mit Skalarprodukt (Hilbertraum)
- $\\ket{\\psi}$: Dirac-Ket-Vektor (Zustand)
- $\\langle \\psi | \\psi \\rangle$: Skalarprodukt (Normierung auf 1 gewährleistet Gesamtwahrscheinlichkeit 100%)""",
            physical_meaning="Linearität impliziert das fundamentale Superpositionsprinzip: Wenn $\\ket{\\psi_1}$ und $\\ket{\\psi_2}$ mögliche Zustände sind, ist auch jede Linearkombination $c_1\\ket{\\psi_1} + c_2\\ket{\\psi_2}$ ein möglicher Zustand.",
            validity_domain="Gilt universell in der nicht-relativistischen und relativistischen Quantentheorie.",
            tags=["Postulate", "Hilbertraum", "Grundlagen"],
            difficulty=3,
        ),
        Card(
            id="qm_postulate_2",
            deck_id="quantenmechanik",
            title="2. Postulat der Quantenmechanik: Observablen",
            front="Wie lautet das **2. Postulat der Quantenmechanik (Physikalische Observablen)**?",
            back="""Jeder messbaren physikalischen Größe (Observable $\\mathcal{A}$) entspricht ein **linearer, selbstadjungierter (hermitescher) Operator** $\\hat{A}$ auf dem Hilbertraum $\\mathcal{H}$:

$$\\hat{A} = \\hat{A}^\\dagger$$

Die möglichen Messergebnisse sind ausschließlich die reellen Eigenwerte $a_n$ der Eigenwertgleichung:
$$\\hat{A} \\ket{\\phi_n} = a_n \\ket{\\phi_n}, \\quad a_n \\in \\mathbb{R}$$""",
            hint="Warum müssen die Operatoren hermitesch sein?",
            formula_breakdown="""- $\\hat{A}^\\dagger$: Adjungierter Operator $(\\langle \\phi | \\hat{A} \\psi \\rangle = \\langle \\hat{A}^\\dagger \\phi | \\psi \\rangle)$
- $\\ket{\\phi_n}$: Eigenzustand zum Eigenwert $a_n$
- $a_n$: Messwert (reell)""",
            physical_meaning="Hermitesche Operatoren garantieren, dass alle Eigenwerte reell sind (echte Messgrößen müssen reelle Zahlen sein) und die Eigenvektoren eine orthogonale Basis bilden.",
            validity_domain="Standard-Quantenmechanik (in neueren offenen Systemen werden auch PT-symmetrische oder nicht-hermitesche effektive Hamiltonians untersucht).",
            tags=["Postulate", "Operatoren", "Hermitesch"],
            difficulty=3,
        ),
        Card(
            id="qm_postulate_3",
            deck_id="quantenmechanik",
            title="3. Postulat der Quantenmechanik: Bornsche Wahrscheinlichkeitsregel",
            front="Wie lautet das **3. Postulat der Quantenmechanik (Bornsche Regel & Messung)**?",
            back="""Befindet sich ein System im Zustand $\\ket{\\psi}$, so ist die Wahrscheinlichkeit $P(a_n)$, bei einer Messung von $\\hat{A}$ den diskreten Eigenwert $a_n$ zu finden:

$$P(a_n) = |\\langle \\phi_n | \\psi \\rangle|^2$$

Direkt nach der Messung kollabiert der Zustand auf den entsprechenden Eigenzustand (Projektionspostulat / von-Neumann-Reduktion):
$$\\ket{\\psi} \\xrightarrow{\\text{Messung } a_n} \\ket{\\phi_n}$$""",
            hint="Projektionsoperator, Wahrscheinlichkeitsamplitude und Zustandskollaps.",
            formula_breakdown="""- $\\langle \\phi_n | \\psi \\rangle$: Wahrscheinlichkeitsamplitude (Überlappung)
- $|\\langle \\phi_n | \\psi \\rangle|^2$: Wahrscheinlichkeitsdichte nach Max Born
- Für kontinuierliche Spektren: $P(x)dx = |\\psi(x)|^2 dx$""",
            physical_meaning="Der Ausgang einer Quantenmessung ist fundamental probabilistisch (nicht durch unvollständiges Wissen determiniert). Der Messprozess verändert das System irreversibel.",
            validity_domain="Kopenhagener Interpretation der Quantenmechanik.",
            tags=["Postulate", "Born", "Messprozess", "Kollaps"],
            difficulty=4,
        ),
        Card(
            id="qm_postulate_4",
            deck_id="quantenmechanik",
            title="4. Postulat der Quantenmechanik: Zeitentwicklung (Schrödinger-Gleichung)",
            front="Wie lautet die **zeitabhängige Schrödinger-Gleichung** für die Zeitentwicklung eines quantenmechanischen Zustands $\\ket{\\psi(t)}$?",
            back="""$$i\\hbar \\frac{d}{dt} \\ket{\\psi(t)} = \\hat{H} \\ket{\\psi(t)}$$

In Ortsdarstellung für ein Teilchen der Masse $m$ im Potenzial $V(\\vec{r}, t)$:
$$i\\hbar \\frac{\\partial \\psi(\\vec{r}, t)}{\\partial t} = \\left( -\\frac{\\hbar^2}{2m} \\nabla^2 + V(\\vec{r}, t) \\right) \\psi(\\vec{r}, t)$$""",
            hint="Welcher Operator generiert die zeitliche Translation?",
            formula_breakdown="""- $i$: Imaginäre Einheit ($i^2 = -1$)
- $\\hbar = \\frac{h}{2\\pi}$: Reduziertes Plancksches Wirkungsquantum $\\approx 1{,}05457 \\times 10^{-34} \\, \\mathrm{J\\cdot s}$
- $\\hat{H}$: Hamilton-Operator (Gesamtenergieoperator)
- $\\nabla^2 = \\Delta$: Laplace-Operator""",
            physical_meaning="Die Zeitentwicklung ist deterministisch und unitär (Wahrscheinlichkeitserhaltung), solange keine Messung stattfindet. Der Zeitentwicklungsoperator ist $\\hat{U}(t) = \\exp(-i\\hat{H}t / \\hbar)$.",
            validity_domain="Nicht-relativistische Quantenmechanik ($v \\ll c$). Für relativistische Spin-1/2-Teilchen: Dirac-Gleichung.",
            tags=["Schrödinger", "Postulate", "Zeitentwicklung", "Hamiltonian"],
            difficulty=3,
        ),
        Card(
            id="qm_uncertainty",
            deck_id="quantenmechanik",
            title="Heisenbergsche Unschärferelation",
            front="Wie lautet die **Heisenbergsche Unschärferelation** für Ort und Impuls und ihre **allgemeine Form (Robertson-Relation)** für beliebige zwei Observablen $\\hat{A}$ und $\\hat{B}$?",
            back="""**Ort und Impuls:**
$$\\Delta x \\cdot \\Delta p \\ge \\frac{\\hbar}{2}$$

**Allgemeine Robertson-Relation:**
$$\\Delta A \\cdot \\Delta B \\ge \\frac{1}{2} \\left| \\langle [\\hat{A}, \\hat{B}] \\rangle \\right|$$

wobei $[\\hat{A}, \\hat{B}] = \\hat{A}\\hat{B} - \\hat{B}\\hat{A}$ der Kommutator ist.""",
            hint=r"Aus $[\hat{x}, \hat{p}] = i\hbar$ folgt direkt das Produkt der Standardabweichungen.",
            formula_breakdown="""- $\\Delta A = \\sqrt{\\langle \\hat{A}^2 \\rangle - \\langle \\hat{A} \\rangle^2}$: Standardabweichung (Unschärfe)
- $[\\hat{x}, \\hat{p}] = i\\hbar \\hat{\\mathbb{I}}$: Kanonische Vertauschungsrelation
- $\\langle \\dots \\rangle$: Quantenmechanischer Erwartungswert""",
            physical_meaning="Zwei physikalische Größen können nur dann gleichzeitig beliebig scharf präpariert und gemessen werden, wenn ihre Operatoren kommutieren ($[\\hat{A}, \\hat{B}] = 0$).",
            validity_domain="Universell in allen quantenmechanischen Systemen.",
            tags=["Unschärfe", "Heisenberg", "Kommutator"],
            difficulty=3,
        ),
        # ==========================================
        # THERMODYNAMIK & STATISTIK
        # ==========================================
        Card(
            id="stat_gauss",
            deck_id="thermodynamik",
            title="Gaußsche Normalverteilung (Wahrscheinlichkeitsdichte)",
            front="Wie lautet die mathematische Formel der **eindimensionalen Gaußschen Normalverteilung** $\\mathcal{N}(\\mu, \\sigma^2)$ mit Erwartungswert $\\mu$ und Standardabweichung $\\sigma$?",
            back="""$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} \\exp \\left( -\\frac{(x - \\mu)^2}{2\\sigma^2} \\right)$$

Normierungsbedingung:
$$\\int_{-\\infty}^{+\\infty} f(x) \\, dx = 1$$""",
            hint="Exponentielle Glockenkurve mit quadratischem Exponenten und Vorfaktor zur Normierung.",
            formula_breakdown="""- $f(x)$: Wahrscheinlichkeitsdichtefunktion
- $\\mu = \\mathbb{E}[X]$: Erwartungswert (Mittelwert / Symmetriezentrum)
- $\\sigma$: Standardabweichung (Breite der Kurve)
- $\\sigma^2 = \\text{Var}(X)$: Varianz
- Wendepunkte der Glockenkurve liegen exakt bei $x = \\mu \\pm \\sigma$""",
            physical_meaning="Zentraler Grenzwertsatz: Die Summe einer großen Anzahl unabhängiger Zufallsvariablen nähert sich stets einer Normalverteilung an. Beschreibt Brownsche Bewegung, Messfehler und thermisches Rauschen.",
            validity_domain="Mathematische Statistik; kontinuierliche Verteilungen.",
            tags=["Gauß", "Normalverteilung", "Statistik", "Formel"],
            difficulty=2,
        ),
        Card(
            id="stat_boltzmann_entropy",
            deck_id="thermodynamik",
            title="Boltzmannsche Entropieformel",
            front="Wie lautet die berühmte **Boltzmann-Formel für die statistische Entropie** $S$ eines mikrokanonischen Ensembles?",
            back="""$$S = k_B \\ln \\Omega$$""",
            hint=r"Verknüpft makroskopische Thermodynamik mit der mikroskopischen Anzahl an Zuständen $\Omega$.",
            formula_breakdown="""- $S$: Thermodynamische Entropie $[\\mathrm{J/K}]$
- $k_B$: Boltzmann-Konstante $\\approx 1{,}380649 \\times 10^{-23} \\, \\mathrm{J/K}$
- $\\Omega$: Thermodynamische Wahrscheinlichkeit (Anzahl der zugänglichen Mikrozustände zum gegebenen Makrozustand)""",
            physical_meaning="Entropie ist ein logarithmisches Maß für die Anzahl der Mikrozustände, die denselben Makrozustand realisieren. Der 2. Hauptsatz ($dS \\ge 0$) bedeutet mikroskopisch den Übergang zu wahrscheinlicheren Makrozuständen mit größerem $\\Omega$.",
            validity_domain="Mikrokanonisches Ensemble (isolierte Systeme mit fester Energie, Volumen und Teilchenzahl).",
            tags=["Entropie", "Boltzmann", "Statistische Physik"],
            difficulty=2,
        ),
        Card(
            id="td_laws",
            deck_id="thermodynamik",
            title="Die vier Hauptsätze der Thermodynamik",
            front="Nenne die Kernaussagen der **vier Hauptsätze der Thermodynamik (0., 1., 2. und 3. Hauptsatz)**!",
            back="""- **0. Hauptsatz (Thermisches Gleichgewicht):**
  Stehen zwei Systeme A und B jeweils mit einem dritten System C im thermischen Gleichgewicht, so stehen sie auch untereinander im thermischen Gleichgewicht (Grundlage der Temperaturmessung).

- **1. Hauptsatz (Energieerhaltung):**
  $$dU = \\delta Q + \\delta W = T dS - p dV$$
  Die innere Energie eines abgeschlossenen Systems ist konstant.

- **2. Hauptsatz (Entropiesatz):**
  $$dS \\ge \\frac{\\delta Q}{T}, \\quad \\Delta S_{\\text{abgeschlossen}} \\ge 0$$
  Wärme fließt niemals spontan von kälteren zu wärmeren Körpern (kein Perpetuum Mobile 2. Art).

- **3. Hauptsatz (Nernst-Theorem):**
  $$\\lim_{T \\to 0} S = 0$$
  Der absolute Nullpunkt der Temperatur ($0 \\, \\mathrm{K}$) ist prinzipiell unerreichbar.""",
            hint="0: Temperatur existiert; 1: Energieerhaltung; 2: Irreversibilität & Entropie; 3: Absoluter Nullpunkt.",
            formula_breakdown="""- $U$: Innere Energie $[\\mathrm{J}]$
- $Q$: Wärme $[\\mathrm{J}]$
- $W$: Mechanische Arbeit $[\\mathrm{J}]$
- $T$: Absolute Temperatur $[\\mathrm{K}]$
- $S$: Entropie $[\\mathrm{J/K}]$""",
            physical_meaning="Fundamentale Säulen der klassischen Wärmelehre, die Richtung von Prozessen und energetische Grenzen von Wärmekraftmaschinen (Carnot-Wirkungsgrad $\\eta = 1 - \\frac{T_{\\text{kalt}}}{T_{\\text{heiß}}}$) festlegen.",
            validity_domain="Makroskopische thermodynamische Systeme im Gleichgewicht.",
            tags=["Hauptsätze", "Thermodynamik", "Energie", "Entropie"],
            difficulty=3,
        ),
        # ==========================================
        # KLASSISCHE MECHANIK
        # ==========================================
        Card(
            id="mech_newton_axioms",
            deck_id="mechanik",
            title="Die 3 Newtonschen Axiome",
            front="Wie lauten die **drei Newtonschen Gesetze (Axiome der klassischen Mechanik)** in Worten und Formeln?",
            back="""1. **1. Axiom (Trägheitsprinzip / Lex Prima):**
   Ein Körper verharrt im Zustand der Ruhe oder der gleichförmig geradlinigen Bewegung, solange keine resultierende äußere Kraft auf ihn wirkt:
   $$\\sum \\vec{F} = 0 \\implies \\vec{v} = \\text{const.}$$

2. **2. Axiom (Aktionsprinzip / Lex Secunda):**
   Die zeitliche Änderung des Impulses ist gleich der wirkenden Gesamtkraft:
   $$\\vec{F} = \\frac{d\\vec{p}}{dt} = \\frac{d(m\\vec{v})}{dt}$$
   (Bei konstanter Masse $m$: $\\vec{F} = m \\cdot \\vec{a} = m \\ddot{\\vec{r}}$)

3. **3. Axiom (Reaktionsprinzip / Lex Tertia / Actio = Reactio):**
   Kräfte treten immer paarweise auf: Übt Körper 1 eine Kraft auf Körper 2 aus, so übt Körper 2 eine gleich große, entgegengesetzte Gegenkraft auf Körper 1 aus:
   $$\\vec{F}_{12} = -\\vec{F}_{21}$$""",
            hint="Trägheit, Kraft = Masse mal Beschleunigung, Actio = Reactio.",
            formula_breakdown="""- $\\vec{p} = m\\vec{v}$: Impuls $[\\mathrm{kg\\cdot m / s}]$
- $\\vec{a} = \\ddot{\\vec{r}}$: Beschleunigung $[\\mathrm{m/s^2}]$
- $\\vec{F}$: Kraft $[\\mathrm{N} = \\mathrm{kg\\cdot m / s^2}]$""",
            physical_meaning="Basis der klassischen Mechanik. Aus dem 3. Axiom folgt unmittelbar der Gesamtimpulserhaltungssatz abgeschlossener Systeme.",
            validity_domain="Inertialsysteme; nicht-relativistische Geschwindigkeiten ($v \\ll c$); makroskopische Skalen (keine Quanteneffekte).",
            tags=["Newton", "Axiome", "Mechanik", "Impuls"],
            difficulty=1,
        ),
        Card(
            id="mech_lagrange_2",
            deck_id="mechanik",
            title="Lagrange-Gleichungen 2. Art",
            front="Wie lauten die **Lagrange-Gleichungen 2. Art** und wie ist die Lagrange-Funktion $L$ definiert?",
            back="""Lagrange-Funktion:
$$L(q_i, \\dot{q}_i, t) = T - V$$

Lagrange-Gleichungen 2. Art (Euler-Lagrange-Gleichungen):
$$\\frac{d}{dt} \\left( \\frac{\\partial L}{\\partial \\dot{q}_i} \\right) - \\frac{\\partial L}{\\partial q_i} = 0 \\quad (i = 1, \\dots, f)$$""",
            hint="Differenz aus kinetischer und potenzieller Energie im Raum generalisierter Koordinaten.",
            formula_breakdown="""- $q_i$: Generalisierte Koordinate (Freiheitsgrad $i$)
- $\\dot{q}_i = \\frac{dq_i}{dt}$: Generalisierte Geschwindigkeit
- $T$: Kinetische Energie $[\\mathrm{J}]$
- $V$: Potenzielle Energie $[\\mathrm{J}]$
- $f$: Anzahl der Freiheitsgrade des Systems""",
            physical_meaning="Folgt aus dem Hamiltonschen Prinzip der kleinsten Wirkung ($\\delta S = \\delta \\int L dt = 0$). Eliminiert Zwangskräfte automatisch durch geschickte Wahl verallgemeinerter Koordinaten.",
            validity_domain="Holonome, skleronome und rheonome Zwangsbedingungen; konservative Kräfte (für Reibung: Rayleighsche Dissipationsfunktion ergänzbar).",
            tags=["Lagrange", "Analytische Mechanik", "Euler-Lagrange", "Wirkung"],
            difficulty=3,
        ),
        Card(
            id="mech_hamilton_equations",
            deck_id="mechanik",
            title="Kanonische Hamiltonsche Bewegungsgleichungen",
            front="Wie lauten die **kanonischen Hamiltonschen Bewegungsgleichungen** und wie hängen die generalisierten Impulse $p_i$ mit $L$ zusammen?",
            back="""Kanonischer Impuls:
$$p_i = \\frac{\\partial L}{\\partial \\dot{q}_i}$$

Hamilton-Funktion (Legendre-Transformation):
$$H(q_i, p_i, t) = \\sum_{i=1}^f p_i \\dot{q}_i - L = T + V$$

Kanonische Gleichungen:
$$\\dot{q}_i = \\frac{\\partial H}{\\partial p_i}, \\qquad \\dot{p}_i = -\\frac{\\partial H}{\\partial q_i}$$""",
            hint="Zwei Differenzialgleichungen 1. Ordnung im Phasenraum anstelle einer 2. Ordnung.",
            formula_breakdown="""- $q_i, p_i$: Kanonisch konjugiertes Variablenpaar (Orte und Impulse)
- $H$: Gesamtenergie des Systems (bei zeitinvarianten Zwangsbedingungen)
- Phasenraum: $2f$-dimensionaler Raum aller Zustände $(q, p)$""",
            physical_meaning="Symmetrische Beschreibung der Dynamik im Phasenraum. Direkter Übergang zur Quantenmechanik über Korrespondenzprinzip (Poisson-Klammern $\\to$ Kommutatoren).",
            validity_domain="Konservative Systeme der klassischen analytischen Mechanik.",
            tags=["Hamilton", "Kanonisch", "Phasenraum"],
            difficulty=3,
        ),
        # ==========================================
        # RELATIVITÄTSTHEORIE
        # ==========================================
        Card(
            id="rel_lorentz_transformation",
            deck_id="relativitaet",
            title="Spezielle Lorentz-Transformation",
            front="Wie lauten die Formeln der **speziellen Lorentz-Transformation** für Raum und Zeit bei einem Boost mit Relativgeschwindigkeit $v$ entlang der $x$-Achse?",
            back="""$$x' = \\gamma (x - v t)$$
$$y' = y$$
$$z' = z$$
$$t' = \\gamma \\left( t - \\frac{v x}{c^2} \\right)$$

mit dem Lorentz-Faktor:
$$\\gamma = \\frac{1}{\\sqrt{1 - \\frac{v^2}{c^2}}}$$""",
            hint="Ersetzt die Galilei-Transformation, damit die Maxwell-Gleichungen und die Lichtgeschwindigkeit invariant bleiben.",
            formula_breakdown="""- $\\gamma \\ge 1$: Lorentz-Faktor
- $c$: Vakuumlichtgeschwindigkeit $\\approx 299\\,792\\,458 \\, \\mathrm{m/s}$
- $v$: Relativgeschwindigkeit zweier Inertialsysteme ($v < c$)
- Für $v \\ll c$: $\\gamma \\to 1$ und $t' \\to t$ (Galilei-Grenzfall)""",
            physical_meaning="Raum und Zeit sind untrennbar zu einer 4-dimensionalen Raumzeit verknüpft. Gleichzeitigkeit ist relativ! Führt zur Zeitdilatation (bewegte Uhren gehen langsamer) und Längenkontraktion.",
            validity_domain="Spezielle Relativitätstheorie (flache Minkowski-Raumzeit, kräftefreie Inertialsysteme).",
            tags=["SRT", "Lorentz", "Raumzeit", "Lichtgeschwindigkeit"],
            difficulty=2,
        ),
        Card(
            id="rel_energy_momentum",
            deck_id="relativitaet",
            title="Relativistische Energie-Impuls-Relation",
            front="Wie lautet die vollständige **relativistische Energie-Impuls-Beziehung**?",
            back="""$$E^2 = (p c)^2 + (m_0 c^2)^2$$

Oder als 4er-Impuls-Norm:
$$P_\\mu P^\\mu = m_0^2 c^2$$

Für ruhende Teilchen ($p = 0$):
$$E_0 = m_0 c^2$$""",
            hint="Gilt für massebehaftete Teilchen ebenso wie für masselose Photonen ($m_0 = 0$).",
            formula_breakdown="""- $E$: Gesamtenergie des Teilchens $[\\mathrm{J}]$
- $p$: Betrag des relativistischen 3er-Impulses $[\\mathrm{kg\\cdot m/s}]$
- $m_0$: Ruhemasse (invariante Masse) $[\\mathrm{kg}]$
- $c$: Lichtgeschwindigkeit $[\\mathrm{m/s}]$
- Für Photonen ($m_0 = 0$): $E = p c = h \\nu$""",
            physical_meaning="Masse ist eine Form von kondensierter Energie (Äquivalenz von Masse und Energie). Masselose Teilchen wie Photonen tragen stets Impuls $p = E/c$.",
            validity_domain="Spezielle und Allgemeine Relativitätstheorie.",
            tags=["SRT", "Energie", "Impuls", "Einstein"],
            difficulty=2,
        ),
        # ==========================================
        # MATHEMATISCHE METHODEN
        # ==========================================
        Card(
            id="math_gauss_theorem",
            deck_id="mathe_physik",
            title="Gaußscher Integralsatz (Divergenzsatz)",
            front="Wie lautet der **Gaußsche Integralsatz** (Divergenzsatz) für ein glattes Vektorfeld $\\vec{F}$ über ein Volumen $V$ mit Randfläche $\\partial V$?",
            back="""$$\\iiint_V (\\nabla \\cdot \\vec{F}) \\, dV = \\oiint_{\\partial V} \\vec{F} \\cdot d\\vec{A}$$""",
            hint="Verknüpft ein Volumenintegral über die Divergenz mit einem geschlossenen Oberflächenintegral.",
            formula_breakdown="""- $\\vec{F}$: Differenzierbares Vektorfeld
- $\\nabla \\cdot \\vec{F} = \\text{div} \\vec{F} = \\frac{\\partial F_x}{\\partial x} + \\frac{\\partial F_y}{\\partial y} + \\frac{\\partial F_z}{\\partial z}$: Divergenz (Quellendichte)
- $dV = dx\\,dy\\,dz$: Volumenelement
- $d\\vec{A} = \\vec{n} \\, dA$: Nach außen normalisiertes Flächenelement""",
            physical_meaning="Die Gesamtheit aller im Inneren eines Volumens erzeugten Feldlinien (Quellen) entspricht exakt dem Nettofluss des Feldes durch die umschließende Hülle nach außen.",
            validity_domain="Kompakte Volumina mit stückweise glattem Rand im $\\mathbb{R}^3$ (Spezialfall des allgemeinen Stokes-Theorems für Differentialformen: $\\int_M d\\omega = \\int_{\\partial M} \\omega$).",
            tags=["Vektoranalysis", "Gauß", "Integralsatz", "Divergenz"],
            difficulty=2,
        ),
        Card(
            id="math_stokes_theorem",
            deck_id="mathe_physik",
            title="Stokesscher Integralsatz (Rotationssatz)",
            front="Wie lautet der **Stokessche Integralsatz** (Kelvin-Stokes-Satz) für ein Vektorfeld $\\vec{F}$ auf einer Fläche $S$ mit Randkurve $\\partial S$?",
            back="""$$\\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{A} = \\oint_{\\partial S} \\vec{F} \\cdot d\\vec{r}$$""",
            hint="Verknüpft die Flächenintegration über die Rotation mit dem geschlossenen Wegintegral entlang des Randes.",
            formula_breakdown="""- $\\nabla \\times \\vec{F} = \\text{rot} \\vec{F}$: Rotation (Wirbeldichte) des Vektorfeldes
- $d\\vec{A} = \\vec{n} \\, dA$: Orientiertes Flächenelement
- $d\\vec{r}$: Tangentialer Wegevektor entlang der Randkurve $\\partial S$
- Orientierung: Rechte-Hand-Regel (Daumen in Richtung $\\vec{n}$, Finger in Umlaufrichtung)""",
            physical_meaning="Die Summe aller mikroskopischen Wirbel auf einer Fläche summiert sich zu einer makroskopischen Zirkulation entlang des Randes auf (innere Wirbel kompensieren sich gegenseitig).",
            validity_domain="Orientierbare Flächen mit stückweise glatter geschlossener Randkurve im $\\mathbb{R}^3$.",
            tags=["Vektoranalysis", "Stokes", "Integralsatz", "Rotation"],
            difficulty=2,
        ),
        Card(
            id="math_dirac_delta",
            deck_id="mathe_physik",
            title="Diracsche Delta-Distribution",
            front="Wie ist die **Dirac-Delta-Distribution** $\\delta(x - x_0)$ durch ihre Siebeigenschaft definiert?",
            back="""Für jede stetige Testfunktion $\\phi(x)$:

$$\\int_{-\\infty}^{+\\infty} \\phi(x) \\, \\delta(x - x_0) \\, dx = \\phi(x_0)$$

Eigenschaften:
$$\\delta(x - x_0) = 0 \\quad \\text{für } x \\neq x_0, \\qquad \\int_{-\\infty}^{+\\infty} \\delta(x) \\, dx = 1$$
$$\\delta(a x) = \\frac{1}{|a|} \\delta(x)$$""",
            hint="Verallgemeinerte Funktion (Distribution), die unendlich hoch und unendlich schmal ist.",
            formula_breakdown="""- $\\delta(x)$: Keine gewöhnliche Funktion, sondern lineares Funktional auf dem Raum der Schwartz-Testfunktionen
- In 3D: $\\delta(\\vec{r}) = \\delta(x)\\delta(y)\\delta(z)$
- Darstellung einer Punktladung: $\\rho(\\vec{r}) = q \\, \\delta(\\vec{r} - \\vec{r}_0)$""",
            physical_meaning="Ermöglicht die mathematisch saubere Modellierung idealisierter Punktmassen, Punktladungen oder impulsiver Stöße in infinitesimaler Zeit.",
            validity_domain="Distributionentheorie nach Laurent Schwartz.",
            tags=["Distribution", "Dirac-Delta", "Mathematische Methoden"],
            difficulty=2,
        ),
        Card(
            id="qm_postulate_5",
            deck_id="quantenmechanik",
            title="5. Postulat der Quantenmechanik: Identische Teilchen (Symmetrisierung)",
            front="Wie lautet das **Symmetrisierungspostulat für identische Teilchen** in der Quantenmechanik und wie unterscheidet es **Bosonen** und **Fermionen**?",
            back=r"""Der Gesamtzustand eines Systems identischer Teilchen ist unter Vertauschung zweier Teilchen $i \leftrightarrow j$ entweder **vollständig symmetrisch** (Bosonen) oder **vollständig antisymmetrisch** (Fermionen):

$$\hat{P}_{ij} \ket{\psi(1, \dots, i, \dots, j, \dots, N)} = \pm \ket{\psi(1, \dots, i, \dots, j, \dots, N)}$$

- **Bosonen** ($+$): ganzzahliger Spin ($s = 0, 1, 2, \dots$), Bose-Einstein-Statistik (z.B. Photonen, Gluonen, $^4\text{He}$).
- **Fermionen** ($-$): halbzahlig ungerader Spin ($s = 1/2, 3/2, \dots$), Fermi-Dirac-Statistik (z.B. Elektronen, Quarks, Protonen, Neutronen).""",
            hint=r"Pauli-Prinzip: Zwei identische Fermionen können nicht denselben Quantenzustand besetzen.",
            formula_breakdown=r"""- $\hat{P}_{ij}$: Permutations- bzw. Vertauschungsoperator
- Antisymmetrie impliziert für Fermionen im selben Einteilchenzustand: $\ket{\psi} = -\ket{\psi} \implies \ket{\psi} = 0$ (Pauli-Verbot)
- Slater-Determinante zur Konstruktion antisymmetrischer Vielteilchen-Wellenfunktionen""",
            physical_meaning="Erklärt den Aufbau des Periodensystems der Elemente, die Stabilität der Materie, die Chandrasekhar-Grenzmasse Weißer Zwerge und Phänomene wie Suprafluidität / Bose-Einstein-Kondensation.",
            validity_domain="Fundamentales Spin-Statistik-Theorem der relativistischen Quantenfeldtheorie.",
            tags=["Postulate", "Fermionen", "Bosonen", "Pauli-Prinzip"],
            difficulty=4,
        ),
        Card(
            id="qm_ladder_operators",
            deck_id="quantenmechanik",
            title="Leiteroperatoren des harmonischen Oszillators",
            front=r"Wie sind die **Erzeugungs- und Vernichtungsoperatoren** $(\hat{a}^\dagger, \hat{a})$ des quantenmechanischen harmonischen Oszillators definiert und wie lautet ihr **Kommutator**?",
            back=r"""Vernichtungsoperator $\hat{a}$ und Erzeugungsoperator $\hat{a}^\dagger$:
$$\hat{a} = \sqrt{\frac{m\omega}{2\hbar}} \left( \hat{x} + \frac{i}{m\omega} \hat{p} \right), \qquad \hat{a}^\dagger = \sqrt{\frac{m\omega}{2\hbar}} \left( \hat{x} - \frac{i}{m\omega} \hat{p} \right)$$

Kanonische Vertauschungsrelation:
$$[\hat{a}, \hat{a}^\dagger] = \hat{a}\hat{a}^\dagger - \hat{a}^\dagger \hat{a} = 1$$

Hamilton-Operator mit Besetzungszahloppertor $\hat{N} = \hat{a}^\dagger \hat{a}$:
$$\hat{H} = \hbar\omega \left( \hat{a}^\dagger \hat{a} + \frac{1}{2} \right) = \hbar\omega \left( \hat{N} + \frac{1}{2} \right)$$""",
            hint=r"Wirkung auf Fock-Zustände: $\hat{a}\ket{n} = \sqrt{n}\ket{n-1}$, $\hat{a}^\dagger\ket{n} = \sqrt{n+1}\ket{n+1}$.",
            formula_breakdown=r"""- $E_n = \hbar\omega(n + 1/2)$: Diskrete Energie-Eigenwerte ($n = 0, 1, 2, \dots$)
- $E_0 = \frac{1}{2}\hbar\omega$: Nullpunktsenergie (Vakuumfluktuation)
- $\ket{0}$: Grundzustand definiert durch $\hat{a}\ket{0} = 0$""",
            physical_meaning="Algebraische Lösung des Oszillators ohne Differenzialgleichung. Grundstein für die 2. Quantisierung und Quantenfeldtheorie (Teilchenerzeugung und -vernichtung).",
            validity_domain=r"Harmonisches Potenzial $V(x) = \frac{1}{2}m\omega^2 x^2$.",
            tags=["Harmonischer Oszillator", "Leiteroperatoren", "Quantenmechanik"],
            difficulty=3,
        ),
        Card(
            id="qm_pauli_matrices",
            deck_id="quantenmechanik",
            title="Die drei Pauli-Spinmatrizen",
            front="Wie lauten die drei **Pauli-Spinmatrizen** $\\sigma_x, \\sigma_y, \\sigma_z$ in der Standard-z-Basis und wie hängen sie mit dem Spinoperator $\\hat{\\vec{S}}$ zusammen?",
            back=r"""$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

Spin-Operator für Spin-1/2:
$$\hat{\vec{S}} = \frac{\hbar}{2} \vec{\sigma} = \frac{\hbar}{2} (\sigma_x \vec{e}_x + \sigma_y \vec{e}_y + \sigma_z \vec{e}_z)$$

Eigenschaften:
$$\sigma_i^2 = \mathbb{I}, \quad \det(\sigma_i) = -1, \quad \text{Tr}(\sigma_i) = 0, \quad [\sigma_i, \sigma_j] = 2i \sum_k \varepsilon_{ijk} \sigma_k$$""",
            hint=r"Hermitesch, unitär und spurfrei.",
            formula_breakdown=r"""- $\sigma_x, \sigma_y, \sigma_z$: Generatoren der Gruppe $\text{SU}(2)$
- $\varepsilon_{ijk}$: Levi-Civita-Symbol
- Eigenwerte jeder Pauli-Matrix: $\pm 1$""",
            physical_meaning="Beschreiben den intrinsischen Drehimpuls (Spin) elementarer Spin-1/2-Teilchen (Elektronen, Quarks, Neutrinos) sowie 2-Niveau-Quantensysteme (Qubits im Quantencomputing).",
            validity_domain=r"Zweidimensionaler Spin-Hilbertraum $\mathbb{C}^2$.",
            tags=["Spin", "Pauli-Matrizen", "Qubit", "Quantenmechanik"],
            difficulty=3,
        ),
        Card(
            id="stat_maxwell_boltzmann",
            deck_id="thermodynamik",
            title="Maxwell-Boltzmann-Geschwindigkeitsverteilung",
            front="Wie lautet die **Maxwell-Boltzmann-Geschwindigkeitsverteilung** $f(v)$ für die Beträge der Geschwindigkeiten in einem klassischen idealen Gas?",
            back=r"""$$f(v) = 4\pi \left( \frac{m}{2\pi k_B T} \right)^{3/2} v^2 \exp \left( -\frac{m v^2}{2 k_B T} \right)$$""",
            hint=r"Zusammengesetzt aus 3D-Kugeloberfläche im Geschwindigkeitsraum ($4\pi v^2$) und Boltzmann-Faktor.",
            formula_breakdown=r"""- $f(v)dv$: Wahrscheinlichkeit, dass ein Teilchen einen Geschwindigkeitsbetrag zwischen $v$ und $v+dv$ hat
- $m$: Masse eines Gasteilchens $[\mathrm{kg}]$
- $k_B$: Boltzmann-Konstante $[\mathrm{J/K}]$
- $T$: Absolute Temperatur $[\mathrm{K}]$
- Wahrscheinlichste Geschwindigkeit: $v_{\text{mp}} = \sqrt{\frac{2k_B T}{m}}$
- Mittlere Geschwindigkeit: $\bar{v} = \sqrt{\frac{8k_B T}{\pi m}}$
- Quadratisch gemittelte Geschwindigkeit: $v_{\text{rms}} = \sqrt{\frac{3k_B T}{m}}$""",
            physical_meaning="Beschreibt die statistische Geschwindigkeitsverteilung thermischer Teilchen im thermischen Gleichgewicht. Die Kurve ist asymmetrisch mit einem langen Ausläufer zu hohen Geschwindigkeiten.",
            validity_domain="Klassisches ideales Gas im thermodynamischen Gleichgewicht ohne relativistische Effekte.",
            tags=["Statistik", "Maxwell-Boltzmann", "Geschwindigkeit", "Thermodynamik"],
            difficulty=3,
        ),
        Card(
            id="stat_equipartition",
            deck_id="thermodynamik",
            title="Äquipartitionstheorem (Gleichverteilungssatz)",
            front="Wie lautet das **Äquipartitionstheorem (Gleichverteilungssatz der klassischen statistischen Mechanik)**?",
            back=r"""Im thermischen Gleichgewicht bei Temperatur $T$ entfällt auf jeden quadratischen Freiheitsgrad im Hamilton-Operator im Mittel die Energie:

$$\langle E_i \rangle = \frac{1}{2} k_B T$$

Für ein Teilchen mit $f$ quadratischen Freiheitsgraden gilt für die mittlere Gesamtenergie:
$$\langle E \rangle = \frac{f}{2} k_B T, \qquad U = \frac{f}{2} N k_B T = \frac{f}{2} n R T$$""",
            hint=r"Pro Translations-, Rotations- und harmonischem Schwingungsfreiheitsgrad.",
            formula_breakdown=r"""- $f$: Anzahl der Freiheitsgrade (Einatomiges Gas: $f=3$ Translationen; zweiatomiges Gas bei Raumtemperatur: $f=5$, 3 Translationen + 2 Rotationen)
- $k_B$: Boltzmann-Konstante
- $T$: Absolute Temperatur $[\mathrm{K}]$
- Molare Wärmekapazität bei konstantem Volumen: $C_V = \frac{f}{2} R$""",
            physical_meaning="Erklärt molare Wärmekapazitäten von Gasen und Festkörpern (Dulong-Petit-Gesetz $C_V = 3R$). Bei tiefen Temperaturen frieren Freiheitsgrade aufgrund von Quantisierung ein (Quanteneffekt!).",
            validity_domain=r"Klassischer Grenzfall ($k_B T \gg \Delta E_{\text{Quant}}$).",
            tags=["Gleichverteilungssatz", "Thermodynamik", "Freiheitsgrade"],
            difficulty=2,
        ),
        Card(
            id="mech_harmonic_oscillator",
            deck_id="mechanik",
            title="Klassischer harmonischer Oszillator",
            front="Wie lautet die **Bewegungsgleichung** des freien ungedämpften **harmonischen Oszillators** und wie hängen Kreisfrequenz $\\omega_0$ und Periodendauer $T$ mit Masse $m$ und Federkonstante $k$ zusammen?",
            back=r"""Differentialgleichung:
$$\ddot{x}(t) + \omega_0^2 \, x(t) = 0$$

Kreisfrequenz:
$$\omega_0 = \sqrt{\frac{k}{m}}$$

Periodendauer und Frequenz:
$$T = \frac{2\pi}{\omega_0} = 2\pi \sqrt{\frac{m}{k}}, \qquad f = \frac{1}{T} = \frac{\omega_0}{2\pi}$$

Allgemeine Lösung:
$$x(t) = A \cos(\omega_0 t + \varphi_0)$$""",
            hint=r"Aus dem Hookeschen Gesetz $F = -kx$ und Newtons 2. Axiom $F = m\ddot{x}$.",
            formula_breakdown=r"""- $x(t)$: Auslenkung aus der Ruhelage $[\mathrm{m}]$
- $k$: Federkonstante (Richtgröße) $[\mathrm{N/m}]$
- $m$: Masse $[\mathrm{kg}]$
- $A$: Amplitude (maximale Auslenkung)
- $\varphi_0$: Nullphasenwinkel""",
            physical_meaning="Prototyp für fast jede Schwingung in der Natur: Jedes glatte Potenzial lässt sich nahe einem stabilen Minimum durch eine Taylor-Entwicklung quadratisch annähern ($V(x) \approx V(x_0) + \frac{1}{2} V''(x_0)(x-x_0)^2$).",
            validity_domain="Lineare Elastizität / kleine Auslenkungen ohne Reibung.",
            tags=["Oszillator", "Schwingung", "Klassische Mechanik"],
            difficulty=1,
        ),
        Card(
            id="mech_noether",
            deck_id="mechanik",
            title="Noether-Theorem & Erhaltungssätze",
            front="Was besagt das berühmte **Noether-Theorem** (Emmy Noether, 1918) und welche Symmetrien entsprechen der **Energie-**, **Impuls-** und **Drehimpulserhaltung**?",
            back=r"""**Kernaussage des Noether-Theorems:**
Zu jeder kontinuierlichen globalen Symmetrie der Wirkung $S$ (Invarianz der Lagrange-Funktion) existiert eine zeitlich streng erhaltene physikalische Größe (Noether-Ladung bzw. Erhaltungsgröße) und ein erhaltener Noether-Strom:

- **Homogenität der Zeit** (Invarianz unter Zeittranslation $t \to t + \Delta t$) $\implies$ **Energieerhaltung** ($E = \text{const.}$)
- **Homogenität des Raumes** (Invarianz unter Raumtranslation $\vec{r} \to \vec{r} + \Delta \vec{r}$) $\implies$ **Impulserhaltung** ($\vec{p} = \text{const.}$)
- **Isotropie des Raumes** (Invarianz unter räumlicher Rotation $\vec{r} \to R\vec{r}$) $\implies$ **Drehimpulserhaltung** ($\vec{L} = \text{const.}$)
- **U(1)-Eichinvarianz** der Wellenfunktion ($\psi \to e^{i\alpha}\psi$) $\implies$ **Ladungserhaltung**""",
            hint=r"Symmetrie der Naturgesetze = Erhaltungssatz.",
            formula_breakdown=r"""- Kontinuierliche Transformation: Lie-Gruppe (Translationen, Rotationen)
- Aus $\delta L = \frac{d}{dt} K$ folgt Erhaltungsgröße $Q = \sum_i \frac{\partial L}{\partial \dot{q}_i} \delta q_i - K = \text{const.}$""",
            physical_meaning="Eines der tiefgründigsten Theoreme der theoretischen Physik: Erhaltungssätze sind keine isolierten Postulate, sondern direkte mathematische Konsequenzen geometrischer Symmetrien unseres Universums.",
            validity_domain="Lagrange- und Hamilton-Mechanik, Quantenmechanik, Relativitätstheorie, Quantenfeldtheorie.",
            tags=["Noether", "Symmetrie", "Erhaltungssatz", "Theoretische Physik"],
            difficulty=3,
        ),
        Card(
            id="rel_time_dilation",
            deck_id="relativitaet",
            title="Zeitdilatation & Längenkontraktion",
            front="Wie lauten die Formeln für die relativistische **Zeitdilatation** und **Längenkontraktion**?",
            back=r"""**Zeitdilatation (bewegte Uhren gehen langsamer):**
$$\Delta t = \gamma \, \Delta t_0 = \frac{\Delta t_0}{\sqrt{1 - \frac{v^2}{c^2}}}$$

**Längenkontraktion (bewegte Maßstäbe sind in Bewegungsrichtung verkürzt):**
$$L = \frac{L_0}{\gamma} = L_0 \sqrt{1 - \frac{v^2}{c^2}}$$""",
            hint=r"Achte darauf, welche Größe die Eigenzeit $\Delta t_0$ und welche die Ruhelänge $L_0$ ist!",
            formula_breakdown=r"""- $\Delta t_0$: Eigenzeit (Zeitintervall gemessen im Ruhesystem der Uhr)
- $\Delta t$: Zeitintervall gemessen von einem relativ dazu mit Geschwindigkeit $v$ bewegten Beobachter ($\Delta t \ge \Delta t_0$)
- $L_0$: Ruhelänge (Länge des Objekts in seinem eigenen Ruhesystem)
- $L$: Kontrahierte Länge in Bewegungsrichtung ($L \le L_0$)
- Senkrecht zur Bewegungsrichtung: Keine Kontraktion ($L_\perp = L_{0\perp}$)""",
            physical_meaning="Zeit und Raum sind keine absoluten Kulissen, sondern vom Bewegungszustand des Beobachters abhängig. Bestätigt durch Myonen-Zerfall in der Erdatmosphäre und Atomuhren in Satelliten (GPS).",
            validity_domain="Inertialsysteme der Speziellen Relativitätstheorie.",
            tags=["SRT", "Zeitdilatation", "Längenkontraktion", "Relativität"],
            difficulty=2,
        ),
        Card(
            id="math_fourier",
            deck_id="mathe_physik",
            title="Fourier-Transformation & Inverse Transformation",
            front="Wie lauten die Definitionen der kontinuierlichen **Fourier-Transformation** $\\mathcal{F}[f](k)$ und der **inversen Fourier-Transformation** $\\mathcal{F}^{-1}[\\hat{f}](x)$ in symmetrischer Konvention?",
            back=r"""**Fourier-Transformation:**
$$\hat{f}(k) = \mathcal{F}[f](k) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{+\infty} f(x) \, e^{-i k x} \, dx$$

**Inverse Fourier-Transformation:**
$$f(x) = \mathcal{F}^{-1}[\hat{f}](x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{+\infty} \hat{f}(k) \, e^{+i k x} \, dk$$""",
            hint=r"Zerlegung einer Funktion in ebene Wellen $e^{ikx}$.",
            formula_breakdown=r"""- $x$: Ortskoordinate $[\mathrm{m}]$
- $k = \frac{2\pi}{\lambda}$: Wellenzahl $[\mathrm{m^{-1}}]$
- In der Quantenmechanik ($p = \hbar k$): Transformation zwischen Orts- und Impulsraum
  $$\psi(p) = \frac{1}{\sqrt{2\pi\hbar}} \int \psi(x) e^{-\frac{i}{\hbar}px} dx$$""",
            physical_meaning=r"Wandelt zeit- oder ortsabhängige Signale in ihr Frequenz- bzw. Wellenzahlspektrum um. Verwandelt Differentiationen im Ortsraum in algebraische Multiplikationen ($\mathcal{F}[\frac{df}{dx}] = ik \hat{f}(k)$).",
            validity_domain=r"Quadratintegrierbare Funktionen $f \in L^2(\mathbb{R})$ und temperierte Distributionen.",
            tags=["Fourier", "Frequenzraum", "Wellenzahl", "Mathematische Methoden"],
            difficulty=3,
        ),
        # ==========================================
        # FUNDAMENTALE NATURKONSTANTEN & GRÖSSENORDNUNGEN
        # ==========================================
        Card(
            id="const_c",
            deck_id="konstanten",
            title="Lichtgeschwindigkeit im Vakuum (c)",
            front=r"Wie groß ist die **Vakuum-Lichtgeschwindigkeit** $c$ (exakter Wert und Faustwert)?",
            back=r"""**Exakter Wert:**
$$c = 299\,792\,458 \, \mathrm{m/s}$$

**Faustwert:**
$$c \approx 3 \times 10^8 \, \mathrm{m/s} = 300\,000 \, \mathrm{km/s}$$

**Nützliche Daumenregel für Elektronik & Optik:**
Licht legt in **$1 \, \mathrm{ns}$** etwa **$30 \, \mathrm{cm}$** zurück ($\approx 1 \, \text{Fuß}$).""",
            hint=r"Seit 1983 ist der Meter über die Lichtgeschwindigkeit exakt definiert.",
            formula_breakdown=r"""- $c$: Universelle Grenzgeschwindigkeit für Information und Kausalität
- Exakt ohne Messunsicherheit, da der Meter als die Strecke definiert ist, die Licht in $\frac{1}{299\,792\,458} \, \mathrm{s}$ durchläuft.""",
            physical_meaning=r"Gleichzeitig die Ausbreitungsgeschwindigkeit aller masselosen Teilchen (Photonen, Gravitationswellen, hypothetische Gravitonen) und Skalierungsfaktor zwischen Raum und Zeit.",
            validity_domain=r"Vakuum. In Medien mit Brechungsindex $n$ gilt Phasengeschwindigkeit $v = c/n < c$.",
            tags=["Konstanten", "Relativität", "Optik", "Grundwissen"],
            difficulty=1,
        ),
        Card(
            id="const_h_hbar",
            deck_id="konstanten",
            title="Plancksches Wirkungsquantum (h und ħ)",
            front=r"Wie groß sind das **Plancksche Wirkungsquantum** $h$ und das **reduzierte Wirkungsquantum** $\hbar$ in $\mathrm{J\cdot s}$ und $\mathrm{eV\cdot s}$?",
            back=r"""**Plancksches Wirkungsquantum $h$:**
$$h \approx 6{,}626 \times 10^{-34} \, \mathrm{J\cdot s}$$

**Reduziertes Wirkungsquantum $\hbar = \frac{h}{2\pi}$:**
$$\hbar \approx 1{,}055 \times 10^{-34} \, \mathrm{J\cdot s} \approx 6{,}582 \times 10^{-16} \, \mathrm{eV\cdot s}$$

**Nützliche Kombination mit $c$:**
$$\hbar c \approx 197{,}3 \, \mathrm{MeV \cdot fm} = 197{,}3 \, \mathrm{eV \cdot nm}$$""",
            hint=r"Exponent ist $-34$ in SI-Einheiten, $-16$ in Elektronenvolt-Sekunden.",
            formula_breakdown=r"""- Einheit: Wirkung $=$ Energie $\times$ Zeit $=$ Drehimpuls $[\mathrm{J\cdot s}]$
- $1 \, \mathrm{eV} \approx 1{,}602 \times 10^{-19} \, \mathrm{J}$""",
            physical_meaning=r"Fundamentale Quantisierungsskala unseres Universums. Markiert die Grenze, ab der klassische Punktmechanik versagt und Wellen-Teilchen-Dualismus / Unschärfe dominant werden.",
            validity_domain=r"Exakt im SI-System definiert seit der Neudefinition 2019.",
            tags=["Konstanten", "Quantenmechanik", "Grundwissen"],
            difficulty=1,
        ),
        Card(
            id="const_elementary_charge",
            deck_id="konstanten",
            title="Elementarladung (e)",
            front=r"Wie groß ist die **Elementarladung** $e$ eines Protons bzw. der Betrag der Ladung eines Elektrons?",
            back=r"""$$e \approx 1{,}602 \times 10^{-19} \, \mathrm{C}$$

(Exakt: $e = 1{,}602\,176\,634 \times 10^{-19} \, \mathrm{A\cdot s}$)""",
            hint=r"Exponent $-19$ Coulomb.",
            formula_breakdown=r"""- $e$: Kleinste frei existierende Ladungseinheit stabiler Teilchen
- Quarks tragen zwar Drittelladungen ($\pm \frac{1}{3}e, \pm \frac{2}{3}e$), treten aber durch Confinement niemals isoliert auf.""",
            physical_meaning=r"Bestimmt die Stärke der elektromagnetischen Wechselwirkung und verknüpft makroskopischen Strom mit mikroskopischer Teilchenanzahl.",
            validity_domain=r"Exakt festgelegt im überarbeiteten SI-System (2019).",
            tags=["Konstanten", "Elektrodynamik", "Teilchenphysik"],
            difficulty=1,
        ),
        Card(
            id="const_electron_mass",
            deck_id="konstanten",
            title="Masse des Elektrons (m_e)",
            front=r"Wie groß ist die **Ruhemasse des Elektrons** $m_e$ in $\mathrm{kg}$ und in $\mathrm{keV}/c^2$?",
            back=r"""In Kilogramm:
$$m_e \approx 9{,}109 \times 10^{-31} \, \mathrm{kg}$$

In Ruheenergie:
$$m_e c^2 \approx 511 \, \mathrm{keV} \approx 0{,}511 \, \mathrm{MeV}$$""",
            hint=r"Knapp $10^{-30} \, \mathrm{kg}$ bzw. etwa ein halbes MeV.",
            formula_breakdown=r"""- $m_e$: Invariante Ruhemasse des leichtesten geladenen Leptons
- $m_e c^2 \approx 511 \, \mathrm{keV}$: Typische Energieschwelle für Paarvernichtung $e^+ e^- \to 2\gamma$ ($2 \times 511 \, \mathrm{keV}$ Annihilationsstrahlung).""",
            physical_meaning=r"Bestimmt den Bohr-Radius der Atomhülle und die chemische Skala (ca. 1836-mal leichter als das Proton).",
            validity_domain=r"Universell.",
            tags=["Konstanten", "Atomphysik", "Teilchenphysik"],
            difficulty=2,
        ),
        Card(
            id="const_proton_mass",
            deck_id="konstanten",
            title="Masse des Protons (m_p)",
            front=r"Wie groß ist die **Ruhemasse des Protons** $m_p$ in $\mathrm{kg}$ und in $\mathrm{MeV}/c^2$, und wie verhält sie sich zur Elektronenmasse?",
            back=r"""In Kilogramm:
$$m_p \approx 1{,}673 \times 10^{-27} \, \mathrm{kg} \approx 1 \, \mathrm{u}$$

In Ruheenergie:
$$m_p c^2 \approx 938{,}3 \, \mathrm{MeV} \approx 1 \, \mathrm{GeV}$$

Verhältnis zur Elektronenmasse:
$$\frac{m_p}{m_e} \approx 1836$$""",
            hint=r"Etwa $1 \, \mathrm{GeV}$ Ruheenergie bzw. $1{,}67 \times 10^{-27} \, \mathrm{kg}$.",
            formula_breakdown=r"""- $1 \, \mathrm{u} \approx 1{,}661 \times 10^{-27} \, \mathrm{kg}$ (atomare Masseneinheit)
- $m_n c^2 \approx 939{,}6 \, \mathrm{MeV}$ (Neutron ist um $1{,}3 \, \mathrm{MeV}$ schwerer als das Proton $\implies$ freie Neutronen zerfallen!).""",
            physical_meaning=r"Nahezu die gesamte sichtbare Masse gewöhnlicher Materie (Atome) stammt aus den Massen der Nukleonen (Protonen & Neutronen), erzeugt durch die Bindungsenergie der Quantenchromodynamik (Gluonenfeld).",
            validity_domain=r"Universell.",
            tags=["Konstanten", "Kernphysik", "Masse"],
            difficulty=2,
        ),
        Card(
            id="const_boltzmann",
            deck_id="konstanten",
            title="Boltzmann-Konstante (k_B)",
            front=r"Wie groß ist die **Boltzmann-Konstante** $k_B$ in $\mathrm{J/K}$ und in $\mathrm{eV/K}$?",
            back=r"""In SI-Einheiten:
$$k_B \approx 1{,}381 \times 10^{-23} \, \mathrm{J/K}$$

In Elektronenvolt pro Kelvin:
$$k_B \approx 8{,}617 \times 10^{-5} \, \mathrm{eV/K} \approx 10^{-4} \, \mathrm{eV/K}$$""",
            hint=r"Exponent $-23$ in Joule/Kelvin.",
            formula_breakdown=r"""- Verknüpft absolute Temperatur $T$ $[\mathrm{K}]$ mit mikroskopischer Energie $E = k_B T$
- Exakt: $k_B = 1{,}380\,649 \times 10^{-23} \, \mathrm{J/K}$""",
            physical_meaning=r"Übersetzungsfaktor zwischen unserer makroskopischen Temperaturskala in Kelvin und der mittleren mikroskopischen kinetischen Energie pro Teilchen.",
            validity_domain=r"Thermodynamik & Statistische Physik.",
            tags=["Konstanten", "Thermodynamik", "Statistik"],
            difficulty=1,
        ),
        Card(
            id="const_avogadro",
            deck_id="konstanten",
            title="Avogadro-Konstante (N_A)",
            front=r"Wie groß ist die **Avogadro-Konstante** $N_A$ und was gibt sie an?",
            back=r"""$$N_A \approx 6{,}022 \times 10^{23} \, \mathrm{mol}^{-1}$$

(Exakt: $6{,}022\,140\,76 \times 10^{23} \, \mathrm{mol}^{-1}$)""",
            hint=r"Sechs mal zehn hoch 23 Teilchen pro Mol.",
            formula_breakdown=r"""- $1 \, \mathrm{mol}$: Stoffmenge, die exakt $N_A$ Teilchen enthält
- Verknüpfung: Universelle Gaskonstante $R = N_A \cdot k_B$""",
            physical_meaning=r"Brücke zwischen der Mikrowelt einzelner Moleküle und der makroskopischen Laborwelt (Gramm und Mol). $12 \, \mathrm{g}$ Kohlenstoff-12 enthalten exakt $N_A$ Atome.",
            validity_domain=r"SI-Basiseinheit Mol.",
            tags=["Konstanten", "Stoffmenge", "Chemie", "Statistik"],
            difficulty=1,
        ),
        Card(
            id="const_gravitation",
            deck_id="konstanten",
            title="Gravitationskonstante (G)",
            front=r"Wie groß ist die newtonsche **Gravitationskonstante** $G$ und was ist ihre SI-Einheit?",
            back=r"""$$G \approx 6{,}674 \times 10^{-11} \, \frac{\mathrm{m}^3}{\mathrm{kg \cdot s^2}} = 6{,}674 \times 10^{-11} \, \frac{\mathrm{N \cdot m^2}}{\mathrm{kg^2}}$$""",
            hint=r"Zwei Drittel mal zehn hoch minus 10 ($\approx 6{,}67 \times 10^{-11}$).",
            formula_breakdown=r"""- Tritt auf im Newtonschen Gravitationsgesetz $F = G \frac{m_1 m_2}{r^2}$ und in den Einsteinschen Feldgleichungen $G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$""",
            physical_meaning=r"Kopplungskonstante der Gravitation. Im Vergleich zu den anderen fundamentalen Kräften extrem schwach (um 36 bis 40 Größenordnungen schwächer als die elektromagnetische Kraft zwischen zwei Protonen!).",
            validity_domain=r"Klassische Gravitation und Allgemeine Relativitätstheorie.",
            tags=["Konstanten", "Gravitation", "Astrophysik"],
            difficulty=2,
        ),
        Card(
            id="const_earth_g",
            deck_id="konstanten",
            title="Erdbeschleunigung (g)",
            front=r"Wie groß ist die standardisierte **Erdbeschleunigung** (Fallbeschleunigung) $g$ auf Meereshöhe?",
            back=r"""Standard-Normwert:
$$g = 9{,}80665 \, \mathrm{m/s^2} \approx 9{,}81 \, \mathrm{m/s^2}$$

Für schnelle Überschlagsrechnungen:
$$g \approx 10 \, \mathrm{m/s^2} \approx \pi^2 \, \mathrm{m/s^2}$$""",
            hint=r"Etwa 9,81 Meter pro Sekunde-Quadrat oder grob 10.",
            formula_breakdown=r"""- $g = \frac{G M_\oplus}{R_\oplus^2} - \omega^2 R_\oplus \cos^2\varphi$ (Zentrifugalbeschleunigung an den Polen null, am Äquator maximal).
- Pol: $g \approx 9{,}83 \, \mathrm{m/s^2}$, Äquator: $g \approx 9{,}78 \, \mathrm{m/s^2}$.""",
            physical_meaning=r"Beschleunigung eines frei fallenden Körpers im Schwerefeld der Erde im Vakuum. Kraft auf $1 \, \mathrm{kg}$ Masse beträgt ca. $9{,}81 \, \mathrm{N} \approx 10 \, \mathrm{N}$.",
            validity_domain=r"Erdoberfläche.",
            tags=["Konstanten", "Mechanik", "Erde"],
            difficulty=1,
        ),
        Card(
            id="const_eps0_mu0",
            deck_id="konstanten",
            title="Elektrische und magnetische Feldkonstante (ε_0 und μ_0)",
            front=r"Wie groß sind die **elektrische Feldkonstante** $\varepsilon_0$ und die **magnetische Feldkonstante** $\mu_0$ im Vakuum?",
            back=r"""**Elektrische Feldkonstante (Permittivität des Vakuums):**
$$\varepsilon_0 \approx 8{,}854 \times 10^{-12} \, \frac{\mathrm{F}}{\mathrm{m}} = 8{,}854 \times 10^{-12} \, \frac{\mathrm{A\cdot s}}{\mathrm{V\cdot m}}$$

**Magnetische Feldkonstante (Permeabilität des Vakuums):**
$$\mu_0 = 4\pi \times 10^{-7} \, \frac{\mathrm{N}}{\mathrm{A^2}} \approx 1{,}257 \times 10^{-6} \, \frac{\mathrm{V\cdot s}}{\mathrm{A\cdot m}}$$

Zusammenhang mit der Lichtgeschwindigkeit:
$$c = \frac{1}{\sqrt{\varepsilon_0 \mu_0}}$$""",
            hint=r"Coulomb-Voraktor $\frac{1}{4\pi\varepsilon_0} \approx 9 \times 10^9 \, \mathrm{N\cdot m^2 / C^2}$.",
            formula_breakdown=r"""- $[\varepsilon_0] = \mathrm{Farad/Meter}$, $[\mu_0] = \mathrm{Henry/Meter}$
- Vakuum-Wellenwiderstand (Impedanz des Vakuums): $Z_0 = \sqrt{\frac{\mu_0}{\varepsilon_0}} \approx 377 \, \Omega \approx 120\pi \, \Omega$""",
            physical_meaning=r"Charakterisieren die Reaktion des Vakuums auf elektrische bzw. magnetische Felder und bestimmen die Impedanz des freien Raumes für elektromagnetische Wellen.",
            validity_domain=r"Vakuum.",
            tags=["Konstanten", "Elektrodynamik", "Vakuum"],
            difficulty=2,
        ),
        Card(
            id="const_bohr_radius",
            deck_id="konstanten",
            title="Bohrscher Atomradius (a_0)",
            front=r"Wie groß ist der **Bohrsche Radius** $a_0$ des Wasserstoff-Grundzustands in Angström und Nanometern?",
            back=r"""$$a_0 = \frac{4\pi\varepsilon_0 \hbar^2}{m_e e^2} \approx 0{,}529 \times 10^{-10} \, \mathrm{m} = 0{,}529 \, \mathrm{\AA} \approx 0{,}053 \, \mathrm{nm}$$

**Faustregel:**
Ein typischer Atomdurchmesser liegt bei ca. **$1 \, \mathrm{\AA} = 0{,}1 \, \mathrm{nm} = 10^{-10} \, \mathrm{m}$**.""",
            hint=r"Etwa ein halbes Angström ($0{,}53 \, \text{Å}$).",
            formula_breakdown=r"""- $a_0$: Erwartungswert des Abstands des Elektrons vom Proton im 1s-Zustand des Wasserstoffatoms
- $1 \, \mathrm{\AA} = 10^{-10} \, \mathrm{m} = 0{,}1 \, \mathrm{nm}$""",
            physical_meaning=r"Die fundamentale Längenskala der Atomphysik. Ergibt sich aus dem Gleichgewicht zwischen quantenmechanischer Unschärfe (Nullpunktsimpuls $\sim \hbar/r$) und elektrostatischer Coulomb-Anziehung.",
            validity_domain=r"Wasserstoffatom.",
            tags=["Konstanten", "Atomphysik", "Bohr"],
            difficulty=2,
        ),
        Card(
            id="const_finestructure",
            deck_id="konstanten",
            title="Sommerfeldsche Feinstrukturkonstante (α)",
            front=r"Wie lautet die Definition der **Feinstrukturkonstante** $\alpha$ und wie groß ist ihr Näherungswert als Bruch?",
            back=r"""$$\alpha = \frac{e^2}{4\pi\varepsilon_0 \hbar c} \approx \frac{1}{137} \approx 7{,}297 \times 10^{-3}$$""",
            hint=r"Berühmte Zahl der Physik: Eins durch 137.",
            formula_breakdown=r"""- $\alpha$: Reines, einheitenloses (dimensionsloses) Maß!
- Verhältnis der Elektronengeschwindigkeit im Bohrschen Grundzustand zur Lichtgeschwindigkeit: $v_1 / c = \alpha \approx \frac{1}{137}$.""",
            physical_meaning=r"Universelle Kopplungskonstante der Quantenelektrodynamik (QED). Bestimmt die Stärke der elektromagnetischen Wechselwirkung zwischen geladenen Teilchen und Photonen sowie atomare Feinstrukturaufspaltungen.",
            validity_domain=r"Gültig bei niedrigen Energien (läuft bei höheren Energieskalen, z.B. bei der $Z^0$-Masse $\sim 91 \, \mathrm{GeV}$, auf ca. $1/128$).",
            tags=["Konstanten", "QED", "Dimensionslos"],
            difficulty=2,
        ),
        Card(
            id="const_sec_in_year",
            deck_id="konstanten",
            title="Sekunden pro Jahr (Fermi-Faustregel)",
            front=r"Wie viele **Sekunden hat ein Jahr** grob (berühmter physikalischer Fermi-Trick)?",
            back=r"""**Fermi-Faustregel:**
$$1 \, \text{Jahr} \approx \pi \times 10^7 \, \mathrm{s} \approx 3{,}15 \times 10^7 \, \mathrm{s}$$

(Exakt bei 365 Tagen: $31\,536\,000 \, \mathrm{s}$)""",
            hint=r"Pi mal zehn hoch sieben!",
            formula_breakdown=r"""- $365{,}25 \, \text{Tage} \times 24 \, \frac{\text{h}}{\text{Tag}} \times 3600 \, \frac{\text{s}}{\text{h}} = 31\,557\,600 \, \mathrm{s}$
- Da $\pi \approx 3{,}14159$, beträgt der Fehler der Näherung $\pi \times 10^7$ weniger als $0{,}5\,\%$!""",
            physical_meaning=r"Extrem beliebter Schätzwert für astrophysikalische und thermodynamische Fermi-Probleme, Zerfallsraten und Lebensdauer-Abschätzungen.",
            validity_domain=r"Tropisches/Gregorianisches Erdjahr.",
            tags=["Konstanten", "Faustformel", "Fermi-Problem"],
            difficulty=1,
        ),
        Card(
            id="const_room_temp_energy",
            deck_id="konstanten",
            title="Thermische Energie bei Raumtemperatur (k_B T)",
            front=r"Wie groß ist die **thermische Energie** $k_B T$ bei **Raumtemperatur** ($T \approx 300 \, \mathrm{K} \approx 20^\circ\mathrm{C}$) in $\mathrm{eV}$ und $\mathrm{J}$?",
            back=r"""In Elektronenvolt:
$$k_B T \approx \frac{1}{40} \, \mathrm{eV} = 0{,}025 \, \mathrm{eV} = 25 \, \mathrm{meV}$$

In Joule:
$$k_B T \approx 4{,}1 \times 10^{-21} \, \mathrm{J} \approx 4 \times 10^{-21} \, \mathrm{J}$$""",
            hint=r"Etwa ein Vierzigstel Elektronenvolt (25 Millielektronenvolt).",
            formula_breakdown=r"""- Bei $T = 293 \, \mathrm{K}$ ($20^\circ\mathrm{C}$): $k_B T \approx 25{,}2 \, \mathrm{meV}$
- Bei $T = 300 \, \mathrm{K}$: $k_B T \approx 25{,}8 \, \mathrm{meV}$""",
            physical_meaning=r"Referenzskala für alle thermischen Phänomene: Prozesse mit Aktivierungsenergie $\gg 25 \, \mathrm{meV}$ (z.B. kovalente chemische Bindungen $\sim 1-4 \, \mathrm{eV}$) sind bei Raumtemperatur thermisch stabil. Prozesse mit $\ll 25 \, \mathrm{meV}$ fluktuieren chaotisch.",
            validity_domain=r"Umgebungstemperatur ca. 300 K.",
            tags=["Konstanten", "Thermodynamik", "Festkörperphysik", "Faustformel"],
            difficulty=1,
        ),
        Card(
            id="const_sun_earth_mass",
            deck_id="konstanten",
            title="Massen & Radien im Sonnensystem (Sonne & Erde)",
            front=r"Welche Größenordnungen haben **Sonnenmasse** $M_\odot$, **Erdmasse** $M_\oplus$ und der **Erdradius** $R_\oplus$?",
            back=r"""**Sonnenmasse:**
$$M_\odot \approx 2 \times 10^{30} \, \mathrm{kg}$$

**Erdmasse:**
$$M_\oplus \approx 6 \times 10^{24} \, \mathrm{kg} \quad (M_\odot \approx 333\,000 \, M_\oplus)$$

**Mittlerer Erdradius:**
$$R_\oplus \approx 6371 \, \mathrm{km} \approx 6{,}4 \times 10^6 \, \mathrm{m}$$

(Erdumfang am Äquator: $2\pi R_\oplus \approx 40\,000 \, \mathrm{km}$)""",
            hint=r"Sonne: $2 \times 10^{30} \, \mathrm{kg}$, Erde: $6 \times 10^{24} \, \mathrm{kg}$, Radius: $6400 \, \mathrm{km}$.",
            formula_breakdown=r"""- Astronomische Einheit (mittlerer Erde-Sonne-Abstand): $1 \, \mathrm{AE} \approx 1{,}5 \times 10^8 \, \mathrm{km} = 1{,}5 \times 10^{11} \, \mathrm{m}$ (Lichtlaufzeit: ca. $8{,}3 \, \text{Minuten}$)""",
            physical_meaning=r"Fundamentale astronomische Eichmaße für Stern- und Planetenphysik.",
            validity_domain=r"Sonnensystem.",
            tags=["Konstanten", "Astrophysik", "Größenordnungen"],
            difficulty=2,
        ),
        Card(
            id="const_speed_of_sound",
            deck_id="konstanten",
            title="Schallgeschwindigkeit in Luft (c_s)",
            front=r"Wie groß ist die **Schallgeschwindigkeit in Luft** bei Raumtemperatur und welche **Faustregel** gilt für Gewitter (Distanz zu einem Blitz)?",
            back=r"""Schallgeschwindigkeit in trockener Luft ($20^\circ\mathrm{C}$):
$$c_s \approx 343 \, \mathrm{m/s} \approx 340 \, \mathrm{m/s} \approx \frac{1}{3} \, \mathrm{km/s}$$

**Gewitter-Faustregel:**
Zähle die Sekunden zwischen Blitz und Donnergrollen:
$$\text{Entfernung } [\mathrm{km}] \approx \frac{\text{Sekunden}}{3}$$
(D.h. **3 Sekunden Verzögerung** entsprechen **$1 \, \mathrm{km}$** Abstand).""",
            hint=r"Rund ein Drittel Kilometer pro Sekunde.",
            formula_breakdown=r"""- Thermische Formel für ideales Gas: $c_s = \sqrt{\kappa \frac{R T}{M}} = \sqrt{\kappa \frac{p}{\rho}}$ mit Adiabatenexponent $\kappa \approx 1{,}4$ für zweiatomige Gase ($\mathrm{N_2}, \mathrm{O_2}$)""",
            physical_meaning=r"Geschwindigkeit, mit der sich adiabatische Druckwellen durch molekulare Stöße in einem elastischen Medium ausbreiten.",
            validity_domain=r"Luft bei Normalbedingungen.",
            tags=["Konstanten", "Akustik", "Mechanik", "Faustformel"],
            difficulty=1,
        ),
        Card(
            id="const_atm_pressure",
            deck_id="konstanten",
            title="Atmosphärischer Normaldruck (1 atm)",
            front=r"Wie groß ist der **physikalische Normaldruck** auf Meereshöhe in Pascal, Bar und Millibar?",
            back=r"""$$1 \, \mathrm{atm} = 101\,325 \, \mathrm{Pa} \approx 10^5 \, \mathrm{Pa} = 1 \, \mathrm{bar} = 1000 \, \mathrm{hPa} = 1000 \, \mathrm{mbar}$$

(Oder in Wassersäule: $10 \, \mathrm{m} \, \mathrm{H_2O} \approx 1 \, \mathrm{bar}$, in Quecksilber: $760 \, \mathrm{Torr} = 760 \, \mathrm{mmHg}$)""",
            hint=r"Etwa zehn hoch fünf Pascal ($10^5 \, \text{N/m}^2$).",
            formula_breakdown=r"""- $1 \, \mathrm{Pa} = 1 \, \mathrm{N/m^2}$
- $10^5 \, \mathrm{Pa}$ entspricht dem Gewicht einer Masse von $10\,000 \, \mathrm{kg}$ ($10 \, \text{Tonnen}$) pro Quadratmeter!""",
            physical_meaning=r"Statistischer hydrostatischer Druck der Erdatmosphäre erzeugt durch die Gravitationskraft auf die gesamte Luftsäule oberhalb der Erdoberfläche.",
            validity_domain=r"Erdoberfläche / Standardatmosphäre.",
            tags=["Konstanten", "Thermodynamik", "Hydrostatik"],
            difficulty=1,
        ),
        Card(
            id="const_visible_light",
            deck_id="konstanten",
            title="Wellenlängen & Photonenenergien des sichtbaren Lichts",
            front=r"In welchem **Wellenlängenbereich** und welchem **Photonenenergiebereich** liegt das für den Menschen **sichtbare Licht**?",
            back=r"""**Wellenlängenbereich:**
$$\lambda \approx 400 \, \mathrm{nm} \text{ (Violett/Blau)} \quad \text{bis} \quad 750 \, \mathrm{nm} \text{ (Rot)}$$

**Photonenenergien ($E = \frac{hc}{\lambda}$):**
$$E_{\text{rot}} \approx 1{,}65 \, \mathrm{eV} \quad \text{bis} \quad E_{\text{blau}} \approx 3{,}1 \, \mathrm{eV}$$

**Faustregel:**
Grünes Licht ($\lambda \approx 500 \, \mathrm{nm}$) hat eine Photonenenergie von ca. **$2{,}5 \, \mathrm{eV}$**.""",
            hint=r"400 bis 700 Nanometer; etwa 1,8 bis 3 Elektronenvolt.",
            formula_breakdown=r"""- $E [\mathrm{eV}] \approx \frac{1240 \, \mathrm{eV\cdot nm}}{\lambda [\mathrm{nm}]}$ (äußerst nützliche Faustformel!)
- Beispiel: $\lambda = 500 \, \mathrm{nm} \implies E \approx \frac{1240}{500} \approx 2{,}48 \, \mathrm{eV}$.""",
            physical_meaning=r"Entspricht dem optischen Fenster der Erdatmosphäre und der maximalen Strahlungsintensität der Sonne nach dem Planckschen Strahlungsgesetz.",
            validity_domain=r"Optisches Spektrum.",
            tags=["Konstanten", "Optik", "Photonen", "Faustformel"],
            difficulty=1,
        ),
        # ==========================================
        # KLEINE FORMELN & INTUITION: QUANTENMECHANIK
        # ==========================================
        Card(
            id="qm_de_broglie",
            deck_id="quantenmechanik",
            title="De-Broglie-Wellenlänge",
            front=r"Wie lautet die Formel für die **De-Broglie-Wellenlänge** $\lambda$ eines Teilchens mit Impuls $p$?",
            back=r"""$$\lambda = \frac{h}{p} = \frac{h}{m v}$$

Oder mit Wellenzahl $k = \frac{2\pi}{\lambda}$ und $\hbar = \frac{h}{2\pi}$:
$$p = \hbar k$$""",
            hint=r"Plancksches Wirkungsquantum geteilt durch Impuls.",
            formula_breakdown=r"""- $\lambda$: De-Broglie-Materiewellenlänge $[\mathrm{m}]$
- $h$: Plancksches Wirkungsquantum $\approx 6{,}626 \times 10^{-34} \, \mathrm{J\cdot s}$
- $p$: Impuls des Teilchens $[\mathrm{kg\cdot m/s}]$
- Für nicht-relativistische Teilchen mit kinetischer Energie $E_{\text{kin}}$: $\lambda = \frac{h}{\sqrt{2m E_{\text{kin}}}}$""",
            physical_meaning=r"Begründet den Welle-Teilchen-Dualismus für Materie: Jedes bewegte massebehaftete Teilchen besitzt Welleneigenschaften (Interferenz, Beugung am Doppelspalt, Elektronenmikroskop).",
            validity_domain=r"Universell. Für relativistische Teilchen gilt der relativistische Impuls $p = \gamma m v$.",
            tags=[
                "De-Broglie",
                "Welle-Teilchen-Dualismus",
                "Quantenmechanik",
                "Formel",
            ],
            difficulty=1,
        ),
        Card(
            id="qm_wavevector_momentum",
            deck_id="quantenmechanik",
            title="Zusammenhang Impuls und Wellenvektor",
            front=r"Wie hängen **Impulsvektor** $\vec{p}$ und **Wellenvektor** $\vec{k}$ zusammen?",
            back=r"""$$\vec{p} = \hbar \vec{k}$$

Betrag:
$$p = \hbar k = \frac{h}{\lambda}$$""",
            hint=r"Proportionalitätskonstante ist $\hbar$.",
            formula_breakdown=r"""- $\vec{p}$: Mechanischer Impuls
- $\vec{k}$: Wellenvektor (Richtung der Wellenausbreitung, Betrag $k = \frac{2\pi}{\lambda}$)
- $\hbar = \frac{h}{2\pi}$""",
            physical_meaning=r"Verknüpft die mechanische Teilchengröße (Impuls $\vec{p}$) direkt mit der geometrischen Wellengröße (räumliche Frequenz bzw. Wellenvektor $\vec{k}$).",
            validity_domain=r"Allgemein in Quantenmechanik und Quantenoptik.",
            tags=["Impuls", "Wellenvektor", "Quantenmechanik"],
            difficulty=1,
        ),
        Card(
            id="qm_energy_frequency",
            deck_id="quantenmechanik",
            title="Planck-Einstein-Relation (Energie & Frequenz)",
            front=r"Wie lautet die **Planck-Einstein-Beziehung** zwischen der **Energie** $E$ eines Photons und seiner **Frequenz** $\nu$ bzw. **Kreisfrequenz** $\omega$?",
            back=r"""$$E = h \nu = \hbar \omega$$""",
            hint=r"$h$ mit Frequenz $\nu$, $\hbar$ mit Kreisfrequenz $\omega$.",
            formula_breakdown=r"""- $E$: Quantenenergie $[\mathrm{J}]$
- $\nu$: Frequenz in Hertz $[\mathrm{s^{-1}}]$
- $\omega = 2\pi\nu$: Kreisfrequenz in $[\mathrm{rad/s}]$
- $h$: Plancksches Wirkungsquantum
- $\hbar = \frac{h}{2\pi}$""",
            physical_meaning=r"Licht wird in diskreten Energiepaketen (Quanten bzw. Photonen) emittiert, absorbiert und propagiert. Basis des Photoeffekts (Nobelpreis für Einstein 1921).",
            validity_domain=r"Universell für elektromagnetische Strahlung und beliebige Quantenzustände.",
            tags=["Energie", "Frequenz", "Photon", "Quantenmechanik"],
            difficulty=1,
        ),
        Card(
            id="qm_photon_momentum",
            deck_id="quantenmechanik",
            title="Impuls eines Photons",
            front=r"Wie lautet die Formel für den **Impuls eines Photons** $p$ in Abhängigkeit von seiner Energie $E$ und Wellenlänge $\lambda$?",
            back=r"""$$p = \frac{E}{c} = \frac{h \nu}{c} = \frac{h}{\lambda} = \hbar k$$""",
            hint=r"Aus $E = p c$ für masselose Teilchen.",
            formula_breakdown=r"""- $E$: Photonenenergie
- $c$: Lichtgeschwindigkeit
- $\lambda$: Wellenlänge
- Strahlungsdruck: Bei vollständiger Reflexion wird der doppelte Impuls $2p$ übertragen!""",
            physical_meaning=r"Obwohl Photonen keine Ruhemasse besitzen ($m_0 = 0$), tragen sie echten mechanischen Impuls. Führt zum Strahlungsdruck (Sonnenwind, Kometenschweife, Laserkühlung, optische Pinzetten).",
            validity_domain=r"Masselose Teilchen im Vakuum.",
            tags=["Photon", "Impuls", "Strahlungsdruck"],
            difficulty=1,
        ),
        Card(
            id="qm_compton_wavelength",
            deck_id="quantenmechanik",
            title="Compton-Wellenlänge",
            front=r"Wie ist die **Compton-Wellenlänge** $\lambda_C$ eines Teilchens der Masse $m$ definiert und wie groß ist sie für ein Elektron?",
            back=r"""Definition:
$$\lambda_C = \frac{h}{m c}$$

Reduzierte Compton-Wellenlänge:
$$\bar{\lambda}_C = \frac{\hbar}{m c}$$

Für das **Elektron** ($m = m_e$):
$$\lambda_{C,e} \approx 2{,}426 \times 10^{-12} \, \mathrm{m} \approx 2{,}43 \, \mathrm{pm} = 0{,}0243 \, \mathrm{\AA}$$""",
            hint=r"Plancksches Wirkungsquantum geteilt durch Masse mal Lichtgeschwindigkeit.",
            formula_breakdown=r"""- Bei Compton-Streuung an ruhendem Elektron: $\Delta \lambda = \lambda' - \lambda = \lambda_{C,e} (1 - \cos\theta)$
- Unabhängig von der Wellenlänge des einfallenden Lichts!""",
            physical_meaning=r"Skala, bei der quantenmechanische Lokalisierung so scharf wird ($\Delta x \sim \lambda_C$), dass die Impulsunschärfe $\Delta p \sim m c$ ausreicht, um virtuelle Teilchen-Antiteilchen-Paare zu erzeugen. Grenze der Einteilchen-Quantenmechanik hin zur Quantenfeldtheorie.",
            validity_domain=r"Relativistische Quantenphysik.",
            tags=["Compton", "Streuung", "Wellenlänge"],
            difficulty=2,
        ),
        Card(
            id="qm_rydberg_energy",
            deck_id="quantenmechanik",
            title="Bohr-Energieniveaus & Rydberg-Energie",
            front=r"Wie lautet die Formel für die diskreten **Energieniveaus des Wasserstoffatoms** $E_n$ im Bohrschen Atommodell und wie groß ist die **Rydberg-Energie**?",
            back=r"""$$E_n = -\frac{R_y}{n^2} = -\frac{13{,}6 \, \mathrm{eV}}{n^2} \quad (n = 1, 2, 3, \dots)$$

Rydberg-Energie (Bindungsenergie des Grundzustands):
$$R_y = \frac{m_e e^4}{8 \varepsilon_0^2 h^2} = \frac{1}{2} \alpha^2 m_e c^2 \approx 13{,}606 \, \mathrm{eV}$$""",
            hint=r"Minus 13,6 eV geteilt durch $n^2$.",
            formula_breakdown=r"""- $n$: Hauptquantenzahl
- Grundzustand ($n=1$): $E_1 = -13{,}6 \, \mathrm{eV}$ (Ionisierungsenergie von Wasserstoff)
- Angeregte Zustände: $E_2 = -3{,}4 \, \mathrm{eV}$, $E_3 = -1{,}51 \, \mathrm{eV}$, $\dots$, $E_\infty = 0$ (Kontinuum/Ionisation)""",
            physical_meaning=r"Diskrete Energieniveaus erklären die diskreten Absorptions- und Emissionslinien der Spektroskopie (Lyman-, Balmer-, Paschen-Serie).",
            validity_domain=r"Wasserstoff und wasserstoffähnliche Ionen mit Kernladung $Z$ ($E_n = -Z^2 \frac{13{,}6\,\mathrm{eV}}{n^2}$).",
            tags=["Wasserstoff", "Bohr", "Rydberg", "Spektroskopie"],
            difficulty=2,
        ),
        # ==========================================
        # KLEINE FORMELN & INTUITION: KLASSISCHE MECHANIK
        # ==========================================
        Card(
            id="mech_kinetic_momentum",
            deck_id="mechanik",
            title="Kinetische Energie & Impuls (Intuition: v verdoppelt)",
            front=r"Wie lautet die Formel für die **kinetische Energie** ausgedrückt durch den **Impuls** $p$, und um welchen Faktor vervielfacht sich die kinetische Energie (bzw. der Bremsweg), wenn sich die Geschwindigkeit **verdoppelt**?",
            back=r"""**Formel:**
$$E_{\text{kin}} = \frac{1}{2} m v^2 = \frac{p^2}{2m}$$

**Physikalische Intuition:**
Verdoppelt sich die Geschwindigkeit ($v \to 2v$), so **vervierfacht** sich die kinetische Energie ($E_{\text{kin}} \to 4 E_{\text{kin}}$)!

Deshalb vervierfacht sich auch der Bremsweg eines Autos bei doppelter Geschwindigkeit ($W = F_{\text{Brems}} \cdot s = \Delta E_{\text{kin}}$).""",
            hint=r"Quadratische Abhängigkeit von der Geschwindigkeit.",
            formula_breakdown=r"""- $m$: Masse $[\mathrm{kg}]$
- $v$: Geschwindigkeit $[\mathrm{m/s}]$
- $p = mv$: Impuls $[\mathrm{kg\cdot m/s}]$""",
            physical_meaning=r"Grundlegende quadratische Energieskalierung der Newtonschen Mechanik. Die Schreibweise $\frac{p^2}{2m}$ ist der direkte Ausgangspunkt für den Hamilton-Operator in der analytischen und Quantenmechanik.",
            validity_domain=r"Klassische Mechanik ($v \ll c$).",
            tags=["Kinetische Energie", "Mechanik", "Intuition", "Faustformel"],
            difficulty=1,
        ),
        Card(
            id="mech_escape_velocity",
            deck_id="mechanik",
            title="Fluchtgeschwindigkeit (Zweite kosmische Geschwindigkeit)",
            front=r"Wie lautet die Formel für die **Fluchtgeschwindigkeit** $v_{\text{esc}}$ von der Oberfläche eines sphärischen Himmelskörpers und wie groß ist sie für die Erde?",
            back=r"""**Formel:**
$$v_{\text{esc}} = \sqrt{\frac{2 G M}{R}} = \sqrt{2 g R}$$

**Wert für die Erde:**
$$v_{\text{esc, Erde}} \approx 11{,}2 \, \mathrm{km/s} \approx 40\,300 \, \mathrm{km/h}$$""",
            hint=r"Aus Energieerhaltung: $E_{\text{kin}} + E_{\text{pot}} = \frac{1}{2}m v^2 - G\frac{Mm}{R} = 0$.",
            formula_breakdown=r"""- $G$: Gravitationskonstante
- $M$: Masse des Himmelskörpers (Erde $\approx 6 \times 10^{24} \, \mathrm{kg}$)
- $R$: Radius des Himmelskörpers (Erde $\approx 6371 \, \mathrm{km}$)
- $g = \frac{GM}{R^2}$: Oberflächenbeschleunigung""",
            physical_meaning=r"Mindestgeschwindigkeit, die ein kräftefreier Körper an der Oberfläche benötigt, um dem Gravitationsfeld des Himmelskörpers ohne weiteren Antrieb ins Unendliche zu entkommen (parabolische Fluchtbahn).",
            validity_domain=r"Klassische Newtonsche Gravitation ohne Luftwiderstand.",
            tags=["Fluchtgeschwindigkeit", "Gravitation", "Raumfahrt", "Mechanik"],
            difficulty=2,
        ),
        Card(
            id="mech_orbital_velocity",
            deck_id="mechanik",
            title="Erste kosmische Geschwindigkeit (Kreisbahngeschwindigkeit)",
            front=r"Wie lautet die Formel für die **Kreisbahngeschwindigkeit** $v_0$ (1. kosmische Geschwindigkeit) knapp über der Erdoberfläche und wie hängt sie mit der Fluchtgeschwindigkeit zusammen?",
            back=r"""**Formel:**
$$v_0 = \sqrt{\frac{G M}{R}} = \sqrt{g R}$$

**Wert für die Erde:**
$$v_0 \approx 7{,}9 \, \mathrm{km/s} \approx 8 \, \mathrm{km/s} \approx 28\,500 \, \mathrm{km/h}$$

**Zusammenhang mit der Fluchtgeschwindigkeit:**
$$v_{\text{esc}} = \sqrt{2} \cdot v_0 \approx 1{,}414 \cdot v_0$$""",
            hint=r"Gleichgewicht aus Gravitationskraft und Zentrifugalkraft: $G\frac{Mm}{R^2} = m\frac{v^2}{R}$.",
            formula_breakdown=r"""- $v_0$: Geschwindigkeit für einen erdnahen kreisförmigen Orbit (z.B. ISS bei ca. $400 \, \mathrm{km}$ Höhe mit $v \approx 7{,}7 \, \mathrm{km/s}$, Umlaufdauer ca. $90 \, \text{Minuten}$).""",
            physical_meaning=r"Minimal nötige Geschwindigkeit, um ohne Absturz um einen Planeten zu kreisen.",
            validity_domain=r"Kreisbahnen im Vakuum.",
            tags=["Kreisbahn", "Orbit", "Gravitation", "Mechanik"],
            difficulty=1,
        ),
        Card(
            id="mech_pendulum_period",
            deck_id="mechanik",
            title="Schwingungsdauer eines Fadenpendels (Mathematisches Pendel)",
            front=r"Wie lautet die Formel für die **Schwingungsdauer** $T$ eines mathematischen Fadenpendels und wie ändert sich $T$, wenn man die **Masse verdoppelt** bzw. die **Länge vervierfacht**?",
            back=r"""**Formel:**
$$T = 2\pi \sqrt{\frac{l}{g}}$$

**Physikalische Intuition:**
1. **Masse verdoppeln:** Ändert die Schwingungsdauer **überhaupt nicht** ($T$ ist unabhängig von der Masse $m$, da schwere Masse $=$ träge Masse!).
2. **Fadenlänge vervierfachen ($l \to 4l$):** Die Schwingungsdauer **verdoppelt sich** ($T \to 2T$), wegen der Quadratwurzel!

**Faustregel:** Ein Pendel mit $l \approx 1 \, \mathrm{m}$ hat eine Halbschwingung von ca. $1 \, \mathrm{s}$ ($T \approx 2 \, \mathrm{s}$).""",
            hint=r"Zwei Pi Wurzel aus l durch g.",
            formula_breakdown=r"""- $l$: Fadenlänge $[\mathrm{m}]$
- $g$: Erdbeschleunigung $\approx 9{,}81 \, \mathrm{m/s^2}$
- Kleinwinkelnäherung: $\sin\varphi \approx \varphi$""",
            physical_meaning=r"Klassisches Beispiel für harmonische Schwingungen. Die Unabhängigkeit von der Amplitude (bei kleinen Winkeln) entdeckte Galileo Galilei und begründete den Bau mechanischer Pendeluhren durch Huygens.",
            validity_domain=r"Kleine Auslenkwinkel $\varphi \ll 1$ (für große Winkel: elliptische Integrale).",
            tags=["Pendel", "Schwingung", "Intuition", "Mechanik"],
            difficulty=1,
        ),
        Card(
            id="mech_spring_potential",
            deck_id="mechanik",
            title="Potenzielle Energie einer Feder (Hookesches Gesetz)",
            front=r"Wie lautet die Formel für die **potenzielle Energie** einer linearen Feder mit Federkonstante $k$ bei Auslenkung $x$?",
            back=r"""$$E_{\text{pot}} = \frac{1}{2} k x^2$$

Herleitung aus der Federkraft $F = kx$:
$$E_{\text{pot}} = \int_0^x F(x') \, dx' = \int_0^x k x' \, dx' = \frac{1}{2} k x^2$$""",
            hint=r"Halbe mal k mal x-Quadrat.",
            formula_breakdown=r"""- $k$: Federkonstante (Federhärte) in $[\mathrm{N/m}]$
- $x$: Auslenkung aus der Ruhelage in $[\mathrm{m}]$
- $E_{\text{pot}}$: Gespeicherte elastische Energie in $[\mathrm{J}]$""",
            physical_meaning=r"Quadratisches Potenzial. Da jede glatte Potenzialkurve um ein lokales Minimum als Parabel genähert werden kann, beschreibt dies jede Schwingung bei kleiner Anregung.",
            validity_domain=r"Linear elastischer Bereich (unterhalb der Fließgrenze des Materials).",
            tags=["Feder", "Energie", "Hooke", "Mechanik"],
            difficulty=1,
        ),
        Card(
            id="mech_grav_potential",
            deck_id="mechanik",
            title="Gravitationspotenzial und potenzielle Energie",
            front=r"Wie lautet die Formel für die **potenzielle Gravitationsenergie** zweier Punktmassen $M$ und $m$ im Abstand $r$ (mit Konvention $V(\infty) = 0$)?",
            back=r"""$$E_{\text{pot}}(r) = -G \frac{M m}{r}$$

Gravitationspotenzial $\Phi(r) = \frac{E_{\text{pot}}}{m}$:
$$\Phi(r) = -G \frac{M}{r}$$""",
            hint=r"Achte auf das fundamentale Minuszeichen!",
            formula_breakdown=r"""- $G$: Gravitationskonstante
- $M, m$: Massen
- $r$: Abstand der Schwerpunkte
- Minuszeichen: Gravitation ist rein anziehend. Man muss Arbeit hineinstecken, um die Massen voneinander zu trennen.""",
            physical_meaning=r"Gebundene Zustände besitzen negative Gesamtenergie ($E_{\text{tot}} = E_{\text{kin}} + E_{\text{pot}} < 0$).",
            validity_domain=r"Newtonsches Gravitationsgesetz für Abstände außerhalb der Massenverteilungen.",
            tags=["Gravitation", "Potenzial", "Energie", "Mechanik"],
            difficulty=1,
        ),
        # ==========================================
        # KLEINE FORMELN & INTUITION: ELEKTRODYNAMIK
        # ==========================================
        Card(
            id="em_ohms_law_power",
            deck_id="elektrodynamik",
            title="Ohmsches Gesetz & Elektrische Verlustleistung",
            front=r"Wie lautet das **Ohmsche Gesetz** und wie berechnet sich die **elektrische Leistung** $P$ aus Spannung $U$, Strom $I$ und Widerstand $R$?",
            back=r"""**Ohmsches Gesetz:**
$$U = R \cdot I \iff I = \frac{U}{R}$$

**Elektrische Leistung (Joulesche Wärme):**
$$P = U \cdot I = I^2 \cdot R = \frac{U^2}{R}$$""",
            hint=r"Leistung ist Strom mal Spannung, oder $I^2 R$.",
            formula_breakdown=r"""- $U$: Elektrische Spannung $[\mathrm{V}]$
- $I$: Stromstärke $[\mathrm{A}]$
- $R$: Elektrischer Widerstand $[\Omega = \mathrm{V/A}]$
- $P$: Leistung $[\mathrm{W} = \mathrm{J/s}]$""",
            physical_meaning=r"Verdoppelt man den Strom durch einen Widerstand, vervierfacht sich die Wärmeleistung ($P \propto I^2$). Deshalb transportieren Hochspannungsleitungen elektrische Energie bei extrem hoher Spannung und minimalem Strom, um Leitungsverluste zu minimieren.",
            validity_domain=r"Ohmsche Leiter (temperaturunabhängig bzw. stationär).",
            tags=["Ohmsches Gesetz", "Leistung", "Elektrodynamik", "Grundwissen"],
            difficulty=1,
        ),
        Card(
            id="em_capacitor_capacitance",
            deck_id="elektrodynamik",
            title="Kapazität des Plattenkondensators & Gespeicherte Energie",
            front=r"Wie lauten die Formeln für die **Kapazität** $C$ eines Plattenkondensators und die im elektrischen Feld **gespeicherte Energie** $W$?",
            back=r"""**Kapazität:**
$$C = \frac{Q}{U} = \varepsilon_0 \varepsilon_r \frac{A}{d}$$

**Gespeicherte Energie:**
$$W = \frac{1}{2} C U^2 = \frac{1}{2} \frac{Q^2}{C} = \frac{1}{2} Q U$$""",
            hint=r"Halbe mal C mal U-Quadrat (analog zu $\frac{1}{2}mv^2$ und $\frac{1}{2}kx^2$!).",
            formula_breakdown=r"""- $A$: Plattenfläche $[\mathrm{m^2}]$
- $d$: Plattenabstand $[\mathrm{m}]$
- $\varepsilon_0$: Elektrische Feldkonstante
- $\varepsilon_r$: Relative Dielektrizitätszahl des Zwischenmediums""",
            physical_meaning=r"Die Energie ist im elektrischen Feld im Raum zwischen den Platten gespeichert mit der Energiedichte $w_e = \frac{1}{2} \varepsilon_0 E^2$.",
            validity_domain=r"Plattenkondensator mit homogener Feldverteilung (Randeffekte vernachlässigt, d.h. $d \ll \sqrt{A}$).",
            tags=["Kondensator", "Kapazität", "Energie", "Elektrodynamik"],
            difficulty=1,
        ),
        Card(
            id="em_inductor_energy",
            deck_id="elektrodynamik",
            title="Gespeicherte Energie einer Spule (Induktivität)",
            front=r"Wie lautet die Formel für die im **Magnetfeld einer Induktivität** $L$ gespeicherte Energie $W$ bei Strom $I$?",
            back=r"""$$W = \frac{1}{2} L I^2$$

(Magnetische Energiedichte: $w_m = \frac{1}{2\mu_0} B^2$)""",
            hint=r"Halbe mal L mal I-Quadrat (vollkommen analog zum Kondensator $\frac{1}{2}CU^2$!).",
            formula_breakdown=r"""- $L$: Induktivität $[\mathrm{H} = \mathrm{V\cdot s / A}]$
- $I$: Momentane Stromstärke $[\mathrm{A}]$
- $W$: Gespeicherte magnetische Energie $[\mathrm{J}]$""",
            physical_meaning=r"Analog zur kinetischen Energie $\frac{1}{2}mv^2$: Der Strom $I$ kann wegen der Selbstinduktionsspannung $U_{\text{ind}} = -L \frac{dI}{dt}$ nicht sprunghaft geändert werden (Trägheit des Stromflusses).",
            validity_domain=r"Lineare Magnetwerkstoffe ohne magnetische Sättigung.",
            tags=["Spule", "Induktivität", "Energie", "Magnetismus"],
            difficulty=1,
        ),
        Card(
            id="em_lc_circuit",
            deck_id="elektrodynamik",
            title="Thomsonsche Schwingungsformel (LC-Schwingkreis)",
            front=r"Wie lautet die **Thomsonsche Schwingungsformel** für die Resonanz-Kreisfrequenz $\omega_0$ und Periodendauer $T$ eines ungedämpften **LC-Schwingkreises**?",
            back=r"""$$\omega_0 = \frac{1}{\sqrt{L C}}$$

Periodendauer und Resonanzfrequenz:
$$T = \frac{2\pi}{\omega_0} = 2\pi \sqrt{L C}, \qquad f_0 = \frac{1}{2\pi \sqrt{L C}}$$""",
            hint=r"Eins durch Wurzel aus L mal C.",
            formula_breakdown=r"""- $L$: Induktivität der Spule $[\mathrm{H}]$
- $C$: Kapazität des Kondensators $[\mathrm{F}]$
- Analogie zur Mechanik: $L \leftrightarrow m$ (Trägheit), $\frac{1}{C} \leftrightarrow k$ (Federhärte), $\omega_0 = \sqrt{\frac{k}{m}} \leftrightarrow \frac{1}{\sqrt{LC}}$""",
            physical_meaning=r"Periodischer Austausch zwischen elektrischer Feldenergie im Kondensator ($\frac{1}{2}CU^2$) und magnetischer Feldenergie in der Spule ($\frac{1}{2}LI^2$). Grundlage aller Radioempfänger, Sender und Schwingquarze.",
            validity_domain=r"Verlustfreier LC-Kreis (ohne ohmschen Widerstand $R=0$).",
            tags=["Schwingkreis", "Thomson", "Resonanz", "Elektrodynamik"],
            difficulty=1,
        ),
        Card(
            id="em_snell_law",
            deck_id="elektrodynamik",
            title="Brechungsgesetz von Snellius",
            front=r"Wie lautet das **Snelliussche Brechungsgesetz** der geometrischen Optik an der Grenzfläche zweier Medien mit Brechungsindizes $n_1$ und $n_2$?",
            back=r"""$$n_1 \sin \alpha_1 = n_2 \sin \alpha_2$$

Mit Brechungsindex $n = \frac{c}{v}$:
$$\frac{\sin \alpha_1}{\sin \alpha_2} = \frac{n_2}{n_1} = \frac{v_1}{v_2} = \frac{\lambda_1}{\lambda_2}$$""",
            hint=r"$n_1 \sin \alpha_1 = n_2 \sin \alpha_2$.",
            formula_breakdown=r"""- $\alpha_1$: Einfallswinkel zum Lot
- $\alpha_2$: Brechungswinkel zum Lot
- $n$: Brechungsindex (Vakuum $n=1$, Luft $n \approx 1{,}0003$, Wasser $n \approx 1{,}33$, Glas $n \approx 1{,}5$)
- Übergang von optisch dünner zu dichter ($n_2 > n_1$): Brechung **zum Lot hin** ($\alpha_2 < \alpha_1$).""",
            physical_meaning=r"Folgt direkt aus dem Fermatschen Prinzip des kürzesten Lichtwegs (Licht nimmt stets den zeitlich schnellsten Weg zwischen zwei Punkten). Bei Übergang von optisch dicht zu dünn existiert Totalreflexion für $\sin\alpha_c = \frac{n_2}{n_1}$.",
            validity_domain=r"Isotrope, homogene Medien.",
            tags=["Optik", "Brechung", "Snellius", "Fermat"],
            difficulty=1,
        ),
        Card(
            id="em_c_from_constants",
            deck_id="elektrodynamik",
            title="Lichtgeschwindigkeit aus ε_0 und μ_0",
            front=r"Welche fundamentale Gleichung verknüpft die **Lichtgeschwindigkeit** $c$ mit der elektrischen Feldkonstante $\varepsilon_0$ und der magnetischen Feldkonstante $\mu_0$?",
            back=r"""$$c = \frac{1}{\sqrt{\varepsilon_0 \mu_0}}$$""",
            hint=r"Eins durch die Quadratwurzel aus Epsilon-Null mal My-Null.",
            formula_breakdown=r"""- $\varepsilon_0 \approx 8{,}854 \times 10^{-12} \, \mathrm{F/m}$
- $\mu_0 = 4\pi \times 10^{-7} \, \mathrm{N/A^2}$
- Setzt man beide Werte ein, erhält man exakt $c \approx 2{,}998 \times 10^8 \, \mathrm{m/s}$!""",
            physical_meaning=r"Maxwells historische Entdeckung: Als Maxwell die Ausbreitungsgeschwindigkeit elektromagnetischer Wellen aus rein elektrostatischen ($\varepsilon_0$) und magnetostatischen ($\mu_0$) Laborwerten berechnete und der Wert exakt mit der gemessenen Lichtgeschwindigkeit übereinstimmte, erkannte er: **Licht ist eine elektromagnetische Welle!**",
            validity_domain=r"Vakuum.",
            tags=["Licht", "Maxwell", "Elektrodynamik", "Historisch"],
            difficulty=1,
        ),
        # ==========================================
        # KLEINE FORMELN & INTUITION: THERMODYNAMIK
        # ==========================================
        Card(
            id="td_molar_volume_gas",
            deck_id="thermodynamik",
            title="Molares Volumen eines idealen Gases (Normalbedingungen)",
            front=r"Wie groß ist das **molare Volumen** $V_m$ eines idealen Gases bei **Standard-Normalbedingungen** ($T_0 = 0^\circ\mathrm{C} = 273{,}15 \, \mathrm{K}$ und $p_0 = 1013{,}25 \, \mathrm{hPa}$)?",
            back=r"""$$V_m \approx 22{,}4 \, \frac{\mathrm{l}}{\mathrm{mol}} = 0{,}0224 \, \frac{\mathrm{m^3}}{\mathrm{mol}}$$

(Bei Standard-Raumtemperatur $20^\circ\mathrm{C}$ und $1 \, \mathrm{bar}$: $V_m \approx 24{,}4 \, \mathrm{l/mol}$)""",
            hint=r"22,4 Liter pro Mol.",
            formula_breakdown=r"""- Berechnet aus $V_m = \frac{R T_0}{p_0} = \frac{8{,}314 \times 273{,}15}{101\,325} \, \mathrm{m^3/mol}$""",
            physical_meaning=r"Amédéo Avogadros Hypothese (1811): Gleiche Volumina beliebiger Gase enthalten bei gleichem Druck und gleicher Temperatur stets die gleiche Anzahl an Molekülen, unabhängig von der Art oder chemischen Zusammensetzung des Gases!",
            validity_domain=r"Ideales Gas (verdünnte Gase weit oberhalb des Siedepunkts).",
            tags=["Gase", "Molares Volumen", "Thermodynamik", "Chemie"],
            difficulty=1,
        ),
        Card(
            id="td_stefan_boltzmann_law",
            deck_id="thermodynamik",
            title="Stefan-Boltzmann-Gesetz (T^4-Abhängigkeit)",
            front=r"Wie lautet das **Stefan-Boltzmann-Gesetz** für die gesamte thermische Strahlungsleistung $P$ eines schwarzen Körpers und um welchen Faktor steigt die Abstrahlung, wenn man die absolute Temperatur **verdoppelt**?",
            back=r"""**Formel:**
$$P = \sigma \cdot A \cdot T^4$$

Strahlungsfluss / Intensität:
$$j = \frac{P}{A} = \sigma T^4$$

**Physikalische Intuition:**
Wegen der **4. Potenz** ($T^4$):
Verdoppelt man die absolute Temperatur ($T \to 2T$), steigt die emittierte Wärmestrahlung um das **16-fache** ($2^4 = 16$)!
Verdreifacht man die Temperatur, steigt sie um das **81-fache** ($3^4 = 81$)!""",
            hint=r"Sigma mal Fläche mal Temperatur hoch vier.",
            formula_breakdown=r"""- $\sigma \approx 5{,}670 \times 10^{-8} \, \frac{\mathrm{W}}{\mathrm{m^2 K^4}}$: Stefan-Boltzmann-Konstante
- $A$: Oberfläche $[\mathrm{m^2}]$
- $T$: Absolute Temperatur in Kelvin $[\mathrm{K}]$""",
            physical_meaning=r"Beschreibt die Gesamtemission über alle Wellenlängen (Integral über das Plancksche Strahlungsspektrum). Erklärt, warum glühende Metalle bei steigender Temperatur extrem viel schneller Energie abstrahlen und warum Sterne ihre Leuchtkraft primär über die Oberflächentemperatur steuern.",
            validity_domain=r"Idealer schwarzer Strahler im thermischen Gleichgewicht (für reale Körper: $P = \varepsilon \sigma A T^4$ mit Emissionsgrad $\varepsilon \le 1$).",
            tags=["Strahlung", "Stefan-Boltzmann", "Thermodynamik", "Intuition"],
            difficulty=2,
        ),
        Card(
            id="td_wien_displacement",
            deck_id="thermodynamik",
            title="Wiensches Verschiebungsgesetz",
            front=r"Wie lautet das **Wiensche Verschiebungsgesetz** für das Wellenlängenmaximum $\lambda_{\text{max}}$ der thermischen Schwarzkörperstrahlung bei Temperatur $T$?",
            back=r"""$$\lambda_{\text{max}} \cdot T = b \approx 2{,}898 \times 10^{-3} \, \mathrm{m \cdot K} \approx 2900 \, \mathrm{\mu m \cdot K}$$

Oder:
$$\lambda_{\text{max}} = \frac{b}{T}$$""",
            hint=r"Produkt aus Wellenlängenmaximum und Temperatur ist konstant ($\approx 2{,}9 \times 10^{-3} \, \mathrm{m\cdot K}$).",
            formula_breakdown=r"""- $b \approx 2{,}898 \times 10^{-3} \, \mathrm{m\cdot K}$: Wiensche Verschiebungskonstante
- **Beispiel Sonne:** $T_{\text{Sonne}} \approx 5800 \, \mathrm{K} \implies \lambda_{\text{max}} \approx \frac{2{,}9 \times 10^{-3}}{5800} \approx 500 \, \mathrm{nm}$ (mitten im sichtbaren, grün-gelben Bereich!).
- **Beispiel Mensch:** $T \approx 310 \, \mathrm{K} \implies \lambda_{\text{max}} \approx 9{,}3 \, \mathrm{\mu m}$ (thermisches Infrarot!).""",
            physical_meaning=r"Je heißer ein Körper wird, desto kürzer ist die Wellenlänge, bei der er am stärksten strahlt (Verschiebung von Infrarot über Dunkelrot, Gelb nach Weiß und schließlich Blau).",
            validity_domain=r"Plancksche Hohlraumstrahlung / Schwarzer Körper.",
            tags=["Wien", "Strahlung", "Spektrum", "Thermodynamik"],
            difficulty=2,
        ),
        Card(
            id="td_carnot_efficiency",
            deck_id="thermodynamik",
            title="Carnot-Wirkungsgrad",
            front=r"Wie lautet die Formel für den maximal möglichen **Carnot-Wirkungsgrad** $\eta_C$ einer zyklischen Wärmekraftmaschine zwischen zwei Temperaturniveaus $T_{\text{heiß}}$ und $T_{\text{kalt}}$?",
            back=r"""$$\eta_C = 1 - \frac{T_{\text{kalt}}}{T_{\text{heiß}}} = \frac{T_{\text{heiß}} - T_{\text{kalt}}}{T_{\text{heiß}}}$$""",
            hint=r"Eins minus Temperatur kalt durch Temperatur heiß (in Kelvin!).",
            formula_breakdown=r"""- $T_{\text{heiß}}$: Absolute Temperatur des Wärmereservoirs $[\mathrm{K}]$
- $T_{\text{kalt}}$: Absolute Temperatur der Wärmesenke / Umgebung $[\mathrm{K}]$
- Immer in **Kelvin** rechnen, niemals in Grad Celsius!""",
            physical_meaning=r"Fundamentale obere Grenze nach dem 2. Hauptsatz der Thermodynamik: Keine reale Wärmekraftmaschine (Verbrennungsmotor, Dampfturbine, Gasturbine) kann effizienter sein als der ideale Carnot-Prozess. Ein Wirkungsgrad von $100\,\%$ erfordert $T_{\text{kalt}} = 0 \, \mathrm{K}$ (was nach dem 3. Hauptsatz unerreichbar ist!).",
            validity_domain=r"Reversible Kreisprozesse.",
            tags=["Carnot", "Wirkungsgrad", "Thermodynamik", "Hauptsätze"],
            difficulty=1,
        ),
        Card(
            id="td_ideal_gas_law",
            deck_id="thermodynamik",
            title="Thermische Zustandsgleichung des idealen Gases",
            front=r"Wie lautet die **Zustandsgleichung des idealen Gases** in mikroskopischer und makroskopischer Form?",
            back=r"""**Makroskopische Form (mit Stoffmenge $n$ und Gaskonstante $R$):**
$$p V = n R T$$

**Mikroskopische Form (mit Teilchenzahl $N$ und Boltzmann-Konstante $k_B$):**
$$p V = N k_B T$$

Zusammenhang:
$$n R = N k_B \quad (\text{da } R = N_A k_B \text{ und } N = n N_A)$$""",
            hint=r"$p V = n R T = N k_B T$.",
            formula_breakdown=r"""- $p$: Druck $[\mathrm{Pa} = \mathrm{N/m^2}]$
- $V$: Volumen $[\mathrm{m^3}]$
- $T$: Absolute Temperatur $[\mathrm{K}]$
- $n$: Stoffmenge $[\mathrm{mol}]$
- $R \approx 8{,}314 \, \mathrm{J/(mol\cdot K)}$
- $N$: Absolute Teilchenanzahl
- $k_B \approx 1{,}381 \times 10^{-23} \, \mathrm{J/K}$""",
            physical_meaning=r"Verknüpft die thermischen Zustandsgrößen eines idealisierten Gases ohne Eigenvolumen und ohne zwischenmolekulare Anziehungskräfte (Kombination aus Boyle-Mariotte, Gay-Lussac und Amontons).",
            validity_domain=r"Ideales Gas (hohe Temperaturen und niedrige Drücke. Bei realen Gasen: Van-der-Waals-Gleichung).",
            tags=["Ideales Gas", "Thermodynamik", "Zustandsgleichung"],
            difficulty=1,
        ),
        Card(
            id="math_taylor_approximations",
            deck_id="mathe_physik",
            title="Wichtige Taylor-Reihen & Kleinwinkelnäherungen",
            front=r"Wie lauten die wichtigsten **Taylor-Näherungen für kleine Größen** ($|x| \ll 1$) für $\sin x$, $\cos x$, $e^x$, $\ln(1+x)$ und $(1+x)^\alpha$?",
            back=r"""$$\sin x \approx x - \frac{x^3}{6} \approx x$$
$$\cos x \approx 1 - \frac{x^2}{2}$$
$$\tan x \approx x$$
$$e^x \approx 1 + x + \frac{x^2}{2} \approx 1 + x$$
$$\ln(1+x) \approx x - \frac{x^2}{2} \approx x$$
$$(1+x)^\alpha \approx 1 + \alpha x$$

**Wichtige Spezialfälle der binomischen Näherung:**
$$\sqrt{1+x} \approx 1 + \frac{1}{2}x, \qquad \frac{1}{\sqrt{1+x}} \approx 1 - \frac{1}{2}x, \qquad \frac{1}{1+x} \approx 1 - x$$""",
            hint=r"Sinus und Tangens fangen mit $x$ an, Kosinus mit $1 - x^2/2$, binomische Näherung mit $1 + \alpha x$.",
            formula_breakdown=r"""- Taylor-Formel um $x_0 = 0$ (Maclaurin-Reihe):
  $f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \dots$
- $|x| \ll 1$: Höhere Ordnungen $\mathcal{O}(x^2)$ bzw. $\mathcal{O}(x^3)$ werden vernachlässigt.""",
            physical_meaning=r"Das universelle Werkzeug der theoretischen und angewandten Physik: Linearisierung von Differentialgleichungen, Kleinwinkelnäherung des Fadenpendels, relativistische Korrektur kinetischer Energie ($\gamma \approx 1 + \frac{1}{2}v^2/c^2$), Dipol- und Multipolentwicklungen.",
            validity_domain=r"Konvergenzbereich der jeweiligen Reihe für kleine Argumente $|x| \ll 1$.",
            tags=["Taylor", "Näherung", "Mathematische Methoden", "Intuition"],
            difficulty=1,
        ),
        Card(
            id="math_gaussian_integral",
            deck_id="mathe_physik",
            title="Gaußsches Fehlerintegral (Euler-Poisson-Integral)",
            front=r"Wie lautet der Wert des uneigentlichen **Gauß-Integrals** $\int_{-\infty}^{+\infty} e^{-a x^2} \, dx$ für $a > 0$?",
            back=r"""$$\int_{-\infty}^{+\infty} e^{-a x^2} \, dx = \sqrt{\frac{\pi}{a}}$$

Für die Standard-Normalverteilung ($a = \frac{1}{2\sigma^2}$):
$$\int_{-\infty}^{+\infty} \exp\left(-\frac{x^2}{2\sigma^2}\right) \, dx = \sigma \sqrt{2\pi}$$""",
            hint=r"Wurzel aus Pi durch a.",
            formula_breakdown=r"""- $a > 0$: Konvergenzparameter
- Berechnungstrick von Gauß/Poisson über 2D-Polarkoordinaten:
  $I^2 = \int_{-\infty}^\infty e^{-ax^2} dx \int_{-\infty}^\infty e^{-ay^2} dy = \int_0^{2\pi} d\varphi \int_0^\infty r e^{-ar^2} dr = 2\pi \left[ -\frac{e^{-ar^2}}{2a} \right]_0^\infty = \frac{\pi}{a}$""",
            physical_meaning=r"Tritt überall in der Natur auf: Normierung von Wahrscheinlichkeitsdichten, kinetische Gastheorie, Zustandssummen in der statistischen Mechanik, quantenmechanischer Grundzustand des harmonischen Oszillators und Feynman-Pfadintegrale.",
            validity_domain=r"Reelle Integrationsgrenzen von $-\infty$ bis $+\infty$ und reelles $a > 0$.",
            tags=["Gauß-Integral", "Analysis", "Statistik", "Mathematische Methoden"],
            difficulty=2,
        ),
        Card(
            id="const_gas_constant",
            deck_id="konstanten",
            title="Universelle Gaskonstante (R)",
            front=r"Wie groß ist die **universelle Gaskonstante** $R$ und wie hängt sie mit der Avogadro- und Boltzmann-Konstante zusammen?",
            back=r"""$$R \approx 8{,}314 \, \frac{\mathrm{J}}{\mathrm{mol \cdot K}}$$

Exakter Zusammenhang:
$$R = N_A \cdot k_B$$""",
            hint=r"Rund 8,31 Joule pro Mol und Kelvin.",
            formula_breakdown=r"""- $N_A \approx 6{,}022 \times 10^{23} \, \mathrm{mol^{-1}}$: Avogadro-Konstante
- $k_B \approx 1{,}381 \times 10^{-23} \, \mathrm{J/K}$: Boltzmann-Konstante
- Multipliziert man die mikroskopische Energie pro Kelvin ($k_B$) mit einem Mol ($N_A$), erhält man exakt $R$.""",
            physical_meaning=r"Die molare Skalierungskonstante der Thermodynamik. Tritt in der idealen Gasgleichung ($pV = nRT$), der Nernst-Gleichung und der Reaktionskinetik (Arrhenius-Gleichung) auf.",
            validity_domain=r"Universell für ideale thermodynamische Systeme.",
            tags=["Gaskonstante", "Konstanten", "Thermodynamik", "Chemie"],
            difficulty=1,
        ),
        Card(
            id="mech_centripetal",
            deck_id="mechanik",
            title="Zentripetalbeschleunigung und Zentripetalkraft",
            front=r"Wie lauten die Formeln für die **Zentripetalbeschleunigung** $a_z$ und **Zentripetalkraft** $F_z$ einer gleichförmigen Kreisbewegung mit Radius $r$ und Bahngeschwindigkeit $v$?",
            back=r"""**Zentripetalbeschleunigung:**
$$a_z = \frac{v^2}{r} = \omega^2 \cdot r$$

**Zentripetalkraft (zum Kreiszentrum gerichtet):**
$$F_z = m \cdot a_z = m \, \frac{v^2}{r} = m \, \omega^2 \, r$$""",
            hint=r"$v^2/r$ oder $\omega^2 r$.",
            formula_breakdown=r"""- $v$: Bahngeschwindigkeit $[\mathrm{m/s}]$
- $r$: Bahnradius $[\mathrm{m}]$
- $\omega = \frac{v}{r} = 2\pi f$: Winkelgeschwindigkeit $[\mathrm{rad/s}]$
- $m$: Masse des umlaufenden Körpers $[\mathrm{kg}]$""",
            physical_meaning=r"**Physikalische Intuition:** Die Zentripetalkraft skaliert quadratisch mit der Geschwindigkeit ($F_z \propto v^2$)! Fährt man mit doppelter Geschwindigkeit durch dieselbe Kurve ($v \to 2v$), benötigt man die **4-fache** Reibungskraft der Reifen, um nicht aus der Kurve geschleudert zu werden.",
            validity_domain=r"Kreisbewegung im Inertialsystem (im rotierenden Bezugssystem entspricht ihr die nach außen gerichtete Zentrifugalkraft als Trägheitskraft).",
            tags=["Kreisbewegung", "Zentripetalkraft", "Mechanik", "Intuition"],
            difficulty=1,
        ),
        Card(
            id="mech_angular_momentum",
            deck_id="mechanik",
            title="Drehimpuls, Drehmoment & Drehimpulserhaltung",
            front=r"Wie sind **Drehimpuls** $\vec{L}$ und **Drehmoment** $\vec{M}$ definiert und was besagt der **Pirouetteneffekt**?",
            back=r"""**Drehimpuls:**
$$\vec{L} = \vec{r} \times \vec{p} = I \cdot \vec{\omega}$$

**Drehmoment (zeitliche Änderung des Drehimpulses):**
$$\vec{M} = \vec{r} \times \vec{F} = \frac{d\vec{L}}{dt} = \dot{\vec{L}}$$

**Drehimpulserhaltung (Pirouetteneffekt):**
Ist das resultierende äußere Drehmoment null ($\vec{M} = 0$), so bleibt der Gesamtdrehimpuls konstant:
$$\vec{L} = I \cdot \vec{\omega} = \text{const.} \implies I_1 \omega_1 = I_2 \omega_2$$""",
            hint=r"Hebelarm Kreuz Kraft, bzw. Trägheitsmoment mal Winkelgeschwindigkeit.",
            formula_breakdown=r"""- $\vec{r}$: Ortsvektor vom Drehpunkt $[\mathrm{m}]$
- $\vec{p} = m\vec{v}$: Linearer Impuls $[\mathrm{kg\cdot m/s}]$
- $I$: Trägheitsmoment bezüglich der Drehachse $[\mathrm{kg\cdot m^2}]$
- $\vec{\omega}$: Winkelgeschwindigkeitsvektor $[\mathrm{rad/s}]$""",
            physical_meaning=r"Zieht eine Eiskunstläuferin bei einer Pirouette die Arme an ihren Körper heran, sinkt ihr Trägheitsmoment $I$ ($\propto r^2$). Zur Drehimpulserhaltung steigt ihre Winkelgeschwindigkeit $\omega$ dramatisch an! Gleiches Prinzip bei Neutronensternen (Pulsaren), die beim Kollaps eines Riesensterns auf Millisekunden-Perioden beschleunigen.",
            validity_domain=r"Starrkörper- und Teilchendynamik im Inertialsystem.",
            tags=["Drehimpuls", "Drehmoment", "Erhaltungssatz", "Mechanik"],
            difficulty=1,
        ),
        Card(
            id="td_bernoulli",
            deck_id="thermodynamik",
            title="Bernoulli-Gleichung & Hydrostatischer Druck",
            front=r"Wie lauten die **Bernoulli-Gleichung** für stationäre, inkompressible und reibungsfreie Strömungen und wie berechnet sich der **hydrostatische Schweredruck** in Tiefe $h$?",
            back=r"""**Bernoulli-Gleichung:**
$$p + \frac{1}{2}\rho v^2 + \rho g h = \text{const.}$$

**Hydrostatischer Schweredruck einer ruhenden Flüssigkeitssäule:**
$$p_{\text{hydr}} = \rho \cdot g \cdot h$$""",
            hint=r"Statischer Druck + Staudruck + geodätischer Druck = konstant.",
            formula_breakdown=r"""- $p$: Statischer Druck $[\mathrm{Pa}]$
- $\frac{1}{2}\rho v^2$: Dynamischer Druck (Staudruck) $[\mathrm{Pa}]$
- $\rho g h$: Geodätischer Schweredruck $[\mathrm{Pa}]$
- $\rho$: Dichte des Fluids $[\mathrm{kg/m^3}]$ (Wasser $\approx 1000 \, \mathrm{kg/m^3}$, Luft $\approx 1{,}2 \, \mathrm{kg/m^3}$)
- $g \approx 9{,}81 \, \mathrm{m/s^2}$: Erdbeschleunigung""",
            physical_meaning=r"""**Physikalische Intuition:**
1. **Bernoulli:** Fließt ein Fluid schneller ($v$ steigt), sinkt der statische Druck $p$ (Venturi-Düse, Wasserstrahlpumpe, Auftrieb am Tragflügel).
2. **Tauchtiefe:** In Wasser ($\rho \approx 1000 \, \mathrm{kg/m^3}$) steigt der hydrostatische Druck pro $10 \, \mathrm{m}$ Tiefe um ziemlich genau $1 \, \mathrm{bar}$ ($1000 \times 9{,}81 \times 10 \approx 10^5 \, \mathrm{Pa}$).""",
            validity_domain=r"Ideale Flüssigkeiten/Gase: stationär, inkompressibel ($v \ll c_s$), reibungsfrei entlang einer Stromlinie.",
            tags=["Hydrodynamik", "Bernoulli", "Druck", "Intuition"],
            difficulty=2,
        ),
        Card(
            id="qm_heisenberg_energy_time",
            deck_id="quantenmechanik",
            title="Energie-Zeit-Unschärferelation & Lebensdauer",
            front=r"Wie lautet die **Energie-Zeit-Unschärferelation** und wie hängt die energetische **Linienbreite / Zerfallsbreite** $\Gamma$ mit der Lebensdauer $\tau$ eines Zustands zusammen?",
            back=r"""$$\Delta E \cdot \Delta t \ge \frac{\hbar}{2}$$

Für einen Zustand mit mittlerer Zerfallslebensdauer $\tau$ gilt für die energetische Linienbreite:
$$\Gamma = \Delta E \approx \frac{\hbar}{\tau}$$""",
            hint=r"Produkt aus Energieunsicherheit und Zeitdauer ist mindestens $\hbar/2$.",
            formula_breakdown=r"""- $\Delta E = \Gamma$: Energieunschärfe / natürliche Zerfallsbreite $[\mathrm{eV}]$
- $\tau = \Delta t$: Mittlere Lebensdauer des Zustands bzw. Teilchens $[\mathrm{s}]$
- $\hbar \approx 6{,}582 \times 10^{-16} \, \mathrm{eV\cdot s}$
- Im Gegensatz zur Ort-Impuls-Unschärfe ist Zeit in der Standard-Quantenmechanik kein Operator, sondern ein Parameter.""",
            physical_meaning=r"**Physikalische Intuition:** Je kürzer ein Quantenzustand oder ein instabiles Elementarteilchen existiert (extrem kleines $\tau$), desto unschärfer ist seine Energie bzw. invariante Ruhemasse ($E=mc^2$). Extrem kurzlebige Resonanzen (z.B. $W^\pm$-, $Z^0$- oder Higgs-Boson) erscheinen im Detektor als breite Energieverteilungen mit $\Gamma \sim \mathrm{GeV}$.",
            validity_domain=r"Quantenmechanik und Quantenfeldtheorie bei instabilen Zuständen und spektralen Linien.",
            tags=["Unschärfe", "Lebensdauer", "Linienbreite", "Quantenmechanik"],
            difficulty=3,
        ),
        # ==========================================
        # DECK: REINE MATHEMATIK & ANALYSIS
        # ==========================================
        Card(
            id="math_l2_space_definition",
            deck_id="reine_mathematik",
            title=r"$L^2$-Raum: Definition & Norm",
            front=r"Was versteht man unter dem Funktionenraum $L^2(\Omega)$ der **quadratintegrierbaren Funktionen** und wie ist die zugehörige **$L^2$-Norm** $\|f\|_2$ definiert?",
            back=r"""$$L^2(\Omega) = \left\{ f: \Omega \to \mathbb{C} \;\middle|\; \int_\Omega |f(x)|^2 \, dx < \infty \right\}$$

Die zugehörige **$L^2$-Norm** lautet:
$$\|f\|_2 = \sqrt{\int_\Omega |f(x)|^2 \, dx}$$""",
            hint=r"Menge aller Funktionen mit endlichem Integral über das Betragsquadrat.",
            formula_breakdown=r"""- $L^2(\Omega)$: Lebesgue-Raum der Ordnung $p=2$ über dem Gebiet $\Omega \subseteq \mathbb{R}^n$
- $\|f\|_2$: $L^2$-Norm (euklidische Norm für Funktionen)
- Streng mathematisch besteht $L^2$ aus Äquivalenzklassen von Funktionen, die sich nur auf Lebesgue-Nullmengen unterscheiden ($f \sim g \iff f = g \text{ f.ü.}$)""",
            physical_meaning=r"**Physikalische & Mathematische Bedeutung:** Der $L^2(\mathbb{R}^3)$ ist der fundamentale Zustandsraum der Quantenmechanik. Wellenfunktionen $\psi \in L^2$ repräsentieren physikalische Zustände mit Gesamt-Aufenthaltswahrscheinlichkeit $\int |\psi(x)|^2 \, dx = 1$ (Bornsche Interpretation).",
            validity_domain=r"Lebesgue-messbare Funktionen auf $\Omega \subseteq \mathbb{R}^n$. Funktionen mit gleicher Wirkung unter dem Integral gelten als identisch.",
            tags=[
                "L2-Raum",
                "Funktionalanalysis",
                "Norm",
                "Hilbertraum",
                "Quantenmechanik",
            ],
            difficulty=3,
        ),
        Card(
            id="math_l2_inner_product",
            deck_id="reine_mathematik",
            title=r"Skalarprodukt im $L^2$-Raum",
            front=r"Wie ist das kanonische **Skalarprodukt** zweier komplexwertiger Funktionen $f, g \in L^2(\Omega)$ definiert und wie induziert es die $L^2$-Norm?",
            back=r"""$$\langle f, g \rangle_{L^2} = \int_\Omega f^*(x) \, g(x) \, dx$$

Das Skalarprodukt induziert die $L^2$-Norm über:
$$\|f\|_2 = \sqrt{\langle f, f \rangle_{L^2}} = \sqrt{\int_\Omega |f(x)|^2 \, dx}$$""",
            hint=r"Integral über das Produkt von $f^*$ (komplex konjugiert) und $g$.",
            formula_breakdown=r"""- $\langle \cdot, \cdot \rangle$: Sesquilinearform (antilinear im 1. Argument, linear im 2. Argument nach Physik-Konvention)
- $f^*(x) = \overline{f(x)}$: Komplex konjugierte Funktion
- Hermitesche Symmetrie: $\langle g, f \rangle = \langle f, g \rangle^*$
- Positiv definit: $\langle f, f \rangle \ge 0$, mit $\langle f, f \rangle = 0 \iff f = 0 \text{ f.ü.}$""",
            physical_meaning=r"**Physikalische Bedeutung:** In der Quantenmechanik entspricht $\langle \phi | \psi \rangle = \int \phi^*(x) \psi(x) \, dx$ der quantenmechanischen Übergangsamplitude. Orthogonalität $\langle \phi, \psi \rangle = 0$ bedeutet, dass sich zwei Zustände gegenseitig ausschließen.",
            validity_domain=r"Definiert für alle $f, g \in L^2(\Omega)$.",
            tags=["Skalarprodukt", "L2-Raum", "Hilbertraum", "Bra-Ket", "Analysis"],
            difficulty=2,
        ),
        Card(
            id="math_hilbert_space_riesz_fischer",
            deck_id="reine_mathematik",
            title=r"Hilbertraum-Eigenschaft & Satz von Riesz-Fischer",
            front=r"Warum ist der $L^2(\Omega)$ ein **Hilbertraum** und welche Eigenschaft unterscheidet ihn von einem unvollständigen Prä-Hilbertraum (z.B. $C^0$)?",
            back=r"""Der $L^2(\Omega)$ ist **vollständig** bezüglich der induzierten $L^2$-Norm.

Jede Cauchy-Folge $(f_n)_{n \in \mathbb{N}}$ in $L^2$ konvergiert gegen eine Grenzfunktion $f \in L^2$:
$$\lim_{n,m \to \infty} \|f_n - f_m\|_2 = 0 \implies \exists f \in L^2: \lim_{n \to \infty} \|f_n - f\|_2 = 0$$

Dies ist die fundamentale Aussage des **Satzes von Riesz-Fischer**.""",
            hint=r"Vollständigkeit: Jede Cauchy-Folge besitzt einen Grenzwert innerhalb des Raumes.",
            formula_breakdown=r"""- Hilbertraum: Vollständiger Skalarproduktraum
- Der Raum stetiger Funktionen $C^0([a, b])$ mit $\langle f, g \rangle = \int f g \, dx$ ist nicht vollständig, da Grenzwerte stetiger Funktionen Sprünge haben können (z.B. Fourier-Reihe einer Rechteckwelle)
- $L^2$ ist die vollständige Hülle (Vervollständigung) von $C^0$ bzgl. der $L^2$-Metrik""",
            physical_meaning=r"**Bedeutung:** Ohne Vollständigkeit könnten unendliche Reihen von Basiszuständen (z.B. $\sum c_n |n\rangle$) aus dem Raum „herausfallen“. Die Vollständigkeit garantiert, dass jede physikalisch konsistente Linearkombination wieder einen wohldefinierten Quantenzustand darstellt.",
            validity_domain=r"Lebesgue-Räume $L^p$ sind für alle $1 \le p \le \infty$ Banachräume, und speziell $L^2$ ist ein Hilbertraum.",
            tags=[
                "Hilbertraum",
                "Vollständigkeit",
                "Riesz-Fischer",
                "Funktionalanalysis",
            ],
            difficulty=4,
        ),
        Card(
            id="math_cauchy_schwarz_inequality",
            deck_id="reine_mathematik",
            title=r"Cauchy-Schwarzsche Ungleichung für Integrale",
            front=r"Wie lautet die **Cauchy-Schwarzsche Ungleichung** für zwei Funktionen $f, g \in L^2(\Omega)$ und wann gilt das Gleichheitszeichen?",
            back=r"""$$|\langle f, g \rangle| \le \|f\|_2 \cdot \|g\|_2$$

In Integralschreibweise:
$$\left| \int_\Omega f^*(x) \, g(x) \, dx \right| \le \sqrt{\int_\Omega |f(x)|^2 \, dx} \cdot \sqrt{\int_\Omega |g(x)|^2 \, dx}$$

Gleichheit gilt genau dann, wenn $f$ und $g$ **linear abhängig** sind ($f = \lambda g$ f.ü. für ein $\lambda \in \mathbb{C}$).""",
            hint=r"Betrag des Skalarprodukts ist kleiner oder gleich dem Produkt der Normen.",
            formula_breakdown=r"""- Analog zu $|\vec{a} \cdot \vec{b}| = \|\vec{a}\| \|\vec{b}\| |\cos\theta| \le \|\vec{a}\| \|\vec{b}\|$ in $\mathbb{R}^3$
- Erlaubt die geometrische Definition des Winkels zwischen Funktionen: $\cos\theta = \frac{\operatorname{Re}\langle f, g \rangle}{\|f\|_2 \|g\|_2}$""",
            physical_meaning=r"**Physikalischer Ursprung:** Sie ist der mathematische Kern der Heisenbergschen Unschärferelation: Wendet man Cauchy-Schwarz auf $(\hat{A}-\langle A \rangle)|\psi\rangle$ und $(\hat{B}-\langle B \rangle)|\psi\rangle$ an, folgt unmittelbar $\Delta A \cdot \Delta B \ge \frac{1}{2}|\langle [\hat{A}, \hat{B}] \rangle|$.",
            validity_domain=r"Gültig in jedem Prähilbertraum und Hilbertraum.",
            tags=["Cauchy-Schwarz", "Ungleichung", "L2-Raum", "Unschärfe", "Analysis"],
            difficulty=2,
        ),
        Card(
            id="math_minkowski_inequality",
            deck_id="reine_mathematik",
            title=r"Minkowski-Ungleichung ($L^2$-Dreiecksungleichung)",
            front=r"Wie lautet die **Minkowski-Ungleichung** für Funktionen im $L^2(\Omega)$ und welche fundamentale Eigenschaft sichert sie?",
            back=r"""$$\|f + g\|_2 \le \|f\|_2 + \|g\|_2$$

In Integralform:
$$\sqrt{\int_\Omega |f(x) + g(x)|^2 \, dx} \le \sqrt{\int_\Omega |f(x)|^2 \, dx} + \sqrt{\int_\Omega |g(x)|^2 \, dx}$$

Sie beweist die **Dreiecksungleichung** und sichert, dass $\|\cdot\|_2$ eine mathematisch valide **Norm** ist.""",
            hint=r"Verallgemeinerung der Vektor-Dreiecksungleichung $|\vec{a} + \vec{b}| \le |\vec{a}| + |\vec{b}|$ auf Integrale.",
            formula_breakdown=r"""- Folgt direkt aus der Cauchy-Schwarz-Ungleichung:
  $\|f+g\|^2 = \|f\|^2 + 2\operatorname{Re}\langle f, g \rangle + \|g\|^2 \le \|f\|^2 + 2\|f\|\|g\| + \|g\|^2 = (\|f\| + \|g\|)^2$
- Allgemein für $L^p$-Räume: $\|f + g\|_p \le \|f\|_p + \|g\|_p$ für $1 \le p \le \infty$""",
            physical_meaning=r"**Geometrische Bedeutung:** Garantiert die geometrische Konsistenz des unendlichdimensionalen Funktionenraums: Der direkte Abstand zwischen zwei Zuständen ist niemals größer als die Summe zweier Teilstrecken über einen Zwischenzustand.",
            validity_domain=r"Gültig für alle $f, g \in L^p(\Omega)$ mit $1 \le p \le \infty$.",
            tags=["Minkowski", "Dreiecksungleichung", "Norm", "Funktionalanalysis"],
            difficulty=3,
        ),
        Card(
            id="math_geometric_series",
            deck_id="reine_mathematik",
            title=r"Geometrische Reihe & Konvergenzradius",
            front=r"Wie lautet die Summenformel der **geometrischen Reihe** $\sum_{k=0}^\infty q^k$, wann konvergiert sie und wie lautet die endliche Partialsumme?",
            back=r"""**Unendliche Reihe:**
$$\sum_{k=0}^\infty q^k = \frac{1}{1 - q} \quad \text{für } |q| < 1$$

**Endliche Partialsumme ($q \neq 1$):**
$$s_n = \sum_{k=0}^{n-1} q^k = 1 + q + q^2 + \dots + q^{n-1} = \frac{1 - q^n}{1 - q}$$

Für $|q| \ge 1$ divergiert die unendliche Reihe.""",
            hint=r"Beweis über $s_n - q s_n = 1 - q^n \implies s_n(1-q) = 1 - q^n$.",
            formula_breakdown=r"""- $q \in \mathbb{C}$: Quotient zweier Folgenglieder ($a_{k+1}/a_k = q$)
- Konvergenzgebiet in der komplexen Zahlenebene: Offene Kreisscheibe $\{q \in \mathbb{C} \mid |q| < 1\}$
- Bei $q = 1$: Divergenz ($1 + 1 + 1 + \dots = \infty$)
- Bei $q = -1$: Oszillierende Divergenz (Grandis Reihe: $1 - 1 + 1 - 1 \dots$)""",
            physical_meaning=r"**Physikalische Allgegenwart:** Bildet das Fundament für Mehrfachstreuungen, Resonatoren (Fabry-Pérot-Interferometer), Neumann-Reihen zur Inversion von Operatoren $(1 - \hat{A})^{-1} = \sum \hat{A}^n$ und die Zustandssummen harmonischer Oszillatoren in der statistischen Physik.",
            validity_domain=r"Absolut konvergent für alle $q \in \mathbb{C}$ mit $|q| < 1$.",
            tags=["Reihen", "Geometrische Reihe", "Konvergenz", "Analysis"],
            difficulty=1,
        ),
        Card(
            id="math_harmonic_series_divergence",
            deck_id="reine_mathematik",
            title=r"Harmonische Reihe & Logarithmische Divergenz",
            front=r"Konvergiert die **harmonische Reihe** $\sum_{n=1}^\infty \frac{1}{n}$ und wie wächst ihre $N$-te Partialsumme $H_N$ asymptotisch?",
            back=r"""**Die harmonische Reihe divergiert!**

Obwohl die Summanden eine Nullfolge bilden ($\frac{1}{n} \to 0$), wachsen die Partialsummen $H_N$ logarithmisch:
$$H_N = \sum_{n=1}^N \frac{1}{n} = \ln N + \gamma + \mathcal{O}\left(\frac{1}{N}\right) \xrightarrow{N \to \infty} \infty$$

Hierbei ist $\gamma \approx 0{,}57721566$ die **Euler-Mascheroni-Konstante**.""",
            hint=r"Integralvergleichskriterium: $\int_1^\infty \frac{1}{x} \, dx = [\ln x]_1^\infty = \infty$.",
            formula_breakdown=r"""- Blockbeweis nach Oresme (ca. 1350): $1 + \frac{1}{2} + (\frac{1}{3}+\frac{1}{4}) + (\frac{1}{5}+\dots+\frac{1}{8}) > 1 + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \dots = \infty$
- $\gamma = \lim_{N \to \infty} (H_N - \ln N) \approx 0{,}5772$ (Euler-Mascheroni-Konstante)""",
            physical_meaning=r"**Didaktische & Physikalische Bedeutung:** Wichtigstes Mahnbeispiel: Eine Nullfolge der Summanden ist nur eine *notwendige*, aber *keine hinreichende* Bedingung für Konvergenz! Physikalisch tritt logarithmische Divergenz bei Infrarot-Divergenzen in der Quantenelektrodynamik (Bremsstrahlung) und bei 2D-Diffusionsproblemen auf.",
            validity_domain=r"Allgemein divergiert $\sum 1/n^p$ für alle $p \le 1$ und konvergiert für $p > 1$.",
            tags=[
                "Reihen",
                "Harmonische Reihe",
                "Divergenz",
                "Euler-Mascheroni",
                "Analysis",
            ],
            difficulty=2,
        ),
        Card(
            id="math_basel_problem",
            deck_id="reine_mathematik",
            title=r"Basler Problem ($\sum 1/n^2 = \pi^2/6$)",
            front=r"Welchen exakten Grenzwert hat die Reihe der reziproken Quadratzahlen $\sum_{n=1}^\infty \frac{1}{n^2}$ (**Basler Problem**, $\zeta(2)$) und wer löste es erstmals?",
            back=r"""$$\sum_{n=1}^\infty \frac{1}{n^2} = 1 + \frac{1}{4} + \frac{1}{9} + \frac{1}{16} + \dots = \frac{\pi^2}{6} \approx 1{,}644934$$

Gelöst 1734 von **Leonhard Euler** in Basel.

In der Sprache der analytischen Zahlentheorie entspricht dies dem Wert der **Riemannschen Zeta-Funktion** an der Stelle $s=2$:
$$\zeta(2) = \frac{\pi^2}{6}$$""",
            hint=r"Der Grenzwert ist proportional zu $\pi^2$.",
            formula_breakdown=r"""- Eulers genialer Beweis verglich die Taylor-Reihe des kardinalen Sinus mit seiner Produktdarstellung über die Nullstellen $x = \pm n \pi$:
  $\frac{\sin x}{x} = 1 - \frac{x^2}{6} + \dots = \prod_{n=1}^\infty \left(1 - \frac{x^2}{n^2 \pi^2}\right) = 1 - x^2 \sum_{n=1}^\infty \frac{1}{n^2 \pi^2} + \dots$
  Koeffizientenvergleich bei $x^2$: $\frac{1}{\pi^2} \sum \frac{1}{n^2} = \frac{1}{6} \implies \sum \frac{1}{n^2} = \frac{\pi^2}{6}$""",
            physical_meaning=r"**Physikalische Relevanz:** Taucht u.a. bei der Auswertung thermodynamischer Zustandssummen, der Planckschen Schwarzkörper-Strahlungsformel (Integration über Bose-Einstein-Verteilungen) und bei Vakuum-Fluktuationen auf.",
            validity_domain=r"Allgemein konvergiert die Dirichlet-Reihe $\sum 1/n^s = \zeta(s)$ absolut für $\operatorname{Re}(s) > 1$.",
            tags=["Basler Problem", "Euler", "Zeta-Funktion", "Reihen", "Analysis"],
            difficulty=3,
        ),
        Card(
            id="math_alternating_harmonic_leibniz",
            deck_id="reine_mathematik",
            title=r"Alternierende harmonische Reihe & Leibniz-Kriterium",
            front=r"Welchen Grenzwert hat die **alternierende harmonische Reihe** $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n}$ und welches Kriterium garantiert ihre Konvergenz?",
            back=r"""$$\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n} = 1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \dots = \ln 2 \approx 0{,}693147$$

**Leibniz-Kriterium für alternierende Reihen:**
Eine Reihe $\sum (-1)^n a_n$ konvergiert, wenn die Folge $(a_n)$ eine **monoton fallende Nullfolge** ist:
$$a_{n+1} \le a_n \quad \text{und} \quad \lim_{n \to \infty} a_n = 0$$""",
            hint=r"Folgt aus der Taylor-Reihe von $\ln(1+x)$ bei $x = 1$.",
            formula_breakdown=r"""- $\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \dots$ für $-1 < x \le 1$
- **Bedingte Konvergenz:** Die Reihe konvergiert, aber *nicht absolut* (da $\sum 1/n = \infty$)
- **Riemannscher Umordnungssatz:** Durch geschickte Umordnung der Summanden kann man bei bedingt konvergenten Reihen *jeden beliebigen Grenzwert* oder Divergenz erzwingen!""",
            physical_meaning=r"**Physikalisches Beispiel:** Bei der Madelung-Konstante von Ionenkristallen (z.B. NaCl) treten bedingt konvergente alternierende Coulomb-Summen auf. Nur bei physikalisch neutraler Summationsreihenfolge (Schalenbildung) erhält man das physikalisch richtige Gitterpotential.",
            validity_domain=r"Monotonie ist unverzichtbar: Ohne Monotonie kann $\sum (-1)^n a_n$ trotz $a_n \to 0$ divergieren.",
            tags=[
                "Leibniz-Kriterium",
                "Alternierende Reihe",
                "Bedingte Konvergenz",
                "Riemann-Umordnung",
                "Analysis",
            ],
            difficulty=2,
        ),
        Card(
            id="math_taylor_series_exp_sin_cos",
            deck_id="reine_mathematik",
            title=r"Wichtige Taylor-Reihen ($e^x, \sin x, \cos x$)",
            front=r"Wie lauten die **Taylor-Reihen** um $x_0 = 0$ für die drei Grundfunktionen $e^x$, $\sin x$ und $\cos x$ und wie groß ist ihr Konvergenzradius?",
            back=r"""$$e^x = \sum_{n=0}^\infty \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$$

$$\sin x = \sum_{n=0}^\infty (-1)^n \frac{x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{6} + \frac{x^5}{120} - \dots$$

$$\cos x = \sum_{n=0}^\infty (-1)^n \frac{x^{2n}}{(2n)!} = 1 - \frac{x^2}{2} + \frac{x^4}{24} - \dots$$

Alle drei Reihen besitzen den Konvergenzradius **$R = \infty$** (konvergieren für alle $x \in \mathbb{C}$ absolut).""",
            hint=r"Setzt man $ix$ in die Exponentialreihe ein, erhält man die Eulersche Formel $e^{ix} = \cos x + i\sin x$.",
            formula_breakdown=r"""- Allgemeine Taylor-Formel: $f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n$
- Sinus enthält nur ungerade Potenzen, Kosinus nur gerade Potenzen
- Fundamentale Kleinwinkelnäherungen: $\sin x \approx x$, $\cos x \approx 1 - \frac{x^2}{2}$""",
            physical_meaning=r"**Physikalische Anwendung:** Grundlage aller linearen Näherungen und Störungsrechnungen (z.B. Schwingungen im Minimum eines Potentials $V(x) \approx V(x_0) + \frac{1}{2}V''(x_0)(x-x_0)^2$).",
            validity_domain=r"Ganze analytische Funktionen, absolut konvergent auf ganz $\mathbb{C}$.",
            tags=[
                "Taylor-Reihe",
                "Exponentialfunktion",
                "Trigonometrie",
                "Euler",
                "Analysis",
            ],
            difficulty=1,
        ),
        Card(
            id="math_convergence_radius_hadamard",
            deck_id="reine_mathematik",
            title=r"Konvergenzradius von Potenzreihen",
            front=r"Wie berechnet man den **Konvergenzradius $R$** einer allgemeinen Potenzreihe $\sum_{n=0}^\infty a_n (x - x_0)^n$ mittels Quotienten- und Wurzelkriterium?",
            back=r"""**Quotientenkriterium (falls Grenzwert existiert):**
$$R = \lim_{n \to \infty} \left| \frac{a_n}{a_{n+1}} \right|$$

**Formel von Cauchy-Hadamard (gilt stets):**
$$\frac{1}{R} = \limsup_{n \to \infty} \sqrt[n]{|a_n|}$$

- Für $|x - x_0| < R$: Reihe konvergiert **absolut**
- Für $|x - x_0| > R$: Reihe **divergiert**
- Auf dem Rand $|x - x_0| = R$: Gesonderte Randuntersuchung erforderlich""",
            hint=r"Beachte: Bei Hadamard steht der Kehrwert $1/R = \limsup \sqrt[n]{|a_n|}$.",
            formula_breakdown=r"""- $\limsup = 0 \implies R = \infty$ (konvergiert überall)
- $\limsup = \infty \implies R = 0$ (konvergiert nur im Zentrum $x_0$)
- In der komplexen Ebene ist der Konvergenzbereich eine offene Kreisscheibe um $x_0$ mit Radius $R$""",
            physical_meaning=r"**Geometrische & Analytische Intuition:** In der Funktionentheorie wird der Konvergenzradius durch den Abstand zur *nächstgelegenen Singularität* in $\mathbb{C}$ vorgegeben. Beispiel: $\frac{1}{1+x^2} = \sum (-1)^n x^{2n}$ hat auf der reellen Achse keine Polstelle, aber in $\mathbb{C}$ bei $x = \pm i$, weshalb $R = 1$ ist.",
            validity_domain=r"Gültig für beliebige formale Potenzreihen in $\mathbb{R}$ und $\mathbb{C}$.",
            tags=["Konvergenzradius", "Cauchy-Hadamard", "Potenzreihe", "Analysis"],
            difficulty=3,
        ),
        Card(
            id="math_fourier_parseval",
            deck_id="reine_mathematik",
            title=r"Fourier-Reihen & Parsevalsche Identität in $L^2$",
            front=r"Wie lautet die **Parsevalsche Gleichung** für Fourier-Reihen in $L^2([-\pi, \pi])$ und was bedeutet sie als Verallgemeinerung des Satzes von Pythagoras?",
            back=r"""Für eine Funktion $f \in L^2([-\pi, \pi])$ mit Fourier-Koeffizienten $c_n = \frac{1}{2\pi}\int_{-\pi}^\pi f(x) e^{-inx} \, dx$ gilt:
$$\frac{1}{2\pi} \int_{-\pi}^\pi |f(x)|^2 \, dx = \sum_{n=-\infty}^\infty |c_n|^2$$

Dies ist der **Satz des Pythagoras im Hilbertraum**: Die Gesamtnorm $\|f\|_2^2$ entspricht der Summe der Betragsquadrate der Koeffizienten bezüglich der Orthonormalbasis $\{\frac{1}{\sqrt{2\pi}} e^{inx}\}$. Und die Fourier-Transformation ist eine **Isometrie**.""",
            hint=r"Energie im Ortsraum = Summe der Energien aller Frequenzmoden.",
            formula_breakdown=r"""- Orthonormalsystem: $\langle e^{inx}, e^{imx} \rangle = 2\pi \delta_{nm}$
- Besselsche Ungleichung: $\sum |c_n|^2 \le \|f\|^2$; Gleichheit gilt genau dann, wenn das Orthonormalsystem vollständig ist
- Plancherel-Theorem für Fourier-Transformation auf $L^2(\mathbb{R})$""",
            physical_meaning=r"**Physikalische Bedeutung (Energieerhaltung):** In Elektrodynamik, Signaltheorie und Akustik bedeutet dies, dass die Gesamtenergie bzw. Leistung eines Signals im Zeitbereich exakt der Summe der spektralen Leistungsdichten aller Frequenzkomponenten entspricht.",
            validity_domain=r"Gilt für alle $2\pi$-periodischen Funktionen in $L^2([-\pi, \pi])$.",
            tags=["Fourier", "Parseval", "Hilbertraum", "Isometrie", "Analysis"],
            difficulty=3,
        ),
        Card(
            id="math_spectral_theorem",
            deck_id="reine_mathematik",
            title=r"Spektralsatz für selbstadjungierte Operatoren",
            front=r"Welche fundamentalen Aussagen macht der **Spektralsatz** für selbstadjungierte (hermitesche) Operatoren $\hat{A} = \hat{A}^\dagger$ auf einem Hilbertraum?",
            back=r"""1. **Reelle Eigenwerte:** Alle Eigenwerte $\lambda_n \in \mathbb{R}$ sind rein reell ($\hat{A}|n\rangle = \lambda_n |n\rangle$).

2. **Orthogonale Eigenräume:** Eigenvektoren zu verschiedenen Eigenwerten stehen orthogonal aufeinander:
$$\lambda_i \neq \lambda_j \implies \langle v_i, v_j \rangle = 0$$

3. **Vollständige Orthonormalbasis (Spektraldarstellung):**
$$\hat{A} = \sum_{n} \lambda_n |n\rangle \langle n| \quad \text{bzw.} \quad \hat{A} = \int_{\sigma(\hat{A})} \lambda \, dP(\lambda)$$""",
            hint=r"Mathematische Rechtfertigung dafür, warum quantenmechanische Observablen durch hermitesche Operatoren beschrieben werden.",
            formula_breakdown=r"""- Selbstadjungiert: $\langle \phi, \hat{A} \psi \rangle = \langle \hat{A} \phi, \psi \rangle$
- $P(\lambda)$: Spektralmaß / Projektionsoperatoren für kontinuierliche Spektren (z.B. Ort- und Impulsoperator)
- Funktionalrechnung: Erlaubt $f(\hat{A}) = \sum f(\lambda_n) |n\rangle\langle n|$ (z.B. Zeitentwicklungsoperator $e^{-i\hat{H}t/\hbar}$)""",
            physical_meaning=r"**Physikalisches Fundament:** Messbare physikalische Größen (Observablen) müssen stets reelle Messwerte liefern, weshalb sie durch selbstadjungierte Operatoren dargestellt werden. Der Spektralsatz sichert, dass jeder Quantenzustand nach Eigenzuständen der Messgröße entwickelt werden kann.",
            validity_domain=r"Selbstadjungierte Operatoren auf separablen Hilberträumen.",
            tags=[
                "Spektralsatz",
                "Selbstadjungiert",
                "Hermitesch",
                "Eigenwerte",
                "Quantenmechanik",
                "Funktionalanalysis",
            ],
            difficulty=4,
        ),
    ]
    return cards
