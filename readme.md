# 脚本用户手册

## 简介

作者：张家宝 / bk

使用语言：python

许可证：GNU General Public License v3.0

## names.py

### 介绍 

names.py是更名工具，用python编写，效果是让同文件夹下的所有doc和docx后缀名的变成

> [名字 数字.doc] 的格式

### 使用方法

使用python来打开，或者`shift+右键`该文件夹的空白位置，使用终端**powershell** 打开

然后输入

```powershell
python names.py [-path] [-ext] [-flag]
```

可供的可选选项如下：

- -path='./'   # 遍历指定的位置 ['./sub_dir/']|['./sub_dir/second_sub_dir/']

- -ext='\\.doc|\\.docx'  # 指定后缀名 ['\.zip|\\.tar']。默认对doc和docx后缀名的文件起作用。
- -flag='默认为空' # 遇到更名后重名的时候是否删除的默认方法 [all-yes]|[all-no]

## roll_call.py

### 介绍 

roll_call.py是更名工具，用python编写，效果是以名册为例，给所有文件目录下的文件做一次点名，并列出没有交作业的人的名单。

### 使用方法

使用python来打开，或者`shift+右键`该文件夹的空白位置，使用终端**powershell** 打开

然后输入

```powershell
python roll_call.py [-path] [-ext] 
```

可供的可选选项如下：

- -path='./'   # 遍历指定的位置 ['./sub_dir/']|['./sub_dir/second_sub_dir/']

- -ext='\\.doc|\\.docx'  # 指定后缀名 ['\.zip|\\.tar']
