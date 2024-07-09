import requests
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import re

# Function to fetch text from a URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the text: {e}")
        return None

# Map function
def map_function(word):
    return word, 1

# Shuffle function
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Reduce function
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# MapReduce execution
def map_reduce(text):
    words = re.findall(r'\w+', text.lower())  # Split text into words

    # Parallel Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Step 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Parallel Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Function to visualize the top words
def visualize_top_words(word_counts, top_n=10):
    top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='green')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main block
if __name__ == "__main__":
    # Input URL for text
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Execute MapReduce on the input text
        word_counts = map_reduce(text)

        print("Word frequency analysis result:", word_counts)

        # Visualize the top words
        visualize_top_words(word_counts, top_n=10)
    else:
        print("Error: Unable to fetch the input text.")
