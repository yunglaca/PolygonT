from fastapi import FastAPI, HTTPException, status
from typing import List, Tuple
from services.polygon_services import web3
from schemas.wallet_schemas import *
from utils.wallet import (
    get_token_balance,
    get_token_balances,
    get_top_token_balances,
    get_top_with_transactions,
)
from utils.token import get_token_info, get_transaction_history

app = FastAPI()


@app.post("/get_balance", response_model=BalanceResponse)
def get_balance(request: AddressRequest):
    checksum_address = web3.to_checksum_address(request.wallet_address)

    if not web3.is_address(checksum_address):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid wallet address"
        )

    try:
        # Получаем баланс
        balance = get_token_balance(checksum_address)
        return BalanceResponse(balance=balance)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Эндпоинт для получения балансов нескольких кошельков


@app.post("/get_balances", response_model=List[BalanceResponse])
def get_balances(request: BatchBalanceRequest):
    # Приводим все адреса в запросе к проверочному виду
    checksum_addresses = [
        web3.to_checksum_address(address) for address in request.wallet_addresses
    ]

    try:
        # Получаем балансы для всех адресов
        balances = get_token_balances(checksum_addresses)

        # Возвращаем балансы в виде списка ответов
        return [BalanceResponse(balance=balance) for balance in balances]

    except Exception as e:
        # Обрабатываем ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Эндпоинт для получения топ N адресов по балансу
@app.post("/get_top_balances", response_model=List[Tuple[str, float]])
def get_top_balances(request: TopBalancesRequest):
    # Приводим все адреса в запросе к проверочному виду
    checksum_addresses = [
        web3.to_checksum_address(address) for address in request.wallet_addresses
    ]

    try:
        # Получаем топ балансов для всех адресов
        top_balances = get_top_token_balances(request.n, checksum_addresses)

        # Возвращаем адреса и их балансы
        return [(address, balance) for address, balance in top_balances]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Эндпоинт для получения топ N адресов с балансами и последними транзакциями


@app.post("/get_top_with_transactions", response_model=List[TopBalancesWithTxsResponse])
def get_top_with_transaction(request: TopBalancesRequest):
    checksum_addresses = [
        web3.to_checksum_address(address) for address in request.wallet_addresses
    ]

    try:
        # Получаем топ N адресов с их балансами и последними транзакциями
        top_with_txs = get_top_with_transactions(request.n, checksum_addresses)

        return [
            TopBalancesWithTxsResponse(
                address=address,
                balance=balance,
                last_transaction_date=last_transaction_date,
            )
            for address, balance, last_transaction_date in top_with_txs
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/get_token_info")
def get_token_info_endpoint(request: AddressRequest):
    token_address = request.wallet_address
    return get_token_info(token_address)


@app.post("/get_transaction_history", response_model=list)
def get_transaction_history_endpoint(request: AddressRequest):
    try:
        # Получаем историю транзакций
        transactions = get_transaction_history(request.wallet_address)
        return transactions
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
