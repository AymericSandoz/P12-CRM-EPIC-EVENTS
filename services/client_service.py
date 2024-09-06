from models import Client, Session


class Client_services():
    def get_clients():
        session = Session()
        clients = session.query(Client).all()
        session.close()
        return clients

    def get_client(client_id):
        session = Session()
        client = session.query(Client).filter_by(id=client_id).first()
        session.close()
        return client
