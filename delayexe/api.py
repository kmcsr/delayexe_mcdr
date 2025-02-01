
import re
import threading

import mcdreforged.api.all as MCDR
from .constants import *
from . import globals as GL
from .utils import *

__all__ = [
	'ServerNotRunningError',
	'add_playerlist_handler', 'add_delay_task', 'clear_delay_task', 'get_playerlist_data'
]

delaylist = LockedData(set())
player_empty = LockedData(True)
playerlist_data = LockedData([(0, 0), True], threading.Condition(threading.Lock()))

_HANDLE_MAP = {
	'vanilla_handler': (re.compile(r'There are (\d+) of a max of (\d+) players online.*'), 1, 2),
	'forge_handler': (re.compile(r'There are (\d+)/(\d+) players online.*'), 1, 2)
}

class ServerNotRunningError(RuntimeError):
	def __init__(self):
		super().__init__('Server is not running')

def add_playerlist_handler(name: str, rp: re.Pattern, online_index: int, total_index: int, *, force: bool = False):
	assert force or name not in _HANDLE_MAP, f'Handler "{name}" already registered in handle map'
	_HANDLE_MAP[name] = (rp, online_index, total_index)

def add_delay_task(task):
	with delaylist:
		delaylist.d.add(task)

def clear_delay_task():
	with delaylist:
		delaylist.d.clear()

def _trigger_delay_list(server: MCDR.ServerInterface):
	global delaylist
	with delaylist:
		dl, delaylist.d = delaylist.d, set()
	for c in dl:
		if isinstance(c, str):
			server.execute(c)
		elif callable(c):
			c()
		else:
			raise RuntimeError('Unexpected delay task type {}'.format(type(c)))

def get_playerlist_data(server: MCDR.ServerInterface):
	"""
	:return: (current_player, max_player)
	"""
	with playerlist_data:
		if not server.is_server_startup():
			raise ServerNotRunningError()
		if playerlist_data.d[1]:
			playerlist_data.d[1] = False
			server.execute('list')
		playerlist_data.l.wait()
	return playerlist_data.d[0]

def get_handler(server: MCDR.ServerInterface):
	hdr = server.get_mcdr_config()['handler']
	if hdr not in _HANDLE_MAP:
		hdr = 'vanilla_handler'
	return _HANDLE_MAP[hdr]

def on_load(server: MCDR.PluginServerInterface, prev_module):
	if prev_module is not None:
		if len(prev_module.delaylist.d) > 0:
			with delaylist:
				delaylist.d = prev_module.delaylist.d
			server.execute('list')

def on_info(server: MCDR.ServerInterface, info: MCDR.Info):
	if info.is_from_server:
		global playerlist_data
		handler = get_handler(server)
		if handler is not None:
			ct = handler[0].fullmatch(info.content)
			if ct is not None:
				with playerlist_data:
					playerlist_data.d[0] = (int(ct[handler[1]]), int(ct[handler[2]]))
					playerlist_data.d[1] = True
					playerlist_data.l.notify_all()

@new_thread
def on_player_joined(server: MCDR.PluginServerInterface, player: str, info: MCDR.Info):
	with player_empty:
		if player_empty.d and get_playerlist_data(server)[0] > 0:
			player_empty.d = False
			server.dispatch_event(ON_FIRST_PLAYER_JOIN, tuple())

@new_thread
def on_player_left(server: MCDR.PluginServerInterface, player: str):
	if get_playerlist_data(server)[0] == 0:
		with player_empty:
			player_empty.d = True
		_trigger_delay_list(server)
		server.dispatch_event(ON_LAST_PLAYER_LEAVE, tuple())
