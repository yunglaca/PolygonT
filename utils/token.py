from services.polygon_services import TOKEN_ADDRESS_CHECKSUM
from fastapi import HTTPException
from services.polygon_services import Web3, web3, ERC20_ABI


def get_token_info(token_address: str):
    try:
        # Убедимся, что адрес токена начинается с "0x"
        if not token_address.startswith("0x"):
            token_address = "0x" + token_address

        # Преобразуем адрес токена в формат checksum
        token_address_checksum = Web3.to_checksum_address(token_address)

        # Инициализация контракта токена
        token_contract = web3.eth.contract(
            address=token_address_checksum, abi=ERC20_ABI
        )

        # Получаем символ токена
        symbol = token_contract.functions.symbol().call()
        # Получаем название токена
        name = token_contract.functions.name().call()
        # Получаем общее количество токенов (total supply)
        total_supply = token_contract.functions.totalSupply().call()

        # Возвращаем информацию о токене
        return {"symbol": symbol, "name": name, "totalSupply": total_supply}

    except Exception as e:
        return {"error": f"Error fetching token info: {str(e)}"}


def get_transaction_history(
    wallet_address: str,
    from_block: int = 0,
    to_block: str = "latest",
    batch_size: int = 100,
) -> list:
    """Получение истории транзакций для указанного адреса кошелька с разбивкой по блокам."""
    try:
        if not wallet_address.startswith("0x"):
            wallet_address = "0x" + wallet_address

        wallet_address_checksum = Web3.to_checksum_address(wallet_address)

        # Получаем последний блок
        latest_block = web3.eth.block_number if to_block == "latest" else to_block

        # Подготовка к разбиению запросов по блокам
        transactions = []
        from_block_cursor = from_block

        # Разбиваем запросы по блокам
        while from_block_cursor <= latest_block:
            to_block_cursor = min(from_block_cursor + batch_size - 1, latest_block)

            try:
                # Запрос на логи (события Transfer)
                logs = web3.eth.get_logs(
                    {
                        "fromBlock": from_block_cursor,
                        "toBlock": to_block_cursor,
                        "address": TOKEN_ADDRESS_CHECKSUM,
                        "topics": [
                            web3.keccak(text="Transfer(address,address,uint256)").hex(),
                            # Хеш события Transfer
                            None,  # Фильтровать по отправителю
                            # Фильтровать по получателю (кошельку)
                            web3.to_hex(web3.to_bytes(hexstr=wallet_address)),
                        ],
                    }
                )
                # Добавляем транзакции
                transactions.extend(logs)
            except Exception as e:
                print(
                    f"Error fetching logs for blocks {from_block_cursor}-{to_block_cursor}: {str(e)}"
                )

            # Обновляем курсор блоков для следующего запроса
            from_block_cursor = to_block_cursor + 1

        # Возвращаем все найденные транзакции
        return transactions

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching transaction history: {
                str(e)}",
        )


# ps без понятия как это должно работать, так и не заработало =)
