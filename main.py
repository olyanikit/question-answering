from aiogram import Bot, Dispatcher, executor, types
import os
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from get_context import *

model_name = "deepset/tinyroberta-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(bot)

def main():
    @dp.message_handler(commands='start')
    async def send_welcome(message: types.Message):
        await message.reply(f"Hello {message.from_user.username}")


    @dp.message_handler()
    async def get_answer(message: types.Message):
        print(message)
        question = message.text
        context, snippet = get_context(question)
        qa = pipeline('question-answering', model=model_name, tokenizer=model_name)
        QA_input = {
            'question': question,
            'context': context or snippet
        }
        res = qa(QA_input)

        await bot.send_message(message.chat.id, res['answer'])

    executor.start_polling(dp)


if __name__ == '__main__':
    main()