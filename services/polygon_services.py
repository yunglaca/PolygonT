from web3 import Web3

# Публичный RPC для Polygon
polygon_rpc = "https://polygon-rpc.com/"
web3 = Web3(Web3.HTTPProvider(polygon_rpc))

# Проверка подключения к сети Polygon
if not web3.is_connected():
    raise Exception("Failed to connect to Polygon RPC Gateway")

# Адрес токена (ERC20)
TOKEN_ADDRESS = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"
TOKEN_ADDRESS_CHECKSUM = Web3.to_checksum_address(TOKEN_ADDRESS)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    # добавьте другие функции, которые могут быть полезны
]

# Инициализация контракта токена
token_contract = web3.eth.contract(address=TOKEN_ADDRESS_CHECKSUM, abi=ERC20_ABI)

# Проверка валидности адреса кошелька
wallet_address = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"  # Пример адреса
try:
    wallet_address_checksum = Web3.to_checksum_address(wallet_address)
    print("Checksum address:", wallet_address_checksum)
except Exception as e:
    print(f"Error: {str(e)}")
    wallet_address_checksum = None

if wallet_address_checksum and web3.is_address(wallet_address_checksum):
    print("Valid wallet address")
else:
    print("Invalid wallet address")
