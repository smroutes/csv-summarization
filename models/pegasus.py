import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

torch.device('mps')
MODEL_NAME = 'google/pegasus-xsum'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

localPipeline = pipeline(
    'summarization',
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
    {article}
"""

prompt = PromptTemplate( 
    input_variables = ["article"], 
    template = template
)

chain = LLMChain( llm = localLlm, prompt = prompt);

def getSummary(article):
    result = chain.run(article = article)
    return result