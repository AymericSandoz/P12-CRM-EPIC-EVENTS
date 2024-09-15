from services.user_service import User_Services


def add_user_commands(subparsers):
    # create
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
    subparsers.add_parser('get_users')

    # get
    get_user_parser = subparsers.add_parser('get_user')
    get_user_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the user')

    # update
    update_user_parser = subparsers.add_parser('update_user')
    update_user_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the user')
    update_user_parser.add_argument(
        '--employee_number', help='Employee number of the user')
    update_user_parser.add_argument(
        '--name', help='Name of the user')
    update_user_parser.add_argument(
        '--email', help='Email of the user')
    update_user_parser.add_argument(
        '--department_id', type=int, help='Department ID of the user')

    # delete
    subparsers.add_parser('delete_user')


def handle_user_commands(args, args_dict):
    if args.command == 'create_user':
        user_id, user_name = User_Services.create(
            employee_number=args.employee_number,
            name=args.name,
            email=args.email,
            department_id=args.department_id,
            password=args.password
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
        user = User_Services.get(args.obj_id)
        if not user:
            print("User not found.")
        else:
            print(f"User ID: {user.id}, Name: {
                  user.name}, Email: {user.email}")

    elif args.command == 'update_user':
        username = User_Services.update(args.obj_id, **args_dict)
        print(f"User {username} updated successfully.")

    elif args.command == 'delete_user':
        username = User_Services.delete(args.obj_id)
        print(f"User {username} deleted successfully.")
