import click
from commands.user import user_cli  # Import pour les commandes utilisateurs
from commands.department import department_cli
from commands.event import event_cli  # Import pour les commandes événements
from commands.client import client_cli  # Import pour les commandes clients
from commands.contract import contract_cli  # Import pour les commandes contrats
from commands.log import log_cli
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from config import SENTRY_DSN
from services.auth import check_authorization


@click.group()
def cli():
    ctx = click.get_current_context()
    if 'log' != ctx.invoked_subcommand:
        if not check_authorization():
            exit()
    """Epic Events CRM CLI."""
    pass


cli.add_command(log_cli)
cli.add_command(client_cli)
cli.add_command(user_cli)
cli.add_command(department_cli)
cli.add_command(event_cli)
cli.add_command(contract_cli)

if __name__ == '__main__':

    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        integrations=[sentry_logging],
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

    # token = load_jwt()
    # if not token:
    #     print("No JWT token found. Please log in.")
    #     exit()

    # action, type = Commands.COMMANDS_PERMISSIONS.get()
    # if not check_authorization(token, action, type):
    #     exit()

    cli()
