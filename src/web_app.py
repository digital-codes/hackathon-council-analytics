import streamlit as st
import tomllib
import os
from query import RAG_LLM
import toml
import tomllib


config = None
st_title = "Council Agenda Analytics Chatbot"
st_header = "Ask anything!"
st_user_input = "Enter your question:"
st_get_response = "Get Response"
st_chbt_response = "### Response from the Chatbot:"
st_chbt_history = "### Chat History:"
st_history_input  = "**You**"
st_history_output = "**Chatbot**"
st_error_text = "Please enter a question!"

# TODO: set a cmdline argument for configfile
# configfile = os.path.expanduser(os.path.join('~','.config','hca','config.toml'))
configfile = os.path.expanduser(os.path.join('~','Programmieren','SASHackathon','src', 'config_sample.toml'))

try:
    with open(configfile, "rb") as f:
            config = tomllib.load(f)
except FileNotFoundError:
    pass
    # TODO: setup a cmdline Argument for verbose output
    #print("use defaults")


if config and config.get('streamlit'):
    st_title  = config['streamlit'].get('title') or st_title
    st_header = config['streamlit'].get('header') or st_header
    st_user_input = config['streamlit'].get('user_input') or st_user_input 
    st_get_response = config['streamlit'].get('get_response') or st_get_response
    st_chbt_response =  config['streamlit'].get('chbt_response') or st_chbt_response
    st_chbt_history =  config['streamlit'].get('chbt_history') or st_chbt_history
    st_history_input  = config['streamlit'].get('history_input') or st_history_input
    st_history_output = config['streamlit'].get('history_output') or st_history_output
    st_error_text = config['streamlit'].get('error_text') or st_error_text


page = st.sidebar.radio("Seite auswählen", ["Chat", "Konfiguration"])

if page == "Konfiguration":
    st.title("Konfiguration")
    
    if "frameworks" not in config:
        config["frameworks"] = {
            "filestorage": "local",
            "embed": config["model"]["embed_name"],
            "llm": config["model"]["llm_name"]
        }
    
    filestorage_options = config["frameworks"].get("filestorage")
    print(filestorage_options)
    embed_options = config["frameworks"].get("embed")
    llm_options = config["frameworks"].get("llm")
    
    selected_filestorage = st.selectbox(
        "Wähle den Filestorage-Typ",
        filestorage_options,
        index=filestorage_options.index(config["model"]["filestorage"])
    )  

    selected_embedding = st.selectbox(
        "Wähle das Embedding-Modell",
        embed_options,
        index=embed_options.index(config["model"]["embed_name"])
    )    

    selected_llm = st.selectbox(
        "Wähle das LLM-Modell",
        llm_options,
        index=llm_options.index(config["model"]["llm_name"])
    )
    
    config["model"]["filestorage"] = selected_filestorage
    config["model"]["embed_name"] = selected_embedding
    config["model"]["llm_name"] = selected_llm
    
    st.write("Aktuelle Modell-Konfiguration:", config["model"])
    
    if st.button("Konfiguration speichern"):
        with open(configfile, "w") as f:
            toml.dump(config, f)
        st.success("Konfiguration wurde aktualisiert!")
    
    st.stop()


if page == "chat":
    st.title(st_title)
    st.header(st_header)
    user_input = st.text_input(st_user_input)

    @st.cache_resource
    def load_rag_llm():
        return RAG_LLM(configfile)

    # rag_llm = load_rag_llm()

    if st.button(st_get_response):
        if user_input:
            response = "test" # rag_llm.query_rag_llm(user_input)

            st.markdown(st_chbt_response)
            st.success(response)

            st.markdown(st_chbt_history)
            st.markdown(f"{st_history_input}: {user_input}")
            st.markdown(f"{st_history_output}: {response}")
        else:
            st.error(st_error_text)
