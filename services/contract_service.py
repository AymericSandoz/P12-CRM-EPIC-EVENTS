from models import Contract, Session
from sentry.log import log_action


class Contract_services():
    def create(client_id, total_amount, amount_due, commercial_contact_id, is_signed=False):
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
        session = Session()
        contracts = session.query(Contract).all()
        session.close()
        return contracts

    def get(contract_id):
        session = Session()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        session.close()
        return contract

    def update(contract_id, **kwargs):
        session = Session()
        contract = session.query(Contract).filter_by(id=contract_id).first()

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
        session = Session()
        contract = session.query(Contract).filter_by(id=contract_id).first()
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
