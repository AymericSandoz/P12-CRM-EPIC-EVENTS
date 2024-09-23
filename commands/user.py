from services.user_service import User_Services
import click

# def add_user_commands(subparsers):
#     # create
#     create_user_parser = subparsers.add_parser('create_user')
#     create_user_parser.add_argument(
#         '--employee_number', required=True, help='Employee number of the user')
#     create_user_parser.add_argument(
#         '--name', required=True, help='Name of the user')
#     create_user_parser.add_argument(
#         '--email', required=True, help='Email of the user')
#     create_user_parser.add_argument(
#         '--department_id', type=int, required=True, help='Department ID of the user')
#     create_user_parser.add_argument(
#         '--password', required=True, help='Password for the user')
#     subparsers.add_parser('get_users')

#     # get
#     get_user_parser = subparsers.add_parser('get_user')
#     get_user_parser.add_argument(
#         '--obj_id', type=int, required=True, help='ID of the user')

#     # update
#     update_user_parser = subparsers.add_parser('update_user')
#     update_user_parser.add_argument(
#         '--obj_id', type=int, required=True, help='ID of the user')
#     update_user_parser.add_argument(
#         '--employee_number', help='Employee number of the user')
#     update_user_parser.add_argument(
#         '--name', help='Name of the user')
#     update_user_parser.add_argument(
#         '--email', help='Email of the user')
#     update_user_parser.add_argument(
#         '--department_id', type=int, help='Department ID of the user')

#     # delete
#     subparsers.add_parser('delete_user')


# def handle_user_commands(args, args_dict):
#     if args.command == 'create_user':
#         user_id, user_name = User_Services.create(
#             employee_number=args.employee_number,
#             name=args.name,
#             email=args.email,
#             department_id=args.department_id,
#             password=args.password
#         )
#         print(f"User {user_name} created successfully with ID {user_id}")
#     elif args.command == 'get_users':
#         users = User_Services.get_all()
#         if not users:
#             print("No users found.")
#         else:
#             print(f"There are {len(users)} users")
#             for user in users:
#                 print(f"User ID: {user.id}, Name: {
#                       user.name}, Email: {user.email}")
#     elif args.command == 'get_user':
#         user = User_Services.get(args.obj_id)
#         if not user:
#             print("User not found.")
#         else:
#             print(f"User ID: {user.id}, Name: {
#                   user.name}, Email: {user.email}")

#     elif args.command == 'update_user':
#         username = User_Services.update(args.obj_id, **args_dict)
#         print(f"User {username} updated successfully.")

#     elif args.command == 'delete_user':
#         username = User_Services.delete(args.obj_id)
#         print(f"User {username} deleted successfully.")

@click.group(name='user')
def user_cli():
    """User commands."""
    pass


def user_options(required=True):
    """User options."""
    def decorator(func):
        func = click.option('--employee_number', required=required,
                            help='Employee number of the user')(func)
        func = click.option('--name', required=required,
                            help='Name of the user')(func)
        func = click.option('--email', required=required,
                            help='Email of the user')(func)
        func = click.option('--department_id', type=int,
                            required=required, help='Department ID of the user')(func)
        func = click.option('--password', required=required,
                            help='Password for the user')(func)
        return func
    return decorator


@click.command(name='get_users')
def get_users():
    """Get all users."""
    users = User_Services.get_all()
    if not users:
        click.echo("No users found.")
    else:
        click.echo(f"There are {len(users)} users")
        for user in users:
            click.echo(f"User ID: {user.id}, Name: {
                       user.name}, Email: {user.email}")


@click.command(name='get_user')
@click.option('--obj_id', type=int, required=True, help='ID of the user')
def get_user(obj_id):
    """Get a user by ID."""
    user = User_Services.get(obj_id)
    if not user:
        click.echo("User not found.")
    else:
        click.echo(f"User ID: {user.id}, Name: {
                   user.name}, Email: {user.email}")


@click.command(name='create_user')
@user_options(required=True)
def create_user(employee_number, name, email, department_id, password):
    """Create a new user."""
    user_id, user_name = User_Services.create(
        employee_number=employee_number, name=name, email=email, department_id=department_id, password=password)
    click.echo(
        f"User {user_name} created successfully with ID {user_id}")


@click.command(name='update_user')
@click.option('--obj_id', type=int, required=True, help='ID of the user')
@user_options(required=False)
def update_user(obj_id, employee_number, name, email, department_id, password):
    """Update an existing user."""
    user_name = User_Services.update(
        user_id=obj_id, employee_number=employee_number, name=name, email=email, department_id=department_id, password=password)
    click.echo(f"User {user_name} updated successfully.")


@click.command(name='delete_user')
@click.option('--obj_id', type=int, required=True, help='ID of the user')
def delete_user(obj_id):
    """Delete a user."""
    user_name = User_Services.delete(obj_id)
    click.echo(f"User {user_name} deleted successfully.")


user_cli.add_command(get_users)
user_cli.add_command(get_user)
user_cli.add_command(create_user)
user_cli.add_command(update_user)
user_cli.add_command(delete_user)
