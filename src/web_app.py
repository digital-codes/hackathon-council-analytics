import streamlit as st
from query import RAG_LLM
import tomllib


st.title("Council Agenda Analytics Chatbot")
st.header("Ask anything!")
user_input = st.text_input("Enter your question:")

@st.cache_resource
def load_rag_llm():

    try:
        with open("src/config.toml", "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        print("********\n"
            "Warning: You should copy the sample config file to config.toml and edit it\n"
            "using the sample file for now\n"
            "*******")
        with open("config_sample.toml", "rb") as f:
            config = tomllib.load(f)
            
    llm_name = config['model']['llm_name']
    embed_name = config['model']['embed_name']
    model_dir = config['model']['model_dir']
    index_dir = config['source']['folderEmbeddings']
    token = config['api']['hf_key']
    rag_llm = RAG_LLM(llm_name=llm_name, embed_name=embed_name, model_dir=model_dir, index_dir=index_dir, hf_token=token)
    
    return rag_llm

rag_llm = load_rag_llm()

if st.button("Get Response"):
    if user_input:
        response = rag_llm.query_rag_llm(user_input)

        # Display the response
        st.markdown("### Response from the Chatbot:")
        st.success(response)

        # Optionally, you can show chat history
        st.markdown("### Chat History:")
        st.markdown(f"**You**: {user_input}")
        st.markdown(f"**Chatbot**: {response}")
    else:
        st.error("Please enter a question!")
