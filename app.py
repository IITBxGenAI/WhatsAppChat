import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader, UnstructuredHTMLLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.memory import ConversationBufferMemory
import sys

# Compatibility Settings for ChromaDB
import sqlite3

# Disable telemetry
os.environ['CHROMA_TELEMETRY'] = 'FALSE'
os.environ['ANONYMIZED_TELEMETRY'] = 'FALSE'


# Function to load documents into the VectorDB
def load_docs_to_db(docs_dir, persist_directory) -> Chroma:
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=50)
    documents = []

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                loader = UnstructuredMarkdownLoader(file_path)
                documents.extend(loader.load_and_split(text_splitter=text_splitter))
            elif file.endswith('.txt'):
                file_path = os.path.join(root, file)
                loader = UnstructuredMarkdownLoader(file_path)
                documents.extend(loader.load_and_split(text_splitter=text_splitter))
            elif file.endswith('.html'):
                file_path = os.path.join(root, file)
                loader = UnstructuredHTMLLoader(file_path)
                documents.extend(loader.load_and_split(text_splitter=text_splitter))

    vectordb = Chroma.from_documents(documents=documents, embedding=embedding_function, persist_directory=persist_directory)
    return vectordb


# Function to get the VectorDB
def get_vector_db(verbose=False) -> Chroma:
    docs_dir = './data/'
    persist_directory = './chroma/'
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load or initialize the vector database
    if 'vectordb' not in st.session_state:
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
            print("Creating directory and loading docs into VectorDB")
            st.session_state.vectordb = load_docs_to_db(docs_dir, persist_directory)
        else:
            st.session_state.vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
            vectordb_has_subfolders = any(os.path.isdir(os.path.join(persist_directory, entry)) for entry in os.listdir(persist_directory))

            if not vectordb_has_subfolders:
                print("Loading docs into VectorDB")
                st.session_state.vectordb = load_docs_to_db(docs_dir, persist_directory)

    if verbose:
        print("***\n")
        print("VectorDB Collection Count: ")
        print(st.session_state.vectordb._collection.count())
        print("***\n")

    return st.session_state.vectordb


# Function to create the QA system
def create_qa_system(memory):
    vectordb = get_vector_db(verbose=True)

    template = """[INST] Given the following context, answer the question.
    Context: <context>{context}</context>
    Question: <question>{question}</question>
    Note: <Note>Fetch all the context information and answer thoroughly and detailed. Answer everything about the question</Note>[/INST]"""
    
    pt = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    rag = RetrievalQA.from_chain_type(
        llm=Ollama(model="llama3"),
        retriever=vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
        memory=memory,
        chain_type_kwargs={"prompt": pt, "verbose": False},
    )

    return rag


def initialize_qa_system():
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(max_memory_size=3)
    if 'rag' not in st.session_state:
        st.session_state.rag = create_qa_system(st.session_state.memory)
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

def qa_chatbot(question):
    if question.lower() == 'exit':
        return "Exiting the chat. Goodbye!"

    # Get the answer
    answer = st.session_state.rag.invoke(question)['result']

    # Update chat history with the latest exchange
    st.session_state['chat_history'].append({"question": question, "answer": answer})

    # Save the context in the conversation memory
    st.session_state.memory.save_context({"input": question}, {"output": answer})

    if len(st.session_state['chat_history']) > 50:  # Keep only the last 50 messages
        st.session_state['chat_history'] = st.session_state['chat_history'][-50:]

    return answer


def render_ui():
    st.title('Local RAG UI')
    st.write("Ask questions and get answers from MLIR Docs.")

    # Centered text input for user question at the top
    question = st.text_input("Ask a question:", key="user_input", placeholder="Type your question here...")

    # Centered submit button below the input
    if st.button('Ask Anything', key="ask_button"):
        if question:
            answer = qa_chatbot(question)
            st.rerun()  # Refresh to update the chat history and focus on the new answer

    # Display the latest answer
    if st.session_state['chat_history']:
        latest_exchange = st.session_state['chat_history'][-1]
        st.subheader("Latest Answer")
        st.info(f"**User:** {latest_exchange['question']}\n\n**Bot:** {latest_exchange['answer']}")

    # Display chat history below the latest answer
    st.subheader("Chat History")
    for exchange in reversed(st.session_state['chat_history'][:-1]):  # Display all but the latest exchange, in reverse order
        st.markdown(f"**User:** {exchange['question']}")
        st.markdown(f"**Bot:** {exchange['answer']}")
        st.divider()


def main():
    initialize_qa_system()
    render_ui()


if __name__ == '__main__':
    main()



