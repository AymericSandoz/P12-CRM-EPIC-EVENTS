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


def get_contract_id():
    """ get the contract id from the command line arguments """
    if '--contract_id' in sys.argv:
        contract_id_index = sys.argv.index('--contract_id') + 1
        try:
            contract_id = sys.argv[contract_id_index]
            return contract_id
        except IndexError:
            print("No value provided for --contract_id")
    return None
