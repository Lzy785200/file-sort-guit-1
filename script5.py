import os
import shutil

#引入界面库
import tkinter as tk
from tkinter import filedialog, messagebox
#分类规则字典
RULES = {
    ".txt": "txt",
    ".jpg": "jpg",
    ".png": "png",
    ".gif": "gif",
    ".mp4": "mp4",
    ".avi": "avi",
    ".mov": "mov",
    ".mp3": "mp3",
    ".wav": "wav",
    ".exe": "exe",
    ".dll": "dll",
    ".pdf": "pdf",
    ".doc": "doc",
    ".docx": "docx",
    ".xls": "xls",
    ".xlsx": "xlsx",
    ".ppt": "ppt",
    ".pptx": "pptx",
}
def organize_files(target_path, log):#文件整理函数

    #防呆1：路径存在检查
    if not os.path.exists(target_path):
        log(f"路径{target_path}不存在")
        return

    #防呆2：确保输入的是文件夹，不是单个文件
    if not os.path.isdir(target_path):
        log(f"错误：{target_path}不是一个文件夹")
        return

    #防呆3：交互确认
    log(f"\n开始整理。。。")
    file_list = os.listdir(target_path)


    #初始化统计变量
    success_count = 0
    failure_count = 0
    skip_count = 0

    #遍历文件夹中的所有文件
    for target_name in file_list:
        full_path = os.path.join(target_path, target_name)
        if os.path.isdir(full_path):
            continue

        #提取后缀，统一小写
        name,ext = os.path.splitext(target_name)
        ext = ext.lower()

        #判断后缀是否在规则字典中
        if ext in RULES:
            folder_name = RULES[ext]
            dest_folder = os.path.join(target_path, folder_name)
            #没有就建立
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)


            #防御
            try:
                shutil.move(full_path, os.path.join(dest_folder, target_name))
                log(f"已经把{target_name}移动到{dest_folder}")
                success_count += 1
            except Exception as e:
                log(f"错误：{e}")
                failure_count += 1

        else:
            #如果后缀不在规则里，跳过不处理
            log(f"发现未知文件：{ext},跳过不处理:{ext}")
            skip_count += 1


    #结果
    log(f"\n恭喜，文件整理完成！")
    log(f"成功整理文件：{success_count}个")
    log(f"失败文件：{failure_count}个")
    log(f"跳过文件：{skip_count}个")


#入口



#创建主窗口

root = tk.Tk()
root.title("李祖阳的第一个软件")#窗口标题
root.geometry("400x200")#窗口大小

#让窗口跑起来


# 添加一个日志显示框
log_text = tk.Text(root, height=10, width=60)
log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


def select_and_run():
    #1.弹出文件夹选择框
    target_path = filedialog.askdirectory(title="请选择要整理的文件夹")
    if not target_path:
        return

    #安全提示
    confirm = messagebox.askyesno("安全确认",f"确定要整理该文件夹吗？\n{target_path}")
    if not confirm:
        return

    # 2.清理旧日志，准备开始
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "开始整理。。。\n")

    # 3.调用写好的核心逻辑
    #把target_path 传进去，并告诉它日志要写到哪里（用 lambda 实现）
    organize_files(target_path, lambda msg: log_text.insert(tk.END, msg + "\n"))

    messagebox.showinfo("完成","整理完毕！")

# 创建一个按钮，并绑定上面的函数
btn = tk.Button(root, text="选择文件夹并开始整理", command=select_and_run)
btn.pack(pady=10)

labal = tk.Label(root, text="一键整理文件夹，告别乱糟糟！", font=("微软雅黑", 12,"bold"))
labal.pack(pady=10)
root.mainloop()