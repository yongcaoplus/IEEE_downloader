# 写综述必备！自动批量下载IEEE的论文

<left>
    <a href="https://github.com/misitebao/template-multi-page-vue-ssr" target="_blank" rel="noopener noreferrer">
        <img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_repo_size.svg" alt="version"/>
    </a>
    <a href="https://github.com/misitebao/template-multi-page-vue-ssr" target="_blank" rel="noopener noreferrer">
        <img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_languages.svg" alt="version"/>
    </a>
    <a href="https://github.com/misitebao/template-multi-page-vue-ssr" target="_blank" rel="noopener noreferrer">
        <img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_release.svg" alt="version"/>
    </a>
    <a href="https://github.com/misitebao/template-multi-page-vue-ssr" target="_blank" rel="noopener noreferrer">
        <img src="https://raw.githubusercontent.com/superYong2020/images/master/license.svg" alt="version"/>
    </a>
</left>      



> 如果领域内的大量论文需要下载，基于本工具实现半自动化，无需到IEEE网站手动一篇一篇下载论文啦，科研效率翻倍！
> 工具使用前提： 一定要在能够有权限下载IEEE论文的网络下才能正常使用。

如下，介绍两种方法实现批量下载,代码流程和详细介绍请参考博客。

## 软件界面

<div align=center>
<img src="https://raw.githubusercontent.com/superYong2020/images/master/ui_initial.png" width="500px">
</div>

## 方法1
将IEEE网站上的paper list导出到txt文档中，再基于该txt文件批量下载。    
优点：可筛选不需要的论文    
缺点：一次只能导出一页（≤25篇论文）     

* **step 1**
    * 进入IEEE官网[https://ieeexplore.ieee.org](https://ieeexplore.ieee.org/)，按照需要搜索论文，按照如下方式导出论文列表
  
  <div align=center>
  <img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_website_step_1.png" width="600px">
  </div>

* **step 2**    
    * 导出到txt文件，如下图所示。运行main_ui.py, 进入UI界面,配置论文保存文件夹和URL文件路径两个参数，点击“开始下载”，搞定！
  
  <div align=center>
  <img src="https://raw.githubusercontent.com/superYong2020/images/master/url_txt_example.png" width="600px">
  </div>

## 方法2
优点：可大批量下载论文
缺点：不可在下载前筛选不需要的论文   
* **step 1**     
  * 进入IEEE官网[https://ieeexplore.ieee.org](https://ieeexplore.ieee.org/)，按照关键词搜索论文  
   
* **step 2**
  * 按照同样的关键词在软件界面中配置，以及需要下载的页数，可以用英文逗号、破折号隔开，也可以用一个数字。eg. 2,3 或者 2-5 或者 2
  
## 配置举例

<div align=center>
<img src="https://raw.githubusercontent.com/superYong2020/images/master/example_ieee_download.png" width="500px">
</div>

> 点击下载按钮

<div align=center>
<img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_ui.png" width="500px">
</div>

> 下载成功啦！

<div align=center>
<img src="https://raw.githubusercontent.com/superYong2020/images/master/save_paper.png" width="500px">
</div>

## 搭配EndNote使用

<div align=center>
<img src="https://raw.githubusercontent.com/superYong2020/images/master/ieee_endnote.png" width="600px">
</div>

使用教程请参考博客：    
[科研效率直线提升！如何一键下载会议论文？ACL 2020 论文代码批量下载 打包分享](https://blog.csdn.net/weixin_43955436/article/details/116696395?spm=1001.2014.3001.5501)

### Reference    
本工具主要参考以下资料，感谢作者分享。    
[1] https://blog.csdn.net/ubooksapp/article/details/49518009    
[2] https://github.com/EdwinZhang1970/Python    