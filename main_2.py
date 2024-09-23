import click
from services.auth import login, AuthenticationError
from commands.user import user_cli  # Import pour les commandes utilisateurs
from commands.department import department_cli
from commands.event import event_cli  # Import pour les commandes événements
from commands.client import client_cli  # Import pour les commandes clients
from commands.contract import contract_cli  # Import pour les commandes contrats


@click.group()
def cli():
    """Epic Events CRM CLI."""
    pass


@cli.command()
@click.argument('email')
@click.argument('password')
def login_cli(email, password):
    """Login to the system."""
    try:
        token = login(email, password)
        click.echo(f"Login successful. JWT token: {token}")
    except AuthenticationError:
        click.echo("Invalid credentials.")


@cli.command()
def logout_cli():
    """Logout from the system."""
    click.echo("Logged out.")


@cli.command()
@click.argument('token')
def add_token_cli(token):
    """Add a JWT token."""
    click.echo(f"Token added: {token}")


# Ajouter les sous-groupes de commandes pour les différentes entités
cli.add_command(client_cli)
cli.add_command(user_cli)
cli.add_command(department_cli)
cli.add_command(event_cli)
cli.add_command(contract_cli)

if __name__ == '__main__':
    cli()
