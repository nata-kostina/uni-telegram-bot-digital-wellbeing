import telebot
from config import API_KEY
from telebot import types
from tools import get_country_list, is_input_valid, get_country_info, get_total_info, get_dql_info, get_help_info, \
    get_top_five, get_rank

user_action = "/by_country"


def run_bot():
    bot = telebot.TeleBot(API_KEY)

    actions = ["/country_list", "/total_info", "/total_by_rank", "/total_by_country", "/by_country", "/help",
               "/dql_info", "/top_five", "/rank"]

    @bot.message_handler(commands=['start'])
    def start(message):
        msg = f'Hello, <b>{message.from_user.first_name}</b>👋\n\n' \
              f'I am Digital Wellbeing Bot. 💻🧘‍♀️\n' \
              f'I can tell you about digital quality of life in 1️⃣1️⃣7️⃣ countries.\n\n' \
              f'- Which country has the fastest internet?\n' \
              f'- Where do people feel secure online?\n' \
              f'- What is the rank of your country?\n\n' \
              f'⬇ If you are interested, click buttons below ⬇\n\n' \
              f'Type /help to get the list of available commands'
        user_id = message.from_user.id
        user_full_name = message.from_user.first_name
        print(user_id, user_full_name)
        bot.send_message(message.chat.id, msg, parse_mode="html")
        show_actions(message.from_user.id)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(action):
        if action.message:
            if action.data in actions:
                controller(action.message.chat.id, action.data)
            else:
                bot.send_message(action.message.chat.id, "🗿 Unknown command. Enter /help to see the list of available "
                                                         "actions.")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text in actions:
            controller(message.from_user.id, message.text)
        else:
            validation = is_input_valid(message.text)
            if validation['is_valid']:
                msg = get_rank(validation['valid_data'])
                bot.send_message(message.from_user.id, msg, parse_mode="html")
                if user_action == "/by_country":
                    bot.send_message(message.from_user.id, "⏳ Wait please, data are generating...")
                    info = get_country_info(validation['valid_data'])
                    bot.send_photo(message.from_user.id, info)
                show_actions(message.from_user.id)
            else:
                msg = ""
                if len(validation['invalid_data']) == 1:
                    msg = "Country <b>{}</b> was not found. Please try again.".format(validation['invalid_data'][0])
                else:
                    msg = "Countries <b>{}</b> was not found. Please try again.".format(",".join(validation['data']))
                bot.send_message(message.from_user.id, msg, parse_mode="html")

    def show_actions(user_id):
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        item_dql_info = types.InlineKeyboardButton(text="What is DQL?", callback_data="/dql_info")
        item_total_info = types.InlineKeyboardButton(text="Get DQL of all countries", callback_data="/total_info")
        item_dql_by_country = types.InlineKeyboardButton(text="Get DQL by country", callback_data="/by_country")
        item_top_five = types.InlineKeyboardButton(text="TOP-5 countries", callback_data="/top_five")
        item_rank = types.InlineKeyboardButton(text="Get country rank", callback_data="/rank")
        item_country_list = types.InlineKeyboardButton(text="Show available countries", callback_data="/country_list")
        item_help = types.InlineKeyboardButton(text="Help", callback_data="/help")

        markup_inline.add(item_dql_info, item_total_info, item_dql_by_country, item_top_five, item_rank,
                          item_country_list, item_help)

        bot.send_message(user_id, "Choose action:", parse_mode="html", reply_markup=markup_inline)

    def controller(user_id, action):
        global user_action
        if action == "/country_list":
            bot.send_message(user_id, get_country_list())
            show_actions(user_id)
        elif action == "/by_country":
            user_action = "/by_country"
            bot.send_message(user_id, 'Enter one or more country names:')
        elif action == "/total_info":
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            item_rank = types.InlineKeyboardButton(text="By rank", callback_data="/total_by_rank")
            item_country = types.InlineKeyboardButton(text="By country", callback_data="/total_by_country")
            markup_inline.add(item_rank, item_country)
            bot.send_message(user_id, 'How would you like to sort your data?', parse_mode="html",
                             reply_markup=markup_inline)
        elif action == "/total_by_rank":
            bot.send_message(user_id, "⏳ Wait please, data are generating...")
            info = get_total_info("by_rank")
            bot.send_photo(user_id, info)
            show_actions(user_id)
        elif action == "/total_by_country":
            bot.send_message(user_id, "⏳ Wait please, data are generating...")
            info = get_total_info("by_country")
            bot.send_photo(user_id, info)
            show_actions(user_id)
        elif action == "/dql_info":
            msg = get_dql_info()
            bot.send_message(user_id, msg, parse_mode="html")
            show_actions(user_id)
        elif action == "/help":
            msg = get_help_info()
            bot.send_message(user_id, msg, parse_mode="html")
        elif action == "/top_five":
            bot.send_message(user_id, "⏳ Wait please, data are generating...")
            img, msg = get_top_five()
            bot.send_message(user_id, msg, parse_mode="html")
            bot.send_photo(user_id, img)
            show_actions(user_id)
        elif action == "/rank":
            user_action = "/rank"
            bot.send_message(user_id, 'Enter one or more country names:')

    bot.polling()
