import sys

sys.path.append("../src")

import src.query as Query


def test_query_rag_llm(my_config, my_secrets):
    query = "Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"
    response = Query.query(config=my_config, secrets=my_secrets, user_query=query)
    assert type(response) == str


def test_retrieve(my_config, my_secrets):
    query = "Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"
    response = Query.retrieve(config=my_config, secrets=my_secrets, user_query=query)
    print(res)
    assert type(response) == str
