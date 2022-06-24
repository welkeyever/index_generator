import os
from re import X
import sys
from traceback import print_tb

work_dir = '.'


# 遍历当前路径下所有文件和目录生成md目录结构
def walk_the_dir():
    output = ''
    chapter = []
    for root, dirs, files in os.walk(work_dir):
        for d in dirs:
            if d.startswith('Section'):
                chapter.append(d)
    chapter.sort()
    for c in chapter:
        for root, dirs, sub_ch in os.walk(c):
            if len(sub_ch) == 0:
                continue
            sub_ch.sort()
            has_title_parse = False
            if not has_title_parse:
                with open(os.path.join(root, sub_ch[0]), 'r') as f:
                    first_line = f.readline()
                    title = first_line.split(' ')[-1].strip()
                    output += "## {}\n".format(title)
                    has_title_parse = True
            for f in sub_ch:
                output += '* [{}]({}/{})\n'.format(f.strip('.md'), c, f)
        output += '\n'
    return output


# 持久化内容到磁盘
def persist(content):
    with open('{}/index.md'.format(work_dir), 'w') as f:
        f.write(content)


# 给md文件添加元信息
def add_meta_info(title, content):
    title = get_current_file_name(work_dir) if title == '' else title
    return '# {}\n\n{}'.format(title, content)


# 获取对应路径的文件名
def get_current_file_name(path):
    return os.path.basename(os.path.abspath(path))


def process():
    global work_dir

    if len(sys.argv) >= 2:
        work_dir = sys.argv[1]
        if not os.path.isdir(work_dir):
            exit('{} is not a directory'.format(work_dir))
    work_dir = os.path.abspath(work_dir)

    title = ''
    if len(sys.argv) >= 3:
        title = sys.argv[2]

    c = walk_the_dir()
    c = add_meta_info(title, c)
    persist(c)


if __name__ == '__main__':
    process()
