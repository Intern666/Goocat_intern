# Goocat 问答系统
123
# Goocat 问答系统 123
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

- 运行，打开http://127.0.0.1:5000


