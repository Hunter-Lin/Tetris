# -*- coding:UTF-8 -*-

import pygame
import sys

pygame.init()  # 初始化
screen = pygame.display.set_mode((600, 400))  # 初始化一个窗口(宽, 高)
pygame.display.set_caption("test")  # 窗口名字

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # 退出
    pygame.display.update()
# ##pygame.display.update() 对窗口进行更新
# ##pygame.event.get() 从pygame事件列中取出事件 
# ## sys.exit()  # 退出