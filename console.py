#!/usr/bin/python3

"""

The entry point of the command interpreter

"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Class implement command intrepreter"""

    prompt = "(hbnb) "
    types = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }
    CLASSES = types.keys()

    def do_EOF(self, line):
        """Ctrl + D stops the console"""
        return True

    def do_quit(self, line):
        """quit command will exit the console"""
        return True

    def emptyline(self):
        """Do nothing when getting an empty line"""
        return

    def for_complet(self, text, line, command):
        """General function for auto completion.
        It willl be used as blueprint for other complations
        """
        class_is_availible = False
        class_name = ""

        for cls in self.CLASSES:
            if line.startswith(f"{command} {cls}"):
                class_is_availible = True
                class_name = cls

        if class_is_availible:
            IDs = [i for i in storage.all().keys() if i.startswith(class_name)]
            completions = [arg for arg in IDs if arg.startswith(text)]
            return completions
        elif line.startswith(f"{command}"):
            return [arg for arg in self.CLASSES if arg.startswith(text)]

    def do_create(self, line):
        """Create a new instance and write it to a file"""
        if not line:
            print("** class name missing ** ")
        elif line in self.CLASSES:
            # new_obj = BaseModel()
            new_obj = self.types[line]()
            print(new_obj.id)
            storage.save()
        else:
            print("** class doesn't exist **")

    def complete_create(self, text, line, begidx, endidx):
        if line.startswith("create"):
            return [arg for arg in self.CLASSES if arg.startswith(text)]

    def do_ll(self, line):
        """It is overwhelming writing that long command"""
        self.do_create("BaseModel")

    def do_reset(self, line):
        """Delete all the content of the db file"""
        with open(FileStorage._FileStorage__file_path, "w") as f:
            FileStorage._FileStorage__objects = {}
            f.write("")

    def do_show(self, line):
        """String representation of an instance based on the class name"""
        args = line.split()

        if not line:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        elif args[1] not in storage.all().keys():
            print("** no instance found **")
        else:
            print(storage.all()[args[1]])

    def complete_show(self, text, line, begidx, endidx):
        """Auto completion by providing available IDs"""
        return self.for_complet(text, line, "show")

    def do_destroy(self, line):
        """String representation of an instance based on the class name"""
        args = line.split()

        if not line:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        elif args[1] not in storage.all().keys():
            print("** no instance found **")
        else:
            del storage.all()[args[1]]
            storage.save()

    def complete_destroy(self, text, line, begidx, endidx):
        """Auto completion by providing available classes and IDs"""
        return self.for_complet(text, line, "destroy")

    def do_all(self, line):
        """ Prints all string representation of all instances"""
        if not line or line in self.CLASSES:
            instances =  storage.all().values()
            instance_strings = [str(rep) for rep in instances]
            print(instance_strings)

    def do_update(self, line):
        args = line.split()

        if not line:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[1] not in storage.all().keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = storage.all()[args[1]]
            attr = args[2]
            val = args[3]
            attr_type = type(getattr(obj, attr, None))
            if attr_type is not None:
                setattr(obj, attr,attr_type(val))
            else:
                setattr(obj, attr, val)
            storage.save()

    def complete_update(self, text, line, begidx, endidx):
        """Auto completion by providing available IDs"""
        return self.for_complet(text, line, "update")

    def help_update(self):
        print("Usage: update <class name> <id> py " + \
              "<attribute name> \"<attribute value>\""
              "\nUpdates an instance based on the class "
              "name and id by adding or updating attribute")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
