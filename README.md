# TextAI - Smart Text Processing 

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FF4B4B?style=for-the-badge&logo=huggingface&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-38B2AC?style=for-the-badge&logo=natural-language-processing&logoColor=white)

##  Why I Built This
As a CS graduate exploring AI, I created TextAI to:
- **Learn** NLP/audio processing hands-on
- Solve my **personal need**: Listen to long articles/texts locally on my laptop
- Avoid cloud dependencies for privacy-sensitive content

##  Features
- **Multi-Input Support**: Extract text from PDFs, URLs, and images (OCR)
- **AI Summarization**: 
  - Cloud: GPT-3.5 Turbo (OpenAI API)
  - Local: BART model (offline fallback)
- **Text-to-Speech**: Convert text to audio with adjustable speed
- **Real-Time Sync**: Word-by-word highlighting during playback

##  Challenges Faced
1. **API Limitations**: 
   - OpenAI rate limits → Implemented local model fallback
2. **Large Text Processing**: 
   - Memory issues → Solved with 300-word chunking
3. **Audio-Text Sync**: 
   - Timing discrepancies → Used dynamic delay calculation

##  Get Started  
- Install dependencies: `pip install -r requirements.txt`  
- Run the app: `streamlit run app.py`  
- *No API keys needed for local mode*  

##  How to Contribute  

### Focus Areas & Future Enhancements  
**Immediate Improvements Needed**  
- Improve handwritten text OCR accuracy  
- Enhance audio-text synchronization  
- Add EPUB file support  

**Planned Features**  
- Chrome extension for web article capture  
- Whisper integration for voice commands  
- Batch processing for multiple files  
- Domain-specific fine-tuned models  

### Submission Process  
1. Create a new feature branch  
2. Make your changes  
3. Run formatting checks  
4. Push your branch  
5. Open a pull request with:  
   - Change description  
   - Visual proof if applicable  

### Code Principles  
- Prioritize local processing  
- Use type annotations  
- Include tests for new features






