#!/usr/bin/python3
"""the entry point of the command interpreter."""

import cmd
import shlex
import re
import ast
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def split_braces(my_another_line):
    """
     a function that split curly braces
    """

    braces = re.search(r"\{(.*?)\}", my_another_line)

    if braces:
        coma_id = shlex.split(my_another_line[:braces.span()[0]])

        my_id = [i.strip(",") for i in coma_id][0]

        data_str = braces.group(1)
        try:
            dict_line = ast.literal_eval("{" + data_str + "}")
        except Exception:
            print("** invalid dictionary format **")
            return
        return my_id, dict_line
    else:
        cmds = my_another_line.split(",")
        try:
            my_id = cmds[0]
            attribute_name = cmds[1]
            attribute_value = cmds[2]
            return f"{my_id}", f"{attribute_name} {attribute_value}"
        except Exception:
            print("** argument missing **")


class HBNBCommand(cmd.Cmd):
    """ Class for the command interpreter """

    prompt = "(hbnb) "
    super_class = ["BaseModel", "User", "Amenity",
                   "Review", "State", "City", "Place"]

    def emptyline(self):
        """
         a function that handles to do nothing
         when you press space + ENTER
        """

        pass

    def do_quit(self, line):
        """
         a function that quits
         a program
        """

        return True

    def do_EOF(self, line):
        """
         a function that quits and exit the program
        """
        print()

        return True

    def help_quit(self, line):
        """
         a function that handles
         'help'
        """

        print("Quit command to exit program")

    def do_create(self, line):
        """a function that creates inst
        """
        cmds = shlex.split(line)

        if len(cmds) == 0:
            print("** class name missing **")

        elif cmds[0] not in self.super_class:
            print("** class doesn't exist **")

        else:
            new_instance = eval(f"{cmds[0]}()")
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance.
        """

        cmds = shlex.split(line)

        if len(cmds) == 0:
            print("** class name missing **")

        elif cmds[0] not in self.super_class:
            print("** class doesn't exist **")

        elif len(cmds) < 2:
            print("** instance id missing **")

        else:
            re_objects = storage.all()

            key = "{}.{}".format(cmds[0], cmds[1])

            if key in re_objects:
                print(re_objects[key])

            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        """
        cmds = shlex.split(line)

        if len(cmds) == 0:
            print("** class name missing **")

        elif cmds[0] not in self.super_class:
            print("** class doesn't exist **")

        elif len(cmds) < 2:
            print("** instance id missing **")

        else:
            re_objects = storage.all()
            key = "{}.{}".format(cmds[0], cmds[1])

            if key in re_objects:
                del re_objects[key]
                storage.save()

            else:
                print("** instance not found **")

    def do_all(self, line):
        """Prints all string representation of all instances.
        """
        re_objects = storage.all()

        cmds = shlex.split(line)
        print(f"{cmds = }")

        if len(cmds) == 0:
            for key, value in re_objects.items():
                print(str(value))

        elif cmds[0] not in self.super_class:
            print("** class doesn't exist **")

        else:
            for key, value in re_objects.items():
                if key.split('.')[0] == cmds[0]:
                    print(str(value))

    def default(self, line):
        """Catch commands if nothing else matches then.
        """

        list_line = line.split('.')
        print(f"{list_line = }")

        my_class_name = list_line[0]
        print(f"{my_class_name = }")

        cmd = list_line[1].split('(')

        my_method = cmd[0]

        my_another_line = cmd[1].split(')')[0]

        my_method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
            }

        if my_method in my_method_dict.keys():
            if my_method != "update":
                return my_method_dict[my_method]("{} {}".format(
                    my_class_name, my_another_line))
            else:
                obj_id, dict_line = split_braces(my_another_line)
                try:
                    if isinstance(dict_line, str):
                        attributes = dict_line
                        return my_method_dict[my_method]("{} {} {}".format(
                            my_class_name,
                            obj_id,
                            attributes))
                    elif isinstance(dict_line, dict):
                        attr_dict = dict_line
                        return my_method_dict[my_method]("{} {} {}".format(
                            my_class_name, obj_id, attr_dict))
                except Exception:
                    print("** argument missing **")

        print("** Unknown syntax: {}".format(line))
        return False

    def do_count(self, line):
        """Counts the instances of a class.
        """

        re_objects = storage.all()

        cmds = shlex.split(line)

        if line:
            my_class_name = cmds[0]

        count = 0

        if cmds:
            if my_class_name in self.super_class:
                for objects in re_objects.values():
                    if objects.__class__.__name__ == my_class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.
        """
        cmds = shlex.split(line)

        if len(cmds) == 0:
            print("** class name missing **")

        elif cmds[0] not in self.super_class:
            print("** class doesn't exist **")

        elif len(cmds) < 2:
            print("** instance id missing **")

        else:
            re_objects = storage.all()

            key = "{}.{}".format(cmds[0], cmds[1])

            if key not in re_objects:
                print("** no instance found **")

            elif len(cmds) < 3:
                print("** attriute name missing **")

            elif len(cmds) < 4:
                print("** value missing **")

            else:
                objects = re_objects[key]
                braces = re.search(r"\{(.*?)\}", line)

                if braces:
                    data_str = braces.group(1)

                    dict_line = ast.literal_eval("{" + data_str + "}")
                    attr_names = list(dict_line.keys())
                    attr_values = list(dict_line.values())

                    attribute_name1 = attr_names[0]
                    attribute_value1 = attr_values[0]

                    attribute_name2 = attr_names[1]
                    attribute_value2 = attr_values[1]

                    setattr(objects, attribute_name1, attribute_value1)
                    setattr(objects, attribute_name2, attribute_value2)
                else:
                    attr_name = cmds[2]
                    attr_value = cmds[3]

                    try:
                        attr_value = eval(attr_value)

                    except Exception:
                        pass

                    setattr(objects, attr_name, attr_value)

                objects.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
