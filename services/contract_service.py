from models import Contract, Session


def get_contracts():
    session = Session()
    contract = session.query(Contract).all()
    session.close()
    return contract


def get_contract(contract_id):
    session = Session()
    contract = session.query(Contract).filter_by(id=contract_id).first()
    session.close()
    return contract
