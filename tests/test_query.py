import sys
sys.path.append("..") 

from src.query import RAG_LLM


def test_query_rag_llm():
	rag_llm = RAG_LLM()

	query = "Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"
	response = rag_llm.query_rag_llm(query)

	assert type(response) == str