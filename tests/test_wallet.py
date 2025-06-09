import pytest
from services.wallet_check import is_valid_wallet

def test_wallet_validation():
    assert is_valid_wallet("0x1234567890abcdef1234567890abcdef12345678") == True
    assert is_valid_wallet("0x123") == False
    assert is_valid_wallet("1234567890abcdef1234567890abcdef12345678") == False
