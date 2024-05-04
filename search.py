from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load your CSV data into a DataFrame
df = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/MINI PROJECT WEB/sample.csv')

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    difficulty = request.args.get('difficulty', 'all')
    year = request.args.get('year', 'all')
    subject = request.args.get('subject', 'all')
    query = request.args.get('query', '')

    # Convert numeric difficulty in CSV to string
    difficulty_map = {0: 'easy', 1: 'medium', 2: 'hard'}
    df['difficulty'] = df['difficulty'].map(difficulty_map)

    # Filtering
    filtered_df = df
    if difficulty != 'all':
        filtered_df = filtered_df[filtered_df['difficulty'] == difficulty]
    if year != 'all':
        filtered_df = filtered_df[filtered_df['year'] == int(year)]
    if subject != 'all':
        filtered_df = filtered_df[filtered_df['subject'] == subject]
    
    # Searching
    if query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(query).any(), axis=1)]

    # Convert DataFrame to HTML
    results_html = filtered_df.to_html(classes="result-table", index=False, border=0)

    return render_template('search.html', results_html=results_html)

if __name__ == '__main__':
    app.run(debug=True)
