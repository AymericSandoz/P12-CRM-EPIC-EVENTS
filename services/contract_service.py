from models import Contract, Session


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
        client_id = contract.client_id

        session.close()
        return contract_id, client_id

    def get_all():
        session = Session()
        contract = session.query(Contract).all()
        session.close()
        return contract

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
        return contract_id

    def delete(contract_id):
        session = Session()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        session.delete(contract)
        session.commit()
        session.close()
        return contract_id
