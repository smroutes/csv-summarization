import torch
import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain

torch.device('mps')

MODEL_NAME = 't5-small'
CSV_FILE = 'feedback.csv'

# import the csv file
df = pd.read_csv(CSV_FILE)

print(f"\n--- Total record found %d ---\n" % (len(df)))

columnsList = [
    'What was the most valuable thing you learned from this session?',
    'What other topics related to this topic would you like to see covered in future sessions?'
]
feedbackText = ". ".join(df["What could be improved about this session?"])
relevantColumns = df[columnsList].apply(lambda x: ' - '.join(x.dropna().astype(str)), axis = 1)


combinedText = ". ".join(relevantColumns + ". " + feedbackText)


# Try differnet inputs
randomText = """
Attempting to prepare for every possibility, which is now a part of its ethos, the Indian Space Research Organisation (ISRO) will carry out an abort test for the human space mission, Gaganyaan, today. 
A similar fail-safe approach had been taken for Chandrayaan-3 and had helped ISRO script history by making India the first country to land nearer the south pole of the Moon in August. The stakes, though, are much higher this time because the lives of humans will be involved.

Gaganyaan's crew module escape system will be live tested from Sriharikota. This is the first of the 20 big tests that ISRO has planned for the near future. All in an effort to meet Prime Minister Narendra Modi's target that ISRO sets up an Indian Space Station by 2035 and launch Indian astronaut to the Moon by 2040.
"""


# Lets define the model and tokenizer 
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

localPipeline = pipeline(
    'summarization',
    model = model,
    tokenizer = tokenizer,
    max_lenght = 100,
    batch_size = 1,
    model_kwargs = { "temperature": 0.8 }
)


localLlm = HuggingFacePipeline( pipeline = localPipeline )

def generate_summary(text):
    inputIds = tokenizer.encode(
        f"Summarize: %s" % (text), 
        return_tensors= "pt",
        max_length = 512,
        truncation = True,
        padding = True
    )

    summary_ids = model.generate(
        inputIds,
        max_length = 100,
        num_beams = 4, 
        no_repeat_ngram_size = 2, 
        early_stopping = True
    )

    summary = tokenizer.decode (
        summary_ids[0],
        skip_special_tokens = True
    )

    return summary

summary = generate_summary(combinedText)

print("\n ------------ \n")
print(summary)
print("\n ------------ \n")
