from models import Client, Session


class Client_services():
    def create(name, address, city, state, zip_code, phone, email, notes):
        session = Session()
        client = Client(
            client_name=name,
            client_address=address,
            client_city=city,
            client_state=state,
            client_zip_code=zip_code,
            client_phone=phone,
            client_email=email,
            notes=notes
        )
        session.add(client)
        session.commit()
        session.close()

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
