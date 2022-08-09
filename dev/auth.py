import api.auth
def auth_login(player):
    api.player=player
    api.auth.auth(**player.attr)