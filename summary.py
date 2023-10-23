import os
import pandas as pd
from lamini import getSummary as lamminiSummary
from flant5base import getSummary as flant5Summary

DATA_DIRECTORY = os.path.join(os.getcwd(), '..', 'data')
ALLOWED_MODEL = { 
    "lamini": lamminiSummary, 
    "flant5base": flant5Summary
}

def generateSummary(fileName, columnName, modelName) :
    print(f"Summary asked for {fileName} at {columnName} using {modelName}")

    file = os.path.join(DATA_DIRECTORY, fileName)

    if(os.path.exists(file)):
        df = pd.read_csv(file)
        capturedText = ". ".join(df.head(50)[columnName])

        if modelName not in list(ALLOWED_MODEL.keys()):
            raise Exception("Invalid Model !")
        
        summary = ALLOWED_MODEL.get(modelName)(capturedText)
        return summary
    else: 
        raise Exception("Invalid file !")