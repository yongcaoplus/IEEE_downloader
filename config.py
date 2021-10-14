# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 15:56 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
class pb_value:
    progress_bar_value = 0

    # 对于每个全局变量，都需要定义get_value和set_value接口
    def set_value(value):
        pb_value.progress_bar_value = value

    def get_value():
        return pb_value.value
