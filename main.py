from PIL import Image
import random
from telethon import TelegramClient, events, sync
import logging
import os
from html_telegraph_poster.upload_images import upload_image
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_hash = "set yours"
api_id = "int code  - set yours"

client = TelegramClient("sessione_in_corso", api_id, api_hash)


@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def pfphandler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        image = await client.download_profile_photo(sender)
        await event.respond('Saved your photo {}'.format(sender.username))
        os.remove(image)


@client.on(events.NewMessage(outgoing=True, pattern=r'\.status'))
async def aliveHandler(event):
    chat = await event.get_chat()
    await client.edit_message(event.message, "✅ STATUS ONLINE ✅")


@client.on(events.NewMessage(outgoing=True, pattern=r'\.quote'))
async def quotlyHandler(event):
    chat = await event.get_chat()
    await client.edit_message(event.message, "Caricamento...")
    rep_msg = await event.get_reply_message()
    x = await rep_msg.forward_to('@quotLyBot')
    async with client.conversation('@quotLyBot') as conv:
        xx = await conv.get_response(x.id)
        await client.send_message(chat, xx)
        await event.message.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'\.add'))
async def addStickerHandler(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        me = await client.get_me()
        pack = 1
        emoji = "⚠️"
        chat = await event.get_chat()
        nickname = f"@{me.username}'s sticker pack {pack}"
        n = 1
        num = " "
        ##y = random.random()
        ##num = str(y)
        num = 104

        packname = f"laiffodev_{num}_{pack}"
        sticker = await reply_msg.download_media()
        if sticker.endswith((".jpg", ".png")):
            file = "sticker.png"
            c = Image.open(sticker)
            c = c.resize(512, 512)
            c.save(file, optimaze=True, quality=10)
            os.remove(sticker)
        elif sticker and sticker.endswith(".webp"):
            file = "sticker.png"
            c = Image.open(sticker)
            c = c.resize((512, 512))
            c.save(file, optimaze=True, quality=10)
            os.remove(sticker)
        else:
            return await client.edit_message(event.message, "Rispondi a uno sticker o a un immagine")
    x = await client.edit_message(event.message, "Caricamento...")
    cmd = "/newpack"
    async with client.conversation("@stickers") as conv:
        await conv.send_message("/addsticker")
        await conv.get_response()
        await client.send_read_acknowledge(conv.chat_id)
        await conv.send_message(packname)
        xx = await conv.get_response()
        await client.send_read_acknowledge(conv.chat_id)
        if xx.text == "Invalid set selected.":
            await x.edit("Creando un nuovo pack...")
            await conv.send_message(cmd)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(nickname)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_file(file, force_document=True)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(emoji)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message("/publish")
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message("/skip")
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(packname)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await x.edit(f"'Sticker aggiunto al tuo pack correttamente'\n[Qui](https://t.me/addstickers/{packname}) '",
                         parse_mode="md")
        else:
            await conv.send_file(file, force_document=True)
            await conv.get_response()
            await client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(emoji)
            await conv.get_response()
            await conv.send_message("/done")
            await x.edit(f"'Sticker aggiunto al tuo pack correttamente'\n[Qui](https://t.me/addstickers/{packname}) '",
                         parse_mode="md")


@client.on(events.NewMessage(outgoing=True, pattern=r'\.h'))
async def helpHandler(event):
    await client.edit_message(event.message,
                              "'Comandi UserBot Laiffiano'\n[Qui](https://telegra.ph/Comandi-UserBot-Laiffiano-03-16)",
                              parse_mode="md", link_preview=False)


@client.on(events.NewMessage(outgoing=True, pattern=r'\.id'))
async def idHandler(event):
    reply = await event.get_reply_message()
    sender_ = reply.sender
    await client.edit_message(event.message, "ID: " + str(sender_.id))


@client.on(events.NewMessage(outgoing=True, pattern=r'\.thp'))
async def TeleHPHandler(event):
    chat = await event.get_chat()
    replied = await event.get_reply_message()
    try:
        image = await replied.download_media()
        up = upload_image(image)
    except:
        return await client.edit_message(event.message, "Non è un immagine")

    await client.edit_message(event.message, "Caricamento...")
    await client.edit_message(event.message, up)
    os.remove(image)


@client.on(events.NewMessage(outgoing=True, pattern=r'\.profile'))
async def profileHandler(event):
    await client.edit_message(event.message, "Caricamento...")
    chat = await event.get_chat()
    reply = await  event.get_reply_message()
    sender = reply.sender
    full = await client(GetFullUserRequest(sender))
    bio = full.full_user.about
    id_target = full.full_user.id
    name = sender.first_name
    username = sender.username
    image = await client.download_profile_photo(sender)
    await client.delete_messages(chat, event.message.id)
    await client.send_file(chat, image, caption=f"💬 NOME --> {name}\n"
                                                f"💬 USERNAME --> {username}\n"
                                                f"📌 ID --> {id_target}\n"
                                                f"\n 🖥 BIO --> {bio}\n")
    os.remove(image)


async def main():
    await client.send_message('me', 'Hello, myself!')


client.start()
client.run_until_disconnected()
