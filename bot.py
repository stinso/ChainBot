# bot.py
import discord
import os
import time

from etherscan.accounts import Account
from discord.ext import commands, tasks
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

load_dotenv()

############### DISCORD ###############
TOKEN = os.getenv('DISCORD_TOKEN')
COINGECKO = 'https://www.coingecko.com/en/coins/chain-games'
CONTRACT = '0xc4c2614e694cf534d407ee49f8e44d125e4681c4'
WEBSITE = 'https://chaingames.io/ '
ETHERSCAN = 'https://etherscan.io/token/0xC4C2614E694cF534D407Ee49F8E44D125E4681c4'
UNISWAP = 'https://app.uniswap.org/#/swap?inputCurrency=0xC4C2614E694cF534D407Ee49F8E44D125E4681c4'
WHITEPAPER = 'https://chaingames.io/wp-content/uploads/2020/08/Chain_Games-White-Paper-Aug-2020v4.pdf'



############### ETHERSCAN ###############
KEY = "DCRBPESFCAXRFJRWQ1YMVQHHXWF5T2CFFR"
ADDRESS = '0x33906431e44553411b8668543ffc20aaa24f75f9'
ETH_BOUNDARY = 0.1

api = Account(address=ADDRESS, api_key=KEY) # api

hash = "" # last trx hash

currency_symbol_dict = {'usd': '$', 'btc': '₿', 'eth': 'Ξ', 'ltc': 'Ł', 'eur': '€', 'jpy': '¥', 'rub': '₽',
                        'aed': 'د.إ', 'bdt': '৳', 'bhd': 'BD', 'cny': '¥', 'czk': 'Kč', 'dkk': 'kr.', 'gbp': '£',
                        'huf': 'Ft', 'idr': 'Rp', 'ils': '₪', 'inr': '₹', 'krw': '₩', 'kwd': 'KD', 'lkr': 'රු',
                        'mmk': 'K', 'myr': 'RM', 'nok': 'kr', 'php': '₱', 'pkr': 'Rs', 'pln': 'zł', 'sar': 'SR',
                        'sek': 'kr', 'thb': '฿', 'try': '₺', 'vef': 'Bs.', 'vnd': '₫', 'zar': 'R', 'xdr': 'SDR',
                        'xag': 'XAG', 'xau': 'XAU'}

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    etherscan_poll.start()
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='announcements', help="Announcement Channel :loudspeaker:")
async def announcements(ctx):
        await ctx.send("<#740007189560688722>")

@bot.command(name='burned', help='Deflationary Burning Info :fire:')
async def burned(ctx):
    await ctx.send(
        "Deflationary :fire:\n\n" +
        "1% of CHAIN used as transaction fees will be burned. This decreases the total supply of CHAIN, thus increasing the scarcity of each token."
    )

@bot.command(name='circulating', help='Circulating Supply :repeat:')
async def circulating(ctx):
    await ctx.send(
        "Circulating Supply\n\nThe circulating supply for CHAIN will start at 275M tokens.150M tokens for OTC, and 125M on Uniswap 🦄\n\n" +
        "An additional 18M tokens were used from the dev fund post launch to pay for already rendered legal and marketing services bringing our current circulating supply to 293.38M tokens."
    )

@bot.command(name='contract', help='Contract Address :construction_worker::male_sign:')
async def contract(ctx):
    await ctx.send("Chain Games Contract Address:\n" + CONTRACT)

@bot.command(name='coingecko', help='CoinGecko Listing :lizard:')
async def coingecko(ctx):
    await ctx.send("Check out our CoinGecko listing:\n" + COINGECKO)

