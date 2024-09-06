import argparse
from commands.user import add_user_commands, handle_user_commands
from commands.department import add_department_commands, handle_department_commands
from commands.event import add_event_commands, handle_event_commands
from commands.client import add_client_commands, handle_client_commands
from commands.contract import add_contract_commands, handle_contract_commands


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM CLI")
    subparsers = parser.add_subparsers(dest='command')

    add_user_commands(subparsers)
    add_department_commands(subparsers)
    add_event_commands(subparsers)
    add_client_commands(subparsers)
    add_contract_commands(subparsers)

    args = parser.parse_args()

    if args.command in ['create_user', 'get_users', 'get_user']:
        handle_user_commands(args)
    elif args.command in ['create_department', 'get_departments', 'get_department']:
        handle_department_commands(args)
    elif args.command in ['get_events', 'get_event']:
        handle_event_commands(args)
    elif args.command in ['get_clients', 'get_client']:
        handle_client_commands(args)
    elif args.command in ['get_contracts', 'get_contract']:
        handle_contract_commands(args)


if __name__ == "__main__":
    main()
