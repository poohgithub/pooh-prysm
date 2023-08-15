# Poohnet for Consensus protocol


### genesis
Add the following line to the .zprofile or .bashrc
```
alias genesis='./eth2-testnet-genesis/eth2-testnet-genesis merge --config "./config/chain-config.yaml" --eth1-config "./config/genesis.json" --mnemonics "./config/mnemonics.yaml" --state-output "./config/genesis.ssz" --tranches-dir "./config/tranches"'
```
And run following command in %ROOT/poohnet directory.
```
source ~/.zprofile
genesis
```