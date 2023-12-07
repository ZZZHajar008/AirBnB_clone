from uuid import uuid4
from datetime import datetime
from modelis.file import storage

class BaseModel:
    def __init__(self, *args, **kwargs):
        """Public instance attributes"""
        if kwargs == {}:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            storage.save(self)
        else:
            for key in kwargs.keys():
                if key in ("created_at", "updated_at"):
                    dt = datetime.strptime(kwargs[key], "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, dt)
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, kwargs[key])


    def save(self):
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        dict_clone = {**self.__dict__}
        dict_clone['created_at'] = dict_clone["created_at"].isoformat()
        dict_clone['updated_at'] = dict_clone['updated_at'].isoformat()
        dict_clone["__class__"] = __class__.__name__
        return dict_clone

    def __str__(self):
        """Friendly string representaion of object"""
        return "[{}] ({}) {}".format(__class__.__name__, self.id, self.__dict__)
        
if __name__ == "__main__":

    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))

    print("--")
    print(my_model is my_new_model)
