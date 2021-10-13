# -*- coding: utf-8 -*-
# @Time    : 2021/10/12 22:49 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import os
import re
from tqdm import tqdm
from utils import downLoad_paper


def organize_info_by_txt(dst_dir, url_file, paper_name_with_year=None):
    if not os.path.exists(url_file):
        return False, None
    with open(url_file, "r") as f:
        lines = f.read().split("\n\n")
    rule = r'"(.*?)"'
    rstr = r"[\=\(\)\,\/\\\:\*\?\？\"\<\>\|\'']"
    paper_info = {}
    for i, line in enumerate(lines):
        content = line.split("\n")
        # paper name
        slotList = re.findall(rule, content[0])
        papername = re.sub(rstr, '', slotList[0])
        if paper_name_with_year:
            papername = content[1].split(".")[2] + ' ' + papername
        papername = os.path.join(dst_dir, papername + '.pdf')
        # paper url
        if "URL" in content[3]:
            arnumber = \
            content[3].replace("URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=", "").split("&")[0]
            url = "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=" + arnumber + "&ref="
            paper_info[i] = {}
            paper_info[i]['name'] = papername
            paper_info[i]['url'] = url
    return True, paper_info


if __name__ == '__main__':
    # 配置存储文件夹
    dst_dir = "./save"
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    # 封装下载url和论文名称
    url_txt = "url.txt"
    paper_info = organize_info_by_txt(dst_dir, url_txt, True)
    # 下载论文
    downLoad_paper(paper_info)
