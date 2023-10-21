from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class SummarizeJson(BaseModel) :
    summary: str = Field(description = "Sumamry of the text content")

    def to_dict(self):
        return {
            "summary": self.summary
        }
    
SummarizeJsonParser = PydanticOutputParser(
    pydantic_object = SummarizeJson
)