from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    age:int
    address:Address

address_dict={"city":"burla","state":"odisha","pin":"768017"}
address1=Address(**address_dict)

patient_dict={"name":"man","age":22,"address":address1}
patient1=Patient(**patient_dict)

temp_dict=patient1.model_dump()
temp_json=patient1.model_dump_json()

print(temp_dict)
print(temp_json)
