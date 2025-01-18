import pickle
import faiss
import os
from tqdm import tqdm
import multiprocessing

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document
from llama_index.core import Settings

from preprocessing import upload_to_nextcloud, download_from_nextcloud


def load_existing_index(storage_dir):
    """Load the existing FAISS index and document metadata."""
    faiss_index_path = os.path.join(storage_dir, "faiss_index.idx")
    if os.path.exists(faiss_index_path):
        faiss_index = faiss.read_index(faiss_index_path)
        print(f"Loaded FAISS index with {faiss_index.ntotal} vectors.")
    else:
        faiss_index = None
        print("No existing FAISS index found. Creating a new one.")
    
    # Load document metadata if exists
    metadata_path = os.path.join(storage_dir, "document_metadata.pkl")
    if os.path.exists(metadata_path):
        with open(metadata_path, "rb") as f:
            document_metadata = pickle.load(f)
        print(f"Loaded metadata for {len(document_metadata)} documents.")
    else:
        document_metadata = {}
        print("No existing document metadata found. Starting fresh.")

    return faiss_index, document_metadata


def save_index_and_metadata(faiss_index, document_metadata, storage_dir):
    """Save the FAISS index and document metadata."""
    faiss.write_index(faiss_index, os.path.join(storage_dir, "faiss_index.idx"))
    metadata_path = os.path.join(storage_dir, "document_metadata.pkl")
    with open(metadata_path, "wb") as f:
        pickle.dump(document_metadata, f)
    print(f"Saved FAISS index and metadata for {len(document_metadata)} documents.")


def load_txt_files(directory, processed_filenames):
    """Load new text files from the directory that have not been processed yet."""
    documents = []
    for filename in tqdm(os.listdir(directory), desc="Loading new documents", unit="docs"):
        if filename.endswith(".txt") and filename not in processed_filenames:
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                doc = Document(text=content, metadata={"filename": filename})
                documents.append(doc)
    return documents


def init_vector_store(embedding_model, faiss_index=None):
    """Initialize or load the FaissVectorStore."""
    if faiss_index is None:
        test_embedding = embedding_model.get_text_embedding("test")
        embedding_dim = len(test_embedding)  # 384
        faiss_index = faiss.IndexFlatL2(embedding_dim)
        print("Created a new FAISS index.")
    faiss_store = FaissVectorStore(faiss_index=faiss_index)  # Initialize vector store
    return faiss_store


def initialize_embedding_model():
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_model = HuggingFaceEmbedding(model_name=model_name)
    print("Embedding model initialized.")
    return embedding_model


if __name__ == "__main__":

    storage_dir = "vectorstore_index"
    
    # Initialize embedding model
    embedding_model = initialize_embedding_model()

    # Load existing FAISS index and metadata
    faiss_index, document_metadata = load_existing_index(storage_dir)

    # Initialize vector store (reuse the existing FAISS index if available)
    vector_store = init_vector_store(embedding_model, faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load only new documents
    new_documents = load_txt_files(directory="CouncilDocuments", processed_filenames=document_metadata.keys())

    if new_documents:
        # Configure text splitter for chunking
        Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

        # Embed and add new documents to the FAISS index
        index = VectorStoreIndex.from_documents(
            new_documents,
            storage_context=storage_context,
            embed_model=embedding_model,
            transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)],
            show_progress=True,
        )

        # Update document metadata
        for doc in new_documents:
            document_metadata[doc.metadata["filename"]] = doc.metadata

        # Save the updated FAISS index and metadata
        save_index_and_metadata(vector_store._faiss_index, document_metadata, storage_dir)

        print(f"Added {len(new_documents)} new documents to the index.")
    else:
        print("No new documents found.")
    
    print(f"Total vectors in FAISS index: {vector_store._faiss_index.ntotal}")
    print(f"Total documents in metadata: {len(document_metadata)}")
