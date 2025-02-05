import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP_WORDS
from spacy.lang.fr.stop_words import STOP_WORDS as FR_STOP_WORDS
from string import punctuation
from heapq import nlargest
import pandas as pd

# Main Title
st.markdown('<h1 style="color: LimeGreen;">Text Summarization with spaCy</h1>', unsafe_allow_html=True)

# Language Selection
st.markdown('<h2 style="color: #6a5acd;">Choose Language</h2>', unsafe_allow_html=True)
st.markdown('<h4 style="color: Teal;">Select the language of your text:</h4>', unsafe_allow_html=True)

# Selectbox for language selection
language = st.selectbox("", ["English", "French"])

# Assigning colors based on selection
if language == "English":
    color = "#32cd32"  # Lime Green for English
else:
    color = "#ff6347"  # Coral for French

# Display the selected language with custom color
st.markdown(f'<p style="color: {color};">You selected: {language}</p>', unsafe_allow_html=True)

# Load spaCy model based on selected language
if language == "English":
    nlp = spacy.load("en_core_web_sm")
    stopwords = list(EN_STOP_WORDS)
elif language == "French":
    nlp = spacy.load("fr_core_news_sm")
    stopwords = list(FR_STOP_WORDS)

# Input Text Section
st.markdown('<h3 style="color: #1e90ff;">Enter the Text</h3>', unsafe_allow_html=True)
input_text = st.text_area("Add your text here:", height=100, key="input_text", help="Enter your text for summarization")

if input_text:
    # Process text with spaCy
    doc = nlp(input_text)

    # Token Analysis
    st.markdown('<h3 style="color: #6a5acd;">Token Analysis</h3>', unsafe_allow_html=True)
    token_data = [(token.text, token.pos_, token.lemma_, token.shape_, token.dep_) for token in doc]
    token_df = pd.DataFrame(token_data, columns=["Token", "POS", "Lemma", "Shape", "Dependency"])
    st.write("Tokens with Part of Speech, Lemma, Shape, Dependency:")
    st.table(token_df)

    # Stopword Analysis
    st.markdown('<h3 style="color: #32cd32;">Stopword Analysis</h3>', unsafe_allow_html=True)
    st.write("List of Stopwords:")
    st.write(stopwords)

    # Word Frequency Analysis
    st.markdown('<h3 style="color: #ff6347;">Word Frequency Analysis</h3>', unsafe_allow_html=True)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1

    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    st.write("Most Common Words:")
    st.table(sorted_words[:10])

    # Summary Generation
    st.markdown('<h3 style="color: #1e90ff;">Text Summary</h3>', unsafe_allow_html=True)
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.4)  # 40% of sentences
    summary_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = " ".join([sent.text for sent in summary_sentences])

    if final_summary:
        st.write("Generated Summary:")
        st.write(final_summary)
    else:
        st.write("Not enough text to generate a summary.")
