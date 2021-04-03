import re
import sqlite3
from datetime import datetime, timedelta

import config
from twitchio.ext import commands


@commands.core.cog(name="LinkProtection")
class LinkProtection:
    def __init__(self, bot):
        self.bot = bot
        self.permit = {}

    def lookup_blacklist(self, link):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT url from strolchibot_linkblacklist')
        urls = c.fetchall()
        conn.close()
        return self.is_listed(link, [url[0] for url in urls])

    def lookup_whitelist(self, link):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT url from strolchibot_linkwhitelist')
        urls = c.fetchall()
        conn.close()
        return self.is_listed(link, [url[0] for url in urls])

    def is_listed(self, link, urls):
        for url in urls:
            if link.startswith(url.split("://")[1]):
                return True

        return False

    async def event_message(self, message):
        if message.author.is_mod:
            return

        # Mods are always allowed to post links. So if we reach this point, the author of the message is not a mod,
        # and we can start checking, whether the message contains a link or not
        if links := re.findall(r"(?:https?:\/\/)?((?:[a-zA-Z0-9_-]+\.)+[a-z]{2,}[a-zA-Z0-9?&=_\/-]*)", message.content):
            print(links)
            for link in links:
                if self.lookup_blacklist(link):
                    await message.channel.timeout(message.author.name, 1)
                    return

            for link in links:
                if self.lookup_whitelist(link):
                    return

            # Reaching this point, we now that the message contains at least one link. Now we can check,
            # if Link Protection is turned on or not. If it is turned off, we don't need further checks, because links
            # are allowed.
            if not config.get_bool("LinkProtectionActive"):
                return

            # Reaching this point means, that the message contains a link, the author is not a mod and Link Protection
            # is turned on. Next step is to check, if Subs are permitted to post links and if the author of the message
            # is a sub. If true, no further processing neccessary, posting a link is allowed.
            if self.bot.is_subscriber(message.author) and config.get_bool("LinkProtectionPermitSubs"):
                return

            # Reaching this point means, the author is not a mod, the message contains a link and links protection is
            # turned on. Furthermore, the author is either not a sub, or subs are not permitted to post links.
            # Now we need to check, whether the user is permitted through the whitelist.
            if self.is_user_whitelisted(message.author):
                return

            # Ok, we reached this point! Time for action!!!
            await message.channel.timeout(message.author.name, 1)

    def is_user_whitelisted(self, user):
        if self.has_user_permanent_permit(user):
            return True
        elif until := self.permit.get(user.name):
            return until >= datetime.now()
        else:
            return False

    @staticmethod
    def has_user_permanent_permit(user):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT nick from strolchibot_linkpermit where nick = ?', (user.name,))
        nick = c.fetchone()
        conn.close()

        return nick is not None

    @staticmethod
    def give_user_permanent_permit(user):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('INSERT INTO strolchibot_linkpermit (nick) VALUES(?)', (user,))
        conn.commit()
        conn.close()

    @commands.command(name="permit")
    async def cmd_permit(self, ctx, user, permanent=None):
        if user[0] == "@":
            user = user[1:]

        if ctx.author.is_mod:
            if permanent:
                self.give_user_permanent_permit(user)
            else:
                self.permit[user] = datetime.now() + timedelta(seconds=120)
