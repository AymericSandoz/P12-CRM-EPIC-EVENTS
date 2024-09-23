from services.contract_service import Contract_services
import click


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
    contracts = Contract_services.get_all()
    if not contracts:
        click.echo("No contracts found.")
    else:
        click.echo(f"There are {len(contracts)} contracts")
        for contract in contracts:
            click.echo(f"Contract ID: {contract.id}, Client ID: {
                       contract.client_id}, Total amount: {contract.total_amount}")


@contract_cli.command(name='get_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
def get_contract(obj_id):
    """Get a contract by ID."""
    contract = Contract_services.get(obj_id)
    if not contract:
        click.echo("Contract not found.")
    else:
        click.echo(f"Contract ID: {contract.id}, Client ID: {
                   contract.client_id}, Total Amount: {contract.total_amount}")


@contract_cli.command(name='create_contract')
@contract_options(required=True)
def create_contract(client_id, total_amount, amount_due, commercial_contact_id, is_signed):
    """Create a new contract."""
    contract_id, client_id = Contract_services.create(
        client_id=client_id, total_amount=total_amount, amount_due=amount_due, commercial_contact_id=commercial_contact_id, is_signed=is_signed)
    click.echo(f"Contract created successfully with ID {
               contract_id} for Client ID {client_id}")


@contract_cli.command(name='update_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
@contract_options(required=False)
def update_contract(obj_id, client_id, total_amount, amount_due, commercial_contact_id, is_signed):
    """Update an existing contract."""
    contract_id = Contract_services.update(
        contract_id=obj_id,
        client_id=client_id,
        total_amount=total_amount,
        amount_due=amount_due,
        commercial_contact_id=commercial_contact_id,
        is_signed=is_signed
    )
    click.echo(f"Contract updated successfully with ID {contract_id}")


@contract_cli.command(name='delete_contract')
@click.option('--obj_id', type=int, required=True, help='ID of the contract')
def delete_contract(obj_id):
    """Delete a contract by ID."""
    contract_id = Contract_services.delete(obj_id)
    click.echo(f"Contract deleted successfully with ID {contract_id}")


contract_cli.add_command(get_contracts)
contract_cli.add_command(get_contract)
contract_cli.add_command(create_contract)
contract_cli.add_command(update_contract)
contract_cli.add_command(delete_contract)
