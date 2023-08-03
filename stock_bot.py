import discord
from discord.ext import commands
import yfinance as yf

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
BOT_TOKEN = 'token'
PREFIX = '!'  # You can set the bot's command prefix to any character you prefer

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def stock(ctx, ticker_symbol: str):
    stock_data = get_stock_data(ticker_symbol.upper())
    if stock_data:
        await ctx.send(format_stock_data(stock_data))
    else:
        await ctx.send(f"Could not find data for '{ticker_symbol}'")


def get_stock_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period="1d")
        if data.empty:
            return None
        return data.iloc[-1]
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None


def format_stock_data(stock_data):
    return f"Stock: {stock_data.name}\n" \
           f"Date: {stock_data.name.strftime('%Y-%m-%d')}\n" \
           f"Open: {stock_data['Open']:.2f}\n" \
           f"High: {stock_data['High']:.2f}\n" \
           f"Low: {stock_data['Low']:.2f}\n" \
           f"Close: {stock_data['Close']:.2f}\n" \
           f"Volume: {stock_data['Volume']:,}"


bot.run(BOT_TOKEN)
