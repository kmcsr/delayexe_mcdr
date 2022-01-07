
import re

import mcdreforged.api.all as MCDR
from .utils import *
from . import globals as GL

Prefix = '!!de'

HelpMessage = '''
{0} help 显示帮助信息
{0} restart 延时重启
{0} run <command> 延迟执行
{0} cancel 撤销所有任务
{0} reload 重新加载配置文件
{0} save 保存配置文件
'''.strip().format(Prefix)

delaylist = []

def add_delay_task(task):
	delaylist.append(task)
	GL.SERVER_INS.execute('list')

def clear_delay_task():
	delaylist.clear()

_PLAYER_COUNT_RE = re.compile(r'There are (\d+) of a max of (\d+) players online.*')
def on_info(server: MCDR.ServerInterface, info: MCDR.Info):
	if info.is_from_server:
		ct = _PLAYER_COUNT_RE.fullmatch(info.content)
		if ct is not None:
			online = int(ct[1])
			if online == 0:
				while len(delaylist) > 0:
					c = delaylist.pop(0)
					if isinstance(c, str):
						server.execute(c)
					else:
						c()

def on_player_left(player: str, info: MCDR.Info):
	info.get_server().execute('list')

def register(server: MCDR.PluginServerInterface):
	server.register_command(
		MCDR.Literal(Prefix).
		runs(command_help).
		then(GL.Config.literal('help').runs(command_help)).
		then(GL.Config.literal('query').runs(command_query)).
		then(GL.Config.literal('restart').runs(command_restart)).
		then(GL.Config.literal('run').
			then(MCDR.GreedyText('command').runs(lambda src, ctx: command_run(src, ctx['command'])))).
		then(GL.Config.literal('cancel').runs(command_cancel)).
		then(GL.Config.literal('reload').runs(command_config_load)).
		then(GL.Config.literal('save').runs(command_config_save))
	)

def command_help(source: MCDR.CommandSource):
	send_block_message(source, HelpMessage)

def command_query(source: MCDR.CommandSource):
	send_block_message(source, '当前共有{}个任务:'.format(len(delaylist)), *['- ' + c for c in delaylist if isinstance(c, str)])

def command_restart(source: MCDR.CommandSource):
	add_delay_task(new_thread(source.get_server().restart))

def command_run(source: MCDR.CommandSource, cmd: str):
	add_delay_task(cmd)

def command_cancel(source: MCDR.CommandSource):
	clear_delay_task()

@new_thread
def command_config_load(source: MCDR.CommandSource):
	GL.Config = server.load_config_simple(target_class=GL.SMBConfig, source_to_reply=source)

@new_thread
def command_config_save(source: MCDR.CommandSource):
	GL.Config.save()
	send_message(source, 'Save config file SUCCESS')
