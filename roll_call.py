# -*- coding: utf-8 -*-
# 点名工具，数已交作业份数，
# 把所有未交作业的人员列出来
# 使用方法
# cmd:> python roll_call.py [-path] [-ext]
# 默认值只对此文件目录下docx和doc文件起效果，可以修改附加项

import os
import re
import argparse

# region：这段代码用于在控制台生成可选参数
parser = argparse.ArgumentParser(description="""
-path='.' path to call a roll.
-ext='\.docx' extension will be count in a called list.
""")
parser.add_argument('-path', type=str, default='.')
parser.add_argument('-ext', type=str, default='\.docx|\.doc')
args = parser.parse_args()


# 根据存在文件生成已点名集合
def call_by_path(dir_path, ext, roll):
    name_list = set()
    failed = set()
    file_count = 0
    if not os.path.exists(dir_path):
        return name_list
    for root, dirs, names in os.walk(dir_path):
        for name in names:
            r_name, extension = os.path.splitext(name)
            if re.match(ext, extension):
                person_name = get_chr(name)
                if person_name not in name_list:
                    name_list.add(person_name)
                else:
                    print("\033[1;31m$命名重复: [{}]".format(person_name))
                if person_name not in roll:
                    failed.add(person_name)
                file_count += 1
    print("\033[0m{} files has been affected.".format(file_count))
    return name_list, failed


# 提取名字函数
def get_chr(name):
    return re.sub('[0-9a-zA-Z._\-+/\\\;\'!@#$%^&*()[]|、=]', '', name).strip()


# 从名字手册里拿到所有名字
def get_roll_by_path(file_name):
    called = []
    file = open('./' + file_name, 'r', encoding='UTF-8')
    try:
        for line in file:
            called.append(line.strip())
    finally:
        file.close()
    return called


# 主方法
# 点名思路：
# 已知有一个全员名册，
# 对给出路径的已有文件做提取名字操作，并存于一个已点名集合
# 对全员名册和已点名集合做差，得出为交作业人员集合
# 做打印工作
def main():
    print("\033[1;31m" + '*'*50)
    roll = set(get_roll_by_path('names.list'))
    called, failed = call_by_path(args.path, args.ext, roll)  # 点好名的册
    need_remind = roll - called

    print("\033[0m$上交进度: \033[0;36m{}\033[0m/\033[0;32m{}\033[0m".format(len(called), len(roll)))
    if len(failed):
        print("\033[0;31m$命名错误: {} Error(s)  请重命名: \033[0;34m{}".format(len(failed), failed))
    print("\033[0m$未交人数: \033[4;36m{}\033[0m".format(len(need_remind)))
    print("\033[0m$未交名单: ")
    cnt = 0
    for name in need_remind:  # 没交的显示出来
        cnt += 1
        print("\033[0;37m\t{}.\033[1;36m {}".format(cnt, name))
    print("\033[1;31m" + '*'*50)


if __name__ == '__main__':
    main()
