from object import *
import dev
import log
def play(p):
    dev.auth.auth_login(p)
    dev.auth.get_token(p)
    dev.account.login(p)
    dev.account.sync_data(p)
    if p.data.checkIn['canCheckIn']:
        dev.user.check_in(p)
    else:
        log.d('已签到')
    if act:=p.data.activity['CHECKIN_ONLY']:
        dev.activity.check_in(p,list(act.items())[0])
    else:
        log.d('无可用签到活动')
    if act:=p.data.activity['PRAY_ONLY']:
        dev.activity.get_pray_reward(p,list(act.items())[0])
    else:
        log.d('无可用祈愿活动')
    if act:=p.data.activity['LOGIN_ONLY']:
        dev.activity.get_login_reward(p,list(act.items())[0])
    else:
        log.d('无可用登录活动')
    if p.data.pushFlags['hasGifts']:
        dev.mail.auto_receive_mails(p)
    else:
        log.d ("无可收取邮件")
    dev.gacha.auto_recruit(p)
if __name__=='__main__':
    p=player.Player.load_from_json('user.json')[0]
    play(p)