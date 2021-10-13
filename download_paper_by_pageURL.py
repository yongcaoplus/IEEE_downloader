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
            'Accept': '*/*',
            'Cookie': '__gads=ID=bb245b47dbd075f5:T=1628127999:S=ALNI_Mb5XnCOcql5070-WeOzoSqxMSrmbA; fp=ee04e4c554d738e3d832a3829621eacd; s_ecid=MCMID|00494933450329945092470795121200336155; __utma=98802054.752232687.1628128715.1628128715.1628128715.1; __utmz=98802054.1628128715.1.1.utmcsr=ieeexplore.ieee.org|utmccn=(referral)|utmcmd=referral|utmcct=/; _gcl_au=1.1.1512091105.1628128715; _fbp=fb.1.1628128716073.767760559; _ga=GA1.1.752232687.1628128715; _ga_DRSMCND71P=GS1.1.1628128715.1.1.1628128767.0; _ga_RN78LDXHRB=GS1.1.1628128715.1.1.1628128767.0; roamingToken=dReD3LbRrBXR/WBVfWaWAQQK02lkNQYzR1rFOIWypRh4wHElan+GAw==; ipCheck=175.45.38.98; WLSESSION=186802828.20480.0000; ipList=175.45.38.98; AMCVS_8E929CC25A1FB2B30A495C97@AdobeOrg=1; s_cc=true; cookieconsent_status=dismiss; s_fid=38333AB2642CFE85-21FC1C2DF8C50F28; s_sq=[[B]]; JSESSIONID=V355D7xJPjmeEwt0kx-xRDPxcpL7Sq1aNXGHqphzdj-pK2s8dS-0!-744343754; AMCV_8E929CC25A1FB2B30A495C97@AdobeOrg=1687686476|MCIDTS|18845|vVersion|3.0.0|MCMID|00494933450329945092470795121200336155|MCAAMLH-1634723456|3|MCAAMB-1634723456|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1634125856s|NONE|MCAID|NONE; ERIGHTS=kksOrqJiCwl69xxowT01Uaig4N4r7GUts*zhc16Vzx2BZ5CiLsq95Ox2BPJwx3Dx3D-18x2djh3mdx2BNuRWd6ZPQtUZbfUAx3Dx3Dgx2FWRHf8CWhzifLmO6ERmrwx3Dx3D-seCuihlon4Yn6ravae9KzQx3Dx3D-x2BoJmAJK1Z3DbmTWzFvGVAAx3Dx3D; utag_main=v_id:017b13fdbef50013988dd1e3b6f503073003506b00bd0$_sn:15$_se:6$_ss:0$_st:1634125717447$vapi_domain:ieee.org$ses_id:1634121962244;exp-session$_pn:4;exp-session; xpluserinfo=eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJUaGUgQ2hpbmVzZSBVbml2ZXJzaXR5IG9mIEhvbmcgS29uZyBDVUhLKFNoZW56aGVuKSIsInByb2R1Y3RzIjoiSUVMfFZERXxOT0tJQSBCRUxMIExBQlN8In0=; seqId=4161314; TS01b03060=012f3506238e97585f43b7c490a28732ec3eada808c7db2c6c6acfffc02f001d7132e645a09617cfe06b7ff4154179537525531318'
        }
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
