/**
 * PhysiCards - Active Scratchpad (Whiteboard / Formel-Kritzelblock)
 * Allows active handwriting/drawing of formulas on an interactive canvas
 * before flipping the card to check recall.
 */

class Scratchpad {
    constructor(canvasId, containerId) {
        this.canvas = document.getElementById(canvasId);
        this.container = document.getElementById(containerId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext("2d");
        this.isDrawing = false;
        this.currentColor = "#38bdf8"; // Cyan
        this.currentSize = 3;
        this.isEraser = false;
        this.history = [];
        this.maxHistory = 15;
        this.visible = false;

        this.initEvents();
        this.resize();
        window.addEventListener("resize", () => this.resize());
    }

    resize() {
        if (!this.canvas || !this.container) return;
        const rect = this.container.getBoundingClientRect();
        // Save current content if already drawn
        let tempCanvas = null;
        if (this.canvas.width > 0 && this.canvas.height > 0) {
            tempCanvas = document.createElement("canvas");
            tempCanvas.width = this.canvas.width;
            tempCanvas.height = this.canvas.height;
            const tempCtx = tempCanvas.getContext("2d");
            tempCtx.drawImage(this.canvas, 0, 0);
        }

        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = rect.width * dpr;
        this.canvas.height = Math.max(220, rect.height) * dpr;
        this.canvas.style.width = `${rect.width}px`;
        this.canvas.style.height = `${Math.max(220, rect.height)}px`;

        this.ctx.scale(dpr, dpr);
        this.ctx.lineCap = "round";
        this.ctx.lineJoin = "round";

        if (tempCanvas) {
            this.ctx.drawImage(tempCanvas, 0, 0, rect.width, Math.max(220, rect.height));
        }
    }

    initEvents() {
        const getPos = (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        };

        const startDraw = (e) => {
            if (!this.visible) return;
            e.preventDefault();
            this.isDrawing = true;
            this.saveHistory();
            const pos = getPos(e);
            this.lastX = pos.x;
            this.lastY = pos.y;
            this.ctx.beginPath();
            this.ctx.moveTo(pos.x, pos.y);
            this.ctx.lineTo(pos.x, pos.y);
            this.ctx.strokeStyle = this.isEraser ? "rgba(15, 23, 42, 1)" : this.currentColor;
            this.ctx.lineWidth = this.isEraser ? this.currentSize * 4 : this.currentSize;
            this.ctx.stroke();
        };

        const draw = (e) => {
            if (!this.isDrawing || !this.visible) return;
            e.preventDefault();
            const pos = getPos(e);
            this.ctx.beginPath();
            this.ctx.moveTo(this.lastX, this.lastY);
            this.ctx.lineTo(pos.x, pos.y);
            this.ctx.strokeStyle = this.isEraser ? "rgba(15, 23, 42, 1)" : this.currentColor;
            this.ctx.lineWidth = this.isEraser ? this.currentSize * 4 : this.currentSize;
            this.ctx.stroke();
            this.lastX = pos.x;
            this.lastY = pos.y;
        };

        const stopDraw = () => {
            this.isDrawing = false;
        };

        this.canvas.addEventListener("mousedown", startDraw);
        this.canvas.addEventListener("mousemove", draw);
        window.addEventListener("mouseup", stopDraw);

        this.canvas.addEventListener("touchstart", startDraw, { passive: false });
        this.canvas.addEventListener("touchmove", draw, { passive: false });
        window.addEventListener("touchend", stopDraw);
    }

    saveHistory() {
        if (!this.canvas) return;
        if (this.history.length >= this.maxHistory) {
            this.history.shift();
        }
        this.history.push(this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height));
    }

    undo() {
        if (this.history.length > 0) {
            const prevState = this.history.pop();
            this.ctx.putImageData(prevState, 0, 0);
        } else {
            this.clear();
        }
    }

    clear() {
        if (!this.canvas || !this.ctx) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.history = [];
    }

    setColor(color) {
        this.currentColor = color;
        this.isEraser = false;
    }

    setSize(size) {
        this.currentSize = size;
    }

    setEraser(enabled = true) {
        this.isEraser = enabled;
    }

    toggle() {
        this.visible = !this.visible;
        if (this.container) {
            this.container.classList.toggle("scratchpad-active", this.visible);
            if (this.visible) {
                this.resize();
            }
        }
        return this.visible;
    }

    show() {
        this.visible = true;
        if (this.container) {
            this.container.classList.add("scratchpad-active");
            this.resize();
        }
    }

    hide() {
        this.visible = false;
        if (this.container) {
            this.container.classList.remove("scratchpad-active");
        }
    }
}

window.Scratchpad = Scratchpad;

