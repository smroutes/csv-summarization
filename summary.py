import os
import pandas as pd
from models.lamini import getSummary as lamminiSummary
from models.flant5base import getSummary as flant5Summary
from models.bart import getSummary as bartSummary

DATA_DIRECTORY = os.path.join(os.getcwd(), '..', 'data')
ALLOWED_MODEL = { 
    "MBZUAI/LaMini-Flan-T5-248M": lamminiSummary, 
    "Google/flan-t5-base": flant5Summary,
    "Facebook/bart-large-cnn": bartSummary
}

def generateSummary(fileName, columnName, modelName, rowCount) :
    print(f"Summary asked for {fileName} at {columnName} using {modelName}")

    file = os.path.join(DATA_DIRECTORY, fileName)
    rowCount = int(rowCount)

    if(os.path.exists(file)):
        df = pd.read_csv(file)
        capturedText = ". ".join(df.head(rowCount)[columnName])

        if modelName not in list(ALLOWED_MODEL.keys()):
            raise Exception("Invalid Model !")
        
        summary = ALLOWED_MODEL.get(modelName)(capturedText)
        return summary
    else: 
        raise Exception("Invalid file !")

def textSummary(text):
    summary = bartSummary(text)
    return summary