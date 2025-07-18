#import necessary libraries
import streamlit as st
import os
import base64
import io
import time
from utils.pdf_processor import extract_text_from_pdf
from utils.web_scraper import extract_text_from_url
from utils.ocr import extract_text_from_image
from gtts import gTTS
from transformers import pipeline
from openai import OpenAI

# Set up OpenAI API client
# st.session_state.openai_api_key = st.text_input("OpenAI API Key:", type="password")
st.set_page_config(page_title="TextAI", layout="wide")
st.markdown("""
<style>
    .highlight { background-color: #FFF59D; transition: all 0.3s ease; }
    .text-display { min-height: 200px; border: 1px solid #ddd; padding: 15px; }
    .word-highlight {
        transition: background-color 0.3s ease;
        padding: 2px 0;
        display: inline-block;
    }
    .word-container {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 15px;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# intializing and loading the summarization models
@st.cache_resource
def load_models():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_models()

#text chunking function
def chunk_text(text, max_words=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_words]
        chunks.append(" ".join(chunk))
        i += max_words - overlap
    return chunks

# summarization function using llm
def summarize_with_llm(text, api_key=None):
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize this:\n{text}"}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            pass  # fallback to local model

    # Use chunked summarization for large text
    chunks = chunk_text(text)
    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            summaries.append(f"[Error summarizing chunk {idx+1}]")
    return " ".join(summaries)

# text to speech conversion function
def text_to_speech(text, lang='en'):
    audio_bytes = io.BytesIO()
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# input handling function cache
def input_selector():
    col1, col2 = st.columns(2)
    with col1:
        input_method = st.radio("Input Method:", ["Text", "PDF", "URL", "Image"])
    with col2:
        if input_method == "Text":
            return st.text_area("Enter Text:", height=200)
        elif input_method == "PDF":
            return extract_text_from_pdf(st.file_uploader("Upload PDF"))
        elif input_method == "URL":
            return extract_text_from_url(st.text_input("Enter URL:"))
        elif input_method == "Image":
            return extract_text_from_image(st.file_uploader("Upload Image"))

# js for syncing audio with word highlighted
def get_audio_sync_js(words):
    js_code = f"""
    <script>
    function initializeAudioSync() {{
        const words = {words};
        let audio = document.querySelector("section[data-testid='stExpander'] audio");
        
        if (!audio) {{
            // Alternative selector if the first one fails
            audio = document.querySelector("audio");
        }}
        
        if (!audio) {{
            console.log("Audio element not found");
            return;
        }}
        
        const wordElements = document.querySelectorAll(".word-highlight");
        let currentWord = 0;
        
        function updateHighlight() {{
            // Remove highlight from all words
            wordElements.forEach(el => el.style.backgroundColor = "");
            
            // Calculate current word based on audio time
            const duration = audio.duration || 1;
            const currentTime = audio.currentTime;
            const progress = Math.min(currentTime / duration, 0.999);  // Cap at 99.9%
            currentWord = Math.floor(progress * words.length);
            
            // Ensure we stay within bounds
            currentWord = Math.max(0, Math.min(currentWord, words.length - 1));
            
            // Highlight current word
            if (wordElements[currentWord]) {{
                wordElements[currentWord].style.backgroundColor = "#FFF59D";
                
                // Scroll to keep word in view
                wordElements[currentWord].scrollIntoView({{
                    behavior: "smooth",
                    block: "nearest",
                    inline: "center"
                }});
            }}
        }}
        
        function resetHighlight() {{
            wordElements.forEach(el => el.style.backgroundColor = "");
            currentWord = 0;
        }}
        
        // Clean up any existing listeners
        audio.removeEventListener("timeupdate", updateHighlight);
        audio.removeEventListener("play", updateHighlight);
        audio.removeEventListener("ended", resetHighlight);
        audio.removeEventListener("pause", resetHighlight);
        
        // Add new listeners
        audio.addEventListener("timeupdate", updateHighlight);
        audio.addEventListener("play", updateHighlight);
        audio.addEventListener("ended", resetHighlight);
        audio.addEventListener("pause", resetHighlight);
    }}
    
    // Initialize immediately and reinitialize after Streamlit updates
    initializeAudioSync();
    
    // Set up mutation observer to reinitialize when content changes
    const observer = new MutationObserver(function(mutations) {{
        if (document.querySelector(".word-highlight")) {{
            initializeAudioSync();
        }}
    }});
    
    observer.observe(document.body, {{
        childList: true,
        subtree: true
    }});
    </script>
    """
    
    return js_code

# main function
def main():
    st.title("TextAI - Smart Text Processing")

    # Input Section
    with st.expander("Input Type", expanded=True):
        raw_text = input_selector()

    if not raw_text:
        st.warning("Please provide input method to Summarize Text or Convert to Speech Mode")
        return

    # Process Section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Summarize Text"):
            with st.spinner("Generating summary..."):
                api_key = os.getenv("OPENAI_API_KEY")
                summary = summarize_with_llm(raw_text, api_key)
                st.session_state.summary = summary

    with col2:
        if st.button("🔊 Convert to Speech"):
            st.session_state.audio = text_to_speech(raw_text)
            st.session_state.words = raw_text.split()

    # Results Section
    if "summary" in st.session_state:
        with st.expander("📝 Summary Result", expanded=True):
            st.write(st.session_state.summary)
            st.download_button("Download Summary", st.session_state.summary, file_name="summary.txt")

    if "audio" in st.session_state:
        with st.expander("🎧 Speech Output", expanded=True):
            st.audio(st.session_state.audio, format="audio/mp3")
            st.download_button("Download Audio", st.session_state.audio, file_name="speech.mp3", mime="audio/mpeg")

            # Word Highlighting with Audio Sync
            if st.checkbox("Enable Word Highlighting (Sync with Audio)"):
                words = st.session_state.words
                
                # Create word elements with class for JavaScript targeting
                highlighted_text = " ".join(
                    [f'<span class="word-highlight" id="word-{i}">{word}</span>' 
                     for i, word in enumerate(words)]
                )
                
                st.markdown(f"""
                <div class="word-container">
                    {highlighted_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Inject the JavaScript for synchronization
                import json
                st.markdown(get_audio_sync_js(json.dumps(words)), unsafe_allow_html=True)

if __name__ == "__main__":
    main()