from services.contract_service import Contract_services


def add_contract_commands(subparsers):
    get_contract_parser = subparsers.add_parser('get_contract')
    get_contract_parser.add_argument(
        '--contract_id', type=int, required=True, help='ID of the contract')

    # client_id, total_amount, amount_due,is signed
    create_contract_parser = subparsers.add_parser('create_contract')
    create_contract_parser.add_argument(
        '--client_id', type=int, required=True, help='Client ID for the contract')
    create_contract_parser.add_argument(
        '--total_amount', type=float, required=True, help='Amount of the contract')
    create_contract_parser.add_argument(
        '--amount_due', type=float, required=True, help='Amount due for the contract')
    create_contract_parser.add_argument(
        '--is_signed', type=bool, required=False, help='Is the contract signed?')


def handle_contract_commands(args):
    if args.command == 'get_contracts':
        contracts = Contract_services.get_all()
        if not contracts:
            print("No contracts found.")
        else:
            print(f"There are {len(contracts)} contracts")
            for contract in contracts:
                print(f"Contract ID: {contract.id}, Client ID: {
                      contract.client_id}, Amount: {contract.amount}")
    elif args.command == 'get_contract':
        contract = Contract_services.get(args.contract_id)
        if not contract:
            print("Contract not found.")
        else:
            print(f"Contract ID: {contract.id}, Client ID: {
                  contract.client_id}, Amount: {contract.amount}")

    elif args.command == 'create_contract':
        contract_id, client_id = Contract_services.create(
            client_id=args.client_id, amount=args.amount)
        print(f"Contract created successfully with ID {
              contract_id} for Client ID {client_id}")
