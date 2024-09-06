from services.user_service import User_Services


def add_user_commands(subparsers):
    create_user_parser = subparsers.add_parser('create_user')
    create_user_parser.add_argument(
        '--employee_number', required=True, help='Employee number of the user')
    create_user_parser.add_argument(
        '--name', required=True, help='Name of the user')
    create_user_parser.add_argument(
        '--email', required=True, help='Email of the user')
    create_user_parser.add_argument(
        '--department_id', type=int, required=True, help='Department ID of the user')
    create_user_parser.add_argument(
        '--password', required=True, help='Password for the user')
    create_user_parser.add_argument(
        '--can_create_clients', action='store_true', help='Permission to create clients')
    create_user_parser.add_argument(
        '--can_modify_contracts', action='store_true', help='Permission to modify contracts')
    create_user_parser.add_argument(
        '--can_assign_events', action='store_true', help='Permission to assign events')

    get_user_parser = subparsers.add_parser('get_user')
    get_user_parser.add_argument(
        '--user_id', type=int, required=True, help='ID of the user')


def handle_user_commands(args):
    if args.command == 'create_user':
        user_id, user_name = User_Services.create(
            employee_number=args.employee_number,
            name=args.name,
            email=args.email,
            department_id=args.department_id,
            password=args.password,
            can_create_clients=args.can_create_clients,
            can_modify_contracts=args.can_modify_contracts,
            can_assign_events=args.can_assign_events
        )
        print(f"User {user_name} created successfully with ID {user_id}")
    elif args.command == 'get_users':
        users = User_Services.get_all()
        if not users:
            print("No users found.")
        else:
            print(f"There are {len(users)} users")
            for user in users:
                print(f"User ID: {user.id}, Name: {
                      user.name}, Email: {user.email}")
    elif args.command == 'get_user':
        user = User_Services.get(args.user_id)
        if not user:
            print("User not found.")
        else:
            print(f"User ID: {user.id}, Name: {
                  user.name}, Email: {user.email}")
