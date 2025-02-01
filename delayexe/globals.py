
from typing import List, Dict, Any

import mcdreforged.api.all as MCDR

from kpi.config import Config

__all__ = [
	'MSG_ID', 'BIG_BLOCK_BEFOR', 'BIG_BLOCK_AFTER', 'DLEConfig', 'get_config', 'init', 'destory'
]

MSG_ID = MCDR.RText('[DLE]', color=MCDR.RColor.green)
BIG_BLOCK_BEFOR = '------------ {0} v{1} ::::'
BIG_BLOCK_AFTER = ':::: {0} v{1} ============'


class DLEConfig(Config, msg_id=MSG_ID):
	# 0:guest 1:user 2:helper 3:admin 4:owner
	minimum_permission_level: Dict[str, int] = {
		'help':     0,
		'query':    0,
		'restart':  2,
		'run':      3,
		'cancel':   2,
		'reload':   3,
	}

def get_config() -> DLEConfig:
	return DLEConfig.instance()

def init(server: MCDR.PluginServerInterface):
	global BIG_BLOCK_BEFOR, BIG_BLOCK_AFTER
	metadata = server.get_self_metadata()
	BIG_BLOCK_BEFOR = BIG_BLOCK_BEFOR.format(metadata.name, metadata.version)
	BIG_BLOCK_AFTER = BIG_BLOCK_AFTER.format(metadata.name, metadata.version)
	DLEConfig.init_instance(server, load_after_init=True)

def destory(server: MCDR.PluginServerInterface):
	cfg = get_config()
	if cfg is not None:
		cfg.save()
