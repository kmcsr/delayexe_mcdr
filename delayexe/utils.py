
import functools
import threading

import mcdreforged.api.all as MCDR
from . import globals as GL

__all__ = [
	'new_thread', 'LockedData',
	'join_rtext', 'send_block_message', 'send_message', 'broadcast_message', 'log_info'
]

def new_thread(call):
	@MCDR.new_thread('delayexe')
	@functools.wraps(call)
	def c(*args, **kwargs):
		return call(*args, **kwargs)
	return c

class LockedData:
	def __init__(self, data, lock=None):
		self._data = data
		self._lock = threading.Lock() if lock is None else lock

	@property
	def d(self):
		return self._data

	@d.setter
	def d(self, data):
		self._data = data

	@property
	def l(self):
		return self._lock

	def __enter__(self):
		self._lock.__enter__()
		return self

	def __exit__(self, *args, **kwargs):
		return self._lock.__exit__(*args, **kwargs)

def join_rtext(*args, sep=' '):
	if len(args) == 0:
		return ''
	if len(args) == 1:
		return args[0]
	return MCDR.RTextList(args[0], *(MCDR.RTextList(sep, a) for a in args[1:]))

def send_block_message(source: MCDR.CommandSource, *args, sep='\n', log=False):
	if source is not None:
		t = join_rtext(GL.BIG_BLOCK_BEFOR, join_rtext(*args, sep=sep), GL.BIG_BLOCK_AFTER, sep='\n')
		source.reply(t)
		if log and not source.is_console:
			source.get_server().logger.info(t)

def send_message(source: MCDR.CommandSource, *args, sep=' ', prefix=GL.MSG_ID, log=False):
	if source is not None:
		t = join_rtext(prefix, *args, sep=sep)
		source.reply(t)
		if log and not source.is_console:
			source.get_server().logger.info(t)

def broadcast_message(*args, sep=' ', prefix=GL.MSG_ID):
	if GL.SERVER_INS is not None:
		GL.SERVER_INS.broadcast(join_rtext(prefix, *args, sep=sep))

def log_info(*args, sep=' ', prefix=GL.MSG_ID):
	if GL.SERVER_INS is not None:
		GL.SERVER_INS.logger.info(join_rtext(prefix, *args, sep=sep))
