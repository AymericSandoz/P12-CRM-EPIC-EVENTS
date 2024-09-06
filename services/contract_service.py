from models import Contract, Session


class Contract_services():
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
