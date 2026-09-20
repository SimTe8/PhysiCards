"""
PhysiCards - Main Application Entrypoint
Launches the Flask backend and opens the native Desktop window via PyWebView
with an automatic fallback to the system default browser.
"""

import argparse
import os
import socket
import sys
import threading
import time
import webbrowser

# Ensure current directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app


def find_free_port(preferred_port=5055):
    """Finds an available TCP port starting with preferred_port."""
    for port in range(preferred_port, preferred_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return preferred_port


def start_flask(port):
    """Runs the Flask server in a background thread."""
    # Run with wait_timeout and quiet logging
    import logging

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)


def wait_for_server(port, timeout=5.0):
    """Wait until the Flask server is responding on localhost."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except (TimeoutError, ConnectionRefusedError, OSError):
            time.sleep(0.1)
    return False


def main():
    parser = argparse.ArgumentParser(
        description="PhysiCards - Physik Karteikarten Software"
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Im Standard-Webbrowser anstelle des Desktop-Fensters öffnen",
    )
    parser.add_argument(
        "--port", type=int, default=5055, help="Port für den lokalen Webserver"
    )
    args = parser.parse_args()

    port = find_free_port(args.port)
    url = f"http://127.0.0.1:{port}"

    print("==================================================")
    print("  PhysiCards - Physik Karteikarten & Formeltrainer")
    print(f"  Lokaler Server: {url}")
    print("==================================================")

    # Start Flask server thread
    server_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    server_thread.start()

    if not wait_for_server(port):
        print("[!] Warnung: Server brauchte länger zum Starten, fahre trotzdem fort...")

    if args.browser:
        print(f"[*] Öffne im Standard-Browser: {url}")
        webbrowser.open(url)
        print("[*] Drücke Strg+C zum Beenden.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nBeende PhysiCards. Auf Wiedersehen!")
            sys.exit(0)

    # Try launching PyWebView desktop window
    try:
        import webview

        print("[*] Starte Desktop-Oberfläche...")
        window = webview.create_window(
            title="PhysiCards - Physik Karteikarten & Formeltrainer",
            url=url,
            width=1240,
            height=860,
            min_size=(900, 600),
            background_color="#0f172a",
        )
        webview.start(debug=False)
        print("[*] Desktop-Fenster geschlossen. Beende PhysiCards.")
    except Exception as e:
        print(f"[!] PyWebView konnte nicht gestartet werden ({e}).")
        print(f"[*] Wechsle automatisch zum Browser-Modus: {url}")
        webbrowser.open(url)
        print("[*] Drücke Strg+C zum Beenden.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nBeende PhysiCards. Auf Wiedersehen!")
            sys.exit(0)


if __name__ == "__main__":
    main()
