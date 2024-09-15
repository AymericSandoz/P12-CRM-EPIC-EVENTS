import argparse
from commands.user import add_user_commands
from commands.department import add_department_commands
from commands.event import add_event_commands
from commands.client import add_client_commands
from commands.contract import add_contract_commands
from services.auth import login, AuthenticationError
from utils.jwt_utils import load_jwt
from entities.entities import Commands


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM CLI")

    subparsers = parser.add_subparsers(dest='command')

    # Ajout de la commande login
    login_parser = subparsers.add_parser('login')
    login_parser.add_argument('--email', required=True, help='Email for login')
    login_parser.add_argument(
        '--password', required=True, help='Password for login')

    # logout command
    subparsers.add_parser('logout')

    # Token JWT
    token_parser = subparsers.add_parser('add_token')
    token_parser.add_argument('--token', required=True, help='Token JWT')

    # Ajout des commandes pour les différents objets
    add_user_commands(subparsers)
    add_department_commands(subparsers)
    add_event_commands(subparsers)
    add_client_commands(subparsers)
    add_contract_commands(subparsers)

    # Ajout d'un argument obj_id pour les objets spécifiques
    parser.add_argument('--obj_id', type=int, help="ID de l'objet")

    args = parser.parse_args()

    # login mandatory for all commands
    # if args.command not in ['login']:
    #     print("Please login first")
    #     return

    if args.command == 'logout':
        return

    elif args.command == 'login':
        try:
            token = login(args.email, args.password)
            return
        except AuthenticationError as e:
            print(f"Invalid credentials: {e}")
            return

    elif args.command == 'add_token':
        token = args.token

    else:
        token = load_jwt()

        if not token:
            print("You need to login or add a token first.")
            return

    # Vérification des permissions avant d'exécuter la commande
    # if args.command in Commands.COMMANDS_PERMISSIONS:
    #     action, obj_type = Commands.COMMANDS_PERMISSIONS[args.command]

    #     # Vérification d'un `obj_id` si nécessaire pour les objets spécifiques
    #     obj_id = args.obj_id
    #     if not check_authorization(token, action, obj_type, obj_id):
    #         print("Unauthorized access.")
    #         return

    Commands.handle_command(args)


if __name__ == "__main__":
    main()
