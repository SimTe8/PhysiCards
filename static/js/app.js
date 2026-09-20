/**
 * PhysiCards - Main Frontend Application Logic
 * Manages views, deck/card CRUD, SM-2 study session loop,
 * KaTeX formula rendering, live split editor, and keyboard shortcuts.
 */

class PhysiCardsApp {
    constructor() {
        this.currentView = "dashboard";
        this.decks = [];
        this.cards = [];
        this.stats = null;
        
        // Study session state
        this.currentDeckId = null;
        this.currentStudyMode = "due";
        this.studyQueue = [];
        this.currentCardIndex = 0;
        this.isCardFlipped = false;
        this.studyStartTime = 0;
        this.editingCardId = null;

        this.scratchpad = null;

        // Gemini AI Tutor state
        this.aiSettings = { has_key: false, masked_key: "", model: "gemini-3.6-flash", style: "socratic" };
        this.aiDrawerOpen = false;
        this.aiChatHistory = [];
        this.isAiGenerating = false;
        this.currentChatCardId = null;
    }

    init() {
        this.initTheme();
        this.initScratchpad();
        this.initKeyShortcuts();
        this.initLiveEditorSync();
        this.initAiDrawerResize();
        this.loadDashboard();
        this.loadAiSettings();
    }

    // ==========================================
    // THEME & SOUND
    // ==========================================
    initTheme() {
        const savedTheme = localStorage.getItem("physicards_theme") || "dark";
        document.documentElement.setAttribute("data-theme", savedTheme);
        this.updateThemeIcon(savedTheme);

        const soundEnabled = window.soundFx.enabled;
        const soundIcon = document.getElementById("soundIcon");
        if (soundIcon) soundIcon.textContent = soundEnabled ? "🔊" : "🔇";
    }

    toggleTheme() {
        const current = document.documentElement.getAttribute("data-theme") || "dark";
        const next = current === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("physicards_theme", next);
        this.updateThemeIcon(next);
        if (window.soundFx) window.soundFx.playClick();
    }

    updateThemeIcon(theme) {
        const icon = document.getElementById("themeIcon");
        if (icon) icon.textContent = theme === "dark" ? "🌙" : "☀️";
    }

    toggleSound() {
        const enabled = window.soundFx.toggle();
        const icon = document.getElementById("soundIcon");
        if (icon) icon.textContent = enabled ? "🔊" : "🔇";
        if (enabled) window.soundFx.playClick();
    }

    // ==========================================
    // SCRATCHPAD INITIALIZATION
    // ==========================================
    initScratchpad() {
        if (window.Scratchpad) {
            this.scratchpad = new window.Scratchpad("scratchCanvas", "scratchpadContainer");
        }
    }

    toggleScratchpad() {
        if (this.scratchpad) {
            const active = this.scratchpad.toggle();
            const btn = document.getElementById("btnToggleScratchpad");
            if (btn) btn.classList.toggle("active", active);
            if (window.soundFx) window.soundFx.playClick();
        }
    }

    // ==========================================
    // VIEW NAVIGATION
    // ==========================================
    switchView(viewName) {
        this.currentView = viewName;

        document.querySelectorAll(".nav-btn").forEach(btn => {
            btn.classList.toggle("active", btn.getAttribute("data-view") === viewName);
        });

        document.querySelectorAll(".view-section").forEach(sec => {
            sec.classList.remove("active");
        });

        const target = document.getElementById(`view-${viewName}`);
        if (target) target.classList.add("active");

        if (viewName === "dashboard") {
            this.loadDashboard();
        } else if (viewName === "cards") {
            this.loadCardsManager();
        } else if (viewName === "stats") {
            this.loadStatsView();
        }
    }

    // ==========================================
    // DASHBOARD & DECKS
    // ==========================================
    async loadDashboard() {
        try {
            const [decksRes, statsRes] = await Promise.all([
                fetch("/api/decks").then(r => r.json()),
                fetch("/api/stats").then(r => r.json())
            ]);

            if (decksRes.success) {
                this.decks = decksRes.decks;
                this.renderDecksGrid();
            }

            if (statsRes.success) {
                this.stats = statsRes.stats;
                this.renderDashboardStats();
            }
        } catch (e) {
            console.error("Fehler beim Laden des Dashboards:", e);
        }
    }

    renderDashboardStats() {
        if (!this.stats) return;
        document.getElementById("dashDueCount").textContent = this.stats.due_cards || 0;
        document.getElementById("dashStreak").textContent = `${this.stats.study_streak || 0} Tage`;
        document.getElementById("dashMasteredCount").textContent = this.stats.mastered_cards || 0;
        document.getElementById("dashReviewsToday").textContent = this.stats.reviews_today || 0;
    }

    renderDecksGrid() {
        const grid = document.getElementById("deckGrid");
        if (!grid) return;
        grid.innerHTML = "";

        const iconMap = {
            "atom": "⚛", "zap": "⚡", "flame": "🔥", "orbit": "🪐",
            "compass": "🧭", "calculator": "📐", "microscope": "🔬",
            "sigma": "∑", "function": "ƒ(x)", "infinity": "♾️", "book": "📖"
        };

        this.decks.forEach(d => {
            const total = d.total_cards || 0;
            const mastered = d.mastered_cards || 0;
            const learning = total - mastered - (d.new_cards || 0);
            const newCards = d.new_cards || 0;
            const due = d.due_cards || 0;

            const masteredPct = total > 0 ? (mastered / total) * 100 : 0;
            const learningPct = total > 0 ? (learning / total) * 100 : 0;
            const newPct = total > 0 ? (newCards / total) * 100 : 0;

            const icon = iconMap[d.icon] || "⚛";

            const cardEl = document.createElement("div");
            cardEl.className = "deck-card";
            cardEl.style.setProperty("--deck-color", d.color || "#3b82f6");
            cardEl.innerHTML = `
                <div>
                    <div class="deck-top">
                        <div class="deck-title-area">
                            <div class="deck-icon-badge">${icon}</div>
                            <div>
                                <div class="deck-name">${this.escapeHtml(d.name)}</div>
                                <span style="font-size: 0.78rem; color: var(--text-muted);">${total} Karteikarten</span>
                            </div>
                        </div>
                        <div class="deck-due-badge ${due === 0 ? 'zero' : ''}">
                            ${due} fällig
                        </div>
                    </div>
                    <div class="deck-desc">${this.escapeHtml(d.description || '')}</div>
                </div>

                <div>
                    <div class="deck-progress-container">
                        <div class="deck-progress-labels">
                            <span>Fortschritt: ${Math.round(masteredPct)}%</span>
                            <span>${mastered} gemeistert / ${newCards} neu</span>
                        </div>
                        <div class="progress-bar-stack">
                            <div class="bar-mastered" style="width: ${masteredPct}%;"></div>
                            <div class="bar-learning" style="width: ${learningPct}%;"></div>
                            <div class="bar-new" style="width: ${newPct}%;"></div>
                        </div>
                    </div>

                    <div class="deck-actions">
                        <button class="btn-learn" onclick="app.startStudySession('${d.id}', 'due')">
                            <span>🧠</span> Jetzt Lernen
                        </button>
                        <button class="btn-manage" onclick="app.viewDeckCards('${d.id}')" title="Karten anzeigen">
                            <span>🗂️</span> Karten
                        </button>
                        <button class="icon-btn" onclick="app.openEditDeckModal('${d.id}')" title="Themengebiet bearbeiten (Name, Farbe, Symbol)" style="border-radius: var(--radius-md); width: 36px; height: 36px; font-size: 0.9rem;">
                            <span>✏️</span>
                        </button>
                        <button class="icon-btn" onclick="app.confirmResetDeck('${d.id}', '${this.escapeHtml(d.name)}')" title="Fortschritt zurücksetzen" style="border-radius: var(--radius-md); width: 36px; height: 36px; font-size: 0.9rem;">
                            <span>🔄</span>
                        </button>
                    </div>
                </div>
            `;
            grid.appendChild(cardEl);
        });
    }

    viewDeckCards(deckId) {
        this.switchView("cards");
        const select = document.getElementById("cardDeckFilter");
        if (select) {
            select.value = deckId;
            this.filterCards();
        }
    }

    async confirmResetDeck(deckId, deckName) {
        if (confirm(`Möchtest du den gesamten Lernfortschritt für '${deckName}' zurücksetzen? Alle Karten werden wieder als neu markiert.`)) {
            try {
                await fetch(`/api/decks/${deckId}/reset`, { method: "POST" });
                this.showToast(`Lernfortschritt für '${deckName}' zurückgesetzt.`);
                this.loadDashboard();
            } catch (e) {
                console.error(e);
            }
        }
    }

