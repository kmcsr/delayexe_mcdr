
import functools

import mcdreforged.api.all as MCDR
import kpi.utils

__all__ = [
	'new_thread', 'tr'
]

kpi.utils.export_pkg(globals(), kpi.utils)

def new_thread(call):
	@MCDR.new_thread('delayexe')
	@functools.wraps(call)
	def c(*args, **kwargs):
		return call(*args, **kwargs)
	return c

def tr(key: str, *args, **kwargs):
	return MCDR.ServerInterface.get_instance().rtr(f'delayexe.{key}', *args, **kwargs)
