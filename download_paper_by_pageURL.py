# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 10:37 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import requests
import os
from utils import downLoad_paper
import re


def organize_info_by_query(queryText, pageNumber, save_dir, paper_name_with_year=None):
    paper_info = {}
    count = 0
    for page in pageNumber:
        headers = {
            'Host': 'ieeexplore.ieee.org',
            'Content-Type': "application/json",
            'User-Agent': 'PostmanRuntime/7.28.1',
            'Accept': '*/*'}
        payload = {"queryText": queryText, "pageNumber": str(page), "returnFacets": ["ALL"],
                   "returnType": "SEARCH"}
        toc_res = requests.post("https://ieeexplore.ieee.org/rest/search", headers=headers, data=json.dumps(payload))
        response = json.loads(toc_res.text)
        if 'records' in response:
            for item in response['records']:
                paper_info[count] = {}
                paper_info[count]['url'] = "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=" + item['articleNumber'] + "&ref="
                paper_info[count]['name'] = item['articleTitle']
                rstr = r"[\=\(\)\,\/\\\:\*\?\？\"\<\>\|\'']"
                if paper_name_with_year:
                    paper_info[count]['name'] = os.path.join(save_dir, item['publicationYear'] + ' ' + re.sub(rstr, '', paper_info[count]['name']) + '.pdf')
                else:
                    paper_info[count]['name'] = os.path.join(save_dir, re.sub(rstr, '', paper_info[count]['name']) + '.pdf')
                count += 1
    if len(paper_info) > 0:
        return True, paper_info
    else:
        return False, paper_info


if __name__ == '__main__':
    queryText = "dialog system"
    pageNumber = [3]
    save_dir = "save"
    paper_info = organize_info_by_query(queryText, pageNumber, save_dir, True)
    downLoad_paper(paper_info)
