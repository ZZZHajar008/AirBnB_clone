#!/usr/bin/python3

"""

The entry point of the command interpreter

"""
import cmd
import re
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
        It will be used as blueprint for other complations
        """
        class_is_availible = False
        class_name = ""

        for cls in self.CLASSES:
            if line.startswith(f"{command} {cls}"):
                class_is_availible = True
                class_name = cls

        if class_is_availible:
            keys = storage.all().keys()
            length = len(class_name) + 1
            IDs = [i[length:] for i in keys if i.startswith(class_name)]
            completions = [arg for arg in IDs if arg.startswith(text)]
            return completions
        elif line.startswith(f"{command}"):
            return [arg for arg in self.CLASSES if arg.startswith(text)]

    def do_create(self, line):
        """Create a new instance and write it to a file"""
        if not line:
            print("** class name missing ** ")
        elif line in self.CLASSES:
            new_obj = self.types[line]()
            print(new_obj.id)
            storage.save()
        else:
            print("** class doesn't exist **")

    def complete_create(self, text, line, begidx, endidx):
        """Auto completion for craete"""
        if line.startswith("create"):
            return [arg for arg in self.CLASSES if arg.startswith(text)]

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
        elif len(args) < 2:
            print("** instance id missing **")
        elif args[0]+"."+args[1] not in storage.all().keys():
            print("** no instance found **")
        else:
            print(storage.all()[args[0]+"."+args[1]])

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
        elif args[0]+"."+args[1] not in storage.all().keys():
            print("** no instance found **")
        else:
            del storage.all()[args[0]+"."+args[1]]
            storage.save()

    def complete_destroy(self, text, line, begidx, endidx):
        """Auto completion by providing available classes and IDs"""
        return self.for_complet(text, line, "destroy")

    def do_all(self, line):
        """ Prints all string representation of all instances"""
        instances = storage.all().values()

        if line in self.CLASSES:
            all_obj = [i for i in instances if type(i).__name__ == line]
            instance_strings = [str(rep) for rep in all_obj]
            print(instance_strings)
        elif not line:
            instance_strings = [str(rep) for rep in instances]
            print(instance_strings)
        else:
            print("** class doesn't exist **")

    def complete_all(self, text, line, begidx, endidx):
        """Auto completion by providing available classes"""
        return self.for_complet(text, line, "all")

    def do_update(self, line):
        """Update the a value by its key"""
        args = line.split()

        if not line:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[0]+"."+args[1] not in storage.all().keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = storage.all()[args[0]+"."+args[1]]
            attr = args[2]
            val = args[3]
            attr_type = type(getattr(obj, attr, None))
            if attr_type.__name__ == "NoneType":
                setattr(obj, attr, val)
            else:
                setattr(obj, attr, attr_type(val))
            storage.save()

    def complete_update(self, text, line, begidx, endidx):
        """Auto completion by providing available IDs"""
        return self.for_complet(text, line, "update")

    def help_update(self):
        """THe update usage help"""
        print("Usage: update <class name> <id> py "
              "<attribute name> \"<attribute value>\""
              "\nUpdates an instance based on the class "
              "name and id by adding or updating attribute")

    def do_count(self, line):
        """Count the number of instances of a class"""
        if line in self.CLASSES:
            keys = storage.all().keys()
            available_classes = [i for i in keys if i.startswith(line)]
            print(len(available_classes))

    def parseline(self, line):
        """Handle the case of attr.command()"""
        ret = cmd.Cmd.parseline(self, line)
        cls, command = ret[0], ret[1]
        if cls in self.CLASSES and command.startswith("."):
            return self.start_with_dot_syntax(line)

        return ret

    def start_with_dot_syntax(self, line):
        ret = cmd.Cmd.parseline(self, line)
        cls, command = ret[0], ret[1]

        if command == ".all()":
            return ("all", cls, line)
        if command == ".count()":
            return ("count", cls, line)
        if command.startswith(".show("):
            occurrence = re.search(r'\("([\w-]*)"\)', line)
            if occurrence is None:
                return ("show", cls, "show ")
            else:
                input_id = occurrence.groups()[0]
                return ("show", f"{cls} {input_id}", f"show {cls} {input_id}")
        if command.startswith(".destroy("):
            occurrence = re.search(r'\("([\w-]*)"\)', line)
            if occurrence is None:
                return ("destroy", cls, "destroy ")
            else:
                input_id = occurrence.groups()[0]
                return ("destroy", f"{cls} {input_id}",
                        f"destroy {cls} {input_id}")
        if command.startswith(".update("):
            # regex = r'\("([\w-]*)", "([\w-]*)", "([\w-]*)"\)'
            regex = r'\("([\w-]*)"(, "([\w-]*)")?(, "([\w-]*)")?\)'
            occurrence = re.search(regex, line)
            if occurrence is None:
                print("here?")
                return ("update", cls, "update ")
            else:
                grps = occurrence.groups()
                grps = [el for i, el in enumerate(grps) if i % 2 == 0 and el]
                str1 = f"{cls} {' '.join(grps)}"
                str2 = f"{command} {cls} {' '.join(grps)}"
                return ("update", str1, str2)
        else:
            return ret


if __name__ == '__main__':
    HBNBCommand().cmdloop()
