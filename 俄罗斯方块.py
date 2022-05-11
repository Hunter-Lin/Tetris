# -*- coding:UTF-8 -*-
import pygame
import sys
import numpy as np
import random


def newScreen(Screen, GameSize, ScreenSize):
    Screen.fill("black")
    for i in range(1, GameSize[0]):
        cellS = i*ScreenSize[0]/GameSize[0]
        pygame.draw.line(Screen, "grey", (cellS, 0), (cellS, ScreenSize[1]), 1)

    for i in range(1, GameSize[1]):
        cellH = i*ScreenSize[1]/GameSize[1]
        pygame.draw.line(Screen, "grey", (0, cellH), (ScreenSize[0], cellH), 1)


pygame.init()  # 初始化
screenSize = width, height = 300, 600
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)  # 初始化一个窗口(宽, 高)
pygame.display.set_caption("俄罗斯方块")  # 窗口名字

gameSize = (7, 14)
wholeGame = np.zeros(shape=gameSize)
wholeGameTem = np.zeros(shape=gameSize)

block_0 = [np.matrix([[1, 1], [1, 1]]),
           np.matrix([[1, 1], [1, 1]]),
           np.matrix([[1, 1], [1, 1]]),
           np.matrix([[1, 1], [1, 1]])]
block_1 = [np.matrix([[0, 1, 0], [1, 1, 1], [0, 0, 0]]),
           np.matrix([[0, 1, 0], [0, 1, 1], [0, 1, 0]]),
           np.matrix([[0, 0, 0], [1, 1, 1], [0, 1, 0]]),
           np.matrix([[0, 1, 0], [1, 1, 0], [0, 1, 0]])]
block_2 = [np.matrix([[1, 0, 0], [1, 1, 1], [0, 0, 0]]),
           np.matrix([[0, 1, 1], [0, 1, 0], [0, 1, 0]]),
           np.matrix([[0, 0, 0], [1, 1, 1], [0, 0, 1]]),
           np.matrix([[0, 1, 0], [0, 1, 0], [1, 1, 0]])]
block_3 = [np.matrix([[0, 0, 1], [1, 1, 1], [0, 0, 0]]),
           np.matrix([[0, 1, 0], [0, 1, 0], [0, 1, 1]]),
           np.matrix([[0, 0, 0], [1, 1, 1], [1, 0, 0]]),
           np.matrix([[1, 1, 0], [0, 1, 0], [0, 1, 0]])]
block_4 = [np.matrix([[1, 1, 0], [0, 1, 1], [0, 0, 0]]),
           np.matrix([[0, 0, 1], [0, 1, 1], [0, 1, 0]]),
           np.matrix([[0, 0, 0], [1, 1, 0], [0, 1, 1]]),
           np.matrix([[0, 1, 0], [1, 1, 0], [1, 0, 0]])]
block_5 = [np.matrix([[0, 1, 1], [1, 1, 0], [0, 0, 0]]),
           np.matrix([[0, 1, 0], [0, 1, 1], [0, 0, 1]]),
           np.matrix([[0, 0, 0], [0, 1, 1], [1, 1, 0]]),
           np.matrix([[1, 0, 0], [1, 1, 0], [0, 1, 0]])]
