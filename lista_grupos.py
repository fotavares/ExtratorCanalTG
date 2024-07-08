from pyrogram import Client
from cache import Cache
import glob
import os
import time

# ~~~~~~ CONFIG ~~~~~~~~ #
ACCOUNT = "user"
COPIED_FROM = -1002106230189
COPIED_TO = -1002163642260
# ~~~~~~~~~~~~~~~~~~~~~~ #

copy_protected = None


async def progress(current, total):
    # Imprime o percentual de download
    down = f"{current * 100 / total:.1f}%"
    print(down)


app = Client(ACCOUNT)
app.start()

'''Passo 1'''
# Pega todos os Chats/Grupos/Canais e lista com a ID
# Lists all chats/groups/channels with ID
chats = app.get_dialogs()
num = 0
ids = []
for chat in chats:
    try:
        print((chat.chat.title or chat.chat.first_name) +
              ' - ' + str(chat.chat.id))
    except:
        pass


'''Passo 2'''
# Entra no Canal/Grupo/Chat e pega o historico todo, copiando para outro canal (se nao for protegido) ou baixando as midias
# Reads the whole history and forward to other channel (if not copy protected) or downloading media
message = app.get_chat_history(COPIED_FROM)


# Salva
for m in message:
    if copy_protected is None:
        copy_protected = m.chat.has_protected_content

    if m.video:
        if not Cache.is_a_repost('All', m.video.file_unique_id):
            Cache.save_post_id('All', m.video.file_unique_id)
            if copy_protected:
                app.download_media(m, 'cache/'+str(m.id) +
                                   '.mp4', progress=progress)
            else:
                app.copy_message(COPIED_TO, COPIED_FROM, m.id, caption='')

    if m.photo:
        if not Cache.is_a_repost('All', m.photo.file_unique_id):
            Cache.save_post_id('All', m.photo.file_unique_id)
            if copy_protected:
                app.download_media(m, 'cache/'+str(m.id) +
                                   '.jpg', progress=progress)
            else:
                app.copy_message(COPIED_TO, COPIED_FROM, m.id, caption='')


'''Passo 3'''
if copy_protected:
    # Envia todos os arquivos da pasta para o canal
    # Sends media to channel (if protected)
    app.get_chat(COPIED_TO)

    for file in glob.glob("./cache/*.jpg"):
        app.send_photo(chat_id=COPIED_TO, photo=file,
                       progress=progress, disable_notification=True)
        os.remove(file)
        time.sleep(1)

    for file in glob.glob("./cache/*.mp4"):
        app.send_video(COPIED_TO, video=file, progress=progress,
                       disable_notification=True, supports_streaming=True)
        os.remove(file)
        time.sleep(1)
