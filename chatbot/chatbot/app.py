from flask import Flask, render_template, request, jsonify,redirect
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
import os
import json

from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
app = Flask(__name__)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"


GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load initial documents
loader = TextLoader(r"enter your requirment file path")
documents = loader.load()

# Initialize embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
text_splitter = CharacterTextSplitter(
    separator="/n",
    chunk_size=1000,
    chunk_overlap=200
)
doc_chunks = text_splitter.split_documents(documents)
vectorstore = FAISS.from_documents(doc_chunks, embeddings)

# Initialize LLM and memory
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5
)
retriever = vectorstore.as_retriever()
memory = ConversationBufferMemory(
    llm=llm,
    output_key="answer",
    memory_key="chat_history",
    return_messages=True
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    chain_type="map_reduce",
    memory=memory,
    verbose=True
)

def load_json_data():
    """Load data from update.json and update the vector store."""
    try:
        with open('update.json', 'r') as f:
            json_data = json.load(f)
            # Assuming json_data is a list of text documents
            new_documents = [HumanMessage(content=item) for item in json_data]
            new_doc_chunks = text_splitter.split_documents(new_documents)
            vectorstore.add_documents(new_doc_chunks, embeddings)
            print("Vector store updated with new documents from update.json.")
    except Exception as e:
        print(f"Error loading JSON data: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # Invoke the model and get a response
    output = chain.invoke({"question": user_input})
    bot_response = output.get("answer")

    return jsonify({"response": bot_response})

@app.route('/update', methods=['POST'])
def update():
    """Endpoint to manually trigger the update from update.json."""
    load_json_data()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
