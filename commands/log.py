from services.auth import login as auth_login, logout as auth_logout
import click


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
    auth_login(email, password)
    click.echo("Logged in successfully.")


@log_cli.command(name='logout')
def logout_command():
    """Logout from the system."""
    auth_logout()
    click.echo("Logged out successfully.")


log_cli.add_command(login_command)
log_cli.add_command(logout_command)
