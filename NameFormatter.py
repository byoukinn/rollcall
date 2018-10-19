# -*- coding: utf-8 -*-
# 批量改名工具，效果：‘204051名字’->‘名字 204051’ 
# 使用方法
# cmd:> python NameFormatter.py [-path] [-ext] [-flag]
# 默认值只对此文件目录下docx和doc文件起效果，可以修改附加项

import os
import re
import argparse
import numpy as np

# region: 这段代码用于随控制台的可选参数，仅控制台可用。
parser = argparse.ArgumentParser(description="""
-path='.'  path to use this script.
-ext='\.docx|\.doc' ['\.zip|\.exe']  extension of file to rename.
-flag='' [all-yes | all-no] call when exits same filename after rename.
""")
parser.add_argument('-path', type=str, default='.')
parser.add_argument('-ext', type=str, default='\.docx|\.doc')
parser.add_argument('-flag', type=str, default='')
args = parser.parse_args()


class NameFormatter:
    def __init__(self, path, ext, flag):
        self.path = path
        self.ext = ext
        self.flag = flag

    # 改名函数
    # 思路：
    # 对给出文件树下的每个后缀名为给出ext的
    # 读取名字，做格式化字符串，并重命名回去。
    # 如改名后有重名文件，向用户询问是否删除
    def pretty_name_by_path(self):
        file_list = []
        file_count = 0
        if not os.path.exists(self.path):
            return file_list
        for root, dirs, names in os.walk(self.path):
            for name in names:
                r_name, extension = os.path.splitext(name)
                if re.match(self.ext, extension):
                    try:
                        # TODO: 得加入自动改名程序
                        os.rename(os.path.join(root, name),
                                  os.path.join(root, NameFormatter.formatted(r_name) + extension))
                        file_count += 1
                    except FileExistsError:
                        print('[Warning] exits same filename after rename：{}'.format(os.path.join(root, name)))
                        self.confirm_delete(root, name)
        print("{} files has been affected.".format(file_count))

    # 确认删除方法
    # 会向用户请求是否删除指令
    # 如果输入了 all-no 或者 all-yes 就不再需要用户确认
    def confirm_delete(self, root, name):
        # 三种情况 yes no 缺省
        if self.flag in ('all-no', 'all-yes'):
            if self.flag is 'all-yes':
                os.remove(os.path.join(root, name))
            return
        flag = input("delete this file? y/[n]，| want to delete all?  all-yes/all-no")
        if flag in ('yes', 'y'):
            os.remove(os.path.join(root, name))
        self.flag = flag

    # 格式化字符串（格式：‘名字 12345678910.docx’）
    def formatted(name):
        chr = re.sub('[0-9]', '', name).strip("_-+/\\\;\'!· @#$%^&*()[]|=！￥…（）【】，。、.`~,:\" ")
        num = re.sub('[^0-9]', '', name).strip().lstrip('20175533')
        return '{} {}'.format(chr, num)
    formatted = staticmethod(formatted)

    def fix_failed_name(self, roll, name):
        roll = list(roll)
        matches = []  # TODO 如果两个长度一样，让用户选择
        max_len = -1
        for i in range(len(roll)):
            matches.append(NameFormatter.max_match_of(name, roll[i]))
            if matches[i] > max_len:
                max_len = matches[i]
        return [] if max_len is 0 else matches

    def max_match_of(a, b):
        n = len(a)
        m = len(b)
        dp = np.zeros((n, m))
        # 第一行
        for i in range(len(a)):
            if a[i].__eq__(b[0]):
                for j in range(i + 1):
                    dp[j][0] = 1
                break
        # 第一列
        for i in range(len(b)):
            if b[i].__eq__(a[0]):
                for j in range(i + 1):
                    dp[0][j] = 1
                break
        for i in range(1, n):
            for j in range(1, m):
                if a[i].__eq__(b[j]):
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[-1][-1]
    max_match_of = staticmethod(max_match_of)


# 主方法
def main():
    process = NameFormatter(args.path, args.ext, args.flag)
    process.pretty_name_by_path()
    # roll = ['黄女士', '张经理', '赵管', "叶错干扰", '李导演']  # 给定名册
    # name = ['李错演', '李导', '错导', '李演', '错错导演', "完全不匹配"]  # 考虑情况
    # print("匹配情况如下（左边在右边有多少个相同的字符）")
    # for n in name:
    #     print("[{}] --> {}".format(n, fix_failed_name(roll, n)))


if __name__ == '__main__':
    main()
