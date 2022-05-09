
import mcdreforged.api.all as MCDR

globals_ = globals
from .utils import *
from . import constants
from . import globals as GL
from . import api
from . import commands as CMD

__all__ = []

def include_pkg(pkg):
	global __all__
	__all__.extend(pkg.__all__)
	for n in pkg.__all__:
		globals_()[n] = getattr(pkg, n)

include_pkg(api)
include_pkg(constants)

def on_load(server: MCDR.PluginServerInterface, prev_module):
	GL.init(server)
	if prev_module is None:
		log_info('Delay ExE is on LOAD')
	else:
		log_info('Delay ExE is on RELOAD')
	api.on_load(server)
	CMD.register(server)

def on_unload(server: MCDR.PluginServerInterface):
	log_info('Delay ExE is on UNLOAD')
	GL.destory()

def on_info(server: MCDR.ServerInterface, info: MCDR.Info):
	api.on_info(server, info)

def on_player_joined(server: MCDR.PluginServerInterface, player: str, info: MCDR.Info):
	api.on_player_joined(server, player, info)

def on_player_left(server: MCDR.PluginServerInterface, player: str):
  api.on_player_left(server, player)
