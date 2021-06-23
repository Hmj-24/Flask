# Flask 全国疫情分析实施监控
[项目展示](https://www.bilibili.com/video/BV1UE411P7mv)  

## 一、下载python库
    更新pip：python -m pip install --upgrade pip
    下载python库：pip install +模块名 -i +国内镜像源地址
### 需要下载的模块
    notebook
    pymysql
    flask
    urllib3
    requests
    beautifulsoup4
    selenium
    jieba
     
## 二、自行创建cov数据库<br>
### 1.创建history表
    CREATE TABLE `history` (
      `ds` datetime NOT NULL COMMENT '日期',
      `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
      `confirm_add` int(11) DEFAULT NULL COMMENT '当日新增确诊',
      `suspect` int(11) DEFAULT NULL COMMENT '剩余疑似',
      `suspect_add` int(11) DEFAULT NULL COMMENT '当日新增疑似',
      `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
      `heal_add` int(11) DEFAULT NULL COMMENT '当日新增治愈',
      `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
      `dead_add` int(11) DEFAULT NULL COMMENT '当日新增死亡',
      PRIMARY KEY (`ds`) USING BTREE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
### 2.创建details表
    CREATE TABLE `details` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `update_time` datetime DEFAULT NULL COMMENT '数据最后更新时间',
      `province` varchar(50) DEFAULT NULL COMMENT '省',
      `city` varchar(50) DEFAULT NULL COMMENT '市',
      `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
      `confirm_add` int(11) DEFAULT NULL COMMENT '新增确诊',
      `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
      `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
 ### 3.创建hotsearch表
    CREATE TABLE `hotsearch` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `dt` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
      `content` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
## 三、更改数据库连接中的数据库密码<br>
    data.py 中第216行
    utils.py 中第15行
