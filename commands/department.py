from services.department_service import Department_services
import click


@click.group(name='department')
def department_cli():
    """Manage departments."""
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
    departments = Department_services.get_all()
    if not departments:
        click.echo("No departments found.")
    else:
        click.echo(f"There are {len(departments)} departments")
        for department in departments:
            click.echo(f"Department ID: {
                       department.id}, Name: {department.name}")


@department_cli.command(name='get_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
def get_department(obj_id):
    """Get a department by ID."""
    department = Department_services.get(obj_id)
    if not department:
        click.echo("Department not found.")
    else:
        click.echo(f"Department ID: {department.id}, Name: {department.name}")


@department_cli.command(name='create_department')
@department_options(required=True)
def create_department(name):
    """Create a new department."""
    department_id, department_name = Department_services.create(name=name)
    click.echo(f"Department {department_name} created successfully with ID {
               department_id}")


@department_cli.command(name='update_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
@department_options(required=False)
def update_department(obj_id, name):
    """Update an existing department."""
    department_name = Department_services.update(obj_id, name=name)
    click.echo(f"Department {department_name} updated successfully.")


@department_cli.command(name='delete_department')
@click.option('--obj_id', type=int, required=True, help='ID of the department')
def delete_department(obj_id):
    """Delete a department by ID."""
    department_name = Department_services.delete(obj_id)
    click.echo(f"Department {department_name} deleted successfully.")


department_cli.add_command(get_departments)
department_cli.add_command(get_department)
department_cli.add_command(create_department)
department_cli.add_command(update_department)
department_cli.add_command(delete_department)