    // ==========================================
    // STUDY SESSION & SM-2 ACTIVE RECALL
    // ==========================================
    async startStudySession(deckId = null, mode = "due") {
        this.currentDeckId = deckId;
        this.currentStudyMode = mode;
        this.currentCardIndex = 0;
        this.isCardFlipped = false;

        const modeSelect = document.getElementById("studyModeSelect");
        if (modeSelect) modeSelect.value = mode;

        try {
            let url = `/api/study/queue?mode=${mode}`;
            if (deckId) url += `&deck_id=${deckId}`;
            const res = await fetch(url).then(r => r.json());

            if (res.success) {
                this.studyQueue = res.queue || [];
                this.switchView("study");
                this.updateStudyHeader();
                this.renderCurrentStudyCard();
            }
        } catch (e) {
            console.error("Fehler beim Starten der Lerneinheit:", e);
        }
    }

    changeStudyMode(mode) {
        this.startStudySession(this.currentDeckId, mode);
    }

    updateStudyHeader() {
        const titleEl = document.getElementById("studyDeckName");
        const iconEl = document.getElementById("studyDeckIcon");
        const counterEl = document.getElementById("studyCardCounter");

        if (this.currentDeckId) {
            const deck = this.decks.find(d => d.id === this.currentDeckId);
            if (deck) {
                titleEl.textContent = deck.name;
                const iconMap = { "atom": "⚛", "zap": "⚡", "flame": "🔥", "orbit": "🪐", "compass": "🧭", "calculator": "📐", "microscope": "🔬" };
                iconEl.textContent = iconMap[deck.icon] || "⚛";
            }
        } else {
            titleEl.textContent = "Alle Fachgebiete";
            iconEl.textContent = "🌐";
        }

        const total = this.studyQueue.length;
        const current = total > 0 ? this.currentCardIndex + 1 : 0;
        counterEl.textContent = `Karte ${current} von ${total}`;
    }

    renderCurrentStudyCard(keepFlipped = false) {
        const scene = document.getElementById("cardScene");
        const finishedBox = document.getElementById("studyFinishedBox");
        const flipper = document.getElementById("cardFlipper");

        // Reset flip state unless keepFlipped is true
        if (!keepFlipped) {
            this.isCardFlipped = false;
            if (flipper) flipper.classList.remove("is-flipped");
            if (this.scratchpad) this.scratchpad.clear();
        } else {
            this.isCardFlipped = true;
            if (flipper) flipper.classList.add("is-flipped");
        }

        if (this.currentCardIndex >= this.studyQueue.length) {
            // Queue finished!
            if (scene) scene.style.display = "none";
            if (finishedBox) finishedBox.style.display = "block";
            if (window.soundFx) window.soundFx.playSuccess(4);
            return;
        }

        if (scene) scene.style.display = "block";
        if (finishedBox) finishedBox.style.display = "none";

        const card = this.studyQueue[this.currentCardIndex];
        this.studyStartTime = Date.now();

        // FRONT
        document.getElementById("frontCategoryTag").textContent = card.deck_name || "Physik";
        document.getElementById("frontCardTitle").textContent = card.title || "";
        document.getElementById("frontCardBody").innerHTML = this.formatMarkdownText(card.front);

        // Difficulty dots
        const dots = document.getElementById("frontDifficultyDots");
        dots.innerHTML = "";
        for (let i = 1; i <= 5; i++) {
            const span = document.createElement("span");
            span.className = `diff-dot ${i <= (card.difficulty || 3) ? 'active' : ''}`;
            dots.appendChild(span);
        }

        // Hint
        const hintBox = document.getElementById("frontHintContainer");
        const hintText = document.getElementById("frontHintText");
        if (card.hint) {
            hintBox.style.display = "block";
            hintText.innerHTML = this.formatMarkdownText(card.hint);
        } else {
            hintBox.style.display = "none";
        }

        // BACK
        document.getElementById("backCardTitle").textContent = card.title || "";
        document.getElementById("backCardBody").innerHTML = this.formatMarkdownText(card.back);
        document.getElementById("backRepInfo").textContent = `Wiederholungen: ${card.repetitions || 0} (EF: ${card.ease_factor || 2.5})`;

        // Breakdown
        const bdBox = document.getElementById("backBreakdownContainer");
        const bdText = document.getElementById("backBreakdownText");
        if (card.formula_breakdown) {
            bdBox.style.display = "block";
            bdText.innerHTML = this.formatMarkdownText(card.formula_breakdown);
        } else {
            bdBox.style.display = "none";
        }

        // Physical Meaning
        const meanBox = document.getElementById("backMeaningContainer");
        const meanText = document.getElementById("backMeaningText");
        if (card.physical_meaning) {
            meanBox.style.display = "block";
            meanText.innerHTML = this.formatMarkdownText(card.physical_meaning);
        } else {
            meanBox.style.display = "none";
        }

        // Validity Domain
        const valBox = document.getElementById("backValidityContainer");
        const valText = document.getElementById("backValidityText");
        if (card.validity_domain) {
            valBox.style.display = "block";
            valText.innerHTML = this.formatMarkdownText(card.validity_domain);
        } else {
            valBox.style.display = "none";
        }

        // Update interval previews on rating buttons
        if (card.interval_previews) {
            document.getElementById("rateInterval1").textContent = card.interval_previews[1] || "< 10m";
            document.getElementById("rateInterval2").textContent = card.interval_previews[2] || "1 Tag";
            document.getElementById("rateInterval3").textContent = card.interval_previews[3] || "4 Tage";
            document.getElementById("rateInterval4").textContent = card.interval_previews[4] || "9 Tage";
        }

        this.updateStudyHeader();
        this.renderMathFormulas();
        this.updateTutorCardContext();
    }

    flipCard() {
        if (this.isCardFlipped) return;
        this.isCardFlipped = true;
        const flipper = document.getElementById("cardFlipper");
        if (flipper) flipper.classList.add("is-flipped");
        if (window.soundFx) window.soundFx.playFlip();
    }

