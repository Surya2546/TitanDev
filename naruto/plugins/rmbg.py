import os
from asyncio import sleep

from removebg import RemoveBg
from pyrogram import filters
from naruto import naruto, Command, remove_bg_api, AdminSettings, edrep
from naruto.helpers.PyroHelpers import ReplyCheck

DOWN_PATH = "titan/"

IMG_PATH = DOWN_PATH + "image.jpg"


@naruto.on_message(filters.user(AdminSettings) & filters.command("rmbg", Command))
async def remove_bg(client, message):
    if not remove_bg_api:
        await edrep(
            message,
            text="Get the API from [Remove.bg](https://www.remove.bg/b/background-removal-api)",
            disable_web_page_preview=True,
            parse_mode="html",
        )
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        try:
            rmbg = RemoveBg(remove_bg_api, "rm_bg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + "_no_bg.png"
            await client.send_document(
                chat_id=message.chat.id,
                document=remove_img,
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True,
            )
            await message.delete()
            os.remove(remove_img)
            os.remove(IMG_PATH)
        except Exception as e:
            print(e)
            await edrep(message, text="`Something went wrong!`")
            await sleep(3)
            await message.delete()
    else:
        await edrep(message, text="Usage: reply to a photo to remove background!")
