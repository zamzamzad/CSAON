# Import necessary libraries
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pandas as pd
import torch
import os

# Load the pre-trained GPT-2 model and tokenizer
# - GPT2LMHeadModel: The GPT-2 model class for text generation tasks.
# - GPT2Tokenizer: Tokenizer for encoding and decoding text data compatible with GPT-2.
# - from_pretrained: Loads the model and tokenizer weights pre-trained on a large corpus of text data.
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Ensure the model's pad_token_id is set to eos_token_id
# - pad_token_id: The token used to pad sequences to a common length.
# - eos_token_id: The token indicating the end of a sequence.
# - This step ensures that padding is handled correctly by setting the padding token to the end-of-sequence token.
model.config.pad_token_id = model.config.eos_token_id

# Function to generate a title for a given description
def generate_title(description):
    # Define the prompt that will be used to generate the title
    # - The model is prompted with "Title: <description>\nTitle:" to generate a title continuation.
    prompt = f"Title: {description}\nTitle:"
    
    # Tokenize the input prompt to convert it into numerical format understood by GPT-2
    # - max_length=512: Limits the length of the input sequence to 512 tokens.
    # - truncation=True: Truncates the input sequence to the maximum length if necessary.
    inputs = tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs.get('attention_mask', None)  # Used to ignore padding tokens during processing
    
    # Generate a title using the GPT-2 model
    # - max_new_tokens=50: Limits the generated title to 50 tokens.
    # - num_return_sequences=1: Generates a single title.
    # - do_sample=True: Enables sampling for more diverse outputs.
    # - temperature=0.7: Controls the creativity of the output (lower values make it more conservative).
    # - top_k=50 and top_p=0.95: Controls the sampling strategy to avoid unlikely words.
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=50,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )
    
    # Decode the generated title back into text format
    title = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    # Remove the prompt part from the generated text to extract the title only
    title = title.replace(prompt, "").strip()
    return title

# Load the CSV file containing articles and their descriptions
# - pandas (pd): A powerful library for data manipulation and analysis, especially with tabular data.
df = pd.read_csv('articles_with_topics.csv')

# Print the number of rows loaded from the CSV for debugging purposes
print(f"Loaded {len(df)} rows from the CSV.")

# Limit the data to the first 10 rows for testing purposes
# - head(10): Returns the first 10 rows of the DataFrame.
df = df.head(10)

# Check if 'description' column is properly loaded for debugging
print("Descriptions loaded from the CSV:")
print(df['description'].head(10))

# Function to generate titles for each description and track progress
def apply_generate_title(row):
    # Print the index of the current row being processed for progress tracking
    print(f"Generating title for description index {row.name}")
    
    # Print the original description for debugging
    print(f"Original Description: {row['description']}")
    
    # Generate a title for the current description
    generated_title = generate_title(row['description'])
    
    # Print the generated title for debugging
    print(f"Generated title: {generated_title}")
    
    # Return the generated title to be added to the DataFrame
    return generated_title

# Apply the title generation function to each row in the DataFrame
# - axis=1: Applies the function row-wise.
df['concept_title'] = df.apply(apply_generate_title, axis=1)

# Save the results to a new CSV file with the additional 'concept_title' column
output_csv_path = 'articles_with_titles.csv'

# Ensure the output file is not being used by another process by deleting it if it exists
if os.path.exists(output_csv_path):
    os.remove(output_csv_path)

# Save the DataFrame to a CSV file
df.to_csv(output_csv_path, index=False)

# Print a message indicating the completion of the title generation process
print(f"Title generation complete and saved to '{output_csv_path}'.")

# Load the saved CSV to verify the results
df_saved = pd.read_csv(output_csv_path)

# Ensure generated titles are different from the original descriptions
# Print out the original descriptions and generated titles for verification
print("Verifying generated titles:")
for i, row in df_saved.iterrows():
    print(f"Index {i} - Original: {row['description']}")
    print(f"Index {i} - Generated: {row['concept_title']}")
    print("")
