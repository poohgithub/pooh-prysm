from eth_utils import keccak, to_hex

def bls_pubkey_to_withdrawal_credentials(pubkey: bytes) -> str:
    # Hash the public key
    pubkey_hash = keccak(pubkey)

    # For withdrawal credentials:
    # The first byte is 0x00
    # Followed by the first 31 bytes of the pubkey hash
    withdrawal_credentials = b'\x00' + pubkey_hash[:31]

    return to_hex(withdrawal_credentials)

# Your BLS public key in bytes format
bls_pubkey = bytes.fromhex('b1471a311476212b6585275f211903b010277bab53d7e7a05dea64d3e996d50e3e4dab2c45936e2fe61be39c80050675') 

eth2_address = bls_pubkey_to_withdrawal_credentials(bls_pubkey)
print("Eth2 Withdrawal Credentials:", eth2_address)