@bot.command(name='downloads', help='Downloads Links to Super Crypto Kart :race_car:')
async def downloads(ctx):
    await ctx.send(
        ":race_car::checkered_flag: Super Crypto Kart Version 0.1  is available for download :race_car::checkered_flag:\n\n" +
        ":fire: This first release is offline single player only so you can all hone in your skills and practice a bit before :fire:"
        "the multiplayer real competition heats up with push to mainnet!\n\n" +
        ":white_check_mark: Windows - http://downloads.chaingames.io/SuperCryptoKart-0.10.1-git-installer-64bit.exe\n" +
        ":white_check_mark: Mac OS - http://downloads.chaingames.io/SuperCryptoKart-0.1-catalina-fix.dmg\n" +
        ":white_check_mark: Linux - http://downloads.chaingames.io/SuperCryptoKart-v0.1.3.tar.gz\n\n" +
        "Make sure you turn your graphics to max!  Options -> Graphics\n\n" +
        ":white_check_mark: Change: Graphical Effects Level -> 6\n" +
        ":white_check_mark: Change: Blur Effects Level -> 2\n\n" +
        "Max resolution!"
    )

@bot.command(name='etherscan', help='Etherscan Address :link:')
async def etherscan(ctx):
    await ctx.send(ETHERSCAN)

@bot.command(name='list', help="Shows the supported currencies of the '!price' command")
async def list(ctx):
    currencies = ""
    for currency in currency_symbol_dict:
        if currencies != "":
            currencies += ", " + currency.upper()
        else:
            currencies += currency.upper()
    await ctx.send("List of supported currencies:\n" + currencies)

@bot.command(name='otc', help='Information about the OTC Pre-Sale, KYC, etc :shopping_cart:')
async def otc(ctx):
    await ctx.send(
"""
:shopping_cart: OTC Pre-Sale & KYC Info :shopping_cart:

Total Supply: 500M :moneybag:

Initial Circulation Supply: 275M Tokens :repeat:

Market Cap: 2.75M :chart_with_upwards_trend:

Pre-Sale: 150M @ $0.01 :currency_exchange:

To qualify for the pre-sale, the associated wallet needs to have at least 10k SWAP in it and sign a message via metamask to prove so. We will release a webpage portal and form to securly submit KYC details (passport/driving license/govt. issued ID + selfie holding the id and current date, email id). The first 250 KYCs will be given the opportunity to participate in Pre-Sale. There will be a limit of 6K USD per head.

Uniswap Listing: 125M tokens @ $0.01. :unicorn:

IMO SWAP Pre-Sale Tentatively Scheduled for - Aug 24th :calendar_spiral:

:octagonal_sign: The following countries are restricted from participating in the Pre-Sale :octagonal_sign:

Afghanistan, Australia, Belarus, Bosnia & Herzegovina, Burundi, Central African Republic, Cuba, Democratic Republic of Congo, Estonia, Egypt, Guinea, Guinea-Bissau, Iran, Iraq, Lebanon, Libya, Mali, Moldova, Montenegro, Myanmar (Burma), Nicaragua, North Korea, Somalia, Sudan, Syria, Tunisia, Turkey, Ukraine, United States of America and its territories (American Samoa, Guam, the Northern Mariana Islands, Puerto Rico, and the U.S. Virgin Islands), Venezuela, Yemen, Zimbabwe

Uniswap ILO Launch - Aug 26th :calendar_spiral:
"""
    )

@bot.command(name='payouts', help="Example of how lobbies and payouts work :money_mouth:")
async def payouts(ctx):
    await ctx.send(
        ":video_game: Chain Games has created non-custodial wagering smart contracts for games of skill. The process of how this works is actually pretty straightforward.\n\n"
        ":race_car: Let\'s use our first flagship title release, Super Crypto Kart as an example.\n\n"
        ":moneybag: In the case with Super Crypto Kart, when you login into the online game mode, you will see lobbies organized by entry fee in CHAIN ($5, $10, $25, $50, $100, etc).  You will choose the lobby you want to enter and pay the fee via your Web3 wallet, which will lock your CHAIN tokens into the smart contract for that race.\n\n"
        ":dollar: Let's use the $5 lobby as example.\n\n"
        ":family_mwgb: Up to 8 people can join a lobby, so that would be $5 x 8 = $40 total in the pot minus a 3% rake.\n\n"
        ":white_check_mark: This leaves $38.80 up for grabs!\n\n"
        ":abacus: Payouts are distributed in a 70/20/10 ratio. \n\n"
        ":trophy: 1st Place would receive $27.16\n"
        ":medal: 2nd Place would receive $7.76\n"
        ":military_medal: 3rd Place would receive $3.88\n\n"
        ":cut_of_meat: $0.18 would be sent back to the staking pool"
    )

