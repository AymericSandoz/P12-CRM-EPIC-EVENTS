from services.event_service import Event_services


def add_event_commands(subparsers):
    get_event_parser = subparsers.add_parser('get_event')
    get_event_parser.add_argument(
        '--event_id', type=int, required=True, help='ID of the event')

    # contract_id, client_id, event_name, event_start_date, event_end_date, support_contact, location, attendees, notes
    create_event_parser = subparsers.add_parser('create_event')
    create_event_parser.add_argument(
        '--name', required=True, help='Name of the event')
    create_event_parser.add_argument(
        '--date', required=True, help='Date of the event')
    create_event_parser.add_argument(
        '--contract_id', type=int, required=True, help='Contract ID for the event')
    create_event_parser.add_argument(
        '--client_id', type=int, required=True, help='Client ID for the event')
    create_event_parser.add_argument(
        '--support_contact', required=True, help='Support contact for the event')
    create_event_parser.add_argument(
        '--location', required=True, help='Location of the event')
    create_event_parser.add_argument(
        '--attendees', type=int, required=True, help='Number of attendees')
    create_event_parser.add_argument(
        '--notes', required=False, help='Notes for the event')


def handle_event_commands(args):
    if args.command == 'get_events':
        events = Event_services.get_all()
        if not events:
            print("No events found.")
        else:
            print(f"There are {len(events)} events")
            for event in events:
                print(f"Event ID: {event.id}, Name: {
                      event.name}, Date: {event.date}")
    elif args.command == 'get_event':
        event = Event_services.get(args.event_id)
        if not event:
            print("Event not found.")
        else:
            print(f"Event ID: {event.id}, Name: {
                  event.name}, Date: {event.date}")
