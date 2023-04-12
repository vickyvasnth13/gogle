import requests
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Replace the placeholders with your own values
API_KEY = 'AIzaSyD65i7VGfMCwL5U_29ix9Bn96Bqfb9LT2s'
SEARCH_ENGINE_ID = '<script async src="https://cse.google.com/cse.js?cx=1196e8fc5af77456e">
</script>
<div class="gcse-search"></div>'
BOT_TOKEN = '6217863695:AAGKfl6kDsblPL6_D3e5G8mAl66imDKWBgQ'

# Create a Telegram bot instance
bot = telegram.Bot(token=BOT_TOKEN)

# Define a function that handles the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a search bot. Please enter your query.")

# Define a function that handles text messages
def search(update, context):
    query = update.message.text
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}'
    response = requests.get(url)
    data = response.json()
    results = data.get('items', [])

    if not results:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, no results found.")
        return

    message = f"Here are the top {len(results)} results for your query:\n\n"
    for result in results:
        title = result.get('title', '')
        link = result.get('link', '')
        snippet = result.get('snippet', '')
        message += f"{title}\n{link}\n{snippet}\n\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Create an instance of the Updater class and pass it the bot token
updater = Updater(token=BOT_TOKEN, use_context=True)

# Create handlers for the /start command and text messages
start_handler = CommandHandler('start', start)
search_handler = MessageHandler(Filters.text, search)

# Add the handlers to the Updater
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(search_handler)

# Start the bot
updater.start_polling()

# Keep the bot running until Ctrl-C is pressed
updater.idle()