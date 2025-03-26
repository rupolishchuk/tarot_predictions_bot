nest_asyncio.apply()


os.environ["MISTRAL_API_KEY"] = "YOUR API KEY"


api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот, который даст тебе предсказание на завтрашний день. "
        f"Используй команду /advice для получения сообщения."
    )


async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = """Ты -- гадалка на таро. Дай милое, но смешное предсказание на завтрашний день не более 3 предложений, вытянув карту таро и дав ей интерпритацию, что может произойти завтра длиною не более 3 предложения. делай прдсказания, которые будут подходит и мужчинам и женщинам. Используй разные карты. Твой ответ: "Твоя карта дня — <случайная карта>", /n <интерпритация>. давай разные и непохожие друг на друга ответы.)"""

    try:
        response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )


        prediction_text = response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Ошибка при запросе к Mistral API: {e}")
        prediction_text = "Произошла ошибка при запросе к AI. Пожалуйста, попробуй позже."

    await update.message.reply_text(f"🔮 Твоё предсказание на завтра:\n\n{prediction_text}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")


async def run_bot():
    token = " TELEGRAM BOT TOKEN"


    application = Application.builder().token(token).build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("advice", advice))


    application.add_error_handler(error)


    await application.run_polling()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


    loop.run_until_complete(run_bot())
