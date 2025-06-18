from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=["P001"])]
    name:Annotated[str,Field(...,description="name of the patient")]
    city:Annotated[str,Field(...,description="city of the person")]
    age:Annotated[int,Field(...,gt=0,lt=120)]
    gender:Annotated[Literal['Male','Female','other'],Field(...)]
    height:Annotated[float,Field(...,gt=0,description="in meters")]
    weight:Annotated[float,Field(...,gt=0,description="in kgs")]


    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/self.height**2,2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi<18.5): return "Underweight"
        elif(self.bmi<25): return "Normal"
        elif(self.bmi<30): return "Overweight"
        else: return "Obese"

class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=120)]
    gender:Annotated[Optional[Literal['Male','Female']],Field(default="other")]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]





app=FastAPI()

def load_data():
    with open("patients.json","r") as f :
        data=json.load(f)
    return data

def save_data(data):
    with open("patients.json","w") as f :
        json.dump(data,f)
    


@app.get("/")
def hello():
    return {"message":"patient management system api"}

@app.get("/about")
def about():
    return {"message":"fully functional api to manage patients records"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patients/{id}")#path params
def view_patient(id:str=Path(...,description="id of the patient")):
    data=load_data()
    if id in data:
        return data[id]
    raise HTTPException(status_code=404,detail="patient not found")


@app.get("/sort")#query params
def sort_patients(sort_by:str=Query(...,description="sort on the basis of weight,height or bmi"),
                  order:str=Query("asc",description="arrange in ascending or descending order")):
    valid_fields=["height","weight","bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"choose from {valid_fields}")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail=f"choose from asc and desc")
    
    sort_order=True if order=="desc" else False

    data=load_data()
    sorted_data=sorted(data.values(),key=lambda x : x.get(sort_by,0),reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="this patient already exits")
    data[patient.id]=patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201,content="patient ctreated succesfully")

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient does not exist")
    
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for k,v in updated_patient_info.items():
        existing_patient_info[k]=v
    
    existing_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id]=existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200,content="patient updated")
    



 