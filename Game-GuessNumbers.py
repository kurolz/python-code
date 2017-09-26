#!python3
#coding: utf-8

import random

print ('********* 猜数字游戏规则 *********\n'
       '系统生成4次1-30的随机整数，每个用户猜4次，'
       '猜对的次数越多，排名越靠前。\n'
       '猜完后输入1到下一位用户，'
       '输入0结束游戏并打印出排行榜。\n'
       '·作者：谢育政 · 版本：Python3.6·\n'
       '**********************************')

names_num = {}  # 猜中多少次，key为名字，value为变量count（猜中的次数）。
zhiling = 1 # 指令，2代表猜对了，1代表没猜中。

while (zhiling == 1):
    count = 0   # 猜中的次数
    name = str(input('请输入您的用户名:'))   # 提示用户输入名字
    print ('############## 游戏开始 ##############')
    try:
        for i in range(1, 5):   # 循环4次，代表每个用户有4次猜数字的机会
            num = int(random.randint(1, 2))    # 生成1-30的随机数
            input_num = int(input('猜一猜数字:'))    # 用户输入数字
            if input_num == num:    # 如果用户输入的数字等于生成的随机数，变量zhiling变为2，输出猜对了，并且猜中的次数+1
                zhiling = 2
                print('猜对了')
                count += 1
            elif input_num > num:   # 如果用户输入的数字大于生成的随机数，输出太大了
                print('太大了')
            elif input_num < num:   # 如果用户输入的数字小于生成的随机数，输出太小了
                print('太小了')
        names_num[name] = count     # 把用户的名字和猜中的次数存入names_num字典
        if zhiling == 1:    # 如果用户4次都没有猜中，输出没有猜对
            print ('【很遗憾您没有猜对】')
        if zhiling == 2:    # 如果用户有猜中，输出用户猜对的次数
            print ('【您猜对了',count,'次】')
        zhiling = int(input('输入 1 继续玩，输入 0或其他 结束游戏并打印排行榜:'))
    except ValueError:  # 当用户输入的不是数字，变量zhiling置于1，提示用户重新开始
        zhiling = 1
        print('************** 只能输入数字！请重新开始！！！ **************\n')

print('\n ----------排行榜 ----------')
sorted_names_num = sorted(names_num.items(), key=lambda d:d[1], reverse=True)   # 字典排序，对用户的成绩排序
for key, value in dict(sorted_names_num).items():   # 打印排序后的排行榜
    print('\t【', key, '】猜对了', value, '次!')
print('\n ---------------------------')

