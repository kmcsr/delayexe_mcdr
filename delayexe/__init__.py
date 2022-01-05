
import mcdreforged.api.all as MCDR
from .utils import *
from . import globals as GL
from . import commands as CMD

__all__ = [
	'add_delay_task'
]

add_delay_task, clear_delay_task = CMD.add_delay_task, CMD.clear_delay_task

def on_load(server: MCDR.PluginServerInterface, prev_module):
	if prev_module is None:
		log_info('Delay ExE is on LOAD')
	else:
		log_info('Delay ExE is on RELOAD')
	GL.init(server)
	CMD.register(server)

def on_unload(server: MCDR.PluginServerInterface):
	log_info('Delay ExE is on UNLOAD')
	GL.destory()

def on_info(server: MCDR.ServerInterface, info: MCDR.Info):
  CMD.on_info(server, info)

def on_player_left(player: str, info: MCDR.Info):
  CMD.on_player_left(player, info)
