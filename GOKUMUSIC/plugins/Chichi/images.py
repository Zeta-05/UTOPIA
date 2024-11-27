import requests
from requests import get
from GOKUMUSIC import app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://lexica.qewertyy.dev"
SESSION_HEADERS = {"Host": "lexica.qewertyy.dev"}

@app.on_message(filters.command(["image"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def pinterest(_, message):
    chat_id = message.chat.id

    # Try to get the search query from the user's message
    try:
        query = message.text.split(None, 1)[1].strip()  # Remove leading/trailing spaces
        if not query:
            raise IndexError  # Will trigger the exception if query is empty
    except IndexError:
        return await message.reply("**ɢɪᴠᴇ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍**")

    # Make the request to the new API (Lexica)
    try:
        # Append the query to the URL
        response = get(f"{BASE_URL}/?q={query}", headers=SESSION_HEADERS)
        
        # Log the response for debugging
        logging.info(f"Lexica API response: Status Code {response.status_code}, Response Text: {response.text}")
        
        # Check if the response is successful
        if response.status_code == 200:
            try:
                images = response.json()
                if "images" not in images or not images["images"]:
                    return await message.reply("No images found for the given query.")
            except ValueError:
                return await message.reply("Error: Failed to decode the response from Lexica API.")
        else:
            return await message.reply(f"Error: Received invalid status code {response.status_code} from the API.")

    except Exception as e:
        logging.error(f"Error while fetching images: {str(e)}")
        return await message.reply(f"Error while fetching images: {str(e)}")

    # Prepare the media group to send images
    media_group = []
    count = 0
    msg = await message.reply(f"sᴄʀᴀᴘɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ʟᴇxɪᴄᴀ...")

    for url in images["images"][:6]:
        media_group.append(InputMediaPhoto(media=url))
        count += 1
        await msg.edit(f"=> ᴏᴡᴏ sᴄʀᴀᴘᴇᴅ ɪᴍᴀɢᴇs {count}")

    # Send the images in a media group
    try:
        await app.send_media_group(
            chat_id=chat_id,
            media=media_group,
            reply_to_message_id=message.id
        )
        return await msg.delete()

    except Exception as e:
        await msg.delete()
        logging.error(f"Error sending media group: {str(e)}")
        return await message.reply(f"ᴇʀʀᴏʀ: {str(e)}")
