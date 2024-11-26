import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from GOKUMUSIC import app
from GOKUMUSIC.utils.database import add_served_user, is_on_off
from GOKUMUSIC.utils.inline import start_panel
from Strings import get_string

NEXI_VID = [
    "https://envs.sh/K-d.mp4"
]

async def send_start_video(chat_id):
    """Send a random start video."""
    try:
        video_url = random.choice(NEXI_VID)
        sent_video = await app.send_video(chat_id=chat_id, video=video_url, supports_streaming=True)
        return sent_video
    except Exception as e:
        print(f"Error sending video: {e}")
        return None

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    caption = _["start_2"].format(message.from_user.mention, app.mention)

    # Send the start video first
    video_message = await send_start_video(message.chat.id)

    if video_message:
        # Wait for the video to be sent before sending the next message
        await app.send_message(
            chat_id=message.chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(private_panel(_)),
        )
    else:
        print("Video not sent")

    # Log the start event
    if await is_on_off(2):
        await app.send_message(
            chat_id=LOGGER_ID,
            text=f"{message.from_user.mention} started the bot.\n\n"
                 f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                 f"<b>Username:</b> @{message.from_user.username}",
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    caption = _["start_1"].format(app.mention)

    # Send the start video first
    video_message = await send_start_video(message.chat.id)

    if video_message:
        # Wait briefly before sending the next message
        await app.send_message(
            chat_id=message.chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(out),
        )

    await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)

                # Send the start video first
                video_message = await send_start_video(message.chat.id)

                if video_message:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=_["start_3"].format(
                            message.from_user.mention,
                            app.mention,
                            message.chat.title,
                            app.mention,
                        ),
                        reply_markup=InlineKeyboardMarkup(out),
                    )

                await add_served_chat(message.chat.id)

        except Exception as ex:
            print(f"Error welcoming new members: {ex}")


if __name__ == "__main__":
    app.run()
