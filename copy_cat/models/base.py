from pydantic import BaseModel


class BaseDesign(BaseModel):

    class Config:
        use_enum_values = True
        orm_mode = True


class BaseError(BaseModel):

    class Config:
        use_enum_values = True


class BaseValidationCondition(BaseModel):

    class Config:
        use_enum_values = True
        orm_mode = True
