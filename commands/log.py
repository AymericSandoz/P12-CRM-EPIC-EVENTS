from services.auth import login as auth_login, logout as auth_logout
import click
import sentry_sdk


@click.group(name='log')
def log_cli():
    """Login and logout commands."""
    pass


def log_options(required=True):
    def decorator(f):
        f = click.option('--email', required=required,
                         help='Email of the user')(f)
        f = click.option('--password', required=required,
                         help='Password for the user')(f)
        return f
    return decorator


@log_cli.command(name='login')
@log_options(required=True)
def login_command(email, password):
    """Login to the system."""
    try:
        auth_login(email, password)
        click.echo("Logged in successfully.")
    except Exception:
        click.echo("An error occurred while logging in.")
        sentry_sdk.capture_exception()


@log_cli.command(name='logout')
def logout_command():
    """Logout from the system."""
    try:
        auth_logout()
        click.echo("Logged out successfully.")
    except Exception:
        click.echo("An error occurred while logging out.")
        sentry_sdk.capture_exception()


log_cli.add_command(login_command)
log_cli.add_command(logout_command)
