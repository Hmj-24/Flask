"""
1.热搜入库
2.历史入库
3.详细入库
"""
from selenium.webdriver import Chrome
import time
import utils
import requests
from bs4 import BeautifulSoup
import json
import pymysql


# 爬取热搜
def get_hotdata():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1#tab2"
    # 浏览器
    brower = Chrome('D:\QMDownload\应用\Google\Chrome\Application\chromedriver.exe')
    # 加载 url 地址
    brower.get(url)
    # 加载整个页面的 html 文件
    html = brower.page_source
    # 放爬到的数据，创建一个空列表
    hotdata = []

    # 模拟浏览器点击
    # 第一个点击按钮
    btn = brower.find_element_by_xpath('//*[@id="ptab-2"]/div[1]/div/p/a')
    # 执行点击操作
    btn.click()
    # 等待加载时间为1秒
    time.sleep(1)

    # 第二个点击按钮
    btn = brower.find_element_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/div')
    # 执行点击操作
    btn.click()
    time.sleep(1)

    # 获取数据
    content = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    # print(len(content))
    for item in content:
        # print(item.text)
        hotdata.append(item.text)
    # 关闭浏览器
    brower.quit()
    return hotdata
# 热搜数据入库
def insert_hotdata():
    # 获取数据库连接
    conn, cursor = utils.get_conn()
    sql = 'insert into hotsearch(dt,content) values(%s,%s)'
    datas = get_hotdata()
    # dt 当前时间
    # 获取系统当前时间戳
    dt = time.strftime('%Y-%m-%d %X')
    for item in datas:
        cursor.execute(sql, (dt, item))
        # 提交事务
        conn.commit()

    print('热搜数据插入成功！')
    # 释放数据
    utils.close(conn, cursor)


# 获取历史数据
def get_history():
    # 创建一个要发数据的空字典
    history = {}
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    }
    resp = requests.get(url, headers)
    jsondata = resp.text
    # 把 json 字符串转换为字典
    datas = json.loads(jsondata)

    data = json.loads(datas['data'])

    # print(data['chinaDayList'])
    for day in data['chinaDayList']:
        # 当前时间戳
        dt = '2020.' + day['date']
        # 把格式字符串转换为元组类型
        tup = time.strptime(dt, '%Y.%m.%d')
        # 再把元组类型转换属于数据库类型
        dt = time.strftime('%Y-%m-%d', tup)
        # 当天确诊
        confirm = day['confirm']
        # 当天疑似
        suspect = day['suspect']
        # 当天出院
        heal = day['heal']
        # 当天死亡
        dead = day['dead']
        # 放入到字典
        history[dt] = {'confirm': confirm,
                       'suspect': suspect,
                       'heal': heal,
                       'dead': dead}

    # print(data['chinaDayAddList'])
    for dayadd in data['chinaDayAddList']:
        # 当前时间戳
        dt = '2020.' + dayadd['date']
        tup = time.strptime(dt, "%Y.%m.%d")
        dt = time.strftime("%Y-%m-%d", tup)
        # 新增确诊
        confirm_add = dayadd['confirm']
        # 新增疑似
        suspect_add = dayadd['suspect']
        # 新增出院
        heal_add = dayadd['heal']
        # 新增死亡
        dead_add = dayadd['dead']
        # 新加的字段更新到字典
        history[dt].update({'confirm_add': confirm_add,
                            'suspect_add': suspect_add,
                            'heal_add': heal_add,
                            'dead_add': dead_add})

        # print(history)
        # for item in history.keys():
        #     print(item)
        #     print(history[item])
    return history
# 历史数据入库
def insert_history():
    # 获取 conn 和 cursor
    conn, cursor = utils.get_conn()
    # 获取所有的历史数据数据
    history = get_history()
    sql = ' insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    # 循环执行插入数据操作
    for k, v in history.items():
        cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"),
                             v.get("suspect"), v.get("suspect_add"),
                             v.get("heal"), v.get("heal_add"),
                             v.get("dead"), v.get("dead_add")])
        conn.commit()

    print('历史数据插入成功！')
    utils.close(conn, cursor)


# 获取 details 详情数据
def get_details():
    # 准备一个存放数据的容器，列表
    details = []
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    }
    resp = requests.get(url, headers)
    jsondata = resp.text
    # json 转换为字典
    datas = json.loads(jsondata)
    # 最终解析的数据
    data = json.loads(datas['data'])
    # for item in data.keys():
    #     print(item)
    #     print(data[item])
    # 数据更新时间
    updatetime = data['lastUpdateTime']
    # 中国
    country = data['areaTree'][0]
    # 所有省份
    provinces = country['children']
    for province in provinces:
        # 所有省份的名字
        pro_name = province['name']
        for city in province['children']:
            # 所有城市名字
            city_name = city['name']
            # 确诊
            confirm = city['total']['confirm']
            # 新增确诊
            confirm_add = city['today']['confirm']
            # 出院
            heal = city['total']['heal']
            # 死亡
            dead = city['total']['dead']
            # print(city_name)
            details.append([updatetime, pro_name, city_name, confirm, confirm_add, heal, dead])
    # print(details)
    return details
# details 详情数据入库
def insert_details():
    conn, cursor = utils.get_conn()
    details = get_details()
    # 执行插入数据
    sql = 'insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)'
    # 查询数据库中的数据是否需要更新，如果需要更新就更新，不需要就提示
    sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
    cursor.execute(sql_query, details[0][0])
    if not cursor.fetchone()[0]:
        print("详情表开始更新数据！")
        for item in details:
            cursor.execute(sql, item)
            conn.commit()

        print("详情表数据更新成功！")
    else:
        print("详情表已经是最新数据，不需要更新！")
    utils.close(conn, cursor)

# 删除数据库中热搜表和历史表
def delete():
    # 创建与数据库连接对象
    db = pymysql.connect(
        host='127.0.0.1',port=3306,
        user='root',password='toor',
        database='cov',charset='utf8')

    # 利用db方法创建游标对象
    cur = db.cursor()

    # 利用游标对象execute()方法执行SQL命令
    # cur.execute(";") ,这里填写正确的SQL语句
    cur.execute("delete from history;")
    cur.execute("delete from hotsearch;")
    # 提交到数据库执行
    db.commit()
    print("删除热搜和历史数据成功")
    # 关闭游标对象
    cur.close()

    # 断开数据库连接
    db.close()

# 创建一个执行删除，查询添加入库的运行函数
def to_update():
    delete()
    time.sleep(1)
    insert_hotdata()
    insert_history()
    insert_details()


# if __name__ == '__main__':
#     # get_hotdata()
#     # insert_hotdata()
#     # get_history()
#     # insert_history()
#     # get_details()
#     # insert_details()
#     to_update()


