# coding=[shift-jis]


import GameLib as lib
from GameLocal import *
import GameHome as hm
import GameOption as op
import GamePose as ps
import GamePlayNormal as pn
import GamePlayTimeattak as pta
import pygame as pg



home = hm.Home()#準備
pose = ps.Pose()
#option = op.Option()

game_mode = 0
game_list = [pn.PlayNormal(),pta.PlayTA()]
game_play = game_list[0]

game_data = lib.GameData()
game_rank = lib.HighScoreRanking()

while 1:
    game_data.install(mod=game_mode)#ファイルからデータを取り出す
    game_rank.install(mod=game_data)
    res = home.main()#開始
    if res in (1,2):#ゲーム画面
        if res == 2:#途中から
                
                game_play.gd_lord(game_data.get_gamedata())#PlayNormalにデータを入れる
                #res = game_n.main()#開始
        else:#始めから
                #ハイスコア更新
                game_data = lib.GameData()#データの
                game_data.save(mod=game_mode)#消去
                game_play.gd_reset()#ゲームを初期化

        while 2:#考えやすくするために2にした        
            res = game_play.main()#開始

            if res == 1:#poseボタンを押したとき
                game_data = game_play.get_gd()
                game_data.save(mod=game_mode)
                res = pose.main()#pose画面へ

                if res == 1:#再開
                    game_play.gd_lord(game_data.get_gamedata())#PlayNormalにデータを入れる
                    continue

                elif res == 2:#再開できるようにやめる
                    break

                elif res == 3:#終了,再開できない
                    #ハイスコア更新
                    game_data = lib.GameData()#データの
                    game_data.save(mod=game_mode)#消去
                    game_play.gd_reset()#ゲームを初期化
                    break

            elif res == -1:#GameOverになったとき
                game_data = lib.GameData()#データの
                game_data.save(mod=game_mode)#消去
                game_play.gd_reset()#ゲームを初期化
                #ハイスコアの更新
                break

    
    elif res == 3:#設定画面
        #option.main()
        #game_mode = option.get_gamemode()
        game_play = game_list[game_mode]


