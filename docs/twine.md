
# 打包上传的步骤
## 安装打包工具
~~~python
python -m pip install --upgrade setuptools wheel
~~~

## 打包模块
~~~python
### 创建存放模块的目录，执行如下命令
python setup.py sdist bdist_wheel
~~~
## 上传模块

安装用于发布模块的工具：twine 【已安装无需重复安装】
~~~python
python -m pip install --upgrade twine
或
pip install --upgrade twine
~~~
提示：python -m 的作用是 run library module as a script (terminates option list)[作为脚本运行库模块(终止选项列表)]

## 发布（上传）
~~~python
python -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/*
或
twine upload --repository-url https://upload.pypi.org/legacy/  dist/*
~~~
 注意：上传时，提示需要输入PyPI的用户名和密码.
 
## 测试在线安装模块



