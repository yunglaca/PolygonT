from services.polygon_services import token_contract
from fastapi import HTTPException
from typing import List, Tuple


def get_token_balance(wallet_address: str) -> float:
    """Получение баланса ERC20 токена для кошелька через Web3."""
    try:
        balance = token_contract.functions.balanceOf(wallet_address).call()
        decimals = token_contract.functions.decimals().call()

        # Преобразуем в обычные единицы токенов
        return balance / (10**decimals)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_token_balances(wallet_addresses: List[str]) -> List[float]:
    """Получение балансов ERC20 токенов для нескольких кошельков."""
    try:
        balances = [get_token_balance(address) for address in wallet_addresses]
        return balances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_top_token_balances(N: int, all_addresses: List[str]) -> List[Tuple[str, float]]:
    """Функция для получения топ N адресов по балансу токенов."""
    try:
        balances = [get_token_balance(address) for address in all_addresses]

        # Создание списка с адресами и их балансами
        sorted_balances = sorted(
            zip(all_addresses, balances), key=lambda x: x[1], reverse=True
        )

        # Возвращаем топ N
        return sorted_balances[:N]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_last_transaction_date(wallet_address: str) -> str:
    """Получение даты последней транзакции для кошелька."""
    try:
        # Заглушка: здесь должна быть логика для получения последней транзакции
        return "No transactions found"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_top_with_transactions(
    N: int, all_addresses: List[str]
) -> List[Tuple[str, float, str]]:
    """
    Получение топ N адресов с балансами и датами последних транзакций.
    """
    try:
        top_addresses = get_top_token_balances(N, all_addresses)

        result = []
        for address, balance in top_addresses:
            last_transaction_date = get_last_transaction_date(address)
            result.append((address, balance, last_transaction_date))

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
