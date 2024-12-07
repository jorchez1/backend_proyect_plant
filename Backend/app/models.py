#models.py
from bson import ObjectId
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic_core import core_schema
from typing import Any, Dict, Annotated

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetJsonSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class UserModel(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id", default_factory=PyObjectId)]
    username: str
    email: str
    password: str
    phone: str
    role: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AnalysisModel(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id", default_factory=PyObjectId)]
    user_id: PyObjectId
    image: str
    analysis_result: str
    treatment_recommendation: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}