@bot.command(name='price', help="Responds with the price of the awesome CHAIN token. Type '!price eur' for the price in €. Type '!list' to show supported currencies.")
async def price(ctx, currency='usd'):
    currency = currency.lower()
    if currency in currency_symbol_dict:
        response = cg.get_token_price(id='ethereum', contract_addresses=CONTRACT, vs_currencies=currency)
        await ctx.send("CHAIN Price is " + currency_symbol_dict[currency] + str(response[CONTRACT][currency]))
    else:
        await ctx.send("Your selected currency is not supported. Type '!list' to show supported currencies.")

@bot.command(name='project', help='Chain Games Project Brief Overview :video_game:')
async def project(ctx):
    await ctx.send(
        ":fire: Chain Games: Blockchain Gaming Redefined :fire:\n\n" +
        "Chain Games is an evolution in Web 3.0 blockchain gaming combining smart contract based wagering with state of the art gameplay.\n\n" +
        "We will be launching  on ropsten testnet mid August with our first game, a cross-platform racing game Super Crypto Kart\n\n" +
        ":fire: Mainnet will be launching at the end of August :fire:\n\n" +
        ":chains::video_game: Website - " + WEBSITE + " :chains::video_game:\n\n" +
        "Announcements: <#740007189560688722>\n\n" +
        "Price Speculation/Discussion: <#740004196295901308>"
    )

@bot.command(name='social', help='Chain Games Social Media Channels(twitter/discord/telegram/facebook) :man::woman:')
async def social(ctx):
    await ctx.send(
"""
:white_small_square: Discord:  https://discord.gg/UheqRXZ

:white_small_square: Telegram: https://t.me/ChainGames

:white_small_square: Twitter: https://twitter.com/RealChainGames

:white_small_square: Facebook: https://www.facebook.com/realchaingames
"""
    )

@bot.command(name='staking', help='')
async def staking(ctx):
    await ctx.send(
        ":cut_of_meat: Staking Rewards :cut_of_meat:\n\n" +
        "Every entry fee paid in CHAIN rewards stakers on the network with 15 % of the transaction fee distributed automatically to their wallet.:money_mouth:"
    )

@bot.command(name='total', help='Total Supply :moneybag:')
async def total(ctx):
    await ctx.send(
        ":moneybag: Total Supply :moneybag:\n\n" +
        "CHAIN will have a maximum total supply of 500M tokens, however 1% of all tokens are burned during transaction fees, so this number will continually decrease over time."
    )

@bot.command(name='rank', help='Market Cap Rank :first_place:')
async def rank(ctx):
    response = CoinGeckoAPI().get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=CONTRACT)
    await ctx.send('#' + str(response['market_cap_rank']))

@bot.command(name='rate', help="Rate of CHAIN (default=usd) :chart_with_upwards_trend:")
async def rate(ctx, currency='usd'):
    currency = currency.lower()
    if currency in currency_symbol_dict:
        response = cg.get_token_price(id='ethereum', contract_addresses=CONTRACT, vs_currencies=currency)
        price = response[CONTRACT][currency]
        if price > 0:
            rate = 1 / price
            if rate > 1:
                rate = int(rate * 100)
                rate = rate / 100
            await ctx.send("1 " + currency_symbol_dict[currency] + " = " + str(rate) + " CHAIN")
    else:
        await ctx.send("Your selected currency is not supported. Type '!list' to show supported currencies.")

@bot.command(name='marketcap', help='Market cap of our token in :dollar:')
async def marketcap(ctx):
    response = CoinGeckoAPI().get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=CONTRACT)
    await ctx.send('$' + str(response['market_data']['market_cap']['usd']))

