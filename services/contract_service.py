from models import Contract, Session


class Contract_services():
    def create(name, start_date, end_date, client_id, amount, notes):
        session = Session()
        contract = Contract(
            contract_name=name,
            contract_start_date=start_date,
            contract_end_date=end_date,
            client_id=client_id,
            contract_amount=amount,
            notes=notes
        )
        session.add(contract)
        session.commit()
        session.close()

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
        for key, value in kwargs.items():
            setattr(contract, key, value)
        session.commit()
        session.close()
        return contract

    def delete(contract_id):
        session = Session()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        session.delete(contract)
        session.commit()
        session.close()
        return contract
