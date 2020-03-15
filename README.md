# Goocat 问答系统
### 项目介绍
一个可以自动问答的校园论坛

### 所需环境
python2.7  python3

mysql版本 5.7

### 使用方法
- 克隆项目到本地

```
git clone https://github.com/Intern666/Goocat_intern.git
```

- 先创建一个虚拟环境，避免污染整个Python的环境。

```
pip install virtualenv
```

- 创建一个文件夹，名字：Virtualenv

```
mkdir Virtualenv
cd Virtualenv
```

- 创建一个虚拟环境 venv

```
virtualenv venv
```

激活虚拟环境

```
cd venv
cd Scripts
activate
```

- 安装需要的各种包

```
pip install -r requirements.txt
```

- 导入数据库，sql文件放在sql文件夹中

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
``````
host: 101.37.23.58
User: root
Password: root
Database: goocat
``````
- 运行，打开http://127.0.0.1:5000

### 实现自动问答

- 如果要实现自动问答的效果，需要另外自动问答的部分 

- 切换路径到socket文件夹，安装对应的环境变量

```
pip install -r socket/requirements_socks.txt
运行 python socket/recall_model_socket.py 
将会占用50008端口传送自动回答的数据
```

