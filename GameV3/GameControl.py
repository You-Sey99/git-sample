# coding=[shift-jis]


import GameLib as lib
from GameLocal import *
import GameHome as hm
import GameOption as op
import GamePose as ps
import GamePlayNormal as pn
import GamePlayTimeattak as pta
import GamePlayVS as pvs

#音楽：魔王魂


home = hm.Home()#準備
pose = ps.Pose()


game_mode = 0
game_list = [pn.PlayNormal(),pta.PlayTA(),pvs.PlayVS(level=10)]
game_play = game_list[0]
game_mode_list = ["Normal","TimeAttak","VS CPU"]

option = op.Option(sounds={},gamemode_list=game_mode_list)

game_data = lib.GameData()
game_rank = lib.HighScoreRanking()

while 1:
    if game_mode == 2:
        game_data = pvs.VSGameData()
    else:
        game_data = lib.GameData()

    game_data.install(mod=game_mode)#ファイルからデータを取り出す
    game_rank.install(mod=game_mode)
    game_play = game_list[game_mode]
    
    res = home.main()#開始
    if res in (1,2):#ゲーム画面
        if res == 2:#途中から        
            game_play.gd_lord(game_data.get_gamedata())#PlayNormalにデータを入れる
            #res = game_n.main()#開始
        else:#始めから
            if game_mode == 2:#VSmode
                vs_scr = game_data.get_gamedata()
                vsc = vs_scr[1][0] - vs_scr[3][0]#pl_hp - en_hp
                game_rank.ranking_update(vsc)
                game_rank.save(mod=game_mode)#ハイスコア更新
                game_data = pvs.VSGameData()
            else:
                game_rank.ranking_update(game_data.get_gamedata()[3])
                game_rank.save(mod=game_mode)#ハイスコア更新
                game_data = lib.GameData()
            #game_data = lib.GameData()#データの
            game_data.save(mod=game_mode)#消去
            game_play.gd_reset()#ゲームを初期化

        while 2:#考えやすくするために2にした        
            res = game_play.main()#開始
            game_data = game_play.get_gd()
            game_data.save(mod=game_mode)

            if res == 1:#poseボタンを押したとき
                
                res = pose.main()#pose画面へ

                if res == 1:#再開
                    game_play.gd_lord(game_data.get_gamedata())#PlayNormalにデータを入れる
                    continue

                elif res == 2:#再開できるようにやめる
                    break

                elif res == 3:#終了,再開できない
                    if game_mode == 2:#vs
                        vs_scr = game_data.get_gamedata()
                        vsc = vs_scr[1][0] - vs_scr[3][0]#pl_hp - en_hp
                        game_rank.ranking_update(vsc)
                        game_rank.save(mod=game_mode)#ハイスコア更新
                        game_data = pvs.VSGameData()
                    else:
                        game_rank.ranking_update(game_data.get_gamedata()[3])
                        game_rank.save(mod=game_mode)#ハイスコア更新
                        game_data = lib.GameData()
                    #game_data = lib.GameData()#データの
                    game_data.save(mod=game_mode)#消去
                    game_play.gd_reset()#ゲームを初期化
                    break

            elif res == -1:#GameOverになったとき
                if game_mode == 2:#VSmode
                    vs_scr = game_data.get_gamedata()
                    vsc = vs_scr[1][0] - vs_scr[3][0]#pl_hp - en_hp
                    game_rank.ranking_update(vsc)
                    game_rank.save(mod=game_mode)#ハイスコア更新
                    game_data = pvs.VSGameData()
                else:
                    game_rank.ranking_update(game_data.get_gamedata()[3])
                    game_rank.save(mod=game_mode)#ハイスコア更新
                    game_data = lib.GameData()
                #game_data = lib.GameData()#データの
                game_data.save(mod=game_mode)#消去
                game_play.gd_reset()#ゲームを初期化
                break

    
    elif res == 3:#設定画面
        game_mode = option.main(mod=game_mode)
        game_play = game_list[game_mode]
        home.set_vol(bgc_vol=option.bgm_vol,se_vol=option.se_vol)
        for i in range(len(game_list)):
            game_list[i].set_vol(bgc_vol=option.bgm_vol,se_vol=option.se_vol)


