import os
import re
import fitz
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Define a function to search for the keyword in a PDF file
def search_pdf_file(pdf_file, pattern):
    with fitz.open(pdf_file) as pdf:
        num_words_list = []
        for page_num, page in enumerate(pdf):
            text = page.get_text()
            num_words = len(text.split())
            num_words_list.append(num_words)
            match = pattern.search(text)
            if match:
                return (pdf_file, page_num + 1, num_words_list)

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the search page route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the keyword from the form
        keyword = request.form['keyword']

        # Define the search keyword
        search_keyword = keyword

        # Define a regular expression pattern to match the search keyword
        pattern = re.compile(search_keyword, re.IGNORECASE)

        # Define the folder path to search for PDF files
        folder_path = 'E:\MICROBIOLOGY PDF\THEORY\Biology\cell biology'

        # Get the total number of words in all PDF files
        total_words = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file = os.path.join(root, file)
                    with fitz.open(pdf_file) as doc:
                        for page in doc:
                            total_words += len(page.get_text("text").split())

        # Calculate the average number of words per minute based on the average reading speed of 200-250 words per minute
        avg_words_per_minute = 225

        # Calculate the expected search time in minutes
        expected_time = round(total_words / avg_words_per_minute, 2)

        # Calculate the time the search started
        start_time = datetime.now()

        # Search for PDF files in the folder and its subfolders
        results = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file = os.path.join(root, file)
                    result = search_pdf_file(pdf_file, pattern)
                    if result:
                        # Open the PDF file and get the total number of words
                        doc = fitz.open(result[0])
                        total_words = 0
                        for page in doc:
                            total_words += len(page.get_text("text").split())

                        # Define a regular expression pattern to match the search keyword
                        pattern = re.compile(search_keyword, re.IGNORECASE)

                        # Search for the keyword in each page of the PDF file
                        keyword_counts = []
                        for page_num, page in enumerate(doc):
                            text = page.get_text("text")
                            matches = pattern.findall(text)
                            count = len(matches)
                            keyword_counts.append(count)

                        # Add the results to the list
                        results.append((result[0], result[1], result[2][result[1] - 1], sum(keyword_counts)))

        # Render the search results template
        return render_template('index.html', keyword=keyword, results=results)

    # Render the search form template
    return render_template('search_form.html')


if __name__ == '__main__':
    app.run(debug=True)
