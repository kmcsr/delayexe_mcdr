
import mcdreforged.api.all as MCDR

__all__ = [
	'ON_LAST_PLAYER_LEAVE', 'ON_FIRST_PLAYER_JOIN'
]

ON_LAST_PLAYER_LEAVE = MCDR.LiteralEvent('delayexe.player.leave.last')
ON_FIRST_PLAYER_JOIN = MCDR.LiteralEvent('delayexe.player.join.first')
