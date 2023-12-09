#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

objs = storage.all()
print("-- Reload objects --")
for obj_id in objs.keys():
    obj = objs[obj_id]
    print(obj)

print("-- Create a new object --")
my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
my_model.save()
print(my_model)   