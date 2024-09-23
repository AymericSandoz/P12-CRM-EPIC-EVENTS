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
        session.add(client)
        session.commit()
        client_id = client.id
        session.close()
        return client_id, full_name

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

        # Filtrer les champs non nuls
        filtered_kwargs = {key: value for key,
                           value in kwargs.items() if value is not None}

        for key, value in filtered_kwargs.items():
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
