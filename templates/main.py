from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    # Perform search logic here
    return render_template('results.html', keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)


'''from flask import Flask, render_template

app = Flask(__name__)

def scan_files(directory):
    return results

from scan import scan_files
@app.route('/scan')

if __name__ == '__main__':
    app.run(debug=True)

def scan():
    directory = 'scan.py'
    results = scan_files(directory)
    return render_template('index.html', results=results)
'''