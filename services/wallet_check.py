import re

WALLET_REGEX = r"^0x[a-fA-F0-9]{40}$"

def is_valid_wallet(address):
    return bool(re.match(WALLET_REGEX, address))
