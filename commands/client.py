import click
from services import client_service
import sentry_sdk


@click.group(name='client')
def client_cli():
    """Commands for managing clients."""
    pass


def client_options(required=True):
    """Decorator to add common client options to a command."""
    def decorator(func):
        func = click.option('--full_name', required=required,
                            help='Name of the client')(func)
        func = click.option('--email', required=required,
                            help='Email of the client')(func)
        func = click.option('--phone', required=required,
                            help='Phone number of the client')(func)
        func = click.option('--company_name', required=required,
                            help='Company name of the client')(func)
        func = click.option('--last_update', required=False,
                            help='Last contact date of the client')(func)
        func = click.option('--contact_person', required=required,
                            help='Contact person of the client')(func)
        return func
    return decorator


@click.command(name='get_clients')
def get_clients():
    """Get all clients."""
    try:
        clients = client_service.get_all()
        if not clients:
            click.echo("No clients found.")
        else:
            click.echo(f"There are {len(clients)} clients")
            for client in clients:
                click.echo(f"Client ID: {client.id}, Name: {
                    client.full_name}, Email: {client.email}")

    except Exception as e:
        click.echo("An unexpected error occurred")
        sentry_sdk.capture_exception(e)


@click.command(name='get_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
def get_client(obj_id):
    """Get a client by ID."""
    try:
        client = client_service.get(obj_id)
        if not client:
            click.echo("Client not found.")
        else:
            click.echo(f"Client ID: {client.id}, Name: {
                client.full_name}, Email: {client.email}")
    except Exception:
        click.echo("An unexpected error occurred")
        sentry_sdk.capture_exception()


@click.command(name='create_client')
@client_options(required=True)
def create_client(full_name, email, phone, company_name, last_update, contact_person):
    """Create a new client."""
    try:
        client_id, client_name = client_service.create(
            full_name=full_name, email=email, phone=phone, company_name=company_name, last_update=last_update,
            contact_person=contact_person)
        click.echo(
            f"Client {client_name} created successfully with ID {client_id}")
    except ValueError as e:
        click.echo(f"Erreur lors de la création du client: {e}")
    except Exception:
        click.echo("An unexpected error occurred")
        sentry_sdk.capture_exception()


@click.command(name='update_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
@client_options(required=False)
def update_client(obj_id, full_name, email, phone, company_name, last_update, contact_person):
    """Update an existing client."""
    try:
        client_name = client_service.update(
            client_id=obj_id, full_name=full_name, email=email, phone=phone, company_name=company_name,
            last_update=last_update, contact_person=contact_person)
        click.echo(f"Client {client_name} updated successfully.")
    except ValueError as e:
        click.echo(f"Erreur lors de la mise à jour du client: {e}")
    except Exception:
        click.echo("An unexpected error occurred")
        sentry_sdk.capture_exception()


@click.command(name='delete_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
def delete_client(obj_id):
    """Delete a client by ID."""
    try:
        client_name = client_service.delete(obj_id)
        click.echo(f"Client {client_name} deleted successfully.")
    except ValueError as e:
        click.echo(f"Erreur lors de la suppression du client: {e}")
    except Exception:
        click.echo("An unexpected error occurred")
        sentry_sdk.capture_exception()


# Ajout des commandes au groupe
client_cli.add_command(get_clients)
client_cli.add_command(get_client)
client_cli.add_command(create_client)
client_cli.add_command(update_client)
client_cli.add_command(delete_client)
