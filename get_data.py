import json
import os
import time

import requests
import datetime

def request_get_json(url, headers):
    ret_code = 0
    while ret_code == 0:
        try:
            res = requests.get(url=url, headers=headers)
            ret_code = res.status_code
            # print(ret_code)

            while ret_code == 403:
                nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print('sleeping now. from '+ nowtime)
                time.sleep(1800) #sleap a half an hour
                res = requests.get(url=url, headers=headers)
                ret_code = res.status_code

            if ret_code != 200:  # ret_code != 200表明http请求失败，可以考虑进行处理
                # print(ret_code)
                pass
        except:
            pass
    return res.json(),ret_code


def save_issues2json(json_fn:str,issue_url:str,token):
    header = {'Authorization': f'token {token}'}
    i = 1
    items = []
    while True:
        # res = requests.get(url=issue_url + f'?state=all&page={i}&per_page=30',headers=header).json()
        res, ret_code = request_get_json(url=issue_url  + '/issues'+f'?state=all&page={i}&per_page=30', headers=header)
        if ret_code == 404 or res == []:
            break
        i = i+1
        items.extend(res)
        # print(items)
        # print(len(items))

    if len(items) > 0:
        flag = 0
        for c in items:
            num = c['number']
            print(num)
            c['comments_data'],ret_code = request_get_json(url=issue_url + '/issues'+ f'/{num}' + '/comments', headers=header)
            flag = flag + 1
            print(str(flag) + '_' + str(len(items)))

        with open(json_fn, 'w') as f:
            json.dump(items, f, indent=4)
        print("Saved all issues data to " + json_fn)
        # print(len(items))



def save_pull_requests2json(json_fn: str, pull_url: str,token):
    header = {'Authorization': f'token {token}'}
    i = 1
    items = []
    while True:
        res,ret_code = request_get_json(url=pull_url + '/pulls'+ f'?state=all&page={i}&per_page=30', headers=header)
        if ret_code == 404 or res == []:
            break
        i = i + 1
        items.extend(res)  # res==list
        print(len(items))
    print(len(items))
    if len(items) > 0:
        flag = 0
        for c in items:
            num = c['number']
            print(num)
            c['pull_data'],ret_code = request_get_json(url=pull_url + '/pulls'+ f'/{num}', headers=header)
            c['review_data'],ret_code = request_get_json(url=pull_url + '/pulls'+ f'/{num}/reviews', headers=header)
            c['comments_data'], ret_code = request_get_json(url=pull_url + '/issues'+ f'/{num}' + '/comments', headers=header)
            # print(items)
            flag = flag+1
            print(str(flag) + '_' + str(len(items)))
        with open(json_fn, 'w') as f:
            json.dump(items, f, indent=4)
        print("Saved all pull_requests data to " + json_fn)


def analysisEachProject(token, repo_url, path_store):
    if repo_url.__contains__("//github.com/"):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
        print(repo_url)
        user_repoName = repo_url.replace("https://github.com/", "")
        userName = user_repoName.split("/")[0]
        projectname = user_repoName.split("/")[1]
        print(userName)
        print(projectname)
        # save_pull_requests2json(
        #     json_fn=path_store + userName + '&' + projectname + '&all_pr_data&' + nowtime + '.json',
        #     pull_url='https://api.github.com/repos/' + userName + '/' + projectname , token=token)
        save_issues2json(
            json_fn=path_store + userName + '&' + projectname + '&all_issue_data&' + nowtime + '.json',
            issue_url='https://api.github.com/repos/' + userName + '/' + projectname, token=token)