@bot.command(name='high_24h', help='Highest price in the last 24h')
async def high_24h(ctx, currency='usd'):
    currency = currency.lower()
    if currency in currency_symbol_dict:
        response = CoinGeckoAPI().get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=CONTRACT)
        await ctx.send(currency_symbol_dict[currency] + str(response['market_data']['high_24h'][currency]))
    else:
        await ctx.send("Your selected currency is not supported. Type '!list' to show supported currencies.")

@bot.command(name='low_24h', help='Lowest price in the last 24h')
async def low_24h(ctx, currency='usd'):
    currency = currency.lower()
    if currency in currency_symbol_dict:
        response = CoinGeckoAPI().get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=CONTRACT)
        await ctx.send(currency_symbol_dict[currency] + str(response['market_data']['low_24h'][currency]))
    else:
        await ctx.send("Your selected currency is not supported. Type '!list' to show supported currencies.")

@bot.command(name='low/high_24h', help='Lowest and highest price in the last 24h')
async def low_high_24h(ctx, currency='usd'):
    currency = currency.lower()
    if currency in currency_symbol_dict:
        response = CoinGeckoAPI().get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=CONTRACT)
        await ctx.send(currency_symbol_dict[currency] + str(response['market_data']['low_24h'][currency]) + " / " + currency_symbol_dict[currency] + str(response['market_data']['high_24h'][currency]))
    else:
        await ctx.send("Your selected currency is not supported. Type '!list' to show supported currencies.")


@bot.command(name='unistats', help='Uniswap stats :chart_with_upwards_trend:')
async def unistats(ctx):
    await ctx.send(
        "https://uniswap.info/token/0xC4C2614E694cF534D407Ee49F8E44D125E4681c4 🦄\n"
        "https://uniswap.chartex.pro/?symbol=UNISWAP:CHAIN 🦄\n"
        "https://www.dextools.io/app/uniswap/pair-explorer/0x33906431e44553411b8668543ffc20aaa24f75f9 :chart_with_upwards_trend:"
    )

@bot.command(name='uniswap', help='Uniswap Contract Address :unicorn:')
async def uniswap(ctx):
    await ctx.send("Our Uniswap contract address is:\n" + UNISWAP + " 🦄")

@bot.command(name='website', help=' Website Information :spider_web:')
async def website(ctx):
    await ctx.send(":chains::video_game: Visit our website - " + WEBSITE + " :chains::video_game:")

@bot.command(name='whitepaper', help='Whitepaper Link :person_tipping_hand::male_sign:')
async def whitepaper(ctx):
    await ctx.send(WHITEPAPER)

