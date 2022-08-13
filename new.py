from object import *
import dev
p=player.Player.load_from_json('user.json')[1]
dev.auth.auth_login(p)
dev.auth.get_token(p)
dev.account.login(p)
dev.account.sync_data(p)
dev.user.check_in(p)
#dev.activity.check_in(p)
dev.activity.get_pray_reward(p)
dev.activity.get_login_reward(p)
dev.gacha.auto_recruit(p)
