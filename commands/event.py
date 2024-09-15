from services.event_service import Event_services


def add_event_commands(subparsers):
    get_event_parser = subparsers.add_parser('get_event')
    get_event_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the event')

    subparsers.add_parser('get_events')

    # contract_id, client_id, event_name, event_start_date, event_end_date, support_contact, location, attendees, notes
    create_event_parser = subparsers.add_parser('create_event')
    create_event_parser.add_argument(
        '--name', required=True, help='Name of the event')
    create_event_parser.add_argument(
        '--event_start_date', required=True, help='Start date of the event')
    create_event_parser.add_argument(
        '--event_end_date', required=True, help='End date of the event')
    create_event_parser.add_argument(
        '--client_id', type=int, required=True, help='Client ID for the event')

    create_event_parser.add_argument(
        '--contract_id', type=int, required=True, help='Contract ID for the event')
    create_event_parser.add_argument(
        '--support_contact', required=True, help='Support contact for the event')
    create_event_parser.add_argument(
        '--location', required=True, help='Location of the event')
    create_event_parser.add_argument(
        '--attendees', type=int, required=True, help='Number of attendees')
    create_event_parser.add_argument(
        '--notes', required=False, help='Notes for the event')

    update_event_parser = subparsers.add_parser('update_event')
    update_event_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the event')
    update_event_parser.add_argument(
        '--name', help='Name of the event')
    update_event_parser.add_argument(
        '--date', help='Date of the event')
    update_event_parser.add_argument(
        '--contract_id', type=int, help='Contract ID for the event')
    update_event_parser.add_argument(
        '--client_id', type=int, help='Client ID for the event')
    update_event_parser.add_argument(
        '--support_contact', help='Support contact for the event')

    update_event_parser.add_argument(
        '--location', help='Location of the event')

    update_event_parser.add_argument(
        '--attendees', type=int, help='Number of attendees')

    update_event_parser.add_argument(
        '--notes', help='Notes for the event')

    delete_event_parser = subparsers.add_parser('delete_event')
    delete_event_parser.add_argument(
        '--obj_id', type=int, required=True, help='ID of the event')


def handle_event_commands(args, args_dict):
    if args.command == 'get_events':
        events = Event_services.get_all()
        if not events:
            print("No events found.")
        else:
            print(f"There are {len(events)} events")
            for event in events:
                print(f"Event ID: {event.id}, Name: {
                      event.event_name}, Date: {event.event_start_date}")
    elif args.command == 'get_event':
        event = Event_services.get(args.obj_id)
        if not event:
            print("Event not found.")
        else:
            print(f"Event ID: {event.id}, Name: {
                  event.event_name}, Date: {event.event_start_date}")

    elif args.command == 'create_event':
        event_id, event_name = Event_services.create(**args_dict
                                                     )
        print(f"Event {event_name} created successfully with ID {event_id}")

    elif args.command == 'update_event':
        event_name = Event_services.update(args.obj_id, **args_dict)
        print(f"Event {event_name} updated successfully")

    elif args.command == 'delete_event':
        event_name = Event_services.delete(args.obj_id)
        print(f"Event {event_name} deleted successfully")
