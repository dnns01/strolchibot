from twitchio.ext import commands
import config
import re
import sqlite3
from datetime import datetime, timedelta
import random


@commands.core.cog(name="LinkProtection")
class LinkProtection:
    def __init__(self, bot):
        self.bot = bot
        self.permit = {}

    def get_links(self, message):
        links = []
        if matches := re.findall(r"(?:https?:\/\/)?([\da-z\.-]+\.[a-z\.]{2,6}|[\d\.]+)(?:[\/:?=&#]{1}[\da-z\.-]+)*[\/\?]?",
                   message):
            print("Matches:", matches)
            for match in matches:
                if not re.match(r"^\.+$", match) and "." in match:
                    print("Jo... ")
                    links.append(match)

            if len(links) > 0:
                return links

        return None

    def lookup_blacklist(self, link):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT url from strolchibot_linkblacklist where url like ? or url like ?', ("http://" + link, "https://" + link,))
        link = c.fetchone()
        conn.close()
        return link is not None

    def lookup_whitelist(self, link):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT url from strolchibot_linkwhitelist where url like ? or url like ?', ("http://" + link, "https://" + link,))
        link = c.fetchone()
        conn.close()
        return link is not None


    async def event_message(self, message):
        if message.author.is_mod:
            return

        # Mods are always allowed to post links. So if we reach this point, the author of the message is not a mod,
        # and we can start checking, whether the message contains a link or not
        if links := self.get_links(message.content):
            print(message.content, message.author, links)
            for link in links:
                print(link)
                if self.lookup_blacklist(link):
                    print("Sorry bro, aber der Link geht ja mal gar nicht... nicht mal für nen Sub oder jemand mit Permit.... ")
                    await message.channel.timeout(message.author.name, 1)
                    return

            for link in links:
                if self.lookup_whitelist(link):
                    print("Geil, dein Link steht auf der Whitelist.")
                    return

            # Reaching this point, we now that the message contains at least one link. Now we can check,
            # if Link Protection is turned on or not. If it is turned off, we don't need further checks, because links
            # are allowed.
            if not config.get_bool("LinkProtectionActive"):
                return

            # Reaching this point means, that the message contains a link, the author is not a mod and Link Protection
            # is turned on. Next step is to check, if Subs are permitted to post links and if the author of the message
            # is a sub. If true, no further processing neccessary, posting a link is allowed.
            if message.author.is_subscriber and config.get_bool("LinkProtectionPermitSubs"):
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
