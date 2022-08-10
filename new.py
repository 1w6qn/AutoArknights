from object import *
import dev
p=player.Player.load_from_json('user.json')[0]
dev.auth.auth_login(p)
dev.auth.get_token(p)
dev.account.login(p)
dev.account.sync_data(p)