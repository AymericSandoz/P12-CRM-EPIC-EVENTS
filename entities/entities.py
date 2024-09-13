class Commands:
    user = ['create_user', 'get_users',
            'get_user', 'update_user', 'delete_user']
    department = ['create_department', 'get_departments',
                  'get_department', 'update_department', 'delete_department']
    event = ['create_event', 'get_events',
             'get_event', 'update_event', 'delete_event']
    client = ['create_client', 'get_clients',
              'get_client', 'update_client', 'delete_client']
    contract = ['create_contract', 'get_contracts',
                'get_contract', 'update_contract', 'delete_contract']

    COMMANDS_PERMISSIONS = {
        'create_user': ('create', 'user'),
        'get_users': ('read', 'user'),
        'get_user': ('read', 'user'),
        'update_user': ('update', 'user'),
        'delete_user': ('delete', 'user'),
        'create_department': ('create', 'department'),
        'get_departments': ('read', 'department'),
        'get_department': ('read', 'department'),
        'update_department': ('update', 'department'),
        'delete_department': ('delete', 'department'),
        'create_event': ('create', 'event'),
        'get_events': ('read', 'event'),
        'get_event': ('read', 'event'),
        'update_event': ('update', 'event'),
        'delete_event': ('delete', 'event'),
        'create_client': ('create', 'client'),
        'get_clients': ('read', 'client'),
        'get_client': ('read', 'client'),
        'update_client': ('update', 'client'),
        'delete_client': ('delete', 'client'),
        'create_contract': ('create', 'contract'),
        'get_contracts': ('read', 'contract'),
        'get_contract': ('read', 'contract'),
        'update_contract': ('update', 'contract'),
        'delete_contract': ('delete', 'contract'),
    }

    @staticmethod
    def handle_command(args):
        args_dict = {k: v for k, v in vars(args).items(
        ) if v is not None and k not in ['obj_id', 'command']}
        if args.command in Commands.user:
            from commands.user import handle_user_commands
            handle_user_commands(args, args_dict)
        elif args.command in Commands.department:
            from commands.department import handle_department_commands
            handle_department_commands(args, args_dict)
        elif args.command in Commands.event:
            from commands.event import handle_event_commands
            handle_event_commands(args, args_dict)
        elif args.command in Commands.client:
            from commands.client import handle_client_commands
            handle_client_commands(args, args_dict)
        elif args.command in Commands.contract:
            from commands.contract import handle_contract_commands
            handle_contract_commands(args, args_dict)
