from pydantic import BaseModel, Field


class Thresholds(BaseModel):
    context_precision: float = Field(default=0.7, ge=0, le=1)
    context_recall: float = Field(default=0.7, ge=0, le=1)
    faithfulness: float = Field(default=0.8, ge=0, le=1)
    answer_relevancy: float = Field(default=0.7, ge=0, le=1)
    answer_correctness: float = Field(default=0.7, ge=0, le=1)


THRESHOLDS = Thresholds()
