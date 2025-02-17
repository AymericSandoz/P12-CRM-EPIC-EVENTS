from services import contract_service
import click
import sentry_sdk


@click.group(name='contract')
def contract_cli():
    """Manage contracts."""
    pass


def contract_options(required=True):
    def decorator(f):
        f = click.option('--client_id', type=int, required=required,
                         help='Client ID for the contract')(f)
        f = click.option('--total_amount', type=float,
                         required=required, help='Amount of the contract')(f)
        f = click.option('--amount_due', type=float,
                         required=required, help='Amount due for the contract')(f)
        f = click.option('--commercial_contact_id', type=int, required=required,
                         help='Commercial contact ID for the contract')(f)
        f = click.option('--is_signed', type=bool, required=False,
                         help='Is the contract signed?')(f)
        return f

    return decorator


@contract_cli.command(name='get_contracts')
def get_contracts():
    """Get all contracts."""
    try:
        contracts = contract_service.get_all()
        if not contracts:
            click.echo("No contracts found.")
        else:
            click.echo(f"There are {len(contracts)} contracts")
            for contract in contracts:
                click.echo(
                    f"Contract ID: {contract.id}, Client ID: {contract.client_id},"
                    f"Total amount: {contract.total_amount}")
    except Exception:
        click.echo("An error occurred while fetching contracts.")
        sentry_sdk.capture_exception()


@contract_cli.command(name='filter_contracts')
# is flag is used to indicate that the option is a boolean flag
# so either it is present or not, it does not require a value
@click.option('--unsigned', is_flag=True, help='Filter for unsigned contracts')
@click.option('--amount_due_non_null', is_flag=True, help='Filter for contracts with non-null amount due')
def filter_contracts(unsigned, amount_due_non_null):
    """Filter contracts.
    Args:
        unsigned (bool): Filter for unsigned contracts.
        amount_due_non_null (bool): Filter for contracts with non-null amount due.
    """
    try:
        filtered_contracts = contract_service.filter_contracts(unsigned, amount_due_non_null)
        if not filtered_contracts:
            click.echo("No contracts found matching the criteria.")
        else:
            click.echo(f"There are {len(filtered_contracts)} contracts matching the criteria")
            for contract in filtered_contracts:
                click.echo(f"Contract ID: {contract.id}, Client ID: {contract.client_id}, "
                           f"Total amount: {contract.total_amount}, Amount due: {contract.amount_due}, "
                           f"Is signed: {contract.is_signed}")
    except Exception:
        click.echo("An error occurred while fetching contracts.")
        sentry_sdk.capture_exception()


@contract_cli.command(name='get_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
def get_contract(obj_id):
    """Get a contract by ID."""
    try:
        contract = contract_service.get(obj_id)
        if not contract:
            click.echo("Contract not found.")
        else:
            click.echo(f"Contract ID: {contract.id}, Client ID: {
                contract.client_id}, Total Amount: {contract.total_amount}")
    except Exception:
        click.echo(
            f"Contract ID: {contract.id}, Client ID: {contract.client_id}, Total Amount: {contract.total_amount}")


@contract_cli.command(name='create_contract')
@contract_options(required=True)
def create_contract(client_id, total_amount, amount_due, commercial_contact_id, is_signed):
    """Create a new contract."""
    try:
        contract_id, client_id = contract_service.create(
            client_id=client_id, total_amount=total_amount, amount_due=amount_due,
            commercial_contact_id=commercial_contact_id,
            is_signed=is_signed)
        click.echo(f"Contract created successfully with ID {
            contract_id} for Client ID {client_id}")
    except Exception:
        click.echo("An error occurred while creating the contract.")
        click.echo(f"Contract created successfully with ID {contract_id} for Client ID {client_id}")


@contract_cli.command(name='update_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
@contract_options(required=False)
def update_contract(obj_id, client_id, total_amount, amount_due, commercial_contact_id, is_signed):
    """Update an existing contract."""
    try:
        contract_id = contract_service.update(
            contract_id=obj_id,
            client_id=client_id,
            total_amount=total_amount,
            amount_due=amount_due,
            commercial_contact_id=commercial_contact_id,
            is_signed=is_signed
        )
        click.echo(f"Contract updated successfully with ID {contract_id}")
    except ValueError as e:
        click.echo(f"An error occurred while updating the contract: {e}")
    except Exception:
        click.echo("An error occurred while updating the contract.")
        sentry_sdk.capture_exception()


@contract_cli.command(name='delete_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
def delete_contract(obj_id):
    """Delete a contract by ID."""
    try:
        contract_id = contract_service.delete(obj_id)
        click.echo(f"Contract deleted successfully with ID {contract_id}")
    except ValueError as e:
        click.echo(f"An error occurred while deleting the contract: {e}")


contract_cli.add_command(get_contracts)
contract_cli.add_command(filter_contracts)
contract_cli.add_command(get_contract)
contract_cli.add_command(create_contract)
contract_cli.add_command(update_contract)
contract_cli.add_command(delete_contract)
