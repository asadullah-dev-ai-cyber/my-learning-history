# 🎨 Watermark Studio Pro

A sleek, modern desktop GUI application built in Python that allows users to seamlessly add customizable text watermarks to their images. 

Developed as part of **Day 84 of the 100 Days of Code: Python Bootcamp**.

---

## ✨ Features

* **Custom Text & Positioning:** Place watermarks in 5 locations (*Top-Left*, *Top-Right*, *Bottom-Left*, *Bottom-Right*, or *Center*).
* **Font Style & Sizing:** Choose from popular TrueType system fonts (*Arial*, *Impact*, *Georgia*, *Courier*, *Times New Roman*) and scale text size from 20px up to 100px.
* **Color Picker:** Select any custom text color using an integrated native color palette dialog.
* **Smart Placement Math:** Uses PIL's `textbbox` to dynamically render text margins cleanly without clipping edges.
* **Format Conversion:** Supports loading and exporting `.png`, `.jpg`, `.jpeg`, and `.bmp` files.

---

## 🛠️ Built With

* **[Python 3](https://www.python.org/)**
* **[Tkinter](https://docs.python.org/3/library/tkinter.html)** - Desktop GUI Framework
* **[Pillow (PIL)](https://pypi.org/project/Pillow/)** - Image Processing Engine

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3 installed. You can install the required dependency (`Pillow`) via pip:

```bash
pip install Pillow