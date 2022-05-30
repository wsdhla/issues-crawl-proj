# issues-statistics

#### 介绍
爬取gitlab上的issue管理页面，根据label按不同维度统计issue信息（目前版本为初始版本，可自行扩展）。

#### 运行环境
+ 操作系统：目前仅支持Windows
+ JDK：1.8+
+ Python：Python3

#### 软件架构
+ Python
+ Spring Boot
+ SQLite
+ Thymeleaf
+ Echarts


#### 模块说明
**爬虫模块：issues-crawl**
> 已集成到issues-statistics

**统计模块：issues-statistics**
> issues-statistics应用启动时，根据配置信息使用Python爬取gitlab的issue管理页面，解析页面，将数据保存到SQLite数据库。

#### 安装教程
+ 待补充...

#### 使用说明
+ issues-statistics应用启动成功后，访问`http://localhost:8080`

#### 参与贡献
+ 待补充...

#### 特技
+ 待补充...
