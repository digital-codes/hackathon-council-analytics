import torch
import json
import tomllib
import deepeval
import argparse
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case.llm_test_case import LLMTestCase
from deepeval.models.llms.ollama_model import OllamaModel
from deepeval.models.base_model import DeepEvalBaseLLM
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig
from pydantic import BaseModel
from lmformatenforcer import JsonSchemaParser
from lmformatenforcer.integrations.transformers import (
    build_transformers_prefix_allowed_tokens_fn,
)

import query


class EvalHuggingFaceLLM(DeepEvalBaseLLM):
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
            max_new_tokens=500,
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


def evaluate_model(config: str, secrets: str) -> None:
    
    eval_llm = OllamaModel( # EvalHuggingFaceLLM()
        model="llama3.2",
        base_url="http://localhost:11434"
    )
    questions = ["Wie viele Unterlagen des Finanzausschusses sind vorhanden und welche sind das?"]
    scores = []

    metric_faithful = FaithfulnessMetric(model=eval_llm)

    for question in questions:
        retrieved_texts = query.retrieve(config=config, secrets=secrets, user_query=question)
        generated_answer = query.query(config=config, secrets=secrets, user_query=question)

        print(f"Question: {question}")
        print(f"Retrieved text: {retrieved_texts}")
        print(f"Answer: {generated_answer}")

        test_case = LLMTestCase(
            input=question,
            actual_output=generated_answer,
            retrieval_context=retrieved_texts
        )

        metric_faithful.measure(test_case)
        print(metric_faithful.score)
        print(metric_faithful.reason)

        scores.append((metric_faithful.score, question))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', type=str, default=None, help='path to configfile')
    parser.add_argument('--secrets', '-s', type=str, default=None, help='path to secretsfile')
    parser.add_argument('--verbose', '-v', action='store_true', help='be verbose')
    parser.add_argument('--framework', '-f', type=str, choices=query.FRAMEWORKS, default=None, help='framework haystack or llamastack')
    parser.add_argument('--retriever', '-r', action='store_true', help='use only retriever')
    
    args = parser.parse_args()
    if args.secrets:
        secrets = query.read_config(args.secrets)
    else:
        secrets = query.read_config(query.DEFAULT_SECRETSFILE)
    if args.config:
        config = query.read_config(args.config)
    else:
        config = query.read_config(query.DEFAULT_CONFIGFILE)
    #set the verbose flag in config intead of passing around as parameter
    #use utils.py function vprint to print only if verbose is set
    if args.verbose:
        config['verbose'] = 1 #This allows to set verbosity levels later

    evaluate_model(config, secrets)