from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
from langchain.text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
from huggingface_hub import login
import os
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HUGGINGFACE_TOKEN or not GROQ_API_KEY:
    raise ValueError("Please set HUGGINGFACE_TOKEN and GROQ_API_KEY environment variables")

login(HUGGINGFACE_TOKEN)

app = Flask(__name__)

# Extract text from the first 3 pages of the PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for i, page in enumerate(reader.pages[:3]):
        content = page.extract_text()
        if content:
            text += content
    return text.strip().replace("\n", " ")

# Split text into chunks for embeddings
def split_text_chunks(text):
    splitter = CharacterTextSplitter(separator="\n", chunk_size=300, chunk_overlap=30, length_function=len)
    return splitter.split_text(text)[:5]

# Create FAISS vector store
def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="hkunlp/instructor-base",  # ✅ changed
        model_kwargs={"device": "cpu"}
    )
    return FAISS.from_texts(chunks, embedding=embeddings)



# Create LangChain conversation chain
def create_chain(vectorstore):
    llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY, temperature=0.5)
    memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)

# Generate quiz using vector store and LLM
def generate_quiz_from_pdf(file_path, prompt):
    try:
        text = extract_text_from_pdf(file_path)
        chunks = split_text_chunks(text)
        vectorstore = create_vectorstore(chunks)
        chain = create_chain(vectorstore)
        final_prompt = (
            "Generate a quiz based on the following instructions. "
            "Do NOT include any answers. Just output clear questions.\n\n" + prompt
        )
        return chain.run(final_prompt)
    except Exception as e:
        print("🔥 ERROR:", e)  # <--- Add this
        return f"❌ Error: {str(e)}"


# Serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# Handle PDF and prompt POST request
@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files or 'prompt' not in request.form:
        return jsonify({'error': 'PDF and prompt are required'}), 400

    pdf = request.files['pdf']
    prompt = request.form['prompt']

    # Save the PDF temporarily
    os.makedirs("uploads", exist_ok=True)
    filename = f"temp_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join("uploads", filename)
    pdf.save(filepath)

    # Generate the quiz
    quiz = generate_quiz_from_pdf(filepath, prompt)

    # Delete the file after processing
    try:
        os.remove(filepath)
    except Exception as e:
        print("Warning: Failed to delete file:", e)

    return jsonify({'quiz': quiz})

if __name__ == '__main__':
    app.run(debug=True)
