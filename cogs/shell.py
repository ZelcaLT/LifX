
import os 
import aiofiles
import pickle
import nextcord
import aiosqlite
import urllib
import random
import config
import io
import requests
from cogs import _doc
import contextlib
import asyncio
import collections
from jishaku.codeblocks import codeblock_converter
from jishaku.exception_handling import ReplResponseReactor
from nextcord.ext.commands.cooldowns import BucketType
from jishaku.features.baseclass import Feature
from jishaku.flags import Flags
from nextcord.ext import ipc, commands
from jishaku.functools import AsyncSender
from datetime import datetime, timezone
from jishaku.paginators import PaginatorInterface, WrappedPaginator, use_file_check
from jishaku.repl import AsyncCodeExecutor, Scope, all_inspections, disassemble, get_var_dict_from_ctx
from hashlib import algorithms_available as algorithms
# from _tio import Tio, TioRequest

CommandTask = collections.namedtuple("CommandTask", "index ctx task")

class Shell(commands.Cog, name="👩‍💻Python Tests"):
    """Run some python code"""
    def __init__(self, bot, *args, **kwargs):
        self._scope = Scope()
        self.retain = Flags.RETAIN
        self.start_time: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.tasks = collections.deque()
        self.task_count: int = 0
        self.last_result = None
        self.bot = bot

    documented = {
        'c': _doc.c_doc,
        'cpp': _doc.cpp_doc,
        'haskell': _doc.haskell_doc,
        'python': _doc.python_doc
    }


    @commands.Cog.listener()
    async def on_ready(self):
        name = self.qualified_name
        print(f"Loaded {name}")

    @contextlib.contextmanager
    def submit(self, ctx: commands.Context):
        """
        A context-manager that submits the current task to jishaku's task list
        and removes it afterwards.
        Parameters
        -----------
        ctx: commands.Context
            A Context object used to derive information about this command task.
        """

        self.task_count += 1

        try:
            current_task = asyncio.current_task()  # pylint: disable=no-member
        except RuntimeError:
            # asyncio.current_task doesn't document that it can raise RuntimeError, but it does.
            # It propagates from asyncio.get_running_loop(), so it happens when there is no loop running.
            # It's unclear if this is a regression or an intentional change, since in 3.6,
            #  asyncio.Task.current_task() would have just returned None in this case.
            current_task = None

        cmdtask = CommandTask(self.task_count, ctx, current_task)

        self.tasks.append(cmdtask)

        try:
            yield cmdtask
        finally:
            if cmdtask in self.tasks:
                self.tasks.remove(cmdtask)




    @property
    def scope(self):
        """
        Gets a scope for use in REPL.
        If retention is on, this is the internal stored scope,
        otherwise it is always a new Scope.
        """

        if self.retain:
            return self._scope
        return Scope()

    @commands.command(parent="jsk",description="Turn variable retention for REPL on or off. Provide no argument for current status.", name="retain")
    async def jsk_retain(self, ctx: commands.Context, *, toggle: bool = None):
        """

        """

        if toggle is None:
            if self.retain:
                return await ctx.send("Variable retention is set to ON.")

            return await ctx.send("Variable retention is set to OFF.")

        if toggle:
            if self.retain:
                return await ctx.send("Variable retention is already set to ON.")

            self.retain = True
            self._scope = Scope()
            return await ctx.send("Variable retention is ON. Future REPL sessions will retain their scope.")

        if not self.retain:
            return await ctx.send("Variable retention is already set to OFF.")

        self.retain = False
        return await ctx.send("Variable retention is OFF. Future REPL sessions will dispose their scope when done.")

    async def jsk_python_result_handling(self, ctx: commands.Context, result):  # pylint: disable=too-many-return-statements
        """
        Determines what is done with a result when it comes out of jsk py.
        This allows you to override how this is done without having to rewrite the command itself.
        What you return is what gets stored in the temporary _ variable.
        """

        if isinstance(result, nextcord.Message):
            return await ctx.send(f"<Message <{result.jump_url}>>")

        if isinstance(result, nextcord.File):
            return await ctx.send(file=result)

        if isinstance(result, nextcord.Embed):
            return await ctx.send(embed=result)

        if isinstance(result, PaginatorInterface):
            return await result.send_to(ctx)

        if not isinstance(result, str):
            # repr all non-strings
            result = repr(result)

        # Eventually the below handling should probably be put somewhere else
        if len(result) <= 2000:
            if result.strip() == '':
                result = "\u200b"

            return await ctx.send(result.replace(self.bot.http.token, "[token omitted]"))

        if use_file_check(ctx, len(result)):  # File "full content" preview limit
            # Discord's desktop and web client now supports an interactive file content
            #  display for files encoded in UTF-8.
            # Since this avoids escape issues and is more intuitive than pagination for
            #  long results, it will now be prioritized over PaginatorInterface if the
            #  resultant content is below the filesize threshold
            return await ctx.send(file=nextcord.File(
                filename="output.py",
                fp=io.BytesIO(result.encode('utf-8'))
            ))

        # inconsistency here, results get wrapped in codeblocks when they are too large
        #  but don't if they're not. probably not that bad, but noting for later review
        paginator = WrappedPaginator(prefix='```py', suffix='```', max_size=1985)

        paginator.add_line(result)

        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

    @commands.command(name="py", description="Runs python code within the bot. (mostly for tests)",aliases=["python"])
    async def jsk_python(self, ctx: commands.Context, *, argument: codeblock_converter):
        """
        Direct evaluation of Python code.
        """

        arg_dict = get_var_dict_from_ctx(ctx, Flags.SCOPE_PREFIX)
        arg_dict["_"] = self.last_result

        scope = self.scope

        try:
            async with ReplResponseReactor(ctx.message):
                with self.submit(ctx):
                    executor = AsyncCodeExecutor(argument.content, scope, arg_dict=arg_dict)
                    async for send, result in AsyncSender(executor):
                        if result is None:
                            continue

                        self.last_result = result

                        send(await self.jsk_python_result_handling(ctx, result))

        finally:
            scope.clear_intersection(arg_dict)




def setup(bot):
    bot.add_cog(Shell(bot))


