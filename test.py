from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from transformers import AutoTokenizer, AutoModelForCausalLM


# tokenizer = AutoTokenizer.from_pretrained("gpt2")
# model = AutoModelForCausalLM.from_pretrained("gpt2")

llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    batch_size = 1,
    model_kwargs={"temperature": 0.1, "max_length": 64 },
)

# pipeline = HuggingFacePipeline(tokenizer, model, kwargs={"temperature": 0, "max_length": 64})

template = """
    given the information {info}
"""

prompt = PromptTemplate(input_variables = ["info"], template = template)

chain = LLMChain( llm = llm , prompt = prompt) 

text = """
Positive
"""

result = chain.run( info = text )

print(result)