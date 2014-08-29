import time
from vault import Vault

vault = Vault()

# send coins to vault
while vault.send():
    time.sleep(1)

# withdraw coins from vault
while vault.withdraw():
    time.sleep(1)

# fast withdraw coins from vault
while vault.fastwithdraw():
    time.sleep(1)
