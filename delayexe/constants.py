
import mcdreforged.api.all as MCDR

__all__ = [
	'ON_PLAYER_EMPTY', 'ON_FIRST_PLAYER_JOIN'
]

ON_PLAYER_EMPTY      = MCDR.LiteralEvent('delayexe.player.empty')
ON_FIRST_PLAYER_JOIN = MCDR.LiteralEvent('delayexe.player.join.first')