def start_download(token,category):
    # projectListFile = './repo/'+category+'_repoList.txt'
    path_store = './data/raw_data/'
    if not os.path.exists(path_store):
        os.makedirs(path_store)
        # ['makerdao/dss', 'lidofinance/lido-dao', 'aave/protocol-v2', 'curvefi/curve-contract',
        #  'Uniswap/v3-core', 'convex-eth/platform', 'justlend/justlend-protocol', 'pancakeswap/pancake-swap-core',
        #  'compound-finance/compound-protocol', 'Instadapp/dsa-contracts', 'balancer-labs/balancer-v2-monorepo',
        #  'ArrakisFinance/vault-v1-core',
        #  'FraxFinance/frax-solidity', 'sushiswap/sushiswap', 'VenusProtocol/venus-protocol', 'yearn/yearn-vaults',
        #  'liquity/dev', 'alpaca-finance/bsc-alpaca-contract', 'vvs-finance/vvs-swap-periphery',
        #  'Synthetixio/synthetix', 'dydxprotocol/protocol_v1', 'rocket-pool/rocketpool', 'DeFiCh/ain',
        #  'Benqi-fi/BENQI-Smart-Contracts', 'gmx-io/gmx-contracts', 'beefyfinance/beefy-contracts',
        #  'aurafinance/aura-contracts', 'OlympusDAO/olympus-contracts', 'fox-one/pando',
        #  'orgs/biswap-org/repositories', 'ref-finance/ref-contracts', 'project-serum/serum-dex',
        #  'NexusMutual/smart-contracts', 'euler-xyz/euler-contracts','synapsecns/synapse-contracts','osmosis-labs/osmosis',
        #                   'traderjoe-xyz/joe-core','AcalaNetwork/Acala','Loopring/protocols',
        #                   'amptoken/amp-token-contracts','Kava-Labs/kava','bancorprotocol/contracts-v3','mdexSwap/contracts',
        #                   'defisaver/defisaver-v3-contracts','stakewise/contracts','SpookySwap/spookyswap-core','StakeDAO/smart-contracts',
        #                   'DODOEX/contractV2','alchemix-finance/alchemix-protocol','blockworks-foundation/mango-v3','notional-finance/contracts','sablierhq/sablier','Ankr-network/game-unity-sdk',
        #                   'celo-tools/mento-fi','opynfinance/GammaProtocol','SetProtocol/set-protocol-v2',
        #                   'tranchess/contract-core','QuarryProtocol/quarry','TempleDAO/temple','Badger-Finance/badger-system','orca-so/typescript-sdk',
        #                   'AladdinDAO/aladdin-contracts','ApeSwapFinance/apeswap-banana-farm','AngleProtocol/angle-core',
        #                   'Idle-Labs/idle-contracts','waves-exchange/neutrino-contract/',
        #                   'ribbon-finance/ribbon-v2','stader-labs/bnbX','AlphaFinanceLab/alpha-homora-v2-contract','Folks-Finance/folks-finance-contracts',
        #                   'ellipsis-finance/ellipsis','saber-hq/stable-swap','provable-things/ethereum-api','across-protocol/contracts-v2',
        #                   'Tokemak/tokemak-smart-contracts-public','beethovenxfi/beethovenx-token','bifrost-finance/bifrost','yieldyak/smart-contracts',
        #                   'fei-protocol/fei-protocol-core','PancakeBunny-finance/Bunny','KyberNetwork/smart-contracts','NearDeFi/burrowland',
        #                   'autofarmnetwork/AutofarmV2_CrossChain','pooltogether/pooltogether-pool-contracts','flamincome/contracts','DeFiCh/ain',
        #                   'kokoa-finance/kokonutswap-contract','hop-protocol/contracts','maple-labs/maple-core','reflexer-labs/geb',
        #                   'OriginProtocol/origin-dollar','mstable/mStable-contracts','enzymefinance/protocol','KlimaDAO/klimadao-solidity',
        #                   'SpoolFi/spool-core','flamingo-finance/flamingo-contract-swap','backstop-protocol/BCompound','BendDAO/bend-lending-protocol',
        #                   'creamcoin/cream','moonwell-open-source/moonwell-contracts','Rari-Capital/vaults','element-fi/elf-contracts',
        #                   'Friktion-Labs/user-dash','pangolindex/exchange-contracts','Canto-Network/Canto','BeltFi/belt-contract',
        #                   'trisolaris-labs/trisolaris_core','swim-io/pool','Narwallets/meta-pool',
        #                   'xdao-app/xdao-contracts','vesperfi/vesper-pools-v2','ToucanProtocol/contracts','money-on-chain/main-RBTC-contract',
        #                   'dforce-network/dToken','Layer3Org/spiritswap-core/','defidollar/defidollar-core','dfx-finance/protocol',
        #                   'babyswap/baby-swap-contract','stafiprotocol/stafi-node','icon-project/devportal','DistributedCollective/Sovryn-smart-contracts',
        #                   'connext/nxtp','NFTX-project/nftx-protocol-v2','fildaio/FilDA','vesta-finance/vesta-protocol-v1',
        #                   'mimo-capital/mimo-defi','lyra-finance/lyra-protocol','neoburger/code','harvest-finance/harvest',
        #                   'dfyn/dfyn-exchange','sherlock-protocol/sherlock-v2-core','superfluid-finance/protocol-monorepo',
        #                   'linear-protocol/LiNEAR','idexio/idex-contracts-silverton','InverseFinance/inverse-protocol','consenlabs/tokenlon-contracts',
        #                   'trusttoken/contracts-pre22','kokoa-finance/kokonutswap-contract','StrikeFinance/strike-protocol','astroport-fi/astroport-core',
        #                   'Netswap/exchange-contracts','wrappedfi/wrapped_token_stacks','balancednetwork/balanced-java-contracts','mimoprotocol/mimo-contract',
        #'Gearbox-protocol/gearbox-contracts','dhedge/V2-Public','dystopia-exchange/dystopia-contracts','Scream-Finance/scream-protocol',
                  # 'pickle-finance/protocol','stellaswap/core','cVault-finance/CORE-v1','hundred-finance/hundred-dao',
                  # '88mphapp/88mph-contracts','moolamarket/moola-v2','zetamarkets/sdk','beta-finance/beta',
                  # 'MoonfarmFinance/contracts','aavegotchi/aavegotchi-contracts','O3Labs/o3swap-v2-core','PositionExchange/position-protocol',
                  # 'tinymanorg/tinyman-contracts-v1','kardia-solutions/kaidex-core','SashimiProject/sashimiswap','gnosis/dex-contracts',
                  # 'AlgemDeFi/algem-contracts','ichifarm/ichi-farming','starlay-finance/starlay-protocol','zenlinkpro/zenlink-wasm-v1',
                  # 'tetu-io/tetu-contracts','annexfinance/annex-protocol','Tethys-Finance/tethys-contracts','1Hive/conviction-voting-app',
                  # 'OpenLeverageDev/openleverage-contracts','MaiaDAO/contracts','lendhub/lendhub','SiennaNetwork/SiennaNetwork',
                  # 'Premian-Labs/premia-contracts','ChannelsFinance/ChannelsProtocol','klaybank/klaybank-protocol','saddle-finance/saddle-contract',
                  # 'bumper-dao/1a-bootstrap-contracts','swappidex/swappi-core','Railgun-Privacy/contract','vitelabs/go-vite',
                  # 'jetfuelfinance/jetfuel-protocol','Ubeswap/ubeswap','Synthetify/synthetify-protocol',
                  # 'Linear-finance/linear','swopfi/swopfi-smart-contracts','PaladinFinance/Paladin-Protocol','recursive-research/rift-protocol','cowri/shell-solidity-v1'
        #没跑 'keep-network/keep-core','alexgo-io/alex-v1','pendle-finance/pendle-core','yieldprotocol/vault-v2',
        #404了
    project_list=['UMAprotocol/protocol']


    for i in range(0,len(project_list)):
        repo_url='https://github.com/'+project_list[i]
        analysisEachProject(token, repo_url, path_store)
    # with open(projectListFile, 'r') as f:
    #     content_repo = f.read().splitlines()
    #     for repo_url in content_repo:
    #         analysisEachProject(token,repo_url,path_store)
    # repo_url="https://github.com/makerdao/dss"
    #
    # analysisEachProject(token,repo_url,path_store)



if __name__ == "__main__":
    # token = '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'
    token='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'
    start_download(token,'1')
    # repoCategary = ['multimedia']
    # for each_category in repoCategary:
    #     print(each_category)
    #     start_download(token,each_category)






