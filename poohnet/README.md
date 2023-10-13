# Setup consensus layer for Poohnet

## Steps

### Get genesis block information of execution layer
```
docker exec -it poohgeth-1 geth attach http://localhost:8545
```
```
> eth.getBlockByNumber(0)
{
  baseFeePerGas: "0x3b9aca00",
  difficulty: "0x1",
  extraData: "0x00000000000000000000000000000000000000000000000000000000000000008532654ad638db3dee3836b22b35f7ca707428ca0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  gasLimit: "0x7a1200",
  gasUsed: "0x0",
  hash: "0x1a43f41d4a1daa59cc87902aa5dfe9748945189ccc0a634d99d9ad6f9037cd42",
  logsBloom: "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  miner: "0x0000000000000000000000000000000000000000",
  mixHash: "0x0000000000000000000000000000000000000000000000000000000000000000",
  nonce: "0x0000000000000000",
  number: "0x0",
  parentHash: "0x0000000000000000000000000000000000000000000000000000000000000000",
  receiptsRoot: "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
  sha3Uncles: "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
  size: "0x273",
  stateRoot: "0xb2bcaa2e0c04341cd56aeffd7f08239519ccb798a99daa5289e0393b2e999973",
  timestamp: "0x0",
  totalDifficulty: "0x1",
  transactions: [],
  transactionsRoot: "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
  uncles: []
}
```
- Get hash from the above information

### Set `TERMINAL_BLOCK_HASH` and `MIN_GENESIS_TIME`
- Set `TERMINAL_BLOCK_HASH` to the above genesis blockhash
- Set the consensus layer starting time
```
date +%s
```
You can get like this.
```
1714092636
```
You might add 10 minitues which means 600 to the output, which can be `1714093236`. And add this value to MIN_GENESIS_TIME.


### Create genesis file
```
cd [PROJECT_ROOT]/poohnet
./eth2-testnet-genesis/eth2-testnet-genesis merge --config "./config/chain-config.yaml" --eth1-config "./config/genesis.json" --mnemonics "./config/mnemonics.yaml" --state-output "./config/genesis.ssz" --tranches-dir "./config/tranches"
```

### Install `zcli` and get the validators root
Pre-requisits
- Install Go 1.16+
- And add `$HOME/go/bin` to your PATH.

Install the `zcli` from [here](https://github.com/protolambda/zcli).
```
go install github.com/protolambda/zcli@latest
```
Get the validators root
```
cd [PROJECT_ROOT]/poohnet
zcli pretty bellatrix BeaconState ./config/genesis.ssz > parsedState.json
```
And get the validators root from parsedState.json named `genesis_validators_root`.


### Set the validators root for staking deposit
Open `[PROJECT_ROOT]/poohnet/pooh-deposit-cli/staking_deposit/settings.py`

And set the value to the code `GENESIS_VALIDATORS_ROOT`.
**PLEASE excluede `0x` from the string like e63460dc044e056f26ca8f7406a18867d31f1ec195322f428b5918d4b0153050** 

### Make wallets with `staking-deposit-cli`
```
cd [PROJECT_ROOT]/poohnet/pooh-deposit-cli
sudo ./deposit.sh install
```

If there is some error related to `longinterpr.h`, follow the next instruction.
```
python3.10 -m venv py310
source py310/bin/activate
```

Make wallets. (You can the existing mnemonics from `[PROJECT_ROOT]/poohnet/config/mnemonics.yaml`)
```
./deposit.sh existing-mnemonic
```
```
Please choose your language ['1. العربية', '2. ελληνικά', '3. English', '4. Français', '5. Bahasa melayu', '6. Italiano', '7. 日本語', '8. 한국어', '9. Português do Brasil', '10. român', '11. Türkçe', '12. 简体中文']:  [English]: 3
Please enter your mnemonic separated by spaces (" "). Note: you only need to enter the first 4 letters of each word if you'd prefer.: truth fold access cheese tackle bomb plate kite unhappy squirrel mutual humble
Enter the index (key number) you wish to start generating more keys from. For example, if you've generated 4 keys in the past, you'd enter 4 here. [0]: 0
Please repeat the index to confirm: 0
Please choose how many new validators you wish to run: 8
Please choose the (mainnet or testnet) network/chain name ['mainnet', 'testnet', 'devnet']:  [mainnet]: testnet
Create a password that secures your validator keystore(s). You will need to re-enter this to decrypt them when you setup your BOSagora validators.: 
```


1. 블럭해시과 genesis time(date +%s)을 chain-config 반영하고 eth2-testnet-genesis 실행
    - gen_genesis
    - zcli pretty bellatrix  BeaconState genesis.ssz > parsedState.json로 Validators Root 가져오기
    - settings.py에 GENESIS_VALIDATORS_ROOT에 추가, 근데 이건 거의 안 바뀜.
2. staking-deposit-cli로 wallet 만들기
    - sudo ./deposit.sh install, 만약 longinterpr.h 에러 발생하면 아래 실행
        - python3.10 -m venv py310
        - source py310/bin/activate
    - ./deposit.sh existing-mnemonic
3. 첫번째 cnode 실행하고 enr 알아내서 bootstrap-node
    - cl은 el과 연동되므로 init할 필요 없음
    - poohprysm 루트폴더의 cnode로 실행.
4. 나머지 cl 실행시키기
5. keys &validators 실행
    - poohprysm 루트폴더에서 찾아야 함.

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