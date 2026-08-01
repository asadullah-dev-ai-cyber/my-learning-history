# 📡 Morse Code Converter CLI

A clean, interactive command-line application built in Python that converts standard English text to Morse code and decrypts Morse code back into plain text.

---

## ✨ Features

- **Bidirectional Conversion:** Encrypt English text to Morse code and decrypt Morse code back to English.
- **Robust Error Handling:** Uses dictionary fallbacks (`.get()`) to handle unrecognized characters gracefully without crashing.
- **Word & Letter Spacing Support:** Supports standard international Morse code format (single spaces between letters, slashes `/` or triple spaces between words).
- **Automated Test Suite:** Built-in unit tests covering core translation logic and edge cases using Python's `unittest`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed on your machine.

### How to Run the App
Execute `main.py` directly from your terminal:

```bash
python main.py