from flask import Flask, render_template

@app.route('')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

def scan_files(directory):
    # logic for scanning files in directory
    # ...
    return results
