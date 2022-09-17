
import mcdreforged.api.all as MCDR

globals_ = globals
from . import constants
from . import globals as GL
from .utils import *
from . import api
from . import commands as CMD

__all__ = []

export_pkg(globals_(), api)
export_pkg(globals_(), constants)

def on_load(server: MCDR.PluginServerInterface, prev_module):
	if prev_module is None:
		log_info('Delay ExE is on LOAD')
	else:
		log_info('Delay ExE is on RELOAD')
	GL.init(server)
	api.on_load(server)
	CMD.register(server)

def on_unload(server: MCDR.PluginServerInterface):
	log_info('Delay ExE is on UNLOAD')
	GL.destory(server)

def on_info(server: MCDR.ServerInterface, info: MCDR.Info):
	api.on_info(server, info)

def on_player_joined(server: MCDR.PluginServerInterface, player: str, info: MCDR.Info):
	api.on_player_joined(server, player, info)

def on_player_left(server: MCDR.PluginServerInterface, player: str):
  api.on_player_left(server, player)
