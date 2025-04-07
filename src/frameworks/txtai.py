from txtai import Embeddings
from preprocessor import Preprocessor
from typing import Optional
from utils import vprint

"""
https://github.com/neuml/txtai/blob/master/examples/01_Introducing_txtai.ipynb
"""

#Defaults
llm_model_name = "google/flan-t5-large"
embedding_model_name = "sentence-transformers/nli-mpnet-base-v2"


class Embedor:

    #TODO: Floating Window

    def __init__(self, config: dict, secrets: dict) -> None:
        self.config = config
        self.pp = Preprocessor(config,secrets)
        self.fs = self.pp.fs
        self.embedding_model_name = config.get('embedding', {}).get('txtai', {}).get('embedding_model_name') or embedding_model_name
        self.embedding = Embeddings(path=self.embedding_model_name)


    def embed(self,  start_idx: Optional[int] = None, end_idx: Optional[int] = None) -> None:
        """
        embedding function
        to be called by admin.py
        params:
        - start_idx
        - end_idx
        #ToDo: preprocessed documents, update    
        """
        documents = self.fs.get_documents(start_idx=start_idx,end_idx=end_idx)
        count = self.embed_and_index_documents(documents)
        return count


class Query:
    """
    query the Model
    txtai is an all-in-one embeddings database. It is the only vector database that also supports sparse indexes, graph networks and relational databases with inline SQL support. In addition to this, txtai has support for LLM orchestration.

The RAG pipeline is txtai's spin on retrieval augmented generation (RAG). This pipeline extracts knowledge from content by joining a prompt, context data store and generative model together.
    """

    def __init__(self, config: dict, secrets: dict) -> None:
        self.config = config
        self.embedding_model_name = config.get('embedding', {}).get('txtai', {}).get('embedding_model_name') or embedding_model_name
        self.embedding =  Embeddings(path=self.embedding_model_name, content=True)


    def prompt(self, question):
        return [{"query": question,
            "question": f"""
Answer the following question using the context below.
Question: {question}
Context:
"""
}]    

    def query_rag_llm(self, user_query: str) -> str:
        """
        Query function to be called by webApp
        params:
        - user_query
        """
        rag = RAG(embeddings,
                  "google/flan-t5-large",
                  torch_dtype=torch.bfloat16,
                  output="reference")
        ans = rag(prompt(user_query))[0]
        return ans
