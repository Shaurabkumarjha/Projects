from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to change this to a real secret key in production

# Dummy dataset (replace with your actual data or database)
products = [
    {"Name": "Product 1", "Brand": "Brand A", "ImageURL": "https://via.placeholder.com/200", "ReviewCount": 100, "Rating": 4.5},
    {"Name": "Product 2", "Brand": "Brand B", "ImageURL": "https://via.placeholder.com/200", "ReviewCount": 200, "Rating": 4.7},
    {"Name": "Product 3", "Brand": "Brand C", "ImageURL": "https://via.placeholder.com/200", "ReviewCount": 300, "Rating": 4.0},
    {"Name": "Product 4", "Brand": "Brand D", "ImageURL": "https://via.placeholder.com/200", "ReviewCount": 150, "Rating": 4.3},
]

# Function to truncate the product name if it exceeds a certain length
def truncate(text, length):
    if len(text) > length:
        return text[:length] + '...'
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Get the user inputs for product search and number of recommendations
    product_name = request.form.get('prod')
    num_recommendations = request.form.get('nbr')

    # Validate number of recommendations input
    if not num_recommendations.isdigit() or int(num_recommendations) <= 0:
        flash('Please enter a valid number of products.')
        return redirect(url_for('index'))

    num_recommendations = int(num_recommendations)

    # Here you can replace the following logic with your actual recommendation algorithm
    # For now, we will just return the first `num_recommendations` products
    content_based_rec = pd.DataFrame(products[:num_recommendations])

    return render_template('index.html', content_based_rec=content_based_rec, message="Recommendations displayed below!")

@app.route('/signup', methods=['POST'])
def signup():
    # Handle user sign up here
    # Implement the logic to register a user
    flash("Sign up successful!")
    return redirect(url_for('index'))

@app.route('/signin', methods=['POST'])
def signin():
    # Handle user sign in here
    # Implement the logic to log in a user
    flash("Sign in successful!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
