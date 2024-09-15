import click
from services.client_service import Client_services


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
    clients = Client_services.get_all()
    if not clients:
        click.echo("No clients found.")
    else:
        click.echo(f"There are {len(clients)} clients")
        for client in clients:
            click.echo(f"Client ID: {client.id}, Name: {
                       client.full_name}, Email: {client.email}")


@click.command(name='get_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
def get_client(obj_id):
    """Get a client by ID."""
    client = Client_services.get(obj_id)
    if not client:
        click.echo("Client not found.")
    else:
        click.echo(f"Client ID: {client.id}, Name: {
                   client.full_name}, Email: {client.email}")


@click.command(name='create_client')
@client_options(required=True)
def create_client(full_name, email, phone, company_name, last_update, contact_person):
    """Create a new client."""
    client_id, client_name = Client_services.create(
        full_name=full_name, email=email, phone=phone, company_name=company_name, last_update=last_update, contact_person=contact_person)
    click.echo(
        f"Client {client_name} created successfully with ID {client_id}")


@click.command(name='update_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
@client_options(required=False)
def update_client(obj_id, full_name, email, phone, company_name, last_update, contact_person):
    """Update an existing client."""
    client_name = Client_services.update(
        client_id=obj_id, full_name=full_name, email=email, phone=phone, company_name=company_name, last_update=last_update, contact_person=contact_person)
    click.echo(f"Client {client_name} updated successfully.")


@click.command(name='delete_client')
@click.option('--obj_id', type=int, required=True, help='ID of the client')
def delete_client(obj_id):
    """Delete a client by ID."""
    client_name = Client_services.delete(obj_id)
    click.echo(f"Client {client_name} deleted successfully.")


# Ajout des commandes au groupe
client_cli.add_command(get_clients)
client_cli.add_command(get_client)
client_cli.add_command(create_client)
client_cli.add_command(update_client)
client_cli.add_command(delete_client)
