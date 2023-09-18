from telethon import TelegramClient, events
from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton
from decouple import config
import cv2
import os
import subprocess
import uuid
import mimetypes


API_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("BOT_TOKEN")


bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

picture_path = "best_offer.png"

user_states = {}


START_MESSAGE = """
Привет, это бот уникализатор видео. 
Для выбора режима уникализации введи /menu,
"""

MIRROR_HORIZONTAL_MESSAGE = """
Выбрано действие: Отзеркалить
Теперь отправь видео для уникализации."""

CHANGE_BITRATE_MESSAGE = """
Выбрано действие: Изменить битрейт
Теперь отправь видео для уникализации."""

ADD_A_PICTURE_MESSAGE = """
Выбрано действие: Наложить картинку
Теперь отправь видео для уникализации."""


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(START_MESSAGE)


@bot.on(events.NewMessage(pattern="/menu"))
async def menu(event):
    keyboard_buttons = ReplyKeyboardMarkup(
        [
            KeyboardButtonRow([KeyboardButton(text="Изменить битрейт")]),
            KeyboardButtonRow([KeyboardButton(text="Отзеркалить")]),
            KeyboardButtonRow([KeyboardButton(text="Наложить картинку")]),
        ]
    )
    await event.respond("Выбери действие:", buttons=keyboard_buttons)


@bot.on(events.NewMessage(pattern="(Изменить битрейт|Отзеркалить|Наложить картинку)"))
async def set_state(event):
    global user_states

    user_id = event.sender_id
    new_state = event.pattern_match.group(1)
    

    if new_state == "Изменить битрейт":
        current_state = "change_bitrate"
        user_states[user_id] = current_state
        await event.respond(CHANGE_BITRATE_MESSAGE)

    elif new_state == "Отзеркалить":
        current_state = "mirror_horizontal"
        user_states[user_id] = current_state
        await event.respond(MIRROR_HORIZONTAL_MESSAGE)

    elif new_state == "Наложить картинку":
        current_state = "add_a_picture"
        user_states[user_id] = current_state
        await event.respond(ADD_A_PICTURE_MESSAGE)



@bot.on(events.NewMessage)
async def handle_message(event):
    global user_states

    user_id = event.sender_id

    current_state = user_states.get(user_id)

    if (
        current_state == "change_bitrate"
        or current_state == "mirror_horizontal"
        or current_state == "add_a_picture"
    ):
        if (
            event.media
            and hasattr(event.media, "document")
            and "video" in event.media.document.mime_type
        ):
            video = await event.client.download_media(event.media.document)
            
            if current_state == "change_bitrate":
                await change_bitrate(event, video)
            elif current_state == "mirror_horizontal":
                await mirror_horizontal(event, video)
            elif current_state == "add_a_picture":
                await add_a_picture(event, video)


async def mirror_horizontal(event, video_path):
    
    unique_filename = f"{str(uuid.uuid4())}.mp4"
    unique_video_path = os.path.join(unique_filename)

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-vf",
        "hflip",
        "-map_metadata",
        "-1",
        "-c:a",
        "copy",
        unique_video_path,
    ]
    subprocess.call(ffmpeg_cmd)

    mime_type, _ = mimetypes.guess_type(unique_video_path)

    await event.client.send_file(event.chat_id, unique_video_path, mime_type=mime_type)

    os.remove(video_path)
    os.remove(unique_video_path)


async def add_a_picture(event, video_path):
    global picture_path

    unique_filename = f"{str(uuid.uuid4())}.mp4"
    unique_video_path = os.path.join(unique_filename)

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-i",
        picture_path,
        "-filter_complex",
        f"[0:v][1:v]overlay=W-w-10:H-h-10[v]",
        "-map",
        "[v]",
        "-map",
        "0:a",
        "-map_metadata",
        "-1",
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        unique_video_path,
    ]
    subprocess.call(ffmpeg_cmd)

    mime_type, _ = mimetypes.guess_type(unique_video_path)

    await event.client.send_file(event.chat_id, unique_video_path, mime_type=mime_type)

    os.remove(video_path)
    os.remove(unique_video_path)


async def change_bitrate(event, video_path):

    unique_filename = f"{str(uuid.uuid4())}.mp4"
    unique_video_path = os.path.join(unique_filename)

    cap = cv2.VideoCapture(video_path)
    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS))
    file_size = os.path.getsize(video_path)
    bitrate = (file_size * 8) / duration

    target_bitrate = int(bitrate * 0.7)

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-b:v",
        str(target_bitrate),
        "-map_metadata",
        "-1",
        unique_video_path,
    ]
    subprocess.call(ffmpeg_cmd)

    mime_type, _ = mimetypes.guess_type(unique_video_path)

    await event.client.send_file(event.chat_id, unique_video_path, mime_type=mime_type)

    os.remove(video_path)
    os.remove(unique_video_path)


def main():
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()
