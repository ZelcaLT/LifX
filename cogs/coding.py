
import io
import os
import re
import unicodedata
import zlib
from typing import Dict
import aiohttp

import nextcord 
from nextcord.ext import commands

from utils import fuzzy


class SphinxObjectFileReader:

    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')


class Documention(commands.Cog, name="📄Docs"):
    """Shows all docs about Nextcord"""
    # full credit to https://github.com/Rapptz/RoboDanny
    def __init__(self, bot):
        self.bot = bot

    def parse_object_inv(self, stream: SphinxObjectFileReader, url: str) -> Dict:
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]  # not needed

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError("Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            key = (
                key.replace("nextcord.ext.commands.", "")
                .replace("nextcord.ext.menus.", "")
                .replace("nextcord.ext.ipc.", "")
                .replace("nextcord.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_docs_lookup_table(self, page_types):
        session = aiohttp.ClientSession()
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError('Cannot build docs lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._docs_cache = cache
        await session.close()

    async def do_docs(self, ctx, key, obj):
        page_types = {
            'master': 'https://nextcord.readthedocs.io/en/latest',
            'menus': 'https://nextcord-ext-menus.readthedocs.io/en/latest',
            'ipc': 'https://nextcord-ext-ipc.readthedocs.io/en/latest',
            'python': 'https://docs.python.org/3',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_docs_cache'):
            await ctx.trigger_typing()
            await self.build_docs_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)
        obj = re.sub(r'^(?:nextcord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('master'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(nextcord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._docs_cache[key].items())

        def transform(tup):
            return tup[0]

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:13]

        e = nextcord.Embed(colour=nextcord.Colour.blurple())
        e.set_author(name="LifX", icon_url="https://cdn.discordapp.com/avatars/922489691020873758/3acc5460a031443e4b98745ce0dbea5e.webp?size=40")
        e.set_footer(text=f'Requested By {ctx.author}', icon_url=f'{ctx.author.avatar.url}')
        e.set_thumbnail(url="https://avatars.githubusercontent.com/u/93326875?v=4")
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, nextcord.Message):
            refer = ref.resolved.to_reference()
        await ctx.send(embed=e, reference=refer)

    @commands.group(name="rtfm", description="Get info on a nextcord entity.", invoke_without_command=True, aliases=["docs", "nextcord", "doc", "rtfd", "nc"])
    async def docs_group(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "master", obj)

    @docs_group.command(name="menus")
    async def docs_menu_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "menus", obj)

    @docs_group.command(name="ipc")
    async def docs_ipc_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "ipc", obj)

    @docs_group.command(name="python", aliases=["py"])
    async def docs_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "python", obj)

    @commands.command(help="delete cache of docs (owner only)", aliases=["purge-docs", "deldocs"])
    @commands.is_owner()
    async def docscache(self, ctx: commands.Context):
        del self._docs_cache
        embed = nextcord.Embed(title="Purged docs cache.", color=nextcord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.command(name="charinfo", description="Shows info about a unicode character.", aliases=["char", "unicode", "uni"])
    async def charinfo(self, ctx, *, characters: str):
        """
        Shows you information about a number of characters.
        Only up to 25 characters at a time.
        """
        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <https://www.fileformat.info/info/unicode/char/{digit}>'

        msg = '\n'.join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send('Output too long to display.')
        await ctx.send(msg)





def setup(bot):
    bot.add_cog(Documention(bot))