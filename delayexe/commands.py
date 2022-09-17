
import mcdreforged.api.all as MCDR
from .utils import *
from .api import *
from . import globals as GL

Prefix = '!!de'

def register(server: MCDR.PluginServerInterface):
	server.register_command(
		MCDR.Literal(Prefix).
		runs(command_help).
		then(GL.get_config().literal('help').runs(command_help)).
		then(GL.get_config().literal('query').runs(command_query)).
		then(GL.get_config().literal('restart').runs(command_restart)).
		then(GL.get_config().literal('run').
			then(MCDR.GreedyText('command').runs(lambda src, ctx: command_run(src, ctx['command'])))).
		then(GL.get_config().literal('cancel').runs(command_cancel)).
		then(GL.get_config().literal('reload').runs(command_config_load)).
		then(GL.get_config().literal('save').runs(command_config_save))
	)

def command_help(source: MCDR.CommandSource):
	send_message(source, GL.BIG_BLOCK_BEFOR, tr('help_msg', Prefix), GL.BIG_BLOCK_AFTER, sep='\n')

def command_query(source: MCDR.CommandSource):
	send_message(source, GL.BIG_BLOCK_BEFOR)
	send_message(source, tr('tasks.all_list', len(delaylist)), *['- ' + c for c in delaylist if isinstance(c, str)])
	send_message(source, GL.BIG_BLOCK_AFTER)

def command_restart(source: MCDR.CommandSource):
	add_delay_task(new_thread(source.get_server().restart))

def command_run(source: MCDR.CommandSource, cmd: str):
	add_delay_task(cmd)

def command_cancel(source: MCDR.CommandSource):
	clear_delay_task()

@new_thread
def command_config_load(source: MCDR.CommandSource):
	GL.DLEConfig.load(source)

@new_thread
def command_config_save(source: MCDR.CommandSource):
	GL.get_config().save(source)
