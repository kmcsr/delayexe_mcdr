
import mcdreforged.api.all as MCDR

from .globals import *
from .utils import *
from .api import *
from .api import delaylist

Prefix = '!!de'

def register(server: MCDR.PluginServerInterface):
	cfg = get_config()
	server.register_help_message(Prefix, 'Delay ExE help message')
	server.register_command(
		MCDR.Literal(Prefix).
		runs(command_help).
		then(cfg.literal('help').runs(command_help)).
		then(cfg.literal('query').runs(command_query)).
		then(cfg.literal('restart').runs(command_restart)).
		then(cfg.literal('run').
			then(MCDR.GreedyText('command').runs(lambda src, ctx: command_run(src, ctx['command'])))).
		then(cfg.literal('cancel').runs(command_cancel)).
		then(cfg.literal('reload').runs(command_config_load))
	)

def command_help(source: MCDR.CommandSource):
	send_message(source, BIG_BLOCK_BEFOR, tr('help_msg', Prefix), BIG_BLOCK_AFTER, sep='\n')

def command_query(source: MCDR.CommandSource):
	send_message(source, BIG_BLOCK_BEFOR)
	send_message(source, tr('tasks.all_list', len(delaylist.d)), *['- ' + c for c in delaylist.d if isinstance(c, str)])
	send_message(source, BIG_BLOCK_AFTER)

def command_restart(source: MCDR.CommandSource):
	add_delay_task(new_thread(source.get_server().restart))

def command_run(source: MCDR.CommandSource, cmd: str):
	add_delay_task(cmd)

def command_cancel(source: MCDR.CommandSource):
	clear_delay_task()

@new_thread
def command_config_load(source: MCDR.CommandSource):
	get_config().load()
	send_message(source, MSG_ID, 'Config file reloaded')
