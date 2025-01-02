import pickle
import faiss
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document
from llama_index.core import Settings
import os
from tqdm import tqdm
import multiprocessing

from preprocessing import upload_to_nextcloud, download_from_nextcloud


def load_txt_files(directory):
    documents = []
    for filename in tqdm(os.listdir(directory), desc="Loading documents", unit="docs"):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                doc = Document(text=content, metadata={"filename": filename})
                documents.append(doc)
    return documents


def load_txt_files_nextcloud(start_idx, end_idx):
    documents = []
    for idx in tqdm(range(start_idx, end_idx + 1), desc="Loading documents", unit="docs"):
        filename = f"{idx}.txt"
        content = download_from_nextcloud("CouncilDocuments", filename)
        if content:
            documents.append(Document(text=content, metadata={"filename": filename}))
        else:
            print(f"Skipping {filename} due to download error.")
    return documents


def initFAISSIndex(embedding_model):

    test_embedding = embedding_model.get_text_embedding("test")
    embedding_dim = len(test_embedding) # 384
    faiss_index = faiss.IndexFlatL2(embedding_dim)
    faiss_store = FaissVectorStore(faiss_index=faiss_index) # initialize vector store

    document_metadata = {}

    return faiss_store, document_metadata


def initialize_embedding_model():
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_model = HuggingFaceEmbedding(model_name=model_name)
    print(f"Embedding model '{model_name}' initialized.")
    return embedding_model


if __name__ == "__main__":

    embedding_model = initialize_embedding_model()
    vector_store, document_metadata = initFAISSIndex(embedding_model)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # documents = load_txt_files_from_nextcloud(start_idx=200010, end_idx=200020)
    documents = load_txt_files(directory="CouncilTexts/")

    Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context, 
        embed_model=embedding_model, 
        transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)],
        show_progress=True,
    )    
    
    storage_dir = "CouncilEmbeddings/"
    index.storage_context.persist(persist_dir=storage_dir) # save the data
    # faiss.write_index(vector_store._faiss_index, os.path.join(storage_dir, "faiss_index.idx")) # save the index
    # metadata_path = os.path.join(storage_dir, "document_metadata.pkl")
    # with open(metadata_path, "wb") as f:
    #     pickle.dump(document_metadata, f)

    print(f"Vectors in FAISS index: {vector_store._faiss_index.ntotal}")
    print(f"Documents in Vector Store Index: {len(index.ref_doc_info)}")
