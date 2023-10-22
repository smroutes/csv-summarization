import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

torch.device('mps')
MODEL_NAME = 't5-small'

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, legacy = True)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

localPipeline = pipeline(
    'text2text-generation',
    model = model,
    tokenizer = tokenizer,
    batch_size = 1,
    model_kwargs = { 
        "temperature": 0.8, 
        "max_lenght": 100,
        "padding": True
    }
)

localLlm = HuggingFacePipeline( pipeline = localPipeline )

template = """
    Being a responsible text summarisation model, you always provide non toxic, positive text summarised.
    given the text content {article} I want you to create:
        1. Summary of the text content in 30 words only
"""

prompt = PromptTemplate( 
    input_variables = ["article"], 
    template = template
)

chain = LLMChain( llm = localLlm, prompt = prompt);

def getSummary(article):
    result = chain.run(article = article)
    return result