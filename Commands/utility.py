import asyncio

def read_file(filename):
        file = open(f'./Data/{filename}.txt', 'r', encoding="UTF-8").readlines()
        file_text = ""
        for line in file:
            file_text += line
        return file_text

async def send_edit(channel, msg, edit_msg, delay):
    tk = await channel.send(msg)
    await asyncio.sleep(delay)
    await tk.edit(content=edit_msg)