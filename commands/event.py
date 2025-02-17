from services import event_service
import click
import sentry_sdk


@click.group(name='event')
def event_cli():
    """Manage events."""
    pass


def event_options(required=True):
    def decorator(func):
        func = click.option('--event_name', required=required,
                            help='Name of the event')(func)
        func = click.option('--event_start_date', required=False,
                            help='Start date of the event')(func)
        func = click.option('--event_end_date', required=False,
                            help='End date of the event')(func)
        func = click.option('--client_id', type=int, required=required,
                            help='Client ID for the event')(func)
        func = click.option('--contract_id', type=int, required=required,
                            help='Contract ID for the event')(func)
        func = click.option('--location', required=False,
                            help='Location of the event')(func)
        func = click.option('--attendees', type=int, required=False,
                            help='Number of attendees')(func)
        func = click.option('--notes', required=False,
                            help='Notes for the event')(func)
        return func
    return decorator


@click.command(name='get_events')
def get_events():
    """Get all events."""
    try:
        events = event_service.get_all()
        if not events:
            click.echo("No events found.")
        else:
            click.echo(f"There are {len(events)} events")
            for event in events:
                click.echo(f"Event ID: {event.id}, Name: {
                    event.event_name}, Date: {event.event_start_date}")
    except Exception:
        click.echo("An error occurred while fetching events.")
        sentry_sdk.capture_exception()


@click.command(name='get_incomplete_events')
@click.option('--fields', multiple=True, help='Fields to check for incompleteness')
def get_incomplete_events(fields):
    """Get events with incomplete data."""
    try:
        fields = list(fields) if fields else None
        events = event_service.get_incomplete_events(fields)
        if not events:
            click.echo("No incomplete events found.")
        else:
            click.echo(f"There are {len(events)} incomplete events")
            for event in events:
                click.echo(f"Event ID: {event.id}, Name: {event.event_name}, Date: {event.event_start_date}")
    except Exception:
        click.echo("An error occurred while fetching incomplete events.")
        sentry_sdk.capture_exception()


@click.command(name='filter_own_events')
def filter_own_events():
    """ Get all user events(only for support department)"""
    try:
        events = event_service.filter_own_events()
        if not events:
            click.echo("No events found.")
        else:
            click.echo(f"There are {len(events)} events")
            for event in events:
                click.echo(f"Event ID: {event.id}, Name: {
                    event.event_name}, Date: {event.event_start_date}")
    except Exception:
        click.echo("An error occurred while fetching events.")
        sentry_sdk.capture_exception()


@click.command(name='get_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
def get_event(obj_id):
    """Get an event by ID."""
    try:
        event = event_service.get(obj_id)
        if not event:
            click.echo("Event not found.")
        else:
            click.echo(f"Event ID: {event.id}, Name: {
                event.event_name}, Date: {event.event_start_date}")
    except Exception:
        click.echo("An error occurred while fetching the event.")
        sentry_sdk.capture_exception()


@click.command(name='create_event')
@event_options(required=True)
def create_event(event_name, event_start_date, event_end_date, client_id, contract_id,
                 location, attendees, notes):
    """Create a new event."""
    try:
        event_id, event_name = event_service.create(
            event_name=event_name, event_start_date=event_start_date, event_end_date=event_end_date,
            client_id=client_id,
            contract_id=contract_id, location=location, attendees=attendees, notes=notes)
        click.echo(
            f"Event {event_name} created successfully with ID {event_id}")
    except ValueError as e:
        click.echo(f"An error occurred while creating the event: {e}")
    except Exception:
        click.echo("An error occurred while creating the event.")
        sentry_sdk.capture_exception()


@click.command(name='update_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
@event_options(required=False)
def update_event(obj_id, event_name, event_start_date, event_end_date, client_id, contract_id, location,
                 attendees, notes):
    """Update an existing event."""
    try:
        event_name = event_service.update(
            obj_id, event_name=event_name, event_start_date=event_start_date, event_end_date=event_end_date,
            client_id=client_id, contract_id=contract_id,
            location=location, attendees=attendees, notes=notes)
        click.echo(f"Event {event_name} updated successfully.")
    except ValueError as e:
        click.echo(f"An error occurred while updating the event: {e}")
    except Exception:
        click.echo("An error occurred while updating the event.")
        sentry_sdk.capture_exception()


@click.command(name='assign_support_contact')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
@click.option('--support_contact', required=True, help='Support contact for the event')
def assign_support_contact(obj_id, support_contact):
    """Assign a support contact to an event."""
    try:
        event_name = event_service.assign_support_contact(obj_id, support_contact)
        click.echo(f"Support contact assigned to event {event_name}.")
    except ValueError as e:
        click.echo(f"An error occurred while assigning the support contact: {e}")
    except Exception:
        click.echo("An error occurred while assigning the support contact.")
        sentry_sdk.capture_exception()


@click.command(name='delete_event')
@click.option('--obj_id', type=int, required=True, help='ID of the event')
def delete_event(obj_id):
    """Delete an event by ID."""
    try:
        event_name = event_service.delete(obj_id)
        click.echo(f"Event {event_name} deleted successfully.")
    except ValueError as e:
        click.echo(f"An error occurred while deleting the event: {e}")
    except Exception:
        click.echo("An error occurred while deleting the event.")
        sentry_sdk.capture_exception()


event_cli.add_command(get_events)
event_cli.add_command(get_incomplete_events)
event_cli.add_command(filter_own_events)
event_cli.add_command(get_event)
event_cli.add_command(create_event)
event_cli.add_command(update_event)
event_cli.add_command(assign_support_contact)
event_cli.add_command(delete_event)
