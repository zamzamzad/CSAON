# Import necessary libraries
# - pandas: A powerful Python library used for data manipulation and analysis, particularly for working with structured data like tables (DataFrames).
# - sklearn (scikit-learn): A widely-used library for machine learning in Python. It provides tools for data preprocessing, classification, regression, clustering, and more.
# - CountVectorizer: A tool in sklearn that converts a collection of text documents to a matrix of token counts, useful for text mining and natural language processing (NLP).
# - Latent Dirichlet Allocation (LDA): A probabilistic model provided by sklearn for topic modeling. It identifies abstract topics that occur in a collection of documents.
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load preprocessed data from CSV file
# - pandas.read_csv(): Reads a CSV file into a DataFrame. A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types (like a spreadsheet or SQL table).
# This DataFrame holds the preprocessed text data, with each row representing an article and each column representing different attributes (like the description of the article).
df = pd.read_csv('preprocessed_articles.csv')

# Initialize the CountVectorizer
# - CountVectorizer: Converts a collection of text documents to a matrix of token counts (document-term matrix). 
#   Each row corresponds to a document, and each column corresponds to a term from the corpus (vocabulary).
# - max_df=0.95: Ignores terms that appear in more than 95% of the documents to exclude very common words that are not informative for distinguishing topics.
# - min_df=2: Ignores terms that appear in fewer than 2 documents to exclude very rare words that may not contribute meaningfully to topics.
# - stop_words='english': Removes common English stop words (e.g., 'the', 'and') to focus on more meaningful words.
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')

# Fit the vectorizer to the description column and transform the text data into a document-term matrix
# - fit_transform(): Learns the vocabulary dictionary from the 'description' column and returns the document-term matrix (X).
#   This matrix has rows representing documents and columns representing terms, with the values indicating the frequency of terms in each document.
X = vectorizer.fit_transform(df['description'])

# Initialize the Latent Dirichlet Allocation (LDA) model
# - LDA: A generative probabilistic model used for topic modeling. It assumes each document is a mixture of a small number of topics, and each word in the document is attributable to one of the document's topics.
# - n_components=10: Specifies the number of topics to extract from the corpus (vocabolary). Adjusting this number can change the granularity of the topics discovered.
# - random_state=0: Sets a seed for random number generation to ensure that the results are reproducible (i.e., the same each time you run the code).
lda = LatentDirichletAllocation(n_components=10, random_state=0)

# Fit the LDA model to the document-term matrix
# - lda.fit(X): Trains the LDA model on the document-term matrix (X). The model learns the topic distribution for the entire corpus and the word distribution for each topic.
lda.fit(X)

# Assign topics to articles based on the LDA model
# - lda.transform(X): Transforms the document-term matrix into a matrix of topic probabilities for each document.
# - argmax(axis=1): Finds the index of the highest probability topic for each document, effectively assigning each document to the most likely topic.
df['topic'] = lda.transform(X).argmax(axis=1)

# Save the DataFrame with assigned topics to a new CSV file
# - to_csv(): Saves the DataFrame, now with an additional 'topic' column, to a new CSV file named 'articles_with_topics.csv'.
#   This file can be used for further analysis or integration into other systems.
df.to_csv('articles_with_topics.csv', index=False)
