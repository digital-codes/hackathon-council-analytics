import torch
import json
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig
from pydantic import BaseModel
from lmformatenforcer import JsonSchemaParser
from lmformatenforcer.integrations.transformers import (
    build_transformers_prefix_allowed_tokens_fn,
)

from query import RAG_LLM, huggingface_login


class EvalHuggingFaceLLM(DeepEvalBaseLLM):
    def __init__(self, model, tokenizer):
        # token = "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"
        # huggingface_login(token=token)

        self.model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        self.tokenizer = tokenizer
        self.model = model

    def generate(self, prompt: str) -> str:
        device = "cpu"

        model_inputs = self.tokenizer([prompt], return_tensors="pt").to(device)
        self.model.to(device)

        generated_ids = self.model.generate(**model_inputs, max_new_tokens=100, do_sample=True)
        return self.tokenizer.batch_decode(generated_ids)[0]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt, schema)

    def load_model(self):
        return self.model

    def get_model_name(self):  
        return self.model_name


class CustomLlama3_8B(DeepEvalBaseLLM):
    def __init__(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        model_4bit = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            device_map="auto",
            quantization_config=quantization_config,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct"
        )

        self.model = model_4bit
        self.tokenizer = tokenizer

    def load_model(self):
        return self.model

    def generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        model = self.load_model()

        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=self.tokenizer,
            use_cache=True,
            device_map="auto",
            max_length=3000,
            do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        parser = JsonSchemaParser(schema.schema())
        prefix_function = build_transformers_prefix_allowed_tokens_fn(
            pipeline.tokenizer, parser
        )

        output_dict = pipeline(prompt, prefix_allowed_tokens_fn=prefix_function)
        output = output_dict[0]["generated_text"][len(prompt) :]
        json_result = json.loads(output)

        return schema(**json_result)

    async def a_generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        return self.generate(prompt, schema)

    def get_model_name(self):
        return "Llama-3.1 8B"


def init_eval_llm(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

    eval_llm = EvalHuggingFaceLLM(model, tokenizer)
    return eval_llm



rag_llm = RAG_LLM()
eval_llm = CustomLlama3_8B()
# eval_llm = EvalHuggingFaceLLM(model=rag_llm.llm_model, tokenizer=rag_llm.tokenizer, model_name=rag_llm.llm_name)

questions = ["Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"]
scores = []

metric_faithful = FaithfulnessMetric(model=eval_llm)

for question in questions:
    retrieved_texts = rag_llm.search_relevant_documents(user_query=question)[1]
    generated_answer = rag_llm.query_rag_llm(user_query=question)
    # print(eval_llm.generate(question))

    test_case = LLMTestCase(
        input=question,
        actual_output=generated_answer,
        retrieval_context=retrieved_texts
    )

    metric_faithful.measure(test_case)
    print(metric_faithful.score)
    print(metric_faithful.reason)

    scores.append((metric_faithful.score, question))
