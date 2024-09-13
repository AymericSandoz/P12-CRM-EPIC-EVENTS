from services.client_service import Client_services


def add_client_commands(subparsers):
    # get
    subparsers.add_parser('get_clients')

    get_client_parser = subparsers.add_parser('get_client')
    get_client_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the client')


# create
    create_client_parser = subparsers.add_parser('create_client')
    create_client_parser.add_argument(
        '--full_name', required=True, help='Name of the client')
    create_client_parser.add_argument(
        '--email', required=True, help='Email of the client')
    create_client_parser.add_argument(
        '--phone', required=True, help='Phone number of the client')
    create_client_parser.add_argument(
        '--company_name', required=True, help='Company name of the client')
    create_client_parser.add_argument(
        '--last_update', help='Last contact date of the client')
    create_client_parser.add_argument(
        '--contact_person', required=True, help='Contact person of the client')

    # update
    update_client_parser = subparsers.add_parser('update_client')
    update_client_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the client')
    update_client_parser.add_argument(
        '--full_name', help='Name of the client')
    update_client_parser.add_argument(
        '--email', help='Email of the client')
    update_client_parser.add_argument(
        '--phone', help='Phone number of the client')
    update_client_parser.add_argument(
        '--company_name', help='Company name of the client')
    update_client_parser.add_argument(
        '--last_update', help='Last contact date of the client')
    update_client_parser.add_argument(
        '--contact_person', help='Contact person of the client')

    # delete
    delete_client_parser = subparsers.add_parser('delete_client')
    delete_client_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the client')


def handle_client_commands(args, args_dict):
    if args.command == 'get_clients':
        clients = Client_services.get_all()
        if not clients:
            print("No clients found.")
        else:
            print(f"There are {len(clients)} clients")
            for client in clients:
                print(f"Client ID: {client.id}, Name: {
                      client.full_name}, Email: {client.email}")
    elif args.command == 'get_client':
        client = Client_services.get(args.obj_id)
        if not client:
            print("Client not found.")
        else:
            print(f"Client ID: {client.id}, Name: {
                  client.full_name}, Email: {client.email}")

    elif args.command == 'create_client':
        client_id, client_name = Client_services.create(
            **args_dict)
        print(f"Client {client_name} created successfully with ID {client_id}")

    elif args.command == 'update_client':
        client_name = Client_services.update(args.obj_id, **args_dict)
        print(f"Client {client_name} updated successfully.")

    elif args.command == 'delete_client':
        client_name = Client_services.delete(args.obj_id)
        print(f"Client {client_name} deleted successfully.")