@bot.command(name='help', help="Shows this help :ambulance:")
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='!announcements', value="Announcement Channel :loudspeaker:", inline=False)
    embed.add_field(name='!burned', value="Deflationary Burning Info :fire:", inline=False)
    embed.add_field(name='!circulating', value="Circulating Supply :repeat:", inline=False)
    embed.add_field(name='!contract', value="Contract Address :construction_worker::male_sign:", inline=False)
    embed.add_field(name='!coingecko', value="CoinGecko Listing :lizard:", inline=False)
    embed.add_field(name='!downloads', value="Downloads Links to Super Crypto Kart :race_car:", inline=False)
    embed.add_field(name='!etherscan', value="Etherscan Address :link:", inline=False)
    embed.add_field(name='!help', value="Shows this help :ambulance:", inline=False)
    embed.add_field(name='!high_24h', value="Highest price in the last 24h :chart_with_upwards_trend:", inline=False)
    embed.add_field(name='!list', value="Shows the supported currencies of the '!price' command", inline=False)
    embed.add_field(name='!low_24h', value="Lowest price in the last 24h :chart_with_upwards_trend:", inline=False)
    embed.add_field(name='!low/high_24h', value="Lowest and highest price in the last 24h :chart_with_upwards_trend:", inline=False)
    embed.add_field(name='!marketcap', value="Market cap of our token in :dollar:", inline=False)
    embed.add_field(name='!otc', value="Information about the OTC Pre-Sale, KYC, etc :shopping_cart:", inline=False)
    embed.add_field(name='!payouts', value="Example of how lobbies and payouts work :money_mouth:", inline=False)
    embed.add_field(name='!project', value="Chain Games Project Brief Overview :video_game:", inline=False)
    embed.add_field(name='!price', value= "Price of our Token in USD :money_with_wings:", inline=False)
    embed.add_field(name='!price eur', value="Price in EUR. You can choose any currency from '!list' :money_with_wings:", inline=False)
    embed.add_field(name='!rank', value="Market Cap Rank :first_place:", inline=False)
    embed.add_field(name='!rate', value="Rate of CHAIN (default=usd) :chart_with_upwards_trend:", inline=False)
    embed.add_field(name='!social', value="Chain Games Social Media Channels(twitter/discord/telegram/facebook) :man::woman:", inline=False)
    embed.add_field(name='!staking', value="Staking Rewards Info :cut_of_meat:", inline=False)
    embed.add_field(name='!total', value="Total Supply :moneybag:", inline=False)
    embed.add_field(name='!unistats', value="Uniswap stats :chart_with_upwards_trend:", inline=False)
    embed.add_field(name='!uniswap', value="Uniswap Contract Address :unicorn:", inline=False)
    embed.add_field(name='!website', value=" Website Information :spider_web:", inline=False)
    embed.add_field(name='!whitepaper', value="Whitepaper Link :person_tipping_hand::male_sign:", inline=False)

    await author.send(embed=embed)

@tasks.loop(seconds=1)
async def etherscan_poll():
    global hash
    global api

    try:
        transactions = api.get_transaction_page(page=1, offset=2, sort='desc', erc20=True)
        chains = 0
        eth = 0
        buy = False
        chainId = 0
        if transactions[0]['hash'] == transactions[1]['hash'] and transactions[0]['hash'] != hash:
            hash = transactions[0]['hash']
            if transactions[1]['tokenName'] == 'Chain Games':
                chainId = 1
            if transactions[chainId]['from'] == ADDRESS:
                buy = True
            eth = int(transactions[abs(chainId - 1)]['value']) / 1000000000000000000
            chains = int(transactions[chainId]['value']) / 1000000000000000000
            if eth >= ETH_BOUNDARY:
                embed = None
                if buy:
                    embed = discord.Embed(
                        title=':chainlogo: CHAIN Uniswap V2 Tracker :unicorn:',
                        colour=discord.Colour.green()
                    )
                    embed.add_field(name='Swap ETH for CHAIN :dollar:', value=str(round(eth, 2)) + " :ethereumicon: => " + str(round(chains, 2)) + " :chainlogo:", inline=False)
                    embed.add_field(name='Address:', value=transactions[abs(chainId - 1)]['from'], inline=False)

                else:
                    embed = discord.Embed(
                        title=':chainlogo: CHAIN Uniswap V2 Tracker :unicorn:',
                        colour=discord.Colour.red()
                    )
                    embed.add_field(name='Swap CHAIN for ETH', value=str(round(chains, 2)) + " :chainlogo: => " + str(round(eth, 2)) + " :ethereumicon:", inline=False)
                    embed.add_field(name='Address:', value=transactions[chainId]['from'], inline=False)

                #embed.add_field(name='TxHash:', value=hash, inline=False)
                embed.add_field(name='Link to transaction:', value="[View Transaction](https://etherscan.io/tx/" + hash + ")", inline=False)
                embed.set_footer(text='Made by mukki')
                #embed.set_image(url='https://cdn.discordapp.com/avatars/471304965990776832/5df9624fe375b4252618da61e8975e05.png?size=128')
                #embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/471304965990776832/5df9624fe375b4252618da61e8975e05.png?size=128')

                channel = bot.get_channel(748860624666230806)
                await channel.send(embed=embed)
    except:
        print("No internet connection.")
        time.sleep(10)
        api = Account(address=ADDRESS, api_key=KEY)

bot.run(TOKEN)



