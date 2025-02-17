from services import department_service
import click
import sentry_sdk


@click.group(name='department')
def department_cli():
    """Manage departments.
    Note: Departments were created during the initial setup of the system.
    It is not possible to create, update or delete departments currently via the CLI
    since there is no reason to do so and it will have huge impact on the system.
    """
    pass


def department_options(required=False):
    def decorator(f):
        f = click.option('--name', required=required,
                         help='Name of the department')(f)
        return f
    return decorator


@department_cli.command(name='get_departments')
def get_departments():
    """Get all departments."""
    try:
        departments = department_service.get_all()
        if not departments:
            click.echo("No departments found.")
        else:
            click.echo(f"There are {len(departments)} departments")
            for department in departments:
                click.echo(f"Department ID: {
                    department.id}, Name: {department.name}")
    except Exception:
        click.echo("An error occurred while fetching departments.")
        sentry_sdk.capture_exception()


@department_cli.command(name='get_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
def get_department(obj_id):
    """Get a department by ID."""
    try:
        department = department_service.get(obj_id)
        if not department:
            click.echo("Department not found.")
        else:
            click.echo(f"Department ID: {department.id}, Name: {department.name}")
    except Exception:
        click.echo("An error occurred while fetching the department.")
        sentry_sdk.capture_exception()


@department_cli.command(name='create_department')
@department_options(required=True)
def create_department(name):
    """Create a new department.
    Should be done with caution as it will have huge impact on the system.
    Currently, no users are allowed to create a department.
    """
    try:
        department_id, department_name = department_service.create(name=name)
        click.echo(f"Department {department_name} created successfully with ID {
            department_id}")
    except ValueError as e:
        click.echo(f"An error occurred while creating the department: {e}")
    except Exception:
        click.echo("An error occurred while creating the department.")
        sentry_sdk.capture_exception()


@department_cli.command(name='update_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
@department_options(required=False)
def update_department(obj_id, name):
    """Update an existing department.
    Should be done with caution as it will have huge impact on the system.
    Currently, no users are allowed to update a department.
    """
    try:
        department_name = department_service.update(obj_id, name=name)
        click.echo(f"Department {department_name} updated successfully."
                   f"Careful, this will have huge impact on the system and should be done with caution."
                   f"Adjustement should be made in codebase to reflect the changes.")
    except ValueError as e:
        click.echo(f"An error occurred while updating the department: {e}")
    except Exception:
        click.echo("An error occurred while updating the department.")
        sentry_sdk.capture_exception()


@department_cli.command(name='delete_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
def delete_department(obj_id):
    """Delete a department by ID.
    Should be done with caution as it will have huge impact on the system.
    Currently, no users are allowed to delete a department.
    """
    try:
        department_name = department_service.delete(obj_id)
        click.echo(f"Department {department_name} deleted successfully."
                   f"Careful, this will have huge impact on the system and should be done with caution."
                   f"Adjustement should be made in codebase to reflect the changes.")
    except ValueError as e:
        click.echo(f"An error occurred while deleting the department: {e}")
    except Exception:
        click.echo("An error occurred while deleting the department.")
        sentry_sdk.capture_exception()


department_cli.add_command(get_departments)
department_cli.add_command(get_department)
department_cli.add_command(create_department)
department_cli.add_command(update_department)
department_cli.add_command(delete_department)
