import os
from flask import Flask, render_template, request
from color_processing import get_top_colors




app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html')

        file = request.files['file']

        if file and file.filename != '':
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save file locally
            file.save(filepath)

            try:
                # Extract top hex colors
                colors = get_top_colors(filepath)
                return render_template('index.html', colors=colors, image_url=filepath)
            except Exception as e:
                # Print exact backend trace to terminal for debugging
                print("--- ERROR IN COLOR EXTRACTION ---")
                print(e)
                print("---------------------------------")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)