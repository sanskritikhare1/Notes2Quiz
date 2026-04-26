# Notes2Quiz - Quiz Generator from PDF

A Flask-based web application that generates interactive quizzes from PDF documents using AI and vector embeddings.

## Features

- 📄 Upload PDF documents
- 🤖 AI-powered quiz generation using Groq LLM
- 🔍 Vector-based semantic search using FAISS
- 💬 Conversational retrieval with LangChain
- 🎨 Interactive web interface

## Tech Stack

- **Backend**: Flask (Python)
- **AI/LLM**: Groq API (llama3-8b)
- **Vector DB**: FAISS
- **Embeddings**: HuggingFace Instructor
- **NLP**: LangChain
- **PDF Processing**: PyPDF2

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sanskritikhare1/Notes2Quiz.git
   cd Notes2Quiz
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your API keys to `.env`:
     - **HUGGINGFACE_TOKEN**: Get from https://huggingface.co/settings/tokens
     - **GROQ_API_KEY**: Get from https://console.groq.com/keys

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open in browser**:
   - Navigate to `http://localhost:5000`

## Usage

1. Upload a PDF file
2. The app extracts text from the first 3 pages
3. Creates embeddings and stores them in a vector database
4. Ask questions about the document
5. Get answers powered by the LLM

## Project Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── static/
│   ├── script.js         # Frontend JavaScript
│   └── styles.css        # Frontend styles
├── templates/
│   └── index.html        # HTML template
└── uploads/              # Uploaded PDF files (git ignored)
```

## Environment Variables

Create a `.env` file with the following:

```
HUGGINGFACE_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
```

## Security Notes

⚠️ **Never commit `.env` file to version control**

The `.gitignore` file is configured to exclude `.env` files. Always use `.env.example` as a template for setting up your environment locally.

## License

MIT

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
