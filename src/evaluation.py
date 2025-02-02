from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
from transformers import AutoModelForCausalLM, AutoTokenizer

from query import RAG_LLM


class EvalHuggingFaceLLM(DeepEvalBaseLLM):
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=1024)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def load_model(self):
        return self.model

    def get_model_name(self):
        return self.model_name


rag_llm = RAG_LLM()
eval_llm = EvalHuggingFaceLLM(rag_llm.llm_name)

questions = ["Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"]
scores = []

metric_faithful = FaithfulnessMetric(model=eval_llm)

for question in questions:
    retrieved_texts = rag_llm.search_relevant_documents(user_query=question)[1]
    generated_answer = rag_llm.query_rag_llm(user_query=question)

    test_case = LLMTestCase(
        input=question,
        actual_output=generated_answer,
        retrieval_context=retrieved_texts
    )

    metric_faithful.measure(test_case)
    print(metric_faithful.score)
    print(metric_faithful.reason)

    scores.append((metric_faithful.score, question))
