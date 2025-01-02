- 1、安装依赖

```shell
pip install -r requirements.txt
```
- 2、修改settings.py中的数据库配置
```python
DATABASE = {
    'host': 'localhost',    # 数据库地址
    'port': '3306',         # 数据库端口
    'user': 'root',         # 数据库用户名
    'password': 'mysql',    # 数据库密码
    'database': 'testapi02',# 数据库名
}
```
- 3、生成迁移配置文件

```shell
aerich init -t settings.TORTOISE_ORM
```
- 4、初始化执行迁移，生成数据库表

```shell
aerich init-db
```
- 5、启动项目

```shell
运行 main.py
- 6、接口文档访问地址
```python
http://127.0.0.1:8800/docs
```
- 7、温馨提示：若本地运行，需要有mysql、redis的运行环境
