# Goocat 问答系统
### 项目介绍
一个可以自动问答的校园论坛

### 所需环境
python2.7 

mysql版本 5.7

### 使用方法
- pycharm直接打开该文件夹

- 导入数据库，sql文件放在sql文件夹中

- 安装pymysql，flask包

- 修改数据库配置改成自己的 dbhelper.py
```
config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'language',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
        }
```

- 运行，打开http://127.0.0.1:5000