    async submitReview(rating) {
        if (!this.isCardFlipped) {
            this.flipCard();
            return;
        }

        const card = this.studyQueue[this.currentCardIndex];
        if (!card) return;

        const responseTime = Date.now() - this.studyStartTime;

        // Acoustic feedback
        if (window.soundFx) {
            if (rating === 1) window.soundFx.playLapse();
            else window.soundFx.playSuccess(rating);
        }

        try {
            await fetch("/api/study/review", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    card_id: card.id,
                    rating: rating,
                    response_time_ms: responseTime
                })
            });

            // If rating == 1 (Failed/Nochmal), re-append card to end of current session queue!
            if (rating === 1) {
                this.studyQueue.push(card);
            }

            this.currentCardIndex++;
            this.renderCurrentStudyCard();
        } catch (e) {
            console.error("Fehler beim Absenden des Reviews:", e);
        }
    }

    editCurrentStudyCard() {
        const card = this.studyQueue[this.currentCardIndex];
        if (card) {
            this.openCardEditor(card.id);
        }
    }

    // ==========================================
    // CARD MANAGER & LIVE EDITOR
    // ==========================================
    async loadCards() {
        return this.loadCardsManager();
    }

    async loadCardsManager() {
        try {
            const [decksRes, cardsRes] = await Promise.all([
                fetch("/api/decks").then(r => r.json()),
                fetch("/api/cards").then(r => r.json())
            ]);

            if (decksRes.success) {
                this.decks = decksRes.decks;
                this.populateDeckSelects();
            }

            if (cardsRes.success) {
                this.cards = cardsRes.cards;
                this.renderCardsTable(this.cards);
            }
        } catch (e) {
            console.error(e);
        }
    }

    populateDeckSelects() {
        const filterSelect = document.getElementById("cardDeckFilter");
        const editSelect = document.getElementById("editCardDeck");

        if (filterSelect) {
            filterSelect.innerHTML = `<option value="">Alle Decks</option>`;
            this.decks.forEach(d => {
                filterSelect.innerHTML += `<option value="${d.id}">${this.escapeHtml(d.name)}</option>`;
            });
        }

        if (editSelect) {
            editSelect.innerHTML = "";
            this.decks.forEach(d => {
                editSelect.innerHTML += `<option value="${d.id}">${this.escapeHtml(d.name)}</option>`;
            });
        }
    }

    renderCardsTable(cardsList) {
        const tbody = document.getElementById("cardsTableBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (cardsList.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 30px;">Keine Karten gefunden.</td></tr>`;
            return;
        }

        cardsList.forEach(c => {
            const tr = document.createElement("tr");
            const tagsHtml = (c.tags || []).map(t => `<span class="tag-pill">${this.escapeHtml(t)}</span>`).join("");
            
            // Format next due
            let dueText = "Neu";
            if (c.repetitions > 0 && c.next_due) {
                const dueDt = new Date(c.next_due);
                dueText = dueDt.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
            }

            tr.innerHTML = `
                <td>
                    <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">
                        ${this.escapeHtml(c.title)}
                    </div>
                    <div style="font-size: 0.8rem; color: var(--text-muted); max-height: 2.8em; overflow: hidden;">
                        ${this.escapeHtml(c.front.slice(0, 100))}
                    </div>
                    <div style="margin-top: 6px;">${tagsHtml}</div>
                </td>
                <td>
                    <span style="font-weight: 500; color: var(--accent-cyan); font-size: 0.85rem;">
                        ${this.escapeHtml(c.deck_name || '')}
                    </span>
                </td>
                <td>
                    <div class="card-difficulty-indicator">
                        ${[1, 2, 3, 4, 5].map(i => `<span class="diff-dot ${i <= c.difficulty ? 'active' : ''}"></span>`).join('')}
                    </div>
                </td>
                <td>
                    <span style="font-size: 0.85rem; color: ${c.repetitions >= 3 ? 'var(--accent-emerald)' : 'var(--text-secondary)'};">
                        ${dueText} (Wdh: ${c.repetitions || 0})
                    </span>
                </td>
                <td>
                    <div class="action-btns-cell">
                        <button class="btn-table-action" onclick="app.openCardEditor('${c.id}')">Bearbeiten</button>
                        <button class="btn-table-action delete" onclick="app.deleteCard('${c.id}', '${this.escapeHtml(c.title)}')">Löschen</button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    filterCards() {
        const query = (document.getElementById("cardSearchInput").value || "").toLowerCase();
        const deckId = document.getElementById("cardDeckFilter").value;

        const filtered = this.cards.filter(c => {
            const matchesDeck = !deckId || c.deck_id === deckId;
            const matchesQuery = !query ||
                (c.title && c.title.toLowerCase().includes(query)) ||
                (c.front && c.front.toLowerCase().includes(query)) ||
                (c.back && c.back.toLowerCase().includes(query)) ||
                (c.tags && c.tags.some(t => t.toLowerCase().includes(query)));
            return matchesDeck && matchesQuery;
        });

        this.renderCardsTable(filtered);
    }

    async openCardEditor(cardId = null) {
        this.editingCardId = cardId;
        const modal = document.getElementById("cardEditorModal");
        const titleEl = document.getElementById("editorModalTitle");

        this.populateDeckSelects();

        if (cardId) {
            titleEl.textContent = "Karte bearbeiten";
            // Fast placeholder from in-memory objects
            const localCard = this.cards.find(c => c.id === cardId) || this.studyQueue.find(c => c.id === cardId);
            if (localCard) {
                this.populateEditorFields(localCard);
            }

            // Always fetch authoritative data from server
            try {
                const res = await fetch(`/api/cards/${cardId}`).then(r => r.json());
                if (res.success && res.card) {
                    this.populateEditorFields(res.card);
                }
            } catch (err) {
                console.warn("Konnte Kartendetails nicht vom Server laden, nutze lokalen Cache:", err);
            }
        } else {
            titleEl.textContent = "Neue Karte erstellen";
            document.getElementById("editCardTitle").value = "";
            document.getElementById("editCardFront").value = "";
            document.getElementById("editCardBack").value = "";
            document.getElementById("editCardBreakdown").value = "";
            document.getElementById("editCardMeaning").value = "";
            if (document.getElementById("editCardValidity")) {
                document.getElementById("editCardValidity").value = "";
            }
            document.getElementById("editCardHint").value = "";
            document.getElementById("editCardTags").value = "";
            if (this.currentDeckId) {
                document.getElementById("editCardDeck").value = this.currentDeckId;
            }
        }

        modal.classList.add("active");
        this.updateLiveEditorPreview();
    }

    populateEditorFields(card) {
        if (!card) return;
        if (document.getElementById("editCardDeck")) document.getElementById("editCardDeck").value = card.deck_id;
        if (document.getElementById("editCardDifficulty")) document.getElementById("editCardDifficulty").value = card.difficulty || 3;
        if (document.getElementById("editCardTitle")) document.getElementById("editCardTitle").value = card.title || "";
        if (document.getElementById("editCardFront")) document.getElementById("editCardFront").value = card.front || "";
        if (document.getElementById("editCardBack")) document.getElementById("editCardBack").value = card.back || "";
        if (document.getElementById("editCardBreakdown")) document.getElementById("editCardBreakdown").value = card.formula_breakdown || "";
        if (document.getElementById("editCardMeaning")) document.getElementById("editCardMeaning").value = card.physical_meaning || "";
        if (document.getElementById("editCardValidity")) document.getElementById("editCardValidity").value = card.validity_domain || "";
        if (document.getElementById("editCardHint")) document.getElementById("editCardHint").value = card.hint || "";
        if (document.getElementById("editCardTags")) document.getElementById("editCardTags").value = (card.tags || []).join(", ");
        this.updateLiveEditorPreview();
    }

    closeCardEditor() {
        document.getElementById("cardEditorModal").classList.remove("active");
    }

    initLiveEditorSync() {
        const inputs = ["editCardFront", "editCardBack", "editCardBreakdown", "editCardMeaning", "editCardValidity", "editCardTitle"];
        inputs.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener("input", () => this.updateLiveEditorPreview());
            }
        });
    }

    insertSymbol(latexSym) {
        const activeEl = document.activeElement;
        const target = (activeEl && (activeEl.id === "editCardFront" || activeEl.id === "editCardBack" || activeEl.id === "editCardBreakdown" || activeEl.id === "editCardMeaning" || activeEl.id === "editCardValidity"))
            ? activeEl
            : document.getElementById("editCardBack");

        if (target) {
            const start = target.selectionStart || 0;
            const end = target.selectionEnd || 0;
            const text = target.value;
            target.value = text.substring(0, start) + latexSym + text.substring(end);
            target.selectionStart = target.selectionEnd = start + latexSym.length;
            target.focus();
            this.updateLiveEditorPreview();
        }
    }

    updateLiveEditorPreview() {
        const frontText = document.getElementById("editCardFront").value || "(Leere Vorderseite)";
        const backText = document.getElementById("editCardBack").value || "(Leere Rückseite)";
        const bdText = document.getElementById("editCardBreakdown").value || "";
        const meanText = document.getElementById("editCardMeaning").value || "";
        const valText = document.getElementById("editCardValidity") ? document.getElementById("editCardValidity").value : "";

        document.getElementById("previewFront").innerHTML = this.formatMarkdownText(frontText);
        document.getElementById("previewBack").innerHTML = this.formatMarkdownText(backText);

        const bdEl = document.getElementById("previewBreakdown");
        if (bdEl) {
            if (bdText.trim()) {
                bdEl.innerHTML = `<div style="font-weight: 600; color: var(--accent-cyan); margin-bottom: 4px;">📐 Variablen & Einheiten:</div>` + this.formatMarkdownText(bdText);
            } else {
                bdEl.innerHTML = "";
            }
        }

        const meanEl = document.getElementById("previewMeaning");
        if (meanEl) {
            if (meanText.trim()) {
                meanEl.innerHTML = `<div style="font-weight: 600; color: var(--accent-emerald); margin-bottom: 4px;">🔭 Physikalische Bedeutung & Intuition:</div>` + this.formatMarkdownText(meanText);
            } else {
                meanEl.innerHTML = "";
            }
        }

        const valEl = document.getElementById("previewValidity");
        if (valEl) {
            if (valText.trim()) {
                valEl.innerHTML = `<div style="font-weight: 600; color: var(--accent-amber); margin-bottom: 4px;">⚠️ Gültigkeitsbereich:</div>` + this.formatMarkdownText(valText);
            } else {
                valEl.innerHTML = "";
            }
        }

        this.renderMathFormulas();
    }

    async saveCardFromEditor() {
        const deck_id = document.getElementById("editCardDeck").value;
        const title = document.getElementById("editCardTitle").value.trim();
        const front = document.getElementById("editCardFront").value.trim();
        const back = document.getElementById("editCardBack").value.trim();
        const formula_breakdown = document.getElementById("editCardBreakdown").value.trim();
        const physical_meaning = document.getElementById("editCardMeaning").value.trim();
        const validity_domain = document.getElementById("editCardValidity") ? document.getElementById("editCardValidity").value.trim() : "";
        const hint = document.getElementById("editCardHint").value.trim();
        const difficulty = parseInt(document.getElementById("editCardDifficulty").value) || 3;
        const tagsRaw = document.getElementById("editCardTags").value;
        const tags = tagsRaw.split(",").map(t => t.trim()).filter(Boolean);

        if (!front || !back) {
            alert("Bitte gib sowohl Vorderseite (Frage) als auch Rückseite (Antwort/Formel) an.");
            return;
        }

        const payload = {
            deck_id, title: title || front.split("\n")[0].slice(0, 40),
            front, back, formula_breakdown, physical_meaning, validity_domain, hint,
            difficulty, tags
        };

        try {
            let res;
            if (this.editingCardId) {
                res = await fetch(`/api/cards/${this.editingCardId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                }).then(r => r.json());
            } else {
                res = await fetch("/api/cards", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                }).then(r => r.json());
            }

            if (res.success && res.card) {
                const updatedCard = res.card;

                // 1. Update in-memory studyQueue
                this.studyQueue = this.studyQueue.map(c => {
                    if (c.id === updatedCard.id) {
                        return {
                            ...c,
                            ...updatedCard,
                            interval_previews: c.interval_previews || updatedCard.interval_previews
                        };
                    }
                    return c;
                });

                // 2. Update in-memory cards array
                const cIdx = this.cards.findIndex(c => c.id === updatedCard.id);
                if (cIdx !== -1) {
                    this.cards[cIdx] = { ...this.cards[cIdx], ...updatedCard };
                } else {
                    this.cards.unshift(updatedCard);
                }

                this.closeCardEditor();
                this.showToast(this.editingCardId ? "Karte erfolgreich aktualisiert!" : "Neue Karte erfolgreich erstellt!");
                if (window.soundFx) window.soundFx.playClick();

                // 3. Update view based on current mode
                if (this.currentView === "cards") {
                    this.renderCardsTable(this.cards);
                } else if (this.currentView === "study") {
                    // Keep card flipped to back so the user immediately sees the updated intuition!
                    this.renderCurrentStudyCard(true);
                    // Ensure the physical meaning accordion is expanded
                    const meaningDetails = document.querySelector("#backMeaningContainer details");
                    if (meaningDetails) meaningDetails.open = true;
                }

                // Update dashboard counts in background
                this.loadDashboard();
            } else {
                alert("Fehler: " + (res.error || "Speichern fehlgeschlagen"));
            }
        } catch (e) {
            console.error(e);
            alert("Netzwerkfehler beim Speichern.");
        }
    }

    async deleteCard(cardId, cardTitle) {
        if (confirm(`Möchtest du die Karte '${cardTitle}' wirklich löschen?`)) {
            try {
                await fetch(`/api/cards/${cardId}`, { method: "DELETE" });
                this.showToast("Karte gelöscht.");
                this.loadCardsManager();
            } catch (e) {
                console.error(e);
            }
        }
    }

    // ==========================================
    // DECK MODAL (CREATE & EDIT)
    // ==========================================
    openNewDeckModal() {
        this.openDeckModal(null);
    }

    openEditDeckModal(deckId) {
        this.openDeckModal(deckId);
    }

    openDeckModal(deckId = null) {
        const modal = document.getElementById("deckModal") || document.getElementById("newDeckModal");
        if (!modal) return;

        const titleEl = document.getElementById("deckModalTitle");
        const idInput = document.getElementById("deckModalId");
        const nameInput = document.getElementById("deckModalName");
        const descInput = document.getElementById("deckModalDesc");
        const iconSelect = document.getElementById("deckModalIcon");
        const colorInput = document.getElementById("deckModalColor");
        const saveIcon = document.getElementById("deckModalSaveIcon");
        const saveText = document.getElementById("deckModalSaveText");
        const deleteBtn = document.getElementById("btnDeleteDeck");

        if (idInput) idInput.value = deckId || "";

        if (deckId) {
            const deck = this.decks.find(d => d.id === deckId);
            if (!deck) return;

            if (titleEl) titleEl.textContent = `Themengebiet bearbeiten: ${deck.name}`;
            if (nameInput) nameInput.value = deck.name || "";
            if (descInput) descInput.value = deck.description || "";
            if (iconSelect) iconSelect.value = deck.icon || "atom";
            if (colorInput) colorInput.value = deck.color || "#06b6d4";
            if (saveIcon) saveIcon.textContent = "💾";
            if (saveText) saveText.textContent = "Änderungen speichern";
            if (deleteBtn) deleteBtn.style.display = "inline-flex";
        } else {
            if (titleEl) titleEl.textContent = "Neues Themengebiet erstellen";
            if (nameInput) nameInput.value = "";
            if (descInput) descInput.value = "";
            if (iconSelect) iconSelect.value = "atom";
            if (colorInput) colorInput.value = "#06b6d4";
            if (saveIcon) saveIcon.textContent = "➕";
            if (saveText) saveText.textContent = "Erstellen";
            if (deleteBtn) deleteBtn.style.display = "none";
        }

        modal.classList.add("active");
        if (nameInput) setTimeout(() => nameInput.focus(), 150);
    }

    closeDeckModal() {
        const modal = document.getElementById("deckModal") || document.getElementById("newDeckModal");
        if (modal) modal.classList.remove("active");
    }

    closeNewDeckModal() {
        this.closeDeckModal();
    }

    async saveDeck() {
        const idInput = document.getElementById("deckModalId");
        const deckId = idInput ? idInput.value.trim() : "";
        const name = (document.getElementById("deckModalName") || document.getElementById("newDeckName")).value.trim();
        const description = (document.getElementById("deckModalDesc") || document.getElementById("newDeckDesc")).value.trim();
        const icon = (document.getElementById("deckModalIcon") || document.getElementById("newDeckIcon")).value;
        const color = (document.getElementById("deckModalColor") || document.getElementById("newDeckColor")).value;

        if (!name) {
            alert("Bitte gib einen Namen für das Themengebiet ein.");
            return;
        }

        try {
            let res;
            if (deckId) {
                res = await fetch(`/api/decks/${deckId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, description, icon, color })
                }).then(r => r.json());
            } else {
                res = await fetch("/api/decks", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, description, icon, color })
                }).then(r => r.json());
            }

            if (res.success) {
                this.closeDeckModal();
                this.showToast(deckId ? `Themengebiet '${name}' erfolgreich aktualisiert!` : `Themengebiet '${name}' erstellt!`);
                if (window.soundFx) window.soundFx.playSuccess(4);
                await this.loadDashboard();
                this.populateDeckSelects();
            } else {
                alert("Fehler: " + (res.error || "Speichern fehlgeschlagen"));
            }
        } catch (e) {
            console.error(e);
            alert("Netzwerkfehler beim Speichern des Decks.");
        }
    }

    saveNewDeck() {
        return this.saveDeck();
    }

    async deleteCurrentDeck() {
        const idInput = document.getElementById("deckModalId");
        const deckId = idInput ? idInput.value.trim() : "";
        if (!deckId) return;

        const deck = this.decks.find(d => d.id === deckId);
        const deckName = deck ? deck.name : deckId;

        if (confirm(`Möchtest du das Themengebiet '${deckName}' und alle darin enthaltenen Karten wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.`)) {
            try {
                const res = await fetch(`/api/decks/${deckId}`, { method: "DELETE" }).then(r => r.json());
                if (res.success) {
                    this.closeDeckModal();
                    this.showToast(`Deck '${deckName}' gelöscht.`);
                    await this.loadDashboard();
                    this.populateDeckSelects();
                } else {
                    alert("Fehler beim Löschen: " + (res.error || "Unbekannter Fehler"));
                }
            } catch (e) {
                console.error(e);
                alert("Netzwerkfehler beim Löschen des Decks.");
            }
        }
    }

    // ==========================================
    // STATS VIEW
    // ==========================================
    async loadStatsView() {
        try {
            const res = await fetch("/api/stats").then(r => r.json());
            if (!res.success) return;
            const stats = res.stats;

            document.getElementById("statsTotalCards").textContent = stats.total_cards || 0;
            document.getElementById("statsRetention").textContent = `${stats.retention_rate || 100}%`;
            document.getElementById("statsStreak").textContent = `${stats.study_streak || 0} Tage`;
            document.getElementById("statsTotalReviews").textContent = stats.total_reviews || 0;

            document.getElementById("statsMasteredCount").textContent = stats.mastered_cards || 0;
            document.getElementById("statsLearningCount").textContent = stats.learning_cards || 0;
            document.getElementById("statsNewCount").textContent = stats.new_cards || 0;

            const total = stats.total_cards || 1;
            document.getElementById("barMasteredProgress").style.width = `${(stats.mastered_cards / total) * 100}%`;
            document.getElementById("barLearningProgress").style.width = `${(stats.learning_cards / total) * 100}%`;
            document.getElementById("barNewProgress").style.width = `${(stats.new_cards / total) * 100}%`;

            // Render 14-day activity chart
            const chartWrapper = document.getElementById("activityChart");
            chartWrapper.innerHTML = "";
            const history = stats.days_history || [];
            const maxVal = Math.max(...history.map(h => h.count), 5);

            history.forEach(item => {
                const col = document.createElement("div");
                col.className = "chart-bar-col";
                const heightPct = Math.round((item.count / maxVal) * 100);

                col.innerHTML = `
                    <div class="chart-bar-val">${item.count > 0 ? item.count : ''}</div>
                    <div class="chart-bar" style="height: ${Math.max(4, heightPct)}%;"></div>
                    <div class="chart-bar-lbl">${item.date}</div>
                `;
                chartWrapper.appendChild(col);
            });
        } catch (e) {
            console.error(e);
        }
    }

    // ==========================================
    // BACKUP & IMPORT
    // ==========================================
    openBackupModal() {
        document.getElementById("backupModal").classList.add("active");
    }

    closeBackupModal() {
        document.getElementById("backupModal").classList.remove("active");
    }

    async importJsonFile(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const data = JSON.parse(e.target.result);
                const res = await fetch("/api/import", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                }).then(r => r.json());

                if (res.success) {
                    alert(res.message);
                    this.closeBackupModal();
                    this.loadDashboard();
                } else {
                    alert("Import fehlgeschlagen: " + res.error);
                }
            } catch (err) {
                alert("Ungültige JSON-Datei.");
            }
        };
        reader.readAsText(file);
    }

    // ==========================================
    // KEYBOARD SHORTCUTS
    // ==========================================
    initKeyShortcuts() {
        window.addEventListener("keydown", (e) => {
            // Ignore if focus is in an input or textarea
            const tag = e.target.tagName.toLowerCase();
            if (tag === "input" || tag === "textarea" || tag === "select") {
                if (e.key === "Escape") {
                    this.closeCardEditor();
                    this.closeNewDeckModal();
                    this.closeBackupModal();
                    this.closeAiSettingsModal();
                    this.closeAiCardGenModal();
                    if (this.aiDrawerOpen) this.toggleAiTutor(false);
                }
                return;
            }

            if (e.key === "Escape") {
                this.closeCardEditor();
                this.closeNewDeckModal();
                this.closeBackupModal();
                this.closeAiSettingsModal();
                this.closeAiCardGenModal();
                if (this.aiDrawerOpen) {
                    this.toggleAiTutor(false);
                    return;
                }
                if (this.currentView === "study") {
                    this.switchView("dashboard");
                }
                return;
            }

            if (this.currentView === "study") {
                if (e.code === "Space") {
                    e.preventDefault();
                    if (!this.isCardFlipped) {
                        this.flipCard();
                    }
                } else if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4") {
                    e.preventDefault();
                    this.submitReview(parseInt(e.key));
                } else if (e.key === "w" || e.key === "W") {
                    e.preventDefault();
                    this.toggleScratchpad();
                } else if (e.key === "e" || e.key === "E") {
                    e.preventDefault();
                    this.editCurrentStudyCard();
                } else if (e.key === "t" || e.key === "T") {
                    e.preventDefault();
                    this.toggleAiTutor();
                }
            }
        });
    }

    // ==========================================
    // KATEX FORMULA RENDERING & MARKDOWN
    // ==========================================
    renderMathFormulas() {
        if (window.renderMathInElement) {
            window.renderMathInElement(document.body, {
                delimiters: [
                    { left: "$$", right: "$$", display: true },
                    { left: "$", right: "$", display: false },
                    { left: "\\[", right: "\\]", display: true },
                    { left: "\\(", right: "\\)", display: false }
                ],
                throwOnError: false
            });
        }
    }

    formatMarkdownText(text) {
        if (!text) return "";
        let html = text
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.*?)\*/g, "<em>$1</em>")
            .replace(/\n\n/g, "<br><br>")
            .replace(/\n/g, "<br>");
        return html;
    }

    escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    showToast(message) {
        const existing = document.querySelector(".toast-msg");
        if (existing) existing.remove();

        const toast = document.createElement("div");
        toast.className = "toast-msg";
        toast.innerHTML = `<span>✨</span> <span>${this.escapeHtml(message)}</span>`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transition = "opacity 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 2800);
    }

    // ==========================================
    // GEMINI AI TUTOR & SETTINGS
    // ==========================================
    async loadAiSettings() {
        try {
            const res = await fetch("/api/ai/settings").then(r => r.json());
            if (res.success) {
                this.aiSettings = res;
                const badge = document.getElementById("drawerModelBadge");
                if (badge) badge.textContent = res.model || "gemini-3.6-flash";

                // If server has no key but localStorage has a saved key, restore it to server!
                if (!res.has_key) {
                    const localKey = localStorage.getItem("physicards_gemini_api_key");
                    if (localKey && localKey.trim()) {
                        await fetch("/api/ai/settings", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ api_key: localKey.trim() })
                        });
                        const refreshed = await fetch("/api/ai/settings").then(r => r.json());
                        if (refreshed.success) {
                            this.aiSettings = refreshed;
                        }
                    }
                } else if (res.api_key) {
                    localStorage.setItem("physicards_gemini_api_key", res.api_key);
                }
            }
        } catch (e) {
            console.warn("Konnte KI-Einstellungen nicht laden (Offline?):", e);
        }
    }

    onAiModelChange() {
        const sel = document.getElementById("aiModelSelect");
        const customInp = document.getElementById("aiCustomModelInput");
        if (!sel || !customInp) return;
        if (sel.value === "custom") {
            customInp.style.display = "block";
            customInp.focus();
        } else {
            customInp.style.display = "none";
        }
    }

    getSelectedAiModel() {
        const sel = document.getElementById("aiModelSelect");
        if (!sel) return "gemini-3.6-flash";
        if (sel.value === "custom") {
            const customInp = document.getElementById("aiCustomModelInput");
            return (customInp && customInp.value.trim()) ? customInp.value.trim() : "gemini-3.6-flash";
        }
        return sel.value;
    }

    openAiSettingsModal() {
        document.getElementById("aiSettingsModal").classList.add("active");
        
        // Pre-fill existing API key from settings or localStorage
        const keyInput = document.getElementById("aiApiKeyInput");
        const eyeIcon = document.getElementById("aiKeyEyeIcon");
        const savedKey = this.aiSettings.api_key || localStorage.getItem("physicards_gemini_api_key") || "";
        if (keyInput) {
            keyInput.value = savedKey;
            keyInput.type = "password";
        }
        if (eyeIcon) eyeIcon.textContent = "👁️";

        const currentModel = this.aiSettings.model || "gemini-3.6-flash";
        const modelSelect = document.getElementById("aiModelSelect");
        const customInput = document.getElementById("aiCustomModelInput");

        const options = Array.from(modelSelect.options).map(o => o.value);
        if (options.includes(currentModel) && currentModel !== "custom") {
            modelSelect.value = currentModel;
            if (customInput) {
                customInput.style.display = "none";
                customInput.value = "";
            }
        } else {
            modelSelect.value = "custom";
            if (customInput) {
                customInput.style.display = "block";
                customInput.value = currentModel;
            }
        }

        document.getElementById("aiStyleSelect").value = this.aiSettings.style || "socratic";
        
        const badge = document.getElementById("aiKeyStatusBadge");
        if (badge) {
            if (this.aiSettings.has_key || savedKey) {
                const mask = this.aiSettings.masked_key || (savedKey.length >= 10 ? `${savedKey.slice(0,6)}...${savedKey.slice(-4)}` : "***");
                badge.innerHTML = `<span style="color: var(--accent-emerald);">● Gespeichert & Aktiv (${mask})</span>`;
            } else {
                badge.innerHTML = `<span style="color: var(--text-muted);">○ Kein Key hinterlegt</span>`;
            }
        }
        const testRes = document.getElementById("aiTestResult");
        if (testRes) testRes.innerHTML = "";
    }

    closeAiSettingsModal() {
        document.getElementById("aiSettingsModal").classList.remove("active");
    }

    toggleAiKeyVisibility() {
        const inp = document.getElementById("aiApiKeyInput");
        const icon = document.getElementById("aiKeyEyeIcon");
        if (!inp) return;
        if (inp.type === "password") {
            inp.type = "text";
            if (icon) icon.textContent = "🙈";
        } else {
            inp.type = "password";
            if (icon) icon.textContent = "👁️";
        }
    }

    async saveAiSettings() {
        const apiKey = document.getElementById("aiApiKeyInput").value.trim();
        const model = this.getSelectedAiModel();
        const style = document.getElementById("aiStyleSelect").value;

        const payload = {
            api_key: apiKey,
            model: model,
            style: style
        };

        try {
            const res = await fetch("/api/ai/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(r => r.json());

            if (res.success) {
                if (apiKey) {
                    localStorage.setItem("physicards_gemini_api_key", apiKey);
                } else {
                    localStorage.removeItem("physicards_gemini_api_key");
                }
                this.showToast("KI-Einstellungen & API-Key erfolgreich gespeichert!");
                await this.loadAiSettings();
                this.closeAiSettingsModal();
            } else {
                alert("Fehler: " + (res.error || "Speichern fehlgeschlagen"));
            }
        } catch (e) {
            alert("Fehler beim Speichern der Einstellungen: " + e.message);
        }
    }

    async testAiConnection() {
        const keyInput = document.getElementById("aiApiKeyInput");
        const apiKey = keyInput ? keyInput.value.trim() : "";
        const model = this.getSelectedAiModel();
        const resultEl = document.getElementById("aiTestResult");
        const btn = document.getElementById("btnTestAiConn");

        if (!apiKey && !this.aiSettings.has_key) {
            if (resultEl) {
                resultEl.innerHTML = '<span style="color: var(--accent-rose);">Bitte gib zuerst deinen Google AI Studio API-Key ein.</span>';
            }
            return;
        }

        if (resultEl) {
            resultEl.innerHTML = '<span style="color: var(--accent-cyan);">⏳ Verbindung wird getestet...</span>';
        }
        if (btn) btn.disabled = true;

        try {
            const res = await fetch("/api/ai/test", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: apiKey, model })
            }).then(r => r.json());

            if (res.success) {
                resultEl.innerHTML = `<span style="color: var(--accent-emerald);">✓ Erfolgreich verbunden (${res.model})</span>`;
                // Auto-save the working API key immediately so user doesn't lose it if they exit modal
                if (apiKey) {
                    await fetch("/api/ai/settings", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            api_key: apiKey,
                            model: model,
                            style: document.getElementById("aiStyleSelect").value
                        })
                    });
                    localStorage.setItem("physicards_gemini_api_key", apiKey);
                    await this.loadAiSettings();
                    const badge = document.getElementById("aiKeyStatusBadge");
                    if (badge && this.aiSettings.has_key) {
                        badge.innerHTML = `<span style="color: var(--accent-emerald);">● Gespeichert & Aktiv (${this.aiSettings.masked_key})</span>`;
                    }
                }
            } else {
                resultEl.innerHTML = `<span style="color: var(--accent-rose); font-size: 0.78rem;">✗ ${this.escapeHtml(res.error || 'Verbindung fehlgeschlagen')}</span>`;
            }
        } catch (e) {
            resultEl.innerHTML = `<span style="color: var(--accent-rose);">✗ Fehler: ${this.escapeHtml(e.message)}</span>`;
        } finally {
            if (btn) btn.disabled = false;
        }
    }

    initAiDrawerResize() {
        const drawer = document.getElementById("aiTutorDrawer");
        const resizer = document.getElementById("aiDrawerResizer");
        if (!drawer || !resizer) return;

        // Restore saved width from localStorage
        const savedWidth = parseInt(localStorage.getItem("physicards_ai_drawer_width"), 10);
        if (savedWidth && savedWidth >= 360 && savedWidth <= window.innerWidth - 30) {
            drawer.style.width = `${savedWidth}px`;
        }

        let isResizing = false;

        const onMouseDown = (e) => {
            e.preventDefault();
            isResizing = true;
            drawer.classList.add("resizing");
            document.body.style.cursor = "ew-resize";
            document.body.style.userSelect = "none";

            const onMouseMove = (moveEvent) => {
                if (!isResizing) return;
                const viewportWidth = window.innerWidth;
                const minWidth = 360;
                const maxWidth = Math.max(minWidth, viewportWidth - 30);
                const rawWidth = viewportWidth - moveEvent.clientX;
                const clampedWidth = Math.max(minWidth, Math.min(maxWidth, rawWidth));
                drawer.style.width = `${clampedWidth}px`;
            };

            const onMouseUp = () => {
                if (!isResizing) return;
                isResizing = false;
                drawer.classList.remove("resizing");
                document.body.style.cursor = "";
                document.body.style.userSelect = "";
                window.removeEventListener("mousemove", onMouseMove);
                window.removeEventListener("mouseup", onMouseUp);

                const finalWidth = parseInt(drawer.style.width, 10);
                if (finalWidth) {
                    localStorage.setItem("physicards_ai_drawer_width", finalWidth);
                }
            };

            window.addEventListener("mousemove", onMouseMove);
            window.addEventListener("mouseup", onMouseUp);
        };

        const onTouchStart = (e) => {
            if (!e.touches || e.touches.length === 0) return;
            isResizing = true;
            drawer.classList.add("resizing");

            const onTouchMove = (moveEvent) => {
                if (!isResizing || !moveEvent.touches || moveEvent.touches.length === 0) return;
                const clientX = moveEvent.touches[0].clientX;
                const viewportWidth = window.innerWidth;
                const minWidth = 360;
                const maxWidth = Math.max(minWidth, viewportWidth - 30);
                const rawWidth = viewportWidth - clientX;
                const clampedWidth = Math.max(minWidth, Math.min(maxWidth, rawWidth));
                drawer.style.width = `${clampedWidth}px`;
            };

            const onTouchEnd = () => {
                if (!isResizing) return;
                isResizing = false;
                drawer.classList.remove("resizing");
                window.removeEventListener("touchmove", onTouchMove);
                window.removeEventListener("touchend", onTouchEnd);

                const finalWidth = parseInt(drawer.style.width, 10);
                if (finalWidth) {
                    localStorage.setItem("physicards_ai_drawer_width", finalWidth);
                }
            };

            window.addEventListener("touchmove", onTouchMove, { passive: true });
            window.addEventListener("touchend", onTouchEnd);
        };

        resizer.addEventListener("mousedown", onMouseDown);
        resizer.addEventListener("touchstart", onTouchStart, { passive: true });
    }

    toggleAiDrawerWidth() {
        const drawer = document.getElementById("aiTutorDrawer");
        if (!drawer) return;

        const currentWidth = drawer.getBoundingClientRect().width;
        const targetWidth = currentWidth < 680 ? Math.min(window.innerWidth - 60, 840) : 480;
        drawer.style.width = `${targetWidth}px`;
        localStorage.setItem("physicards_ai_drawer_width", targetWidth);
        if (window.soundFx) window.soundFx.playClick();
    }

    toggleAiTutor(forceState = null) {
        const drawer = document.getElementById("aiTutorDrawer");
        if (!drawer) return;

        this.aiDrawerOpen = forceState !== null ? forceState : !this.aiDrawerOpen;
        drawer.classList.toggle("open", this.aiDrawerOpen);

        const btn = document.getElementById("btnToggleAiTutor");
        if (btn) btn.classList.toggle("active", this.aiDrawerOpen);

        if (this.aiDrawerOpen) {
            this.updateTutorCardContext(false);
            setTimeout(() => {
                const inp = document.getElementById("aiChatInput");
                if (inp) inp.focus();
            }, 300);
        }
    }

    updateTutorCardContext(forceWelcome = false) {
        const currentCard = this.studyQueue[this.currentCardIndex];
        const msgContainer = document.getElementById("aiChatMessages");
        if (!msgContainer) return;

        if (currentCard && (this.currentChatCardId !== currentCard.id || forceWelcome)) {
            this.currentChatCardId = currentCard.id;
            this.aiChatHistory = [];
            msgContainer.innerHTML = "";

            if (!this.aiSettings.has_key) {
                const offlineHint = document.createElement("div");
                offlineHint.className = "ai-offline-hint";
                offlineHint.innerHTML = `<span>💡</span><div><b>Offline / Kein API-Key hinterlegt</b><br>Trage deinen kostenlosen Google AI Studio Key in den <a href="#" onclick="app.openAiSettingsModal(); return false;" style="color: inherit; text-decoration: underline;">Einstellungen ⚙️</a> ein, um live mit Gemini zu diskutieren.</div>`;
                msgContainer.appendChild(offlineHint);
            }

            const welcomeMsg = document.createElement("div");
            welcomeMsg.className = "ai-msg ai";
            welcomeMsg.innerHTML = `👋 <strong>Hallo!</strong> Ich bin dein Physik-Tutor für diese Karte:<br>
            <div style="font-weight: 600; color: var(--accent-cyan); margin: 6px 0;">${this.escapeHtml(currentCard.title)}</div>
            Frag mich nach einer Alltagsanalogie, Herleitung oder lass dich sokratisch abfragen!`;
            msgContainer.appendChild(welcomeMsg);
            this.renderMathFormulas();
        }
    }

    clearAiChat() {
        this.aiChatHistory = [];
        this.updateTutorCardContext(true);
    }

    handleAiInputKeydown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            this.sendAiMessage();
        }
    }

    sendQuickPrompt(type) {
        if (type === "analogy") {
            this.sendAiMessage("Erkläre mir die physikalische Bedeutung und Intuition dieser Formel anhand eines anschaulichen Alltagsbeispiels oder Gedankenexperiments.");
        } else if (type === "socratic") {
            this.sendAiMessage("Stelle mir eine sokratische Frage zu dieser Karte, um mein physikalisches Verständnis und Grenzfälle zu testen.");
        } else if (type === "derivation") {
            this.sendAiMessage("Zeige mir die mathematische Herleitung dieser Formel Schritt für Schritt mit sauberem LaTeX.");
        } else if (type === "traps") {
            this.sendAiMessage("Welche typischen Denkfehler oder Missverständnisse gibt es bei dieser Formel und wo liegen ihre physikalischen Gültigkeitsgrenzen?");
        } else if (type === "generate_card") {
            this.sendAiMessage("Erstelle mir bitte hieraus eine neue, standardisierte Karteikarte.");
        }
    }

    async sendAiMessage(customText = null) {
        if (this.isAiGenerating) return;

        const inputEl = document.getElementById("aiChatInput");
        const text = customText || (inputEl ? inputEl.value.trim() : "");
        if (!text) return;

        if (inputEl) {
            inputEl.value = "";
            inputEl.style.height = "auto";
        }

        const msgContainer = document.getElementById("aiChatMessages");
        if (!msgContainer) return;

        // User message bubble
        const userBubble = document.createElement("div");
        userBubble.className = "ai-msg user";
        userBubble.textContent = text;
        msgContainer.appendChild(userBubble);
        msgContainer.scrollTop = msgContainer.scrollHeight;

        // AI message container
        const aiBubble = document.createElement("div");
        aiBubble.className = "ai-msg ai";
        aiBubble.innerHTML = '<span style="opacity: 0.6;">Denkt nach... ⚛</span>';
        msgContainer.appendChild(aiBubble);
        msgContainer.scrollTop = msgContainer.scrollHeight;

        this.isAiGenerating = true;
        const sendBtn = document.getElementById("btnSendAiChat");
        if (sendBtn) sendBtn.innerHTML = "⏳";

        const currentCard = this.studyQueue[this.currentCardIndex];
        let accumulatedText = "";

        try {
            const response = await fetch("/api/ai/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    card_id: currentCard ? currentCard.id : null,
                    message: text,
                    history: this.aiChatHistory,
                    style: this.aiSettings.style || "socratic"
                })
            });

            if (!response.ok) {
                const err = await response.text();
                aiBubble.innerHTML = `<span style="color: var(--accent-rose);">Fehler (${response.status}): ${this.escapeHtml(err)}</span>`;
                this.isAiGenerating = false;
                if (sendBtn) sendBtn.innerHTML = "➤";
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split("\n\n");
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const dataStr = line.replace("data: ", "").trim();
                        if (dataStr === "[DONE]") continue;

                        try {
                            const parsed = JSON.parse(dataStr);
                            if (parsed.error) {
                                accumulatedText += `\n\n⚠️ *${parsed.error}*`;
                            } else if (parsed.text) {
                                accumulatedText += parsed.text;
                            }
                            aiBubble.innerHTML = this.formatMarkdownText(accumulatedText);
                            msgContainer.scrollTop = msgContainer.scrollHeight;
                        } catch (e) {
                            // Ignore incomplete JSON chunks
                        }
                    }
                }
            }

            // Stream finished: render formulas
            aiBubble.innerHTML = this.formatMarkdownText(accumulatedText);
            this.renderMathFormulas();

            // Record to conversation history
            this.aiChatHistory.push({ role: "user", content: text });
            this.aiChatHistory.push({ role: "model", content: accumulatedText });

            // Check if Gemini generated a flashcard
            this.parseAndRenderCardPreview(aiBubble, accumulatedText);

        } catch (e) {
            aiBubble.innerHTML = `<span style="color: var(--accent-rose);">Verbindungsfehler (Offline?): ${this.escapeHtml(e.message)}</span>`;
        } finally {
            this.isAiGenerating = false;
            if (sendBtn) sendBtn.innerHTML = "➤";
            msgContainer.scrollTop = msgContainer.scrollHeight;
        }
    }

    sanitizeCardLatex(cardData) {
        if (!cardData || typeof cardData !== "object") return cardData;
        const c = { ...cardData };

        const greekList = [
            "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota",
            "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon",
            "phi", "chi", "psi", "omega", "Delta", "Gamma", "Theta", "Lambda", "Xi", "Pi",
            "Sigma", "Phi", "Psi", "Omega", "hbar"
        ];

        const isMathVariable = (s) => {
            s = s.trim();
            if (!s || s.length > 20) return false;
            const words = s.split(/\s+/);
            if (words.length > 2) return false;
            if (words.some(w => w.length > 8)) return false;
            if (/[äöüÄÖÜß]/.test(s)) return false;
            return true;
        };

        const sanitizeText = (text, isBreakdown = false) => {
            if (!text || typeof text !== "string") return text;
            const lines = text.split("\n");
            const processed = lines.map(line => {
                let l = line.trim();
                if (!l) return line;

                let prefix = "";
                let content = line;
                const bMatch = line.match(/^(\s*[\-\*]\s*)(.*)$/);
                if (bMatch) {
                    prefix = bMatch[1];
                    content = bMatch[2];
                }

                const colonIdx = content.indexOf(":");
                if (isBreakdown && prefix && colonIdx !== -1 && !content.startsWith("http")) {
                    let sym = content.substring(0, colonIdx).trim();
                    let rest = content.substring(colonIdx);

                    if (!sym.includes("$") && isMathVariable(sym)) {
                        for (const g of greekList) {
                            const re = new RegExp(`(?<!\\\\)\\b${g}\\b`, "g");
                            sym = sym.replace(re, `\\${g}`);
                        }
                        sym = `$${sym}$`;
                    }
                    content = sym + rest;
                }

                // Wrap [unit] in $[\mathrm{...}]$ if not inside $
                content = content.replace(/\[([^\]\$]+)\]/g, (m, u) => {
                    const cleanU = u.trim();
                    if (cleanU.includes("$") || !cleanU || /[äöüÄÖÜ]/.test(cleanU)) return m;
                    return `$[\\mathrm{${cleanU}}]$`;
                });

                // Physics relations outside $
                const parts = content.split(/(\$\$[\s\S]*?\$\$|\$[^\$]+?\$)/g);
                for (let i = 0; i < parts.length; i += 2) {
                    let p = parts[i];
                    p = p.replace(/\b([a-zA-Z_0-9]+)\s*<<\s*([a-zA-Z_0-9]+)\b/g, "$$1 \\ll $2$");
                    p = p.replace(/\b([a-zA-Z_0-9]+)\s*>>\s*([a-zA-Z_0-9]+)\b/g, "$$1 \\gg $2$");
                    p = p.replace(/\b([a-zA-Z_0-9]+)\s*<=\s*([a-zA-Z_0-9]+)\b/g, "$$1 \\le $2$");
                    p = p.replace(/\b([a-zA-Z_0-9]+)\s*>=\s*([a-zA-Z_0-9]+)\b/g, "$$1 \\ge $2$");
                    p = p.replace(/\b([a-zA-Z_0-9]+)\s*->\s*0\b/g, "$$1 \\to 0$");
                    parts[i] = p;
                }

                return prefix + parts.join("");
            });
            return processed.join("\n");
        };

        if (c.back && typeof c.back === "string" && !c.back.includes("$")) {
            if (/[\=\\\^\_\+\-\/\*]/.test(c.back)) {
                c.back = `$$${c.back.trim()}$$`;
            }
        }

        if (c.formula_breakdown) c.formula_breakdown = sanitizeText(c.formula_breakdown, true);
        if (c.physical_meaning) c.physical_meaning = sanitizeText(c.physical_meaning, false);
        if (c.validity_domain) c.validity_domain = sanitizeText(c.validity_domain, false);
        if (c.front) c.front = sanitizeText(c.front, false);
        if (c.hint) c.hint = sanitizeText(c.hint, false);

        return c;
    }

    parseAndRenderCardPreview(container, text) {
        const match = text.match(/```json:card([\s\S]*?)```/);
        if (!match) return;

        try {
            const rawCardJson = JSON.parse(match[1].trim());
            const cardJson = this.sanitizeCardLatex(rawCardJson);
            const previewBox = document.createElement("div");
            previewBox.className = "ai-card-preview";

            previewBox.innerHTML = `
                <div class="ai-card-preview-header">
                    <span>✨ VORGESCHLAGENE KARTEIKARTE</span>
                    <span>${this.escapeHtml(cardJson.deck_id || 'Deck')}</span>
                </div>
                <div class="ai-card-preview-title">${this.escapeHtml(cardJson.title || 'Neue Karte')}</div>
                <div class="ai-card-preview-body">
                    <strong>Frage:</strong> ${this.formatMarkdownText(cardJson.front || '')}<br><br>
                    <strong>Antwort:</strong> ${this.formatMarkdownText(cardJson.back || '')}
                </div>
                <div class="ai-card-preview-actions">
                    <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;" id="btnAddCardFromAi">
                        <span>✨</span> Direkt zum Deck hinzufügen
                    </button>
                    <button class="btn-secondary" style="padding: 6px 12px; font-size: 0.8rem;" id="btnEditCardFromAi">
                        <span>✏️</span> Im Editor anpassen
                    </button>
                </div>
            `;

            container.appendChild(previewBox);
            this.renderMathFormulas();

            previewBox.querySelector("#btnAddCardFromAi").addEventListener("click", () => {
                this.addCardFromAi(cardJson);
            });

            previewBox.querySelector("#btnEditCardFromAi").addEventListener("click", () => {
                this.openCardInEditorFromAi(cardJson);
            });
        } catch (e) {
            console.warn("Konnte Karten-JSON nicht parsen:", e);
        }
    }

    async addCardFromAi(cardData) {
        cardData = this.sanitizeCardLatex(cardData);
        const payload = {
            deck_id: cardData.deck_id || (this.decks[0] ? this.decks[0].id : "mechanik"),
            title: cardData.title || "Neue Physikkarte",
            front: cardData.front || "",
            back: cardData.back || "",
            hint: cardData.hint || "",
            formula_breakdown: cardData.formula_breakdown || "",
            physical_meaning: cardData.physical_meaning || "",
            validity_domain: cardData.validity_domain || "",
            tags: Array.isArray(cardData.tags) ? cardData.tags : [cardData.tags].filter(Boolean),
            difficulty: parseInt(cardData.difficulty) || 2
        };

        try {
            const res = await fetch("/api/cards", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(r => r.json());

            if (res.success) {
                this.showToast(`Karte '${payload.title}' erfolgreich zum Deck hinzugefügt!`);
                if (this.currentView === "cards") {
                    await this.loadCardsManager();
                }
                await this.loadDashboard();
            } else {
                alert("Fehler: " + res.error);
            }
        } catch (e) {
            alert("Fehler beim Speichern der Karte: " + e.message);
        }
    }

    async openCardInEditorFromAi(cardData) {
        this.toggleAiTutor(false);
        cardData = this.sanitizeCardLatex(cardData);
        await this.openCardEditor(null);

        const safeSet = (id, val) => {
            const el = document.getElementById(id);
            if (el) el.value = val !== undefined && val !== null ? val : "";
        };

        safeSet("editCardTitle", cardData.title || "");
        if (cardData.deck_id && document.getElementById("editCardDeck")) {
            document.getElementById("editCardDeck").value = cardData.deck_id;
        }
        safeSet("editCardFront", cardData.front || "");
        safeSet("editCardBack", cardData.back || "");
        safeSet("editCardBreakdown", cardData.formula_breakdown || "");
        safeSet("editCardMeaning", cardData.physical_meaning || "");
        safeSet("editCardValidity", cardData.validity_domain || "");
        safeSet("editCardHint", cardData.hint || "");
        safeSet("editCardTags", Array.isArray(cardData.tags) ? cardData.tags.join(", ") : (cardData.tags || ""));
        safeSet("editCardDifficulty", cardData.difficulty || 2);

        this.updateLiveEditorPreview();
    }

    // ==========================================
    // AI CARD GENERATION MODAL
    // ==========================================
    openAiCardGenModal() {
        const modal = document.getElementById("aiCardGenModal");
        if (!modal) return;

        const select = document.getElementById("aiCardGenDeckSelect");
        if (select) {
            select.innerHTML = "";
            this.decks.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d.id;
                opt.textContent = `${d.name} (${d.total_cards || 0} Karten)`;
                select.appendChild(opt);
            });
        }

        document.getElementById("aiCardGenTopic").value = "";
        const statusEl = document.getElementById("aiCardGenStatus");
        if (statusEl) statusEl.style.display = "none";

        modal.classList.add("active");
        setTimeout(() => {
            document.getElementById("aiCardGenTopic").focus();
        }, 150);
    }

    closeAiCardGenModal() {
        const modal = document.getElementById("aiCardGenModal");
        if (modal) modal.classList.remove("active");
    }

    async runAiCardGeneration() {
        const topic = document.getElementById("aiCardGenTopic").value.trim();
        const deckId = document.getElementById("aiCardGenDeckSelect").value;
        const statusEl = document.getElementById("aiCardGenStatus");
        const btn = document.getElementById("btnRunCardGen");

        if (!topic) {
            alert("Bitte gib ein Thema oder ein physikalisches Phänomen ein.");
            return;
        }

        if (statusEl) {
            statusEl.style.display = "block";
            statusEl.style.background = "rgba(6, 182, 212, 0.1)";
            statusEl.style.border = "1px solid var(--accent-cyan)";
            statusEl.style.color = "var(--text-primary)";
            statusEl.innerHTML = "⏳ Gemini formuliert die Karteikarte mit LaTeX, Einheiten und physikalischer Intuition...";
        }
        if (btn) btn.disabled = true;

        try {
            const res = await fetch("/api/ai/generate-card", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic, deck_id: deckId })
            }).then(r => r.json());

            if (res.success && res.card) {
                this.closeAiCardGenModal();
                this.openCardInEditorFromAi(res.card);
                this.showToast(`Karte '${res.card.title}' generiert! Bitte im Editor prüfen und speichern.`);
            } else {
                if (statusEl) {
                    statusEl.style.background = "rgba(244, 63, 94, 0.1)";
                    statusEl.style.border = "1px solid var(--accent-rose)";
                    statusEl.style.color = "var(--accent-rose)";
                    statusEl.innerHTML = `Fehler: ${this.escapeHtml(res.error || 'Generierung fehlgeschlagen.')}`;
                }
            }
        } catch (e) {
            if (statusEl) {
                statusEl.style.background = "rgba(244, 63, 94, 0.1)";
                statusEl.style.border = "1px solid var(--accent-rose)";
                statusEl.style.color = "var(--accent-rose)";
                statusEl.innerHTML = `Netzwerkfehler (Offline?): ${this.escapeHtml(e.message)}`;
            }
        } finally {
            if (btn) btn.disabled = false;
        }
    }
}

// Global App Instance
window.app = new PhysiCardsApp();
window.addEventListener("DOMContentLoaded", () => {
    window.app.init();
});
