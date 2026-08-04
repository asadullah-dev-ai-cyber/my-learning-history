from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont

# Global variables
file_path = ""
selected_color = (255, 255, 255, 220)  # Default White with transparency

# Mapping friendly font names to system TrueType font files
FONT_MAP = {
    "Arial": "arial.ttf",
    "Impact": "impact.ttf",
    "Georgia": "georgia.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf"
}


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        file_label.config(text=f"Selected: {file_path.split('/')[-1]}", fg="#2e7d32")


def choose_color():
    global selected_color
    color_code = colorchooser.askcolor(title="Choose Watermark Color")
    if color_code[0]:
        r, g, b = map(int, color_code[0])
        selected_color = (r, g, b, 220)
        color_btn.config(bg=color_code[1])


def add_watermark():
    global file_path, selected_color
    watermark_text = entry.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select an image first!")
        return
    if not watermark_text:
        messagebox.showwarning("Warning", "Please enter watermark text!")
        return

    image = Image.open(file_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Get user font selections
    font_name = font_style_var.get()
    font_file = FONT_MAP.get(font_name, "arial.ttf")
    font_size = int(size_var.get())

    try:
        font = ImageFont.truetype(font_file, size=font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text dimensions
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width, img_height = image.size
    margin = 20

    # Determine position
    choice = position_var.get()
    if choice == "Top-Left":
        position = (margin, margin)
    elif choice == "Top-Right":
        position = (img_width - text_width - margin, margin)
    elif choice == "Bottom-Left":
        position = (margin, img_height - text_height - margin)
    elif choice == "Bottom-Right":
        position = (img_width - text_width - margin, img_height - text_height - margin)
    else:  # Center
        position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

    # Draw watermark text
    draw.text(position, watermark_text, font=font, fill=selected_color)

    # Save Image with pre-populated initial filename
    save_path = filedialog.asksaveasfilename(
        initialfile="watermarked_image.png",
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
    )
    if save_path:
        if save_path.endswith(".jpg") or save_path.endswith(".jpeg"):
            image = image.convert("RGB")
        image.save(save_path)
        messagebox.showinfo("Success", "Watermarked image saved successfully!")


# --- UI Setup ---
window = Tk()
window.title("Watermark Studio Pro")
window.geometry("500x580")
window.config(padx=20, pady=20, bg="#f4f6f8")
window.resizable(False, False)

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_MAIN = ("Segoe UI", 10)

# Header
title_label = Label(window, text="Image Watermarking App", font=FONT_TITLE, bg="#f4f6f8", fg="#1e293b")
title_label.pack(pady=(0, 10))

# 1. Text Entry
label = Label(window, text="1. Watermark Text", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
label.pack(anchor="w", pady=(5, 2))
entry = Entry(window, width=35, font=FONT_MAIN, relief="solid", bd=1)
entry.pack(fill="x", pady=(0, 10), ipady=3)

# 2. File Selector
select_label = Label(window, text="2. Target Image", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
select_label.pack(anchor="w", pady=(5, 2))
select_btn = Button(window, text="Browse Image", command=open_file, font=FONT_MAIN, bg="#e2e8f0", fg="#0f172a",
                    relief="flat", cursor="hand2")
select_btn.pack(fill="x", pady=(0, 2))
file_label = Label(window, text="No image selected", font=("Segoe UI", 9, "italic"), bg="#f4f6f8", fg="#64748b")
file_label.pack(pady=(0, 10))

# 3. Position, Font Style, Size & Color Options Grid
opts_frame = Frame(window, bg="#f4f6f8")
opts_frame.pack(fill="x", pady=(0, 15))

# Position Menu
pos_label = Label(opts_frame, text="Position", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
pos_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
position_var = StringVar(window)
position_var.set("Bottom-Right")
position_menu = OptionMenu(opts_frame, position_var, "Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center")
position_menu.grid(row=1, column=0, padx=(0, 10), sticky="w")

# Font Style Menu
font_style_label = Label(opts_frame, text="Font Style", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
font_style_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
font_style_var = StringVar(window)
font_style_var.set("Arial")
font_menu = OptionMenu(opts_frame, font_style_var, *FONT_MAP.keys())
font_menu.grid(row=1, column=1, padx=(0, 10), sticky="w")

# Font Size Menu
size_label = Label(opts_frame, text="Size", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
size_label.grid(row=0, column=2, sticky="w", padx=(0, 5))
size_var = StringVar(window)
size_var.set("40")
size_menu = OptionMenu(opts_frame, size_var, "20", "30", "40", "60", "80", "100")
size_menu.grid(row=1, column=2, padx=(0, 10), sticky="w")

# Color Picker Button
color_label = Label(opts_frame, text="Color", font=FONT_LABEL, bg="#f4f6f8", fg="#334155")
color_label.grid(row=0, column=3, sticky="w")
color_btn = Button(opts_frame, text="Pick Color", command=choose_color, font=FONT_MAIN, bg="#ffffff", relief="solid",
                   bd=1, cursor="hand2")
color_btn.grid(row=1, column=3, sticky="w")

# 4. Action Button
watermark_btn = Button(window, text="Apply & Save Watermark", command=add_watermark, font=("Segoe UI", 11, "bold"),
                       bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat",
                       cursor="hand2")
watermark_btn.pack(fill="x", ipady=6, pady=(10, 0))

window.mainloop()