from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(max_length=50,title="name of the person",description="maa baap ka diya hua naam",examples=["nona","hulio"])]
    age:int=Field(gt=18,lt=120)
    url:AnyUrl
    email:EmailStr
    married:Optional[bool]=False
    weight:Annotated[float,Field(gt=0,strict=True)]
    height:float
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]

    @field_validator("email",mode="after")
    @classmethod
    def validator(cls,email):
        valids=["icici.com","hdfc.com"]
        if email.split("@")[-1] not in valids:
            raise ValueError("not valid email")
        return email
    @model_validator(mode="after")
    def validate_contact(cls,model):
        if model.age>60 and "emergency" not in model.contact_details:
            raise ValueError("must have emergency contact for people abvove 60")
        return model
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/self.height**2,2)



def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient1.bmi)
    print("data inserted into database")

patient_info={"name":"anish","age":20,"url":"https://www.youtube.com/watch?v=lRArylZCeOs&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&index=5","email":"a@icici.com","married":False,"weight":72,"allergies":["pollen","dust"],"contact_details":{"phone":"123434"},"height":1.75}

patient1=Patient(**patient_info)

insert_patient_data(patient1)