Overview
========

The RAG-LLM in general consists of two main components: a model for retrieval augmented generation (RAG) and a large language model (LLM). 
Both components are combined through a multi-task learning framework to generate answers to questions given a document.

A **RAG** database (DB) combines a document database with a search algorithm to retrieve the most relevant documents for a given user question.
An **embedding model** is used in order to efficiently encode documents in the database for fast search queries.
The **LLM** model together with a corresponding **tokenizer** is a neural network trained for grammatical and semantic text prediction. 

For all three components, open-source libraries are implemented and can be exchanged separately. 
The modular design allows for easy integration of new models and algorithms.

The RAG DB is created in *src/embedding.py* and has to be loaded for a search query in *src/query.py*.
New architectures or modules have to be implemented manually in both files.

Another possibility to adjust the document retrieval is the document embedding which is used to encode the documents and highlight different characteristics for the search query. The embedding model can be adjusted via a string in *src/config.toml* referring to the Hugging Face repository.

New LLMs can be easily accessed via the Hugging Face ``transformers`` library or using local models through `Òllama``. 
The LLM is loaded in *src/query.py*, but can easily be exchanged with the Hugging Face string ``llm_name``` defined in *src/config.toml*.