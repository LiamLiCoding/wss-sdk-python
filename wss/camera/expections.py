#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/10 18:00
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


class CameraDostNotExist(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CameraRunningModeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
