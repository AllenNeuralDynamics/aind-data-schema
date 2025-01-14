from typing import Annotated, List, Union
from pydantic import BaseModel, Field


class TypeA(BaseModel):
    item_type: str = "TypeA"
    value: int


class TypeB(BaseModel):
    item_type: str = "TypeB"
    value: str


class TypeC(BaseModel):
    item_type: str = "TypeC"
    value: float


class MyModel(BaseModel):
    items: List[Annotated[Union[TypeA, TypeB, TypeC], Field(discriminator="item_type")]]


# Example usage:
data = MyModel(items=[TypeA(value=42), TypeB(value="string"), TypeC(value=3.14)])
print(data)

# Example: Providing only a subset
data_subset = MyModel(items=[TypeA(value=42), TypeC(value=3.14)])
print(data_subset)
