
### 打包上传的步骤
4、安装打包工具

python -m pip install --upgrade setuptools wheel

 5、打包模块

# 创建存放模块的目录，执行如下命令
python setup.py sdist bdist_wheel

 6、上传模块

6.1、安装用于发布模块的工具：twine 【已安装无需重复安装】

python -m pip install --upgrade twine
或
pip install --upgrade twine

提示：python -m 的作用是 run library module as a script (terminates option list)[作为脚本运行库模块(终止选项列表)]

 6.2、发布（上传）

python -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/*
或
twine upload --repository-url https://upload.pypi.org/legacy/  dist/*

 注意：上传时，提示需要输入PyPI的用户名和密码.

7、测试在线安装模块



