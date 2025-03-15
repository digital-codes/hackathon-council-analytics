import streamlit as st
import tomllib
import os
from query import RAG_LLM
import tomllib

# Define Defaults
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
configfile = os.path.expanduser(os.path.join('~','.config','hca','config.toml'))

try:
    with open(configfile, "rb") as f:
            config = tomllib.load(f)
except FileNotFoundError:
    pass
    # TODO: setup a cmdline Argument for verbose output
    #print("use defaults")


if config and config.get('streamlit'):
    # We have a configuration and will override the defaults now
    # print("found config")
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
    
    # Sicherstellen, dass der Abschnitt "preprocessor" existiert
    if "preprocessor" not in config:
        config["preprocessor"] = {"filestorage": "nextcloud", "fileformat": "txt"}
    
    # Optionen für die Dropdown-Menüs
    filestorage_options = ["nextcloud", "lokal", "s3"]
    fileformat_options = ["txt", "pdf", "docx"]
    
    # Dropdown-Menüs erstellen (Vorauswahl anhand des aktuellen Werts)
    selected_filestorage = st.selectbox(
        "Wähle den Filestorage-Typ",
        filestorage_options,
        index=filestorage_options.index(config["preprocessor"].get("filestorage", "nextcloud"))
    )
    
    selected_fileformat = st.selectbox(
        "Wähle das Dateiformat",
        fileformat_options,
        index=fileformat_options.index(config["preprocessor"].get("fileformat", "txt"))
    )
    
    # Aktualisiere die Konfiguration im Speicher
    config["preprocessor"]["filestorage"] = selected_filestorage
    config["preprocessor"]["fileformat"] = selected_fileformat
    
    st.write("Aktuelle Preprocessor-Konfiguration:", config["preprocessor"])
    
    # Button zum Speichern der aktualisierten Konfiguration
    if st.button("Konfiguration speichern"):
        with open(configfile, "w") as f:
            toml.dump(config, f)
        st.success("Konfiguration wurde aktualisiert!")
    
    # Bei der Konfigurationsseite soll der Chat-Code nicht weiter ausgeführt werden
    st.stop()


if page == "chat":
    st.title(st_title)
    st.header(st_header)
    user_input = st.text_input(st_user_input)

    @st.cache_resource
    def load_rag_llm():
        return RAG_LLM(configfile)

    rag_llm = load_rag_llm()

    if st.button(st_get_response):
        if user_input:
            response = "test" # rag_llm.query_rag_llm(user_input)

            # Display the response
            st.markdown(st_chbt_response)
            st.success(response)

            # Optionally, you can show chat history
            st.markdown(st_chbt_history)
            st.markdown(f"{st_history_input}: {user_input}")
            st.markdown(f"{st_history_output}: {response}")
        else:
            st.error(st_error_text)
