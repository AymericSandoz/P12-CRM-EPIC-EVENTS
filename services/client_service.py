from models import Client, Session


class Client_services():
    def create(full_name, email, phone, company_name, last_update, contact_person):
        session = Session()
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            last_update=last_update,
            contact_person=contact_person
        )
        client_id = client.id
        client_name = client.full_name
        session.add(client)
        session.commit()
        session.close()
        return client_id, client_name

    def get_all():
        session = Session()
        clients = session.query(Client).all()
        session.close()
        return clients

    def get(client_id):
        session = Session()
        client = session.query(Client).filter_by(id=client_id).first()
        session.close()
        return client

    def update(client_id, **kwargs):
        session = Session()
        client = session.query(Client).filter_by(id=client_id).first()
        for key, value in kwargs.items():
            setattr(client, key, value)
        client_name = client.full_name
        session.commit()
        session.close()
        return client_name

    def delete(client_id):
        session = Session()
        client = session.query(Client).filter_by(id=client_id).first()
        client_name = client.full_name
        session.delete(client)
        session.commit()
        session.close()
        return client_name
