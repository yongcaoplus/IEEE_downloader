# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 14:55 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn


def check_page_valid(page):
    page_comma = []
    try:
        if ',' in page:
            for item in page.split(","):
                if "-" in item:
                    pages = item.split("-")
                    if len(pages) != 2:
                        # show_fail_window("下载页数范围输入错误")
                        return False, None
                    page_comma.extend([item for item in range(int(pages[0].strip()), int(pages[1].strip())+1)])
                else:
                    page_comma.append(int(item.strip()))

        elif "-" in page:
            pages = page.split("-")
            if len(pages) != 2:
                # show_fail_window("下载页数范围输入错误")
                return False, None
            page_comma.extend([item for item in range(int(pages[0].strip()), int(pages[1].strip()) + 1)])
        else:
            page_comma.append(int(page.strip()))
    except Exception as e:
        # show_fail_window("下载页数范围输入错误")
        return False, None
    page = sorted(list(set(page_comma)))
    for item in page:
        if item < 1:
            # show_fail_window("下载页数范围输入错误")
            return False, None
    return True, page


if __name__ == '__main__':
    page_range = ["2", "2-3", "2, 3, 5  ", "2, 3-5", "2,a,5, 9-12", "2,-4, 10, 6-8, 11-14", "100, 102, 1-4, 44, 100, 66"]
    for i, item in enumerate(page_range):
        status, pages = check_page_valid(item)
        print(page_range[i], "\t:", status, pages)