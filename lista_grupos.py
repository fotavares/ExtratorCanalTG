from pyrogram import Client
import glob
import os
import time

# ~~~~~~ CONFIG ~~~~~~~~ #
ACCOUNT = "user"
# ~~~~~~~~~~~~~~~~~~~~~~ #


async def progress(current, total):
    # Imprime o percentual de download
    down = f"{current * 100 / total:.1f}%"
    print(down)


app = Client(ACCOUNT)
app.start()

'''Passo 1'''
# Pega todos os Chats/Grupos/Canais e lista com a ID
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
# Entra no Canal/Grupo/Chat e pega o historico todo
message = app.get_chat_history(-1001867528704)

# Salva
for m in message:
    if m.video:
        app.download_media(m, str(m.id)+'.mp4', progress=progress)
    if m.photo:
        app.download_media(m, str(m.id)+'.jpg', progress=progress)


'''Passo 3'''
# Envia todos os arquivos da pasta para o canal
CANAL = -1002163642260

app.get_chat(CANAL)

for file in glob.glob("./cache/*.jpg"):
    app.send_photo(chat_id=CANAL, photo=file,
                   progress=progress, disable_notification=True)
    os.remove(file)
    time.sleep(1)

for file in glob.glob("./cache/*.mp4"):
    app.send_video(CANAL, video=file, progress=progress,
                   disable_notification=True, supports_streaming=True)
    os.remove(file)
    time.sleep(1)
