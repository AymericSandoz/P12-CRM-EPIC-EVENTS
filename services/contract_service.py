from models import Contract, Session
from sentry.log import log_action
from sqlalchemy import false


def create(client_id, total_amount, amount_due, commercial_contact_id, is_signed=False):
    """Create a new contract.
    Args:
        client_id (int): The id of the client.
        total_amount (float): The total amount of the contract.
        amount_due (float): The amount due for the contract.
        commercial_contact_id (int): The id of the commercial contact.
        is_signed (bool): Whether the contract is signed or not.
    """
    session = Session()
    contract = Contract(
        client_id=client_id,
        total_amount=total_amount,
        amount_due=amount_due,
        commercial_contact_id=commercial_contact_id,
        is_signed=is_signed
    )

    session.add(contract)
    session.commit()

    contract_id = contract.id
    contract_info = {
        'client_id': contract.client_id,
        'total_amount': contract.total_amount,
        'amount_due': contract.amount_due,
        'commercial_contact_id': contract.commercial_contact_id,
        'is_signed': contract.is_signed
    }

    session.close()

    # Log the action
    log_action('create', 'contract', obj_id=contract_id,
               extra_info=contract_info)

    return contract_id, client_id


def get_all():
    """Get all contracts."""
    session = Session()
    contracts = session.query(Contract).all()
    session.close()
    return contracts


def get(contract_id):
    """Get a contract by id.
    Args:
        contract_id (int): The id of the contract to get.
    """
    session = Session()
    contract = session.query(Contract).filter_by(id=contract_id).first()
    session.close()
    return contract


def filter_contracts(unsigned, amount_due_non_null):
    """Filter contracts.
    Args:
        unsigned (bool): Whether the contract is signed or not.
        amount_due_non_null (bool): Whether the amount due is not null.
    """
    session = Session()
    query = session.query(Contract)
    if amount_due_non_null:
        query = query.filter(Contract.amount_due > 0)
    if unsigned:
        query = query.filter(Contract.is_signed.is_(false()))
    contracts = query.all()
    session.close()
    return contracts


def update(contract_id, **kwargs):
    """Update a contract.
    Args:
        contract_id (int): The id of the contract to update.
        **kwargs: The fields to update.
    """
    session = Session()
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        raise ValueError("Contract not found")
    filtered_kwargs = {key: value for key,
                       value in kwargs.items() if value is not None}
    for key, value in filtered_kwargs.items():
        setattr(contract, key, value)
    session.commit()
    session.close()

    # Log the action
    log_action('update', 'contract', obj_id=contract_id,
               extra_info=filtered_kwargs)

    return contract_id


def delete(contract_id):
    """Delete a contract.
    Args:
        contract_id (int): The id of the contract to delete.
    """
    session = Session()
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        raise ValueError("Contract not found")
    contract_info = {
        'client_id': contract.client_id,
        'total_amount': contract.total_amount,
        'amount_due': contract.amount_due,
        'commercial_contact_id': contract.commercial_contact_id,
        'is_signed': contract.is_signed
    }
    session.delete(contract)
    session.commit()
    session.close()

    # Log the action
    log_action('delete', 'contract', obj_id=contract_id,
               extra_info=contract_info)

    return contract_id
