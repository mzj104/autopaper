from fetch_hot import gen_hot
from gen_dir import gen_dirs
from write_agent import gen
from submit import toutiao
import shutil
import os

def clear_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"目录不存在: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或软链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除子文件夹
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"无法删除 {file_path}。错误: {e}")

    print(f"已清空文件夹内容: {folder_path}")

def init():
    folder_path = r'C:\Users\10165\PycharmProjects\autopaper\main\images'
    folder_path2 = r'C:\Users\10165\PycharmProjects\autopaper\main\output'
    try:
        os.remove(r'C:\Users\10165\PycharmProjects\autopaper\main\data.json')
    except:
        pass
    try:
        os.remove(r'C:\Users\10165\PycharmProjects\autopaper\main\hot.txt')
    except:
        pass
    clear_folder(folder_path)
    clear_folder(folder_path2)

init()
# titles = gen_hot()
# for i in range(4, len(titles)):

title = '端午挂艾有讲究'
if len(title) > 30:
    title = title[:30]
gen_dirs(title)
gen()
# toutiao(title)
# break


