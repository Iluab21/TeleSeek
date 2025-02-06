import telebot
from openai import OpenAI

bot = telebot.TeleBot("YOUR_BOT_TOKEN")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="<OPENROUTER_API_KEY>",
)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Спроси меня что хочешь ;)")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_message(message.chat.id, ask_gpt(message.text))
    except Exception as e:
        bot.send_message(message.chat.id, e)


def ask_gpt(message):
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return completion.choices[0].message.content


bot.infinity_polling()
