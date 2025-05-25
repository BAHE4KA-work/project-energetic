from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

from app.telegram_bot.states import AuthStates
from app.telegram_bot.service import (
    authorize_master,
    get_events,
    mark_done,
    get_route,
    get_address_card, assign_report,
)

router = Router()
authorized_masters = {}

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Введите код мастера для авторизации:")
    await state.set_state(AuthStates.waiting_for_code)

@router.message(AuthStates.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    code = message.text.strip()
    master = await authorize_master(code)
    if master is None:
        await message.answer("Неверный код. Попробуйте ещё раз.")
        return
    authorized_masters[message.chat.id] = master.id
    await state.clear()
    await message.answer(f"Привет, {master.name}!\nИспользуйте /plan для получения плана проверок.")

@router.message(Command("plan"))
async def cmd_plan(message: Message):
    master_id = authorized_masters.get(message.chat.id)
    if not master_id:
        await message.answer("Сначала авторизуйтесь через /start")
        return

    events = await get_events(master_id)
    if not events:
        await message.answer("План проверок пуст.")
        return

    # Формируем текст с адресом и списком ивентов
    texts = []
    for ev in events:
        try:
            addr_card = await get_address_card(ev.address_card_id)
            addr = addr_card.address
        except:
            addr = ""
        status = "✅" if ev.is_done else "❌"
        texts.append(f"{status} {ev.type}\nАдрес: {addr}")

    full_text = "Ваш план проверок:\n\n" + "\n\n".join(texts)

    # Формируем inline-клавиатуру
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{'✅' if ev.is_done else '❌'} {ev.type}",
                    callback_data=f"done_{ev.id}"
                )
            ]
            for ev in events
        ]
    )

    await message.answer(full_text, reply_markup=buttons)

@router.callback_query(F.data.startswith("done_"))
async def process_done(callback: CallbackQuery):
    master_id = authorized_masters.get(callback.message.chat.id)
    if not master_id:
        await callback.message.answer("Сначала авторизуйтесь через /start")
        await callback.answer()
        return

    event_id = int(callback.data.split("_")[1])
    try:
        new_event = await mark_done(event_id, master_id)
        await callback.message.edit_reply_markup()  # убрать старые кнопки
        if type(new_event) is dict and new_event['result'] == 'success':
            await callback.message.answer(f'Отчёт успешно завершён!')
        else:
            await callback.message.answer(f"Переходим к этапу: {new_event.type}")
            # await cmd_plan(message=callback.message)
    except Exception:
        await callback.message.answer("Ошибка при отметке.")
    await callback.answer()

@router.message(Command("route"))
async def cmd_route(message: Message):
    await message.answer(
        "Отправьте свою геолокацию, используя кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отправить геолокацию", request_location=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

@router.message(F.location)
async def handle_location(message: Message):
    master_id = authorized_masters.get(message.chat.id)
    if not master_id:
        await message.answer("Сначала авторизуйтесь через /start")
        return

    # Пример: статичные координаты адреса
    dest_lat, dest_lon = 45.0355, 38.9753  # Краснодар

    route = await get_route(
        message.location.latitude,
        message.location.longitude,
        dest_lat,
        dest_lon,
    )
    await message.answer(
        f"Маршрут от вашей позиции до точки:\n"
        f"Расстояние: {route['distance_km']} км\n"
        f"Начало: {route['start']}\n"
        f"Конец: {route['end']}"
    )


@router.message(Command("take"))
async def cmd_take(message: Message):
    master_id = authorized_masters.get(message.chat.id)
    if not master_id:
        await message.answer("Сначала авторизуйтесь через /start")
        return

    events = await get_events(master_id)
    active = next((ev for ev in events if not ev.is_done), None)
    if active:
        await message.answer(f"У вас уже есть активная задача:\n• {active.type}")
        return

    ev = await assign_report(master_id)
    if not ev:
        await message.answer("Свободных задач для назначения пока нет.")
        return

    card = await get_address_card(ev.address_card_id)
    await message.answer(
        f"Вам назначен новый этап проверки:\n"
        f"• Этап: {ev.type}\n"
        f"• Адрес: {card.address}"
    )
