"""
SZT_SonyA7IV_Chatbot_Html.py
Sony Alpha 7 IV (ILCE-7M4) RAG Csevegőrobot - Helyi Webes Kiszolgáló

Készítette: Szellő Tamás
Leírás: Helyi beágyazott HTTP szerver, amely közvetítőként (proxy) működik
        a helyi böngészős csevegőfelület és a távoli Flowise RAG végpont között.
"""

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import sys
import threading
import time
from typing import Any, Dict
import webbrowser

import requests

# ==============================================================================
# 1. KONFIGURÁCIÓ
# ==============================================================================

@dataclass(frozen=True)
class AppConfig:
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    FLOWISE_API_URL: str = (
        "https://flowiseai.itk.ppke.hu/api/v1/prediction/60eb7e87-4d7d-4ba8-aaa9-338e7c9da67a"
    )
    REQUEST_TIMEOUT_SEC: int = 120
    LOG_LEVEL: int = logging.INFO


logging.basicConfig(
    level=AppConfig.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SonyA7IV_Chatbot")


# ==============================================================================
# 2. FLOWISE API KLIENS
# ==============================================================================

class FlowiseClient:
    """A távoli Flowise RAG rendszerrel történő kommunikációért felelős osztály."""

    def __init__(self, endpoint_url: str, timeout: int):
        self._endpoint_url = endpoint_url
        self._timeout = timeout
        self._session = requests.Session()

    def query(self, question: str) -> Dict[str, Any]:
        """Kérdés továbbítása a Flowise láncnak és a válasz feldolgozása."""
        payload = {"question": question}
        try:
            response = self._session.post(
                self._endpoint_url,
                json=payload,
                timeout=self._timeout
            )
            response.raise_for_status()
            data = response.json()

            # Szöveges válasz kinyerése a Flowise JSON válaszstruktúrájából
            if isinstance(data, dict):
                answer_text = data.get("text") or data.get("error") or "Nem érkezett érvényes válaszszöveg."
            else:
                answer_text = str(data)

            return {"success": True, "text": answer_text}

        except requests.exceptions.Timeout:
            logger.error("Időtúllépés a Flowise kapcsolatban.")
            return {"success": False, "text": "A szerver válaszadási ideje lejárt (timeout)."}
        except requests.exceptions.RequestException as exc:
            logger.error("Hálózati hiba a Flowise végpont hívásakor: %s", exc)
            return {"success": False, "text": f"Hálózati hiba történt: {str(exc)}"}
        except Exception as exc:
            logger.error("Váratlan hiba az API kérés közben: %s", exc)
            return {"success": False, "text": f"Váratlan hiba: {str(exc)}"}


# ==============================================================================
# 3. BEÁGYAZOTT FELHASZNÁLÓI FELÜLET (HTML/CSS/JS)
# ==============================================================================

HTML_UI = """<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sony A7 IV Fotós Asszisztens</title>
    <style>
        :root {
            --bg-base: #0f172a;
            --bg-surface: #1e293b;
            --bg-input: #334155;
            --accent-primary: #3b82f6;
            --accent-hover: #2563eb;
            --text-main: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --msg-user: #2563eb;
            --msg-bot: #334155;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            justify-content: center;
        }

        .chat-app {
            width: 100%;
            max-width: 900px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background-color: var(--bg-surface);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        }

        .chat-header {
            padding: 16px 24px;
            background-color: var(--bg-base);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h1 {
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .status-badge {
            font-size: 0.75rem;
            background: #10b981;
            color: #022c22;
            padding: 4px 8px;
            border-radius: 9999px;
            font-weight: 700;
        }

        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .message {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 8px;
            line-height: 1.6;
            font-size: 0.95rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message.user {
            align-self: flex-end;
            background-color: var(--msg-user);
            color: #ffffff;
            border-bottom-right-radius: 2px;
        }

        .message.bot {
            align-self: flex-start;
            background-color: var(--msg-bot);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            border-bottom-left-radius: 2px;
        }

        .input-panel {
            padding: 16px 24px;
            background-color: var(--bg-base);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 12px;
        }

        textarea {
            flex: 1;
            resize: none;
            height: 48px;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background-color: var(--bg-surface);
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            font-family: inherit;
        }

        textarea:focus {
            border-color: var(--accent-primary);
        }

        button {
            background-color: var(--accent-primary);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.15s ease;
        }

        button:hover {
            background-color: var(--accent-hover);
        }

        button:disabled {
            background-color: var(--bg-input);
            cursor: not-allowed;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="chat-app">
        <header class="chat-header">
            <h1>Sony A7 IV Fotós Asszisztens</h1>
            <span class="status-badge">RAG AKTÍV</span>
        </header>

        <main class="messages-container" id="chat">
            <div class="message bot">Szia! Készen állok. Milyen fotózási helyzetben vagy beállításban segíthetek a Sony A7 IV kezelési útmutatója alapján?</div>
        </main>

        <footer class="input-panel">
            <textarea id="prompt" placeholder="Írd ide a kérdésed (Enter: küldés, Shift+Enter: új sor)..."></textarea>
            <button id="send-btn" onclick="submitMessage()">Küldés</button>
        </footer>
    </div>

    <script>
        const chatWindow = document.getElementById('chat');
        const promptInput = document.getElementById('prompt');
        const sendButton = document.getElementById('send-btn');

        promptInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submitMessage();
            }
        });

        async function submitMessage() {
            const queryText = promptInput.value.trim();
            if (!queryText) return;

            renderMessage(queryText, 'user');
            promptInput.value = '';
            sendButton.disabled = true;

            const tempMessageId = renderMessage('A Sony A7 IV útmutató feldolgozása folyamatban...', 'bot');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: queryText })
                });

                const data = await response.json();
                document.getElementById(tempMessageId).innerText = data.text;
            } catch (err) {
                document.getElementById(tempMessageId).innerText = "Hiba történt a helyi kiszolgálóval való kommunikáció során.";
            } finally {
                sendButton.disabled = false;
                promptInput.focus();
            }
        }

        function renderMessage(text, role) {
            const messageId = 'msg-' + Date.now();
            const messageElement = document.createElement('div');
            messageElement.id = messageId;
            messageElement.className = `message ${role}`;
            messageElement.innerText = text;
            chatWindow.appendChild(messageElement);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return messageId;
        }
    </script>
</body>
</html>
"""


# ==============================================================================
# 4. HTTP KÉRÉSKÉZELŐ (ROUTING & PROXY)
# ==============================================================================

class ChatProxyHandler(BaseHTTPRequestHandler):
    """Beépített kéréskezelő a weboldal és az API továbbítására."""

    flowise_client: FlowiseClient

    def do_GET(self) -> None:  # pylint: disable=invalid-name
        """A statikus HTML kezelőfelület kiszolgálása."""
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_UI.encode("utf-8"))
        else:
            self.send_error(404, "Az oldal nem található")

    def do_POST(self) -> None:  # pylint: disable=invalid-name
        """A beérkező JSON kérdések fogadása és továbbítása a Flowise-nak."""
        if self.path == "/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)

            try:
                payload = json.loads(request_body.decode("utf-8"))
                question = payload.get("question", "")

                # Flowise hívás végrehajtása
                result = self.flowise_client.query(question=question)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

            except json.JSONDecodeError:
                self._send_json_error(400, "Érvénytelen JSON formátum")
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Hiba a kérés kiszolgálásakor: %s", exc)
                self._send_json_error(500, f"Belső szerverhiba: {str(exc)}")
        else:
            self.send_error(404, "Végpont nem található")

    def _send_json_error(self, status_code: int, message: str) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "text": message}).encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:  # pylint: disable=redefined-builtin
        """Alapértelmezett BaseHTTPRequestHandler stderr naplózás felülírása."""
        logger.debug("%s - - [%s] %s", self.address_string(), self.log_date_time_string(), format % args)


