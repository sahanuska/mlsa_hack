from flask import Flask, render_template, request, jsonify,redirect
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from flask_sqlalchemy import SQLAlchemy
import os
import json
from werkzeug.security import check_password_hash, generate_password_hash
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

GROQ_API_KEY = "YOUR API KEY"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load initial documents
loader = TextLoader(r"C:\Users\KIIT\Documents\GitHub\mlsa_hack\chatbot\chatbot\map_description.txt")
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
    temperature=0.9
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
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", error="Must Provide Username")
        elif not request.form.get("password"):
            return render_template("error.html", error="Must Provide Password")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("error.html", error="Invalid Username or password")

        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not username or not password or not confirm:
            return render_template("error.html", error="Enter all Feilds")
        if password != confirm:
            return render_template("error.html", error="Passwords donot Match")
        exist = db.execute("SELECT * FROM users WHERE username=?", username)
        if len(exist) != 0:
           return render_template("error.html", error="Username already exists")
        hashed = generate_password_hash(password)
        db.execute("INSERT into users (username,hash) VALUES (?,?)", username, hashed)
        user = db.execute("SELECT id FROM users WHERE username=?", username)
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    prompt = "You are a helpful bot in apocalypse your aim is to help user to navigate safaly dont put them in High-Density Areas always provide route to safe zone. user input= "  
    full_input = prompt + user_input
   
    # Invoke the model and get a response
    output = chain.invoke({"question": full_input})
    bot_response = output.get("answer")

    return jsonify({"response": bot_response})



if __name__ == '__main__':
    app.run(debug=True)
