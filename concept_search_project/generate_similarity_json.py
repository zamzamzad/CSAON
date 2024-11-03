import numpy as np
import pandas as pd
import json

# Load the similarity matrix
similarity_matrix = np.load('similarity_matrix.npy')

# Read the search results CSV to get article titles
df = pd.read_csv('search_results.csv')

# Create nodes from the CSV file
nodes = [{'id': i, 'title': title} for i, title in enumerate(df['title'])]

# Create links based on similarity scores
links = []
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        value = similarity_matrix[i, j]
        if value > 0:  # Adjust this threshold as needed
            links.append({'source': i, 'target': j, 'value': value})

# Create the JSON structure
graph = {'nodes': nodes, 'links': links}

# Save to a JSON file
with open('similarity_matrix.json', 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=4)
