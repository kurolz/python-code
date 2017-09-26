#!python3
# coding: utf-8
#

'''
有时我们无法确认备份与源目录文件是否保持一致，包括源目录中的新文件或目录、更新文件或目录有无成功同步，定期进行校验，没有成功则希望有针对性地进行补备份。

本例使用了filecmp模块的left_only、diff_files方法递归获取源目录的更新项，再通过shutil.copyfile、os.makedirs方法对更新项进行复制，最终保持一致状态。
'''


import os
import sys
import filecmp
import re
import shutil
holderlist=[]

def compareme(dir1,dir2):   #递归获取更新项函数
	dircomp = filecmp.dircmp(dir1,dir2)
	only_in_one = dircomp.left_only     #源目录新文件或目录
	diff_in_one = dircomp.diff_files    #不匹配文件，源目录文件已经发生变化
	dirpath = os.path.abspath(dir1)     #定义源目录绝对路径
	[holderlist.append(os.path.abspath(os.path.join(dir1,x))) for x in only_in_one]
	[holderlist.append(os.path.abspath(os.path.join(dir1,x))) for x in diff_in_one]

	if len(dircomp.common_dirs) > 0:    #判断是否存在相同子目录，以便递归
		for item in dircomp.common_dirs:    #递归子目录
			compareme(os.path.abspath(os.path.join(dir1,item)), os.path.abspath(os.path.join(dir2,item)))
	return holderlist
def checkargv():
	if len(sys.argv) < 2:   #要求输入源目录与备份目录
		print ("Usage: ", sys.argv[0], "datadir backupdir")
		sys.exit()
	else:
		dir1 = sys.argv[1]
		dir2 = sys.argv[2]
		source_files = compareme(dir1,dir2)     #对比源目录与备份目录
		dir1 = os.path.abspath(dir1)

		if not dir2.endswith('/'):      #备份目录路径加“/”符
			dir2 = dir2+'/'
		dir2 = os.path.abspath(dir2)
		destination_files = []
		createdir_bool = False

		for item in source_files:   #遍历返回的差异文件或目录清单
			destination_dir = re.sub(dir1,dir2,item)    #将源目录差异路径清单对应替换成备份目录
			destination_files.append(destination_dir)
			if os.path.isdir(item):     #如果差异路径为目录且不存在，则再备份目录中创建
				if not os.path.exists(destination_dir):
					os.makedirs(destination_dir)
					createdir_bool = True   #再次调用compareme函数标记

		if createdir_bool:      #重新调用compareme函数，重新遍历新创建目录的内容
			destination_files = []
			source_files = []
			source_files = compareme(dir1,dir2)     #调用compareme函数
			for item in source_files:   #获取源目录差异路径清单，对应替换成备份目录
				destination_dir = re.sub(dir1,dir2,item)
				destination_files.append(destination_dir)

		print ("update item: ")
		print (source_files)    #输出更新项列表清单
		copy_pair = zip(source_files,destination_files)     #讲源目录与备份目录文件清单拆分成元组
		for item in copy_pair:
			if os.path.isfile(item[0]):     #判断是否为文件，是则进行复制操作
				shutil.copyfile(item[0], item[1])

if __name__ == '__main__':
	checkargv()