block_6 = [np.matrix([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
           np.matrix([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
           np.matrix([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
           np.matrix([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]])]
blockList = [block_0, block_1, block_2, block_3, block_4, block_5, block_6]


newScreen(screen, gameSize, screenSize)
isDrop = False  # 正在掉落
gameover = False  # 输了
k = 0
m = 200  # 更新时间
fps = 600  # 每秒帧率参数
fClock = pygame.time.Clock()  # 创建Clock对象 操作事件


def stratDrop(BlockList):  # 开始掉落
    BlockChoice = random.randint(0, 6)
    FormChoice = random.randint(0, 3)
    BlockDropping = BlockList[BlockChoice][FormChoice]  # 选择一个方块掉落
    if (BlockChoice == 1 and FormChoice == 1) or (BlockChoice == 2 and FormChoice == 1) or (BlockChoice == 3 and FormChoice == 1) or (BlockChoice == 4 and FormChoice == 1) or (BlockChoice == 5 and FormChoice == 1):
        DropLocation = random.randint(-1, gameSize[0] - len(BlockDropping))
    elif (BlockChoice == 1 and FormChoice == 3) or (BlockChoice == 2 and FormChoice == 3) or (BlockChoice == 3 and FormChoice == 3) or (BlockChoice == 4 and FormChoice == 3) or (BlockChoice == 5 and FormChoice == 3):
        DropLocation = random.randint(0, gameSize[0] - len(BlockDropping) + 1)
    elif BlockChoice == 6 and (FormChoice == 1 or FormChoice == 3):
        DropLocation = random.randint(-2, gameSize[0] - len(BlockDropping) + 1)
    else:
        DropLocation = random.randint(0, gameSize[0] - len(BlockDropping))
    return BlockList[BlockChoice], FormChoice, DropLocation  # 掉落的方块, 方块编号, 方块方向, 掉落点X


def blockChange(BlockForm, Form, BlockX, BlockY, WholeGame, WholeGameTem, GameSize, Operate):  # 用来使得方块改变位置
    if Operate == "Down":
        BlockY = BlockY + 1
        Block = BlockForm[Form]
    if Operate == "Spin":
        Form = (Form - 1) % 4
        Block = BlockForm[Form]
    if Operate == "L":
        BlockX = BlockX - 1
        Block = BlockForm[Form]
    if Operate == "R":
        BlockX = BlockX + 1
        Block = BlockForm[Form]
    Mark = True
    WholeGameTemTem = WholeGameTem.copy()
    WholeGameTem = WholeGame.copy()
    if BlockX < 0 and np.any(Block[:, abs(BlockX) - 1]):
        BlockX = BlockX + 1
    if BlockX + len(Block) > GameSize[0] and np.any(Block[:, GameSize[0] - BlockX]):
        BlockX = BlockX - 1

    for i in range(len(Block)):
        for j in range(len(Block)):
            BlockXX = BlockX + j
            BlockYY = BlockY - i
            if BlockXX >= 0 and BlockXX < GameSize[0] and BlockYY >= 0 and BlockYY < GameSize[1]:
                if Block[i, j] == 1:
                    WholeGameTem[BlockXX, BlockYY] = WholeGameTem[BlockXX, BlockYY] + 1
                if WholeGameTem[BlockXX, BlockYY] > 1:
                    # IsDrop = False
                    WholeGameTem = WholeGameTemTem
                    Mark = False
                    break

        else:  # 跳出双循环 https://www.jb51.net/article/163756.htm
            continue
        break

    if BlockY == GameSize[1] - 1 and np.any(Block[0]):  # 如果到底 则停
        Mark = False
    if BlockY == GameSize[1]:  # 如果到底 则停
        Mark = False

    if Operate == "Down":
        return WholeGameTem, Mark, BlockY
    elif Operate == "Spin":
        return WholeGameTem, BlockX, Form
    else:
        return WholeGameTem, BlockX


def checkDeletion(WholeGame, GameSize):
    WholeGame = WholeGame - 1
    for i in range(GameSize[1]):
        if not(np.any(WholeGame[:, i])):
            for j in range(i):
                WholeGame[:, i-j] = WholeGame[:, i-j-1]
            aa = WholeGame[:, 0]
            bb = np.zeros((GameSize[0], 1)) - 1
            WholeGame[::, 0] = [-1 for _ in range(GameSize[0])]
    WholeGame = WholeGame + 1
    return WholeGame


while True:
    if (not isDrop) and k % m == 0:  # 若不正在掉落 检查删除 并 开启掉落
        wholeGame = wholeGameTem.copy()
        wholeGame = checkDeletion(wholeGame, gameSize)
        wholeGameTem = wholeGame.copy()
        isDrop = True  # 开启掉落
        blockDropping, formChoice, blockX = stratDrop(blockList)
        blockY = -1
        m = 200  # 更新时间
        fps = 600  # 每秒帧率参数
    elif k % m == 0:  # 若正在掉落
        block = blockDropping[formChoice]
        wholeGameTem, mark, blockY = blockChange(BlockForm=blockDropping, Form=formChoice, BlockX=blockX, BlockY=blockY, WholeGame=wholeGame, WholeGameTem=wholeGameTem, GameSize=gameSize, Operate="Down")

        if not(mark) and blockY - len(block) <= 0:  # 判断是否结束
            gameover = True
        isDrop = mark

        wholeGamePrint = wholeGameTem.copy()

        newScreen(screen, gameSize, screenSize)

        for i in range(gameSize[0]):
            for j in range(gameSize[1]):
                if wholeGamePrint[i, j] == 1:
                    rect = pygame.draw.rect(screen, "white", (i*screenSize[0]/gameSize[0], j*screenSize[1]/gameSize[1], screenSize[0]/gameSize[0], screenSize[1]/gameSize[1]), 5)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # 键盘交互
            if event.key == pygame.K_LEFT:  # 左键 向左
                wholeGameTem, blockX = blockChange(BlockForm=blockDropping, Form=formChoice, BlockX=blockX, BlockY=blockY, WholeGame=wholeGame, WholeGameTem=wholeGameTem, GameSize=gameSize, Operate="L")
            elif event.key == pygame.K_RIGHT:  # 右键 向右
                wholeGameTem, blockX = blockChange(BlockForm=blockDropping, Form=formChoice, BlockX=blockX, BlockY=blockY, WholeGame=wholeGame, WholeGameTem=wholeGameTem, GameSize=gameSize, Operate="R")
            elif event.key == pygame.K_UP:  # 上键 旋转
                wholeGameTem, blockX, formChoice = blockChange(BlockForm=blockDropping, Form=formChoice, BlockX=blockX, BlockY=blockY, WholeGame=wholeGame, WholeGameTem=wholeGameTem, GameSize=gameSize, Operate="Spin")
        elif event.type == pygame.QUIT:
            sys.exit()  # 退出
        elif event.type == pygame.VIDEORESIZE:  # 调整屏幕大小
            screenSize = width, height = event.size[0], event.size[1]
            screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
            for i in range(1, gameSize[0]):
                cellS = i*screenSize[0]/gameSize[0]
                lineS = pygame.draw.line(screen, "grey", (cellS, 0), (cellS, screenSize[1]), 1)
            for i in range(1, gameSize[1]):
                cellH = i*screenSize[1]/gameSize[1]
                lineH = pygame.draw.line(screen, "grey", (0, cellH), (screenSize[0], cellH), 1)

    if gameover:
        break

    pygame.display.update()
    fClock.tick(fps)  # 控制窗口刷新速度
    k = k + 1
    k = k % fps

pygame.display.update()
# ##pygame.display.update() 对窗口进行更新
# ##pygame.event.get() 从pygame事件列中取出事件
# ## sys.exit()  # 退出
