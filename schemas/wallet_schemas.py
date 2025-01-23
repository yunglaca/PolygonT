from pydantic import BaseModel, Field


class AddressRequest(BaseModel):
    wallet_address: str = Field(
        default="0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0",
        description="Адрес токена")


class BalanceResponse(BaseModel):
    balance: float


class BatchBalanceRequest(BaseModel):
    wallet_addresses: list[str]


class TopBalancesRequest(BaseModel):
    wallet_addresses: list[str]
    n: int


class TopBalancesWithTxsResponse(BaseModel):
    address: str
    balance: float
    last_transaction_date: str


class TokenInfoRequest(BaseModel):
    token_address: str


class TokenInfoResponse(BaseModel):
    symbol: str
    name: str
    totalSupply: int
