from dotenv import load_dotenv
import os
from telethon import TelegramClient, functions, types
import re

# Загрузка переменных окружения из .env файла
load_dotenv()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
FOLDER_TITLE = os.environ.get("FOLDER_TITLE")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE")


def remove_markdown(text: str) -> str:
    # Удаление жирного текста (**text**)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    # Удаление ссылок в формате [текст](ссылка) → только текст
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    return text


async def start_parce_vacancies(message):
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start()

    resp: types.DialogFilters = await client(
        functions.messages.GetDialogFiltersRequest()
    )
    filters = resp.filters
    folders_if_not_found = []
    for folder in filters:
        if isinstance(folder, types.DialogFilter):
            folders_if_not_found.append(folder.title.text)

    folder = next(
        (
            f
            for f in filters
            if isinstance(f, types.DialogFilter) and f.title.text == FOLDER_TITLE
        ),
        None,
    )
    if not folder:
        print(f"Папка '{FOLDER_TITLE}' не найдена")
        await message.answer(f"Папка '{FOLDER_TITLE}' не найдена")
        await message.answer("Доступные папки: " + ", ".join(folders_if_not_found))
        await message.answer(
            "Папки могут быть не выдны если вы добавили их по ссылке или поделились ссылкой на папку"
        )
        await client.disconnect()
        return
    messages_to_sort = []
    for peer in folder.include_peers:
        peer_dialog = await client(
            functions.messages.GetPeerDialogsRequest(peers=[peer])
        )
        unread = peer_dialog.dialogs[0].unread_count
        if not unread:
            continue

        msgs = await client.get_messages(peer, limit=unread)

        # out.write(f"\n--- {name}: {unread} непрочитанных ---\n")
        for m in reversed(msgs):
            date = m.date.strftime("%Y-%m-%d %H:%M:%S")
            sender = (await m.get_sender()).username or str(m.sender_id)
            text = m.text or "<non-text>"
            text = remove_markdown(text)
            # Генерируем ссылку на сообщение
            try:
                peer_entity = await client.get_entity(peer)

                if peer_entity.username == None:
                    link = f"https://t.me/c/{peer_entity.id}/{m.id}"
                else:
                    link = f"https://t.me/{peer_entity.username}/{m.id}"
            except Exception:
                link = "<no-link>"
            messages_to_sort.append(
                {
                    "date": date,
                    "sender": sender,
                    "text": text,
                    "link": link,
                }
            )
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
                out.write(f"[{date}] {sender}: {text}\nLink: {link}\n\n")
            # out.write(f"[{date}] {sender}: {text}\nLink: {link}\n\n")

        # Отметка как прочитанных
        await client.send_read_acknowledge(
            entity=peer, max_id=msgs[0].id, clear_mentions=True
        )
        print(f" ✅ Отметил до ID {msgs[0].id} как прочитанные")

    print("Готово! Сохранено в", OUTPUT_FILE)
    await client.disconnect()
    return messages_to_sort

    # Реализуйте отправку сообщений в группу по вашему усмотрению
