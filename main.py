# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 12:34 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import os
from download_paper_by_URLfile import organize_info_by_txt
from download_paper_by_pageURL import organize_info_by_query
from utils import downLoad_paper


if __name__ == '__main__':
    ############### 配置1 ##################
    mode = "search"  # "txt" or "search"
    dst_dir = "./save"
    ############### END ##################
    if mode == "txt":
        ############### 配置2 ##################
        url_txt = "url.txt"  # txt mode is needed.
        ############### END ##################
        # 配置存储文件夹
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        # 封装下载url和论文名称
        _, paper_info = organize_info_by_txt(url_txt)
        # 下载论文
        downLoad_paper(paper_info)
    else:
        ############### 配置3 ##################
        queryText = "dialog system"
        pageNumber = [3]
        save_papername_with_year = True
        ############### END ##################
        _, paper_info = organize_info_by_query(queryText, pageNumber, dst_dir, save_papername_with_year)
        downLoad_paper(paper_info, show_bar=True)
