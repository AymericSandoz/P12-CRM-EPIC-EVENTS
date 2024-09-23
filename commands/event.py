from services.event_service import Event_services
import click


@click.group(name='event')
def event_cli():
    """Manage events."""
    pass


def event_options(required=True):
    def decorator(func):
        func = click.option('--event_name', required=required,
                            help='Name of the event')(func)
        func = click.option('--event_start_date', required=required,
                            help='Start date of the event')(func)
        func = click.option('--event_end_date', required=required,
                            help='End date of the event')(func)
        func = click.option('--client_id', type=int, required=required,
                            help='Client ID for the event')(func)
        func = click.option('--contract_id', type=int, required=required,
                            help='Contract ID for the event')(func)
        func = click.option('--support_contact', required=required,
                            help='Support contact for the event')(func)
        func = click.option('--location', required=required,
                            help='Location of the event')(func)
        func = click.option('--attendees', type=int, required=required,
                            help='Number of attendees')(func)
        func = click.option('--notes', required=False,
                            help='Notes for the event')(func)
        return func
    return decorator


@click.command(name='get_events')
def get_events():
    """Get all events."""
    events = Event_services.get_all()
    if not events:
        click.echo("No events found.")
    else:
        click.echo(f"There are {len(events)} events")
        for event in events:
            click.echo(f"Event ID: {event.id}, Name: {
                       event.event_name}, Date: {event.event_start_date}")


@click.command(name='get_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
def get_event(obj_id):
    """Get an event by ID."""
    event = Event_services.get(obj_id)
    if not event:
        click.echo("Event not found.")
    else:
        click.echo(f"Event ID: {event.id}, Name: {
                   event.event_name}, Date: {event.event_start_date}")


@click.command(name='create_event')
@event_options(required=True)
def create_event(event_name, event_start_date, event_end_date, client_id, contract_id, support_contact, location, attendees, notes):
    """Create a new event."""
    event_id, event_name = Event_services.create(
        event_name=event_name, event_start_date=event_start_date, event_end_date=event_end_date, client_id=client_id, contract_id=contract_id, support_contact=support_contact, location=location, attendees=attendees, notes=notes)
    click.echo(
        f"Event {event_name} created successfully with ID {event_id}")


@click.command(name='update_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
@event_options(required=False)
def update_event(obj_id, event_name, event_start_date, event_end_date, client_id, contract_id, support_contact, location, attendees, notes):
    """Update an existing event."""
    event_name = Event_services.update(
        obj_id, event_name=event_name, event_start_date=event_start_date, event_end_date=event_end_date, client_id=client_id, contract_id=contract_id, support_contact=support_contact, location=location, attendees=attendees, notes=notes)
    click.echo(f"Event {event_name} updated successfully.")


@click.command(name='delete_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
def delete_event(obj_id):
    """Delete an event by ID."""
    event_name = Event_services.delete(obj_id)
    click.echo(f"Event {event_name} deleted successfully.")


event_cli.add_command(get_events)
event_cli.add_command(get_event)
event_cli.add_command(create_event)
event_cli.add_command(update_event)
event_cli.add_command(delete_event)
