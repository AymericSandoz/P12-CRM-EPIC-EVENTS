import sys


def get_obj_id():
    """ get the object id from the command line arguments """
    if '--obj_id' in sys.argv:
        obj_id_index = sys.argv.index('--obj_id') + 1
        try:
            obj_id = sys.argv[obj_id_index]
            return obj_id
        except IndexError:
            print("No value provided for --obj_id")
    return None
