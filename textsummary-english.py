import streamlit as st
from collections import Counter
from heapq import nlargest

# Function to calculate word frequencies
def calculate_word_frequencies(sent_tokens):
    word_list = [word.lower() for sent in sent_tokens for word in sent]
    word_frequencies = dict(Counter(word_list))
    return word_frequencies

# Function to calculate sentence scores
def calculate_sentence_scores(sent_tokens, word_frequencies):
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.lower() in word_frequencies.keys():
                if tuple(sent) not in sent_scores:
                    sent_scores[tuple(sent)] = word_frequencies[word.lower()]
                else:
                    sent_scores[tuple(sent)] += word_frequencies[word.lower()]
    return sent_scores

# Streamlit app
st.title("Sentence Score Calculator with Word Frequencies")

# Input for sentences
st.subheader("Enter sentences")
sentence_input = st.text_area("Enter sentences, each separated by a new line", "")
sent_tokens = [sent.split() for sent in sentence_input.split('\n') if sent]

# Calculate word frequencies
if sent_tokens:
    word_frequencies = calculate_word_frequencies(sent_tokens)
    
    # Display word frequencies
    st.subheader("Calculated Word Frequencies:")
    st.write(word_frequencies)

    # Calculate sentence scores
    sentence_scores = calculate_sentence_scores(sent_tokens, word_frequencies)
    
    # Display sentence scores
    st.subheader("Sentence Scores:")
    for sent, score in sentence_scores.items():
        st.write(f"Sentence: {' '.join(sent)} | Score: {score}")

    # Select top N sentences
    select_length = int(len(sent_tokens) * 0.4)  # Select top 40% sentences
    top_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    st.subheader(f"Top {select_length} Sentences:")
    for sent in top_sentences:
        st.write(f"Sentence: {' '.join(sent)} | Score: {sentence_scores[sent]}")