# ==============================================================================
# 5. ALKALMAZÁS INDÍTÁSA
# ==============================================================================

def open_browser_delayed(url: str, delay_sec: float = 1.0) -> None:
    """Várakozás a szerver inicializálására, majd a böngésző megnyitása."""
    time.sleep(delay_sec)
    logger.info("Böngészőfelület megnyitása: %s", url)
    webbrowser.open(url)


def run() -> None:
    """Szerver indítása és eseménykezelése."""
    config = AppConfig()
    client = FlowiseClient(config.FLOWISE_API_URL, config.REQUEST_TIMEOUT_SEC)
    ChatProxyHandler.flowise_client = client

    server_address = (config.HOST, config.PORT)
    try:
        httpd = HTTPServer(server_address, ChatProxyHandler)
    except OSError as err:
        logger.critical("Nem sikerült elindítani a szervert a %s:%s címen: %s", config.HOST, config.PORT, err)
        sys.exit(1)

    app_url = f"http://{config.HOST}:{config.PORT}"
    logger.info("Sony A7 IV Chatbot szerver elindult: %s", app_url)

    # Böngésző indítása külön háttérszálon
    threading.Thread(target=open_browser_delayed, args=(app_url,), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Leállítási parancs érkezett (Ctrl+C). Szerver leállítása...")
    finally:
        httpd.server_close()
        logger.info("A szerver sikeresen leállt.")


if __name__ == "__main__":
    run()