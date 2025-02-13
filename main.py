import telebot
from itertools import cycle
import os
from openai import OpenAI


bot = telebot.TeleBot(os.getenv('TELEGRAM_KEY'))
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENROUTER_KEY'),
)

models = cycle([
    "deepseek/deepseek-chat:free", "deepseek/deepseek-r1:free", "deepseek/deepseek-r1-distill-llama-70b:free",
    ])
client.active_model = next(models)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Спроси меня что хочешь ;)")


@bot.message_handler(func=lambda message: True)
def answer_all(message):
    try:
        answer = ask_gpt(message.text)
        if not answer:
            raise ValueError
        bot.send_message(message.chat.id, answer)

    except ValueError:
        client.active_model = next(models)
        answer_all(message)

    except Exception as e:
        bot.send_message(message.chat.id, e)


def ask_gpt(message):
    completion = client.chat.completions.create(
        model=client.active_model,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return completion.choices[0].message.content


bot.infinity_polling()
