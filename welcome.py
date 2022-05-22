# -*- coding: utf-8 -*-

# Module author: @murkamodules

from .. import loader, utils


@loader.tds
class WelcomeMod(loader.Module):
    """Welcoming new users in chat."""

    strings = {"name": "Welcome"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def welcomecmd(self, message):
        """Enable/disable welcoming new users in chat.
        Usage: .welcome <clearall (if needed)>."""
        welcome = self.db.get("Welcome", "welcome", {})
        chatid = str(message.chat_id)
        args = utils.get_args_raw(message)
        if args == "clearall":
            self.db.set("Welcome", "welcome", {})
            return await message.edit(
                "<b>[Welcome Mode]</b> All settings will be reset."
            )

        if chatid in welcome:
            welcome.pop(chatid)
            self.db.set("Welcome", "welcome", welcome)
            return await message.edit("<b>[Welcome Mode]</b> Was disabled.")

        welcome.setdefault(chatid, {})
        welcome[chatid].setdefault("message", "Welcome in this chat!")
        welcome[chatid].setdefault("is_reply", True)
        self.db.set("Welcome", "welcome", welcome)
        await message.edit("<b>[Welcome Mode]</b> Activated!")

    async def setwelcomecmd(self, message):
        """Use new welcome text for new users in
        chat.\nUsage: .setwelcome <text (optional variables: {name}; {
        chat})>; nothing."""
        welcome = self.db.get("Welcome", "welcome", {})
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        chat = await message.client.get_entity(int(chatid))
        try:
            if not args and not reply:
                return await message.edit(
                    f"<b>Welcoming of new "
                    f"users in "
                    f'"{chat.title}":</b>\n\n'
                    f"<b>Status:</b> Enabled.\n"
                    f'<b>Text:</b> {welcome[chatid]["message"]}\n\n '
                    f"<b>~ You can change the welcome text "
                    f"by using</b> "
                    f".setwelcome <text>."
                )
            else:
                if reply:
                    welcome[chatid]["message"] = reply.id
                    welcome[chatid]["is_reply"] = True
                else:
                    welcome[chatid]["message"] = args
                    welcome[chatid]["is_reply"] = False
                self.db.set("Welcome", "welcome", welcome)
                return await message.edit(
                    "<b>New welcome text was changed " "successfully!</b>"
                )
        except KeyError:
            return await message.edit(
                f'<b>Welcoming new users in "{chat.title}":</b>\n\n '
                f"<b>Status:</b> disabled"
            )

    async def watcher(self, message):
        """Hmm, why is it called so?... 🤔"""
        try:
            welcome = self.db.get("Welcome", "welcome", {})
            chatid = str(message.chat_id)
            if chatid not in welcome:
                return
            if message.user_joined or message.user_added:
                user = await message.get_user()
                chat = await message.get_chat()
                if not welcome[chatid]["is_reply"]:
                    return await message.reply(
                        (welcome[chatid]["message"]).format(
                            name=user.first_name, chat=chat.title
                        )
                    )
                msg = await self.client.get_messages(
                    int(chatid), ids=welcome[chatid]["message"]
                )
                await message.reply(msg)
        except:
            pass
