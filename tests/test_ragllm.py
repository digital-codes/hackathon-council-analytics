import sys

sys.path.append("../src")

from ragllm import RagLlm


def test_llama_index(my_config, my_secrets):
    my_config['model']['framework'] = 'llamastack'
    rag_llm = RagLlm(config=my_config, secrets=my_secrets)
    doc_count = rag_llm.index(start_idx=367896, end_idx=368035)
    print(f"docs processed: {doc_count}")
    assert type(doc_count) == int

def test_haystack_index(my_config, my_secrets):
    my_config['model']['framework'] = 'haystack'
    rag_llm = RagLlm(config=my_config, secrets=my_secrets)
    doc_count = rag_llm.index(start_idx=367896, end_idx=368035)
    assert type(doc_count) == int


def test_llama_query(my_config, my_secrets):
    my_config['model']['framework'] = 'llamastack'
    rag_llm = RagLlm(config=my_config, secrets=my_secrets)
    query = "Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"
    answer = rag_llm.run_query(user_query=query)
    print(answer)
    assert type(answer) == str

def test_haystack_query(my_config, my_secrets):
    my_config['model']['framework'] = 'haystack'
    rag_llm = RagLlm(config=my_config, secrets=my_secrets)
    query = "Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"
    answer = rag_llm.run_query(user_query=query)
    print(answer)
    assert type(answer) == str
