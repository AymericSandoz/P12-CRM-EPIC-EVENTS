from services.department_service import Department_services


def add_department_commands(subparsers):
    create_department_parser = subparsers.add_parser('create_department')
    create_department_parser.add_argument(
        '--name', required=True, help='Name of the department')

    get_department_parser = subparsers.add_parser('get_department')
    get_department_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the department')

    subparsers.add_parser('get_departments')

    update_department_parser = subparsers.add_parser('update_department')
    update_department_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the department')
    update_department_parser.add_argument(
        '--name', help='Name of the department')

    delete_department_parser = subparsers.add_parser('delete_department')
    delete_department_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the department')


def handle_department_commands(args):
    if args.command == 'create_department':
        department_id, department_name = Department_services.create(
            name=args.name)
        print(f"Department {department_name} created successfully with ID {
              department_id}")
    elif args.command == 'get_departments':
        departments = Department_services.get_all()
        if not departments:
            print("No departments found.")
        else:
            print(f"There are {len(departments)} departments")
            for department in departments:
                print(f"Department ID: {
                      department.id}, Name: {department.name}")
    elif args.command == 'get_department':
        department = Department_services.get(args.department_id)
        if not department:
            print("Department not found.")
        else:
            print(f"Department ID: {department.id}, Name: {department.name}")

    elif args.command == 'update_department':
        # convertir avec vars mais enlever les valeurs nulles, obj id et command
        args_dict = {k: v for k, v in vars(args).items(
        ) if v is not None and k not in ['obj_id', 'command']}
        department_name = Department_services.update(
            obj_id=args.obj_id,
            **args_dict
        )
        print(f"Department {department_name} updated successfully with ID {
              department_id}")

    elif args.command == 'delete_department':
        department_name = Department_services.delete(args.obj_id)
        print(f"Department {department_name} deleted successfully")
