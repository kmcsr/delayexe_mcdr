
from typing import List, Dict, Any

import mcdreforged.api.all as MCDR

__all__ = [
	'MSG_ID', 'BIG_BLOCK_BEFOR', 'BIG_BLOCK_AFTER', 'DLEConfig', 'Config', 'SERVER_INS', 'init', 'destory'
]

MSG_ID = MCDR.RText('[DLE]', color=MCDR.RColor.green)
BIG_BLOCK_BEFOR = '------------ {0} v{1} ::::'
BIG_BLOCK_AFTER = ':::: {0} v{1} ============'


class DLEConfig(MCDR.Serializable):
	# 0:guest 1:user 2:helper 3:admin 4:owner
	minimum_permission_level: Dict[str, int] = {
		'help':     0,
		'query':    0,
		'restart':  2,
		'run':      3,
		'cancel':   2,
		'reload':   3,
		'save':     3,
	}
	_cache: Dict[str, Any] = {}

	@property
	def cache(self):
		return self._cache

	def literal(self, literal: str):
		lvl = self.minimum_permission_level.get(literal, 0)
		return MCDR.Literal(literal).requires(lambda src: src.has_permission(lvl),
			lambda: MCDR.RText(MSG_ID.to_plain_text() + ' 权限不足', color=MCDR.RColor.red))

	def save(self, server: MCDR.PluginServerInterface):
		server.save_config_simple(self)


Config: DLEConfig = DLEConfig()
SERVER_INS: MCDR.PluginServerInterface = None

def init(server: MCDR.PluginServerInterface):
	global SERVER_INS
	SERVER_INS = server
	global BIG_BLOCK_BEFOR, BIG_BLOCK_AFTER
	metadata = server.get_self_metadata()
	BIG_BLOCK_BEFOR = BIG_BLOCK_BEFOR.format(metadata.name, metadata.version)
	BIG_BLOCK_AFTER = BIG_BLOCK_AFTER.format(metadata.name, metadata.version)
	global Config
	Config = server.load_config_simple(target_class=DLEConfig)

def destory():
	global SERVER_INS
	SERVER_INS = None
