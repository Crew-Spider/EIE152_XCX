# https://www.thebump.com/real-answers/stages 爬取包含分类：PREGNANCY和PARENTING下的所有子分类的所有问题
# coding:utf-8
import requests
from urllib.parse import urlencode  # 用urlencode()方法构造请求的get参数
import csv  # 为了写入CSV文件

base_url = 'https://www.thebump.com/real-answers/v1/categories/'  # 表示请求的URL的前半部分

# 设置请求头信息 模拟浏览器版本
headers ={
    'Host': 'www.thebump.com',
    'Referer': 'https://www.thebump.com/real-answers/stages/first-trimester',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
def get_total(url_json):
    return url_json["total"]

# 定义一个方法来获取每次请求的结果
def get_page(page, page_num, page_size):
    page_num = "" + str(page_num)
    page= "" + str(page)
    # 构造参数字典
    params = {
        "filter": "ranking",
        "page_num" : page_num,
        "page_size" : page_size
    }
    url_page = base_url + page
    url = base_url + page + "/questions?" + urlencode(params) # base_url与参数拼合形成一个新的URL
    try:
        response_page = requests.get(url_page)
        response_url = requests.get(url)
        # 判断响应的状态码，如果是200，则直接调用json()方法将内容解析为JSON返回，否则不返回任何信息
        if response_page.status_code == 200 and response_url.status_code == 200:
            page_json = response_page.json()
            url_json = response_url.json()
            return page_json, url_json
    except requests.ConnectionError as e:  #如果出现异常，则捕获并输出其异常信息
        print('Error', e.args)

# 定义一个解析方法，用来从结果中提取想要的信息
def parse_page(page_json, url_json):
    if page_json and url_json:
        items = url_json.get("questions")
        for item in items:
            questions = {}
            questions["title"] = item.get("title")
            questions["create_at"] = item.get("created_at")
            questions["user_id"] = item.get("user_id")
            questions["user_name"] = item.get("user")["username"]

            #  通过id号判断所属分类
            if (page_json["id"] <= 35 and page_json["id"] >= 33) or page_json["id"] == 23 or page_json["id"] == 24:
                questions["category_name"] = "PREGNANCY"  # 分类：怀孕，妊娠
                questions["subcategory_name"] = page_json.get("name")
            elif page_json["id"] >= 37 and page_json["id"] <= 47:
                questions["category_name"] = "PARENTING"  # 分类：教育，抚养
                questions["subcategory_name"] = page_json.get("name")
            yield questions  # 赋值为一个新的字典返回

if __name__ == "__main__":
    # 在f盘中保存名为task3的csv文件并指定打开的模式为w（写入）
    with open("f:/task3.csv", 'w', newline='',  encoding="utf-8") as f:
        fieldnames = ["title",  "create_at", "user_id", "user_name","category_name", "subcategory_name"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # 调用csv库的writer()方法初始化写入对象，传入该句柄

        # 接下来的这部分不是非常理解- -
        for i in range(33, 48):   # 遍历提取结果，括号里的代表id号
            num = 1000
            page = i
            page_num = 1
            if get_page(page, page_num, 1):
                page_json, url_json = get_page(page, page_num, 1)
                total = get_total(url_json)
                while total > 0:
                    if get_page(page, page_num, 1):
                        page_json, url_json = get_page(page, page_num, num)
                        results = parse_page(page_json, url_json)
                        for result in results:
                            writer.writerow(result)  # 调用writerow()方法写入一行数据
                        if total - num > 0:
                            total -= num
                        elif total - num // 10 > 0:
                            total -= num // 10
                            num //= 10
                            if num == 0:
                                break
                        else:
                            break
                        page_num += 1
                    else:
                        continue
            else:
                 continue