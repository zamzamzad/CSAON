
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Check if the script received the correct file path argument
if len(sys.argv) != 2:
    print("Usage: python article_similarity_search.py <input_csv_file>")
    sys.exit(1)

input_csv_file = sys.argv[1]

# Read the input CSV file
try:
    df = pd.read_csv(input_csv_file)
    print(f"Successfully read {input_csv_file}")
except Exception as e:
    print(f"Error reading {input_csv_file}: {e}")
    sys.exit(1)

# Check if the necessary columns are present in the CSV file
if 'title' not in df.columns or 'description' not in df.columns:
    print("The input CSV file must contain 'title' and 'description' columns.")
    sys.exit(1)

# Combine title and description for the TF-IDF vectorizer (for machine readable data)
df['text'] = df['title'] + " " + df['description']
print("Combined title and description into 'text' column.")

# Define a list of Arabic stop words
arabic_stop_words = [
    'في', 'من', 'على', 'و', 'أن', 'إلى', 'عن', 'ما', 'لا', 'مع', 'هذا', 'ذلك', 'إلى', 'عند', 'بعد', 'أن', 'إذا', 'لكن', 'كان', 'لقد'
]

# Apply TF-IDF vectorization (transform the text into meaningful representation of integers or numbers which is used to fit machine learning algorithm for predictions)
try:
    tfidf_vectorizer = TfidfVectorizer(stop_words=arabic_stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])
    print("TF-IDF vectorization completed.")
except Exception as e:
    print(f"Error during TF-IDF vectorization: {e}")
    sys.exit(1)

# Compute the cosine similarity matrix (it finds the similarity between the vactors)
try:
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print("Cosine similarity matrix computed.")
except Exception as e:
    print(f"Error computing cosine similarity matrix: {e}")
    sys.exit(1)

# Save the similarity matrix to a file (save the similar topics in a file)
try:
    np.save('similarity_matrix.npy', cosine_sim_matrix)
    print("Saved similarity matrix to 'similarity_matrix.npy'.")
except Exception as e:
    print(f"Error saving similarity matrix: {e}")
    sys.exit(1)
