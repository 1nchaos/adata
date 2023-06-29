# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time:2023/6/30
@log: 
"""
import os
import time
import zipfile


def zip_ya(folder_path, file_news):
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dir_path, dir_names, filenames in os.walk(folder_path):
        # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = dir_path.replace(folder_path, '')
        # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        f_path = f_path and f_path + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    print(f'压缩成功：{file_news}')
    z.close()


if __name__ == '__main__':
    # 要压缩的文件夹路径
    folder_path = '../../docs/.vuepress/dist'
    # 压缩后的 ZIP 文件路径
    output_path = f"../../docs/.vuepress/dist{int(time.time())}.zip"
    zip_ya(folder_path, output_path)
