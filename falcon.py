import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

torch.device('mps')

FALCON_MODEL_NAME = 'tiiuae/falcon-7b-instruct'

falconTokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
falconModel = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct")

falconPipeline = pipeline(
    'text-generation',
    model = falconModel,
    tokenizer = falconTokenizer,
    batch_size = 1,
    pad_token_id = 11,
    max_new_tokens = 512,
    model_kwargs = { 
        "temperature": 0.1, 
        "max_lenght": 512,
    }
)

falconLlm = HuggingFacePipeline( pipeline = falconPipeline )


template = """
    Being a responsible text summarisation model, you always provide non toxic, positive text summarised.
    given the text content {article} I want you to create:
        1. Summary of the text content in 30 words only
"""

prompt = PromptTemplate( 
    input_variables = ["article"], 
    template = template
)

falconChain = LLMChain( llm = falconLlm, prompt = prompt);

def __getSummary(article):
    result = falconChain.run(article = article)
    return result