from config import *
import shutil
import os
import re
import jieba

# # jieba_have_delete = ["于点", "交于", "中高", "外作", "相交于", "上且", "腰交于", "线交", "边交于", "交边", "交作",
# #                      "边于", "线于", "点作"]
# # map_keywords = ["线", "三角形", "△", "Rt△", "rt△", "直角三角形", "直角△", "等腰三角形", "等腰△", "等边三角形", "等边△",
# #                 "等腰直角三角形", "等腰直角△",
# #                 "等腰Rt△", "四边形", "矩形", "正方形", "长方形", "▭", "平行四边形", "▱", "▰", "梯形", "等腰梯形",
# #                 "直角梯形", "等腰直角梯形", "菱形", "◇",
# #                 "◆", "多边形", "凸多边形", "平行且相等", "<>", "平行于"]  # 有坑不等于
# # map_clear_up_keywords = ["线", "三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形", "矩形",
# #                          "正方形", "长方形", "平行四边形",
# #                          "梯形", "等腰梯形", "直角梯形", "菱形", "多边形", "凸多边形", "五边形", "六边形", "七边形",
# #                          "高"]
# # map_clear_up_keywords_value = [0, 1, 2.01, 2.02, 2.03, 4.03, 5, 8.01, 8.04, 8.03, 10.02, 6.01, 7.02, 7.03, 10.01, 9, 10,
# #                                11, 12, 13]
# # map_clear_up_keywords_error = [14.02, 14.04, 14.05, 14.05, 15.03, 15.04, 15.05, 15.06, 15.06, 15.07, 16.02, 16.03,
# #                                17.03, 17.04, 17.04, 17.05, 18.02, 18.03, 23, 24, 25, 0]  # 当权值相加时不可能出现这类情况
# # # print(sorted(list(map_clear_up_keywords_error)))
# # symbol_keywords = ["∠", "°", "+", "-", "/", "*", "·", "^", "'", "√", "≤", "≥"]
# # symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]  # 留坑 三角形的全等无法实现
# # side = ["三边", "四边", "五边", "六边"]
# # the_capital_form_of_a_chinese_number = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
# # seg_list_all_triangle = []


# # def if_letter(seg_list):  # 检查是否为英文
# #     return seg_list.encode('utf-8').isalpha()


# # def if_number(num):  # 检测是否为数字
# #     if len(num) == 0:
# #         return False
# #     for i in range(len(num)):
# #         if '0' <= num[i] <= '9' or num[i] == ".":
# #             continue
# #         else:
# #             return False
# #     return True


# # def if_number_and_letter(seg_list):
# #     for i in range(len(seg_list)):
# #         if if_letter(seg_list[i]) or if_number(seg_list[i]):
# #             continue
# #         else:
# #             return False
# #     return True


# # def delete_blank(seg_list):  # 删除空格
# #     j = 0
# #     while j == 0:
# #         if len(seg_list) == 0:
# #             break
# #         for i in range(len(seg_list)):
# #             if seg_list[i] == " " or seg_list[i] == "":
# #                 seg_list1 = seg_list[i + 1:]
# #                 seg_list2 = seg_list[:i]
# #                 seg_list = seg_list2 + seg_list1
# #                 break
# #             i += 1
# #             if i >= (len(seg_list) - 1):
# #                 j += 1
# #     return seg_list


# # def conversion_parallel(seg_list):  # 对//进行处理
# #     j = 0
# #     while j == 0:
# #         for i in range(len(seg_list) - 1):
# #             if seg_list[i] == "/" and seg_list[i + 1] == "/":
# #                 seg_list1 = seg_list[i + 2:]
# #                 seg_list2 = seg_list[:i]
# #                 seg_list = seg_list2 + ["//"] + seg_list1
# #                 break
# #             if seg_list[i] == "\\" and seg_list[i + 1] == "\\":
# #                 seg_list1 = seg_list[i + 2:]
# #                 seg_list2 = seg_list[:i]
# #                 seg_list = seg_list2 + ["//"] + seg_list1
# #                 break
# #             i += 1
# #             if i >= (len(seg_list) - 1):
# #                 j += 1
# #     return seg_list


# # # 将三边\四边给去掉
# # def transition_side(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if seg_list_having(side, seg_list_list[i]):
# #             seg_list_temp = return_how_many_side(seg_list_having_0(side, seg_list_list[i]))
# #             seg_anger_temp = []
# #             for j in range(seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i]))):
# #                 # 从后面往前面找
# #                 if if_letter(
# #                         seg_list_list[i][seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]):
# #                     seg_list_anger = seg_list_list[i][
# #                         seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]
# #                     if len(seg_list_anger) == seg_list_temp:
# #                         seg_anger = []
# #                         for k in range(len(seg_list_anger)):
# #                             seg_anger.insert(len(seg_list_anger), seg_list_anger[k])
# #                         for k in range(len(seg_list_anger)):
# #                             seg_list_anger_temp = ""
# #                             if k + 1 != len(seg_list_anger):
# #                                 seg_list_anger_temp += seg_list_anger[k]
# #                                 seg_list_anger_temp += seg_list_anger[k + 1]
# #                                 seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
# #                             else:
# #                                 seg_list_anger_temp += seg_list_anger[0]
# #                                 seg_list_anger_temp += seg_list_anger[k]
# #                                 seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
# #                             if len(seg_anger_temp) != len(seg_list_anger) * 2 - 1:
# #                                 seg_anger_temp.insert(len(seg_anger_temp), "、")

# #             seg_list_ = seg_list_list[i]
# #             seg_list_front = seg_list_[:seg_list_.index(seg_list_having_0(side, seg_list_))]
# #             seg_list_behind = seg_list_[seg_list_.index(seg_list_having_0(side, seg_list_)) + 1:]
# #             seg_list_front.extend(",")
# #             seg_list_front.extend(seg_anger_temp)
# #             seg_list_front.extend(seg_list_behind)
# #             seg_list_list[i] = seg_list_front
# #     seg_list_t = []
# #     for i in range(len(seg_list_list)):
# #         seg_list_t.extend(seg_list_list[i])
# #         seg_list_t.extend(",")
# #     return seg_list_t


# # def conversion_symbols(seg_list):  # 将图形转换为汉字
# #     for i in range(len(seg_list)):
# #         temp = seg_list[i]
# #         if seg_list[i] in ["Rt", "rt"] and seg_list[i + 1] in ["△", "三角形"]:
# #             temp = "".join("直角")
# #         elif seg_list[i] in ["Rt△", "rt△"]:
# #             temp = "".join("直角三角形")
# #         elif seg_list[i] in ["▱", "▰"]:
# #             temp = "".join("平行四边形")
# #         elif seg_list[i] in ["▭", "▯", "▮"]:
# #             temp = "".join("长方形")
# #         elif seg_list[i] in ["□", "■", "▪", "▫", "◻", "◼", "◽", "◾"]:
# #             temp = "".join("正方形")
# #         elif seg_list[i] in ["◇", "◆"]:
# #             temp = "".join("菱形")
# #         elif seg_list[i] in ["⊿"]:
# #             temp = "".join("直角三角形")
# #         elif seg_list[i] in ["！"]:
# #             temp = "".join("!")
# #         elif seg_list[i] in ["＜"]:
# #             temp = "".join("<")
# #         elif seg_list[i] in ["＝"]:
# #             temp = "".join("=")
# #         elif seg_list[i] in ["≦", "≮"]:
# #             temp = "".join("≤")
# #         elif seg_list[i] in ["≧", "≯"]:
# #             temp = "".join("≥")
# #         elif seg_list[i] in ["△"]:
# #             temp = "".join("三角形")
# #         elif seg_list[i] in ["角"]:
# #             temp = "".join("∠")
# #         elif seg_list[i] in ["等腰直角梯形"]:
# #             temp = "".join("长方形")
# #         elif seg_list[i] in ["等于"]:
# #             temp = "".join("=")
# #         elif seg_list[i] in ["度"] and if_number(seg_list[i - 1]):
# #             temp = "".join("°")
# #         elif seg_list[i] in ["正三角形"]:
# #             temp = "".join("等边三角形")
# #         elif seg_list[i] in ["想交"]:
# #             temp = "".join("相交")
# #         elif seg_list[i] in ["想交于"]:
# #             temp = "".join("相交于")
# #         elif seg_list[i] in ["重点"]:
# #             temp = "".join("中点")
# #         elif seg_list[i] in ["均"]:
# #             temp = "".join("都")
# #         elif seg_list[i] in ["各"]:
# #             temp = "".join("分别")
# #         elif seg_list[i] in ["读"]:
# #             temp = "".join("°")
# #         elif seg_list[i] in ["∥", "平行于"]:
# #             temp = "".join("//")
# #         elif seg_list[i] in ["已知", "使得", "使", "且有", "并且", "满足", "且", "截取", "∶", "：", "，", "。", "；", "?",
# #                              "？", "(",
# #                              ")", "（", "）", ";"]:
# #             # 将毫无意义的词组删去 将中文符号修改为英文的逗号
# #             temp = "".join(",")
# #         elif seg_list[i] in ["μm"]:
# #             temp = "".join("微米")
# #         elif seg_list[i] in ["nm"]:
# #             temp = "".join("纳米")
# #         elif seg_list[i] in ["mm"]:
# #             temp = "".join("毫米")
# #         elif seg_list[i] in ["cm"]:
# #             temp = "".join("厘米")
# #         elif seg_list[i] in ["dm"]:
# #             temp = "".join("分米")
# #         elif seg_list[i] in ["km"]:
# #             temp = "".join("千米")
# #         elif seg_list[i] in ["m"]:
# #             temp = "".join("米")
# #         seg_list[i] = temp
# #     return seg_list


# # # 将角和三角形等的字母大写
# # def transition_litter_to_super(seg_list):
# #     for i in range(len(seg_list)):
# #         if if_letter(seg_list[i]) and len(seg_list[i]) > 2 and (
# #                 seg_list[i - 1] in "∠" or seg_list[i - 1] in map_clear_up_keywords):
# #             seg_list_letter = str(seg_list[i])
# #             seg_list_letter = seg_list_letter.upper()
# #             seg_list[i] = seg_list_letter
# #     return seg_list


# # # 补全交的符号
# # def seg_list_complement(seg_list):
# #     seg_list_list_temp = []  # 记录三角形的个数
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         # 查询所有的三角形以上的图形，并且合并同类项
# #         if seg_list_having_0(map_clear_up_keywords, seg_list_list[i]):
# #             seg_list_list_i_1 = seg_list_list[i].index(seg_list_having_0(map_clear_up_keywords, seg_list_list[i]))
# #             if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
# #                     seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) > 2 and \
# #                     seg_list_list[i][seg_list_list_i_1 + 1] not in seg_list_list_temp:
# #                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][seg_list_list_i_1 + 1])
# #     if len(seg_list_list_temp) == 0:
# #         return seg_list  # 无三角形等图形，无法进行识别 补全
# #     else:
# #         for i in range(len(seg_list_list)):
# #             if "∠" in seg_list_list[i]:  # 如果存在∠且∠后的字母长度为1
# #                 seg_list_list_i_1 = seg_list_list[i].index("∠")
# #                 if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
# #                         seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) == 1:
# #                     angele_if_in_two_symbol = 0  # 判断是否存在多个图形里面
# #                     angele_in_this_symbol = 0  # 记录当前字母所在的图形的下标
# #                     for j in range(len(seg_list_list_temp)):
# #                         if seg_list_list[i][seg_list_list_i_1 + 1] in seg_list_list_temp[j]:
# #                             if angele_if_in_two_symbol != 0:
# #                                 angele_if_in_two_symbol += 1
# #                                 break  # 如果同时出现在多个图形中也无法 补全
# #                             else:
# #                                 angele_if_in_two_symbol += 1
# #                                 angele_in_this_symbol = j
# #                     if angele_if_in_two_symbol != 1:  # 可能出现角不在前面出现的图形中，也无法处理
# #                         continue
# #                     else:
# #                         tran_angle = ""
# #                         letter = re.findall('[A-Za-z]', seg_list_list_temp[angele_in_this_symbol])
# #                         if seg_list_list[i][seg_list_list_i_1 + 1] in letter:
# #                             if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1 < 0:  # 最前面
# #                                 tran_angle += letter[len(letter) - 1]
# #                             else:
# #                                 tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1]
# #                             tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1])]
# #                             if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1 >= len(letter):  # 最后面
# #                                 tran_angle += letter[0]
# #                             else:
# #                                 tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1]
# #                         seg_list_list[i][seg_list_list_i_1 + 1] = tran_angle
# #     return return_seg_list(seg_list_list)


# # # lAB = 5 --转变---> 边AB = 5 暂时不知道有什么用
# # def seg_list_transition_side(seg_list):
# #     seg_list_temp = 0
# #     while seg_list_temp == 0:
# #         for i in range(len(seg_list)):
# #             if len(seg_list[i]) == 3 and if_letter(seg_list[i]) and seg_list[i][0] == "l":  # lAB
# #                 seg_list_behind = seg_list[i][1:]  # AB
# #                 seg_list[i] = seg_list_behind
# #                 seg_list_front = seg_list[:i]
# #                 seg_list_behind = seg_list[i:]
# #                 seg_list_front.extend("边")
# #                 seg_list_front.extend(seg_list_behind)
# #                 seg_list = seg_list_front
# #                 break
# #             if i + 1 == len(seg_list):
# #                 seg_list_temp += 1
# #     # print("".join(seg_list))
# #     return seg_list


# # # 去除序号
# # def remove_pause(seg_list):
# #     for i in range(len(seg_list) - 1):
# #         if seg_list[i] == "、" and if_number(seg_list[i - 1]) and i <= 2:
# #             seg_list1 = seg_list[i + 1:]
# #             return seg_list1
# #     return seg_list


# # # 删除求证
# # def delete_prove(seg_list):
# #     seg_list_front = []
# #     seg_txt = ["证明", "求解", "求证", "求", "有", "如图", "如图所示"]
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if seg_list_having(seg_txt, seg_list_list[i]):
# #             seg_list_list_wei = seg_list_having_0(seg_txt, seg_list_list[i])
# #             seg_list_front = seg_list_list[i][:seg_list_list[i].index(seg_list_list_wei)]
# #             seg_list_front.extend(",")
# #             if seg_list_list[i].index(seg_list_list_wei) + 1 < len(seg_list_list[i]) and \
# #                     if_number(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1]):
# #                 seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 2:])
# #             else:
# #                 seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1:])
# #             seg_list_list[i] = seg_list_front
# #     return return_seg_list(seg_list_list)


# # # 将大于或者小于或者不等于归一化   <=  --->  ≤
# # def handles_greater_or_less(seg_list):
# #     seg_temp = 0
# #     while seg_temp == 0:
# #         for i in range(len(seg_list)):
# #             if seg_list[i] in ["<", ">", "!"] and i + 1 < len(seg_list) and seg_list[i + 1] in "=":
# #                 seg_list_front = seg_list[:i]
# #                 seg_list_behind = seg_list[i + 2:]
# #                 if seg_list[i] in "<":
# #                     seg_list_front.insert(len(seg_list_front), "≤")
# #                 elif seg_list[i] in ">":
# #                     seg_list_front.insert(len(seg_list_front), "≥")
# #                 elif seg_list[i] in "!":
# #                     seg_list_front.insert(len(seg_list_front), "!=")
# #                 seg_list_front.extend(seg_list_behind)
# #                 seg_list = seg_list_front
# #                 break
# #             if i + 1 == len(seg_list):
# #                 seg_temp = 1
# #     return seg_list


# # # 给末尾加上;
# # def add_end_punctuation(seg_list):
# #     for i in range(len(seg_list)):
# #         if seg_list[len(seg_list) - 1 - i] in [".", ",", ";", "?", "？"] and \
# #                 seg_list[len(seg_list) - 2 - i] in [".", ",", ";", "?", "？"]:
# #             continue
# #         else:
# #             seg_list = seg_list[:len(seg_list) - 1 - i]
# #             seg_list.append(";")
# #             return seg_list
# #     return seg_list


# # # 按照逗号或者句号分句
# # def cut_clause(seg_list):
# #     for i in range(len(seg_list) - 1):
# #         if seg_list[i] in [",", ".", "，", "。"]:
# #             seg_list1 = seg_list[
# #                         i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ['.', ','] else len(seg_list)]
# #             seg_list2 = seg_list[:i]
# #             return seg_list2, seg_list1
# #     return seg_list, ""


# # # 对顿号进行切割
# # def cut_clause_slight_pause(seg_list):
# #     for i in range(len(seg_list) - 1):
# #         if seg_list[i] in ["、", "和", "与", "."]:
# #             seg_list1 = seg_list[
# #                         i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ["、", "和", "与", "."] else len(
# #                             seg_list)]
# #             seg_list2 = seg_list[:i]
# #             return seg_list2, seg_list1
# #     return seg_list, ""


# # # 给长宽高边长面积周长前适当加"的"
# # def add_de_to_side(seg_list):
# #     seg_temp = 0
# #     while seg_temp == 0:
# #         for i in range(len(seg_list)):
# #             if seg_list[i] in ["长", "宽", "高", "边长", "周长", "面积"]:
# #                 if i == 0 or seg_list[i - 1] in [",", "."] or seg_list[i - 1] in ["的"] or seg_list[i - 1] in ["是"]:
# #                     continue
# #                 elif i > 1 and if_letter(seg_list[i - 1]) and len(seg_list[i - 1]) > 1:  # ABC长AD为
# #                     seg_list_front = seg_list[:i]
# #                     seg_list_front.insert(i, "的")
# #                     seg_list_front.extend(seg_list[i:])
# #                     seg_list = seg_list_front
# #                     break
# #                 elif i > 2 and (seg_list[i - 1] in ["中"] and if_letter(seg_list[i - 2])) and len(seg_list[i - 2]) > 1:
# #                     seg_list_front = seg_list[:i]
# #                     seg_list_front.insert(i, "的")
# #                     seg_list_front.extend(seg_list[i:])
# #                     seg_list = seg_list_front
# #                     break
# #             if i + 1 == len(seg_list):
# #                 seg_temp = 1
# #     # print(seg_list)
# #     return seg_list


# # # 将作从（过A 作AS垂直于DF)提取出来
# # def cut_zuo_from_seg_list(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if seg_list_having(symbol_keywords_main, seg_list_list[i]) and "作" in seg_list_list[i]:
# #             seg_list_front = seg_list_list[i][
# #                              :seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i]))]  # 垂直之前
# #             seg_list_behind = seg_list_list[i][
# #                               seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i])):]  # 垂直之后
# #             seg_list_front_behind = seg_list_front[seg_list_front.index("作"):]  # 作之后，找后面的一个词组
# #             seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)  # 找到词组
# #             seg_list_front.extend(",")  # 过A 作AS，
# #             seg_list_front.insert(len(seg_list_front), seg_list_front_behind_letter[0][1])  # 过A 作AS，AS
# #             seg_list_front.extend(seg_list_behind)  # 过A 作AS，AS垂直DF
# #             seg_list_list_front = seg_list_list[:i]
# #             seg_list_list_behind = seg_list_list[i + 1:]
# #             seg_list_list_front.insert(len(seg_list_list_front), seg_list_front)
# #             seg_list_list_front.extend(seg_list_list_behind)
# #             seg_list_list = seg_list_list_front
# #     seg_list = []
# #     for i in range(len(seg_list_list)):
# #         seg_list.extend(seg_list_list[i])
# #         seg_list.extend(",")
# #     # print("".join(seg_list))
# #     return seg_list


# # # 将垂直后加一个逗号切分
# # def add_comma_at_equal(seg_list):
# #     seg_list_temp = 0
# #     while seg_list_temp == 0:
# #         for i in range(len(seg_list)):
# #             if i + 1 == len(seg_list):
# #                 seg_list_temp = 1
# #             if seg_list[i] in symbol_keywords_main:
# #                 for j in range(1, 3):
# #                     if i + j > len(seg_list):
# #                         break
# #                     if seg_list[i + j] not in map_clear_up_keywords and seg_list[
# #                         i + j] not in symbol_keywords and not if_number_and_letter(seg_list[i + j]) and seg_list[
# #                         i + j] not in ["于", "点"]:

# #                         if seg_list[i + j] != ",":
# #                             seg_list_front = seg_list[:i + j]
# #                             seg_list_behind = seg_list[i + j:]
# #                             seg_list_front.extend(",")
# #                             seg_list_front.extend(seg_list_behind)
# #                             seg_list_temp1 = 1
# #                             seg_list = seg_list_front
# #                             break
# #                         else:
# #                             break
# #     return seg_list


# # # 根据输入不同的symbol进行类似连等的分割
# # def find_which_equal(seg_list, symbol):
# #     equal_value = []  # 存储当前段落的所有的等式的元素
# #     seg_list1_front = []
# #     seg_list2_front = []
# #     seg_list2_behind = []
# #     seg_list_behind_behind_letter = []
# #     seg_list_behind_behind_other = []
# #     seg_list_front_front_other = []
# #     seg_list_front_behind_other = []
# #     seg_list1 = seg_list[:seg_list.index(symbol)]
# #     # 梯形ABCD的面积=EF·AB
# #     if len(seg_list1) > 2:
# #         if "作" in seg_list:  # 作三角形ABC的AD垂直CV
# #             seg_list1_front = seg_list1[:seg_list1.index("作")]
# #             seg_list1_behind = seg_list1[seg_list1.index("作"):]
# #             if "的" in seg_list1_behind:
# #                 seg_list_behind_front = seg_list1_behind[:seg_list1_behind.index("的")]
# #                 seg_list1_behind_behind = seg_list1_behind[seg_list1_behind.index("的"):]
# #                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
# #                 if len(seg_list_behind_behind_letter) == 0:
# #                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #                 seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
# #             else:
# #                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind)
# #                 seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
# #         elif "的" in seg_list1:
# #             seg_list_behind_front = seg_list1[:seg_list1.index("的")]
# #             seg_list1_behind_behind = seg_list1[seg_list1.index("的"):]
# #             seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
# #             if len(seg_list_behind_behind_letter) == 0:
# #                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #             seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
# #         else:
# #             seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1)
# #             seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
# #         seg_list_front_front_other = seg_list_behind_behind_other[0]  # 存储前半部分的其他部分
# #         seg_list_front_behind_other = seg_list_behind_behind_other[1]  # 存储字母后半部分的其他部分
# #     seg_list2 = seg_list[seg_list.index(symbol) + 1:]
# #     if len(seg_list_behind_behind_letter) > 0:
# #         equal_value.append(dispose_cut_front_equal(seg_list_behind_behind_letter[0][1]))  # 处理等号前半段
# #     else:
# #         equal_value.append(dispose_cut_front_equal(seg_list1))
# #     while symbol in seg_list2:
# #         seg_list0 = seg_list2.copy()
# #         seg_list1 = seg_list0[:seg_list0.index(symbol)]  # 等号前半段
# #         seg_list2 = seg_list0[seg_list0.index(symbol) + 1:]  # 取等号后半段
# #         equal_value.append(dispose_cut_front_equal(seg_list1))  # 处理等号前半段
# #     if len(seg_list2) > 1:  # 过D作DE⊥BC于E
# #         for i in range(len(seg_list2)):
# #             if if_number_and_letter(seg_list2[i]):
# #                 seg_list2_letter = seg_list2[i]
# #                 seg_list2_front = seg_list2[:i]
# #                 seg_list2_behind = seg_list2[i + 1:]
# #                 seg_list2 = seg_list2_letter
# #                 break

# #     equal_value.append(dispose_cut_front_equal(seg_list2))  # 处理等号后半段
# #     equal_value_all = []
# #     for i in range(len(equal_value) - 1):
# #         j = i + 1
# #         while j < len(equal_value):
# #             equal_value_all.extend(seg_list_front_front_other)
# #             equal_value_all.extend(equal_value[i])
# #             equal_value_all.extend(seg_list_front_behind_other)
# #             equal_value_all.append(symbol)
# #             if j + 1 == len(equal_value):
# #                 equal_value_all.extend(seg_list2_front)
# #             equal_value_all.extend(equal_value[j])
# #             if j + 1 == len(equal_value):
# #                 equal_value_all.extend(seg_list2_behind)
# #             equal_value_all.append(",")
# #             j += 1
# #     return equal_value_all


# # # 处理使用等号分出来的前半段,存在角\边\点种情况
# # def dispose_cut_front_equal(seg_list1):
# #     Str_value = [""]
# #     for i in range(len(seg_list1)):
# #         if seg_list1[i] in symbol_keywords or if_number_and_letter(seg_list1[i]) or seg_list1[i] \
# #                 in map_clear_up_keywords:
# #             if if_letter(seg_list1[i]) and if_letter(Str_value[len(Str_value) - 1]) and len(Str_value) > 0:
# #                 Str_value[len(Str_value) - 1] += (seg_list1[i])
# #             else:
# #                 Str_value.append(seg_list1[i])
# #     Str_value = delete_blank(Str_value)
# #     return Str_value


# # # 提取当前段落的所有英文字母
# # def dispose_cut_front_equal_letter(seg_list1):
# #     Str_value = [""]
# #     for i in range(len(seg_list1)):
# #         if if_letter(seg_list1[i]):
# #             Str_value.append(seg_list1[i])
# #     Str_value_true = "".join(Str_value)
# #     return Str_value_true


# # # 查询当前符号symbol是否在语句seg_list中
# # def seg_list_having(symbol, seg_list):
# #     if len(seg_list) == 0:
# #         return False
# #     for i in range(len(symbol)):
# #         if symbol[i] in seg_list:
# #             return symbol[i]
# #     return False


# # # 查看字符symbol是否有任意一个在字符串中,如果没有返回空字符,否则存在字符.
# # def seg_list_having_0(symbol, seg_list):
# #     if len(seg_list) == 0:
# #         return ""
# #     for i in range(len(symbol)):
# #         if symbol[i] in seg_list:
# #             return symbol[i]
# #     return ""


# # # seg_list[][]中有一点在symbol中的一个值
# # def seg_list_having_1(symbol, seg_list):
# #     if len(seg_list) == 0:
# #         return False
# #     for i in range(len(seg_list)):
# #         for j in range(len(seg_list[i])):
# #             if seg_list[i][j] in symbol:
# #                 return True
# #     return False


# # # symbol与seg_list[][]中存在很小一点的相等
# # def seg_list_having_2(symbol, seg_list):
# #     if len(seg_list) == 0:
# #         return False
# #     for i in range(len(symbol)):
# #         for j in range(len(seg_list)):
# #             for k in range(len(seg_list[j])):
# #                 if symbol[i] == seg_list[j][k]:
# #                     return True
# #     return False


# # def seg_list_having_all(symbol, seg_list):
# #     if len(seg_list) == 0:
# #         return False
# #     for i in range(len(symbol)):
# #         if symbol[i] in seg_list:
# #             continue
# #         else:
# #             return False
# #     return True


# # # 在处理分别中的辅助函数,查看b-b-l的低2列是否是数字
# # def seg_list_behind_behind_letter_if_letter(seg_letter):
# #     for i in range(len(seg_letter)):
# #         if not if_number(seg_letter[i][1]):
# #             break
# #         if i + 1 == len(seg_letter):
# #             return True
# #     return False


# # # 判断是几边形的图形
# # def match_how_many_side(seg_list):
# #     len_seg_list = len(seg_list)
# #     if len_seg_list == 1:
# #         return "点"
# #     elif len_seg_list == 2:
# #         return "边"
# #     elif len_seg_list == 3:
# #         return "三角形"
# #     elif len_seg_list == 4:
# #         return "四边形"
# #     elif len_seg_list == 5:
# #         return "五边形"
# #     elif len_seg_list == 6:
# #         return "六边形"
# #     else:
# #         return "多边形"


# # # 返回两个三角形的边数
# # def return_how_many_side_symbol(symbol1, symbol2):
# #     triangle = ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形"]
# #     quadrangle = ["四边形", "矩形", "正方形", "长方形", "平行四边形", "梯形", "等腰梯形", "直角梯形", "菱形"]
# #     polygon = ["五边形", "六边形", "七边形", "多边形", "凸多边形"]
# #     symbol1_angle = 0
# #     symbol2_angle = 0
# #     if symbol1 in triangle:
# #         symbol1_angle = 3
# #     elif symbol1 in quadrangle:
# #         symbol1_angle = 4
# #     else:
# #         symbol1_angle = 10
# #     if symbol2 in triangle:
# #         symbol2_angle = 3
# #     elif symbol2 in quadrangle:
# #         symbol2_angle = 4
# #     else:
# #         symbol2_angle = 10
# #     return symbol1_angle, symbol2_angle


# # def return_how_many_side(symbol1):
# #     side = ["三边", "四边", "五边", "六边", "七边"]
# #     symbol1_angle = 0
# #     symbol2_angle = 0
# #     if symbol1 in "三边":
# #         symbol1_angle = 3
# #     elif symbol1 in "四边":
# #         symbol1_angle = 4
# #     elif symbol1 in "五边":
# #         symbol1_angle = 5
# #     elif symbol1 in "六边":
# #         symbol1_angle = 6
# #     elif symbol1 in "七边":
# #         symbol1_angle = 7
# #     else:
# #         symbol1_angle = 10

# #     return symbol1_angle


# # def return_how_many_number(symbol, the_capital_form_of_a_chinese_number):
# #     return the_capital_form_of_a_chinese_number.index(symbol) + 1


# # # 查询当前语句是否存在形状,并且形状位置在字母前面
# # def seg_list_having_symbol_letter(symbol, seg_list, letter):
# #     for i in range(len(seg_list)):
# #         if seg_list[i] in symbol and i + 1 == seg_list.index(letter):
# #             return symbol[symbol.index(seg_list[i])]
# #     return ""


# # # 特征值判断是否存在平行且相等的情况
# # def find_if_have_parallel_and_equal(seg_list):
# #     Str = [""]
# #     if "平行且相等" in seg_list:
# #         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
# #         while seg_list1 != "":
# #             if "平行且相等" in seg_list1:  # 如果平行且相等在当前分句里面
# #                 seg_list00 = seg_list1.copy()
# #                 seg_list01 = seg_list00[:seg_list00.index("平行且相等")]
# #                 seg_list02 = seg_list00[seg_list00.index("平行且相等") + 1:]
# #                 seg_list_value_front = dispose_cut_front_equal_letter(seg_list01)
# #                 seg_list_value_behind = dispose_cut_front_equal_letter(seg_list02)
# #                 seg_list1 = [seg_list_value_front, "//", seg_list_value_behind, ",", seg_list_value_front, "=",
# #                              seg_list_value_behind, ","]
# #             Str.extend(seg_list1)
# #             Str.extend(",")
# #             if "平行且相等" not in seg_list2:
# #                 Str.extend(seg_list2)
# #                 return Str
# #             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
# #     return seg_list


# # # 对字母进行形状配对,当形状在前面时
# # def add_all_shape_at_front(seg_list):
# #     len_seg_list = len(seg_list)
# #     Str = []
# #     seg_list_temp_overall = []
# #     seg_list_temp_front = []
# #     type_temp = []  # 储存形状
# #     type_value = []  # 储存字母
# #     if seg_list_having("、", seg_list):
# #         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
# #         while seg_list1 != "":
# #             if seg_list_having("、", seg_list1) and len(seg_list1[seg_list1.index("、") - 1]) > 2:  # 顿号前的字母长度大于三才处理
# #                 seg_list10, seg_list11 = cut_clause_slight_pause(seg_list1)  # 按照顿号进行切割           #可能出现三个字母的代码,露马脚了

# #                 while seg_list10 != "":
# #                     type_value.insert(len(type_value), dispose_cut_front_equal_letter(seg_list10))  # 提取英文字母
# #                     type_temp.insert(len(type_temp), seg_list_having_symbol_letter(map_clear_up_keywords, seg_list10,
# #                                                                                    dispose_cut_front_equal_letter(
# #                                                                                        seg_list10)))  # 提取字母类型
# #                     seg_list10, seg_list11 = cut_clause_slight_pause(seg_list11)  # 按照顿号进行切割
# #                 if len(type_temp[0]) > 0:  # 有标签的情况下
# #                     seg_list_temp_front = seg_list1[:seg_list1.index(type_value[0]) - 1]
# #                     seg_list_temp_behind = seg_list1[seg_list1.index(type_value[len(type_value) - 1]) + 1:]
# #                     for i in range(len(type_temp)):
# #                         if len(type_temp[i]) > 0:
# #                             seg_list_temp_front.insert(len(seg_list_temp_front),
# #                                                        find_the_max_symbol(type_temp[0], type_temp[i], type_value[i]))
# #                         else:
# #                             seg_list_temp_front.insert(len(seg_list_temp_front), type_temp[0])
# #                         seg_list_temp_front.insert(len(seg_list_temp_front), type_value[i])
# #                         if i < len(type_temp) - 1:
# #                             seg_list_temp_front.insert(len(seg_list_temp_front), "、")
# #                     seg_list_temp_front.extend(seg_list_temp_behind)  # 将三角形ABC、DEF、GHZ,拼接
# #                     # print(seg_list_temp_front)
# #             if len(seg_list_temp_front) > 0:
# #                 seg_list_temp_overall.extend(seg_list_temp_front)
# #                 seg_list_temp_front = []
# #             else:
# #                 seg_list_temp_overall.extend(seg_list1)
# #             seg_list_temp_overall.extend(",")
# #             # print(dispose_cut_front_equal_letter(seg_list1))
# #             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
# #         # print("seg_list_temp_overall",seg_list_temp_overall)
# #         # print("".join(seg_list_temp_overall))
# #         return seg_list_temp_overall
# #     return seg_list


# # # 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH
# # def add_all_shape_at_behind(seg_list):
# #     Str = []
# #     seg_list_temp = []
# #     type_temp = []
# #     type_value = []
# #     if seg_list_having(["均为", "都"], seg_list):
# #         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
# #         while seg_list1 != "":
# #             if seg_list_having(["均为", "都"], seg_list1):
# #                 seg_list_symbol_1 = seg_list_having(["均为", "都"], seg_list1)
# #                 seg_list00 = seg_list1[:seg_list1.index(seg_list_symbol_1)]  # 提取"都"前面的句子进入循环
# #                 seg_list20 = seg_list1[seg_list1.index(seg_list_symbol_1) + 1:]  # 提取都后面的句子
# #                 seg_list_symbol_behind = seg_list_having(map_clear_up_keywords, seg_list20)  # 提出"均为"后的图形
# #                 seg_list_letter20 = dispose_cut_front_equal_letter(seg_list20)  # 查看图形后面是否跟着字母
# #                 seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list00)
# #                 while seg_list1_0 != "":
# #                     seg_list_symbol_front = seg_list_having_0(map_clear_up_keywords, seg_list1_0)  # 提出第一个图形的类型
# #                     type_temp.insert(len(type_temp), seg_list_symbol_front)
# #                     seg_list_letter10 = dispose_cut_front_equal_letter(seg_list1_0)
# #                     type_value.insert(len(type_value), seg_list_letter10)
# #                     seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list1_1)
# #                 for i in range(len(type_temp)):
# #                     Str.insert(len(Str), type_temp[i])
# #                     Str.insert(len(Str), type_value[i])
# #                     Str.insert(len(Str), "是")
# #                     Str.insert(len(Str), seg_list_symbol_behind)
# #                     Str.insert(len(Str), seg_list_letter20)
# #                     Str.insert(len(Str), ",")
# #                 seg_list_temp.extend(Str)
# #             else:
# #                 seg_list_temp.extend(seg_list1)
# #                 seg_list_temp.extend(",")
# #             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照顿号与"与"分段
# #         return seg_list_temp
# #     else:
# #         return seg_list


# # def add_all_letter(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     temp = []
# #     for i in range(len(seg_list_list)):
# #         for j in range(len(seg_list_list[i])):
# #             if if_letter(seg_list_list[i][j]) and len(seg_list_list[i][j]) > 2 and seg_list_list[i][j - 1] != "∠":
# #                 temp.insert(len(temp), seg_list_list[i][j])
# #             if seg_list_list[i][j] in ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形",
# #                                        "矩形", "正方形", "长方形", "平行四边形",
# #                                        "梯形", "等腰梯形", "直角梯形", "菱形"] and j + 1 < len(seg_list_list[i]) and \
# #                     not if_letter(seg_list_list[i][j + 1]):
# #                 if seg_list_having_2("三", seg_list_list[i][j]):
# #                     for k in range(len(temp)):
# #                         if len(temp[len(temp) - 1 - k]) == 3:
# #                             seg_list_list_temp = seg_list_list[i][:j + 1]
# #                             seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
# #                             seg_list_list_temp.extend(seg_list_list[i][j + 1:])
# #                             seg_list_list[i] = seg_list_list_temp
# #                             break
# #                 else:
# #                     for k in range(len(temp)):
# #                         if len(temp[len(temp) - 1 - k]) > 3:
# #                             seg_list_list_temp = seg_list_list[i][:j + 1]
# #                             seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
# #                             seg_list_list_temp.extend(seg_list_list[i][j + 1:])
# #                             seg_list_list[i] = seg_list_list_temp
# #                             break
# #                 break
# #     return return_seg_list(seg_list_list)


# # # 对其余的所有的多个连续字母进行基础形状赋值
# # def add_all_shape(seg_list):
# #     seg_list_if = 0
# #     while seg_list_if == 0:
# #         seg_list_temp = []
# #         for i in range(len(seg_list)):
# #             if if_letter(seg_list[i]) and len(seg_list[i]) > 2:
# #                 seg_list_front = seg_list[:i]
# #                 seg_list_behind = seg_list[i + 1:]
# #                 if len(seg_list_front) == 0:  # ABC打头
# #                     seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
# #                     seg_list_temp.insert(len(seg_list_temp), seg_list[i])
# #                     seg_list_temp.extend(seg_list_behind)
# #                     seg_list = seg_list_temp
# #                     seg_list_temp = []
# #                     break
# #                 else:
# #                     if seg_list[i - 1] in map_clear_up_keywords or seg_list[i - 1] == "∠":  # 字母前面有形状或者有角
# #                         continue
# #                     else:
# #                         seg_list_temp.extend(seg_list_front)
# #                         seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
# #                         seg_list_temp.insert(len(seg_list_temp), seg_list[i])
# #                         seg_list_temp.extend(seg_list_behind)
# #                         seg_list = seg_list_temp
# #                         seg_list_temp = []
# #                         break

# #             if i == len(seg_list) - 1:
# #                 seg_list_if = 1
# #     return seg_list


# # # 输出两个图形的权值的最大一个形状
# # def find_the_max_symbol(symbol1, symbol2):
# #     x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
# #     x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
# #     y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
# #     y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
# #     if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
# #         return ""
# #     elif (y1 + y2) in map_clear_up_keywords_value:
# #         seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
# #         return seg_list_temp
# #     else:
# #         if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
# #             return symbol1
# #         else:
# #             return symbol2


# # # 形状 形状 ABC ,如果前两个的图形的边相等,所以判断谁的权值大,否则,就有一个图形是错误的,需要舍弃,如果都错误,那么给予ABC基础图形
# # def find_the_max_symbol(symbol1, symbol2, seg_list):
# #     symbol1_angle, symbol2_angle = return_how_many_side_symbol(symbol1, symbol2)
# #     if symbol1_angle == symbol2_angle:
# #         x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
# #         x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
# #         y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
# #         y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
# #         if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
# #             return ""
# #         elif (y1 + y2) in map_clear_up_keywords_value:
# #             seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
# #             return seg_list_temp
# #         else:
# #             if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
# #                 return symbol1
# #             else:
# #                 return symbol2
# #     else:
# #         if len(seg_list) == symbol1_angle:
# #             return symbol1
# #         elif len(seg_list) == symbol2_angle:
# #             return symbol2
# #         else:
# #             return match_how_many_side(seg_list)


# # # 除去重复的形状
# # def delete_repetition_symbol(seg_list):
# #     seg_temp = 0

# #     while seg_temp == 0:
# #         for i in range(len(seg_list)):
# #             if seg_list[i] in map_clear_up_keywords and i + 1 < len(seg_list) and \
# #                     seg_list[i + 1] in map_clear_up_keywords:  # 当前形状和下一个值都是形状
# #                 seg_list_front = seg_list[:i]
# #                 seg_list_behind = seg_list[i + 2:]
# #                 seg_list_front.insert(len(seg_list_front), find_the_max_symbol(seg_list[i], seg_list[i + 1]))
# #                 seg_list_front.extend(seg_list_behind)
# #                 seg_list = seg_list_front
# #                 break
# #             if i + 1 == len(seg_list):
# #                 seg_temp = 1
# #     return seg_list


# # # 处理四边形ABCD是正方形的情况
# # def dispose_shi_and_symbol(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         for j in range(len(seg_list_list[i])):
# #             if seg_list_list[i][j] in map_clear_up_keywords and j + 1 < len(seg_list_list[i]) and if_letter(
# #                     seg_list_list[i][j + 1]):  # 四边形abcd
# #                 subject = seg_list_list[i][j]  # 当前主语为abcd
# #                 if j + 3 < len(seg_list_list[i]) and seg_list_list[i][j + 2] in ["是", "为"] and \
# #                         seg_list_list[i][j + 3] in map_clear_up_keywords:  # 特殊值判断 四边形ABCD为长方形
# #                     seg_list_list_front = seg_list_list[i][:j]
# #                     seg_list_list_behind = seg_list_list[i][j + 4:]
# #                     seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
# #                     seg_list_list_front.insert(len(seg_list_list_front),
# #                                                find_the_max_symbol(seg_list_list[i][j], seg_list_list[i][j + 3],
# #                                                                    seg_list_list[i][j + 1]))
# #                     seg_list_list_front.insert(len(seg_list_list_front), seg_list_list[i][j + 1])
# #                     if len(seg_list_list_behind_letter) == 1 and seg_list_list_behind_letter[0][1] != seg_list_list[i][
# #                         j + 1]:
# #                         seg_list_list_front.extend(seg_list_list_behind)
# #                     seg_list_list[i] = seg_list_list_front
# #                     break
# #     seg_list = []
# #     for i in range(len(seg_list_list)):
# #         seg_list.extend(seg_list_list[i])
# #         seg_list.extend(",")
# #     # print("^&*","".join(seg_list))
# #     return seg_list


# # # 删去多余的逗号
# # def delete_unnecessary_comma(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if len(seg_list_list[i]) > 0 and seg_list_list[i][0] == ":":
# #             seg_list_list[i] = seg_list_list[i][1:]
# #     seg_list = return_seg_list(seg_list_list)
# #     seg_list_temp = 0
# #     while seg_list_temp == 0:
# #         if len(seg_list) == 0:
# #             break
# #         for i in range(len(seg_list)):
# #             if seg_list[i] == "," and i == 0:
# #                 seg_list = seg_list[1:]
# #                 break
# #             if seg_list[i] == "," and i + 2 < len(seg_list) and seg_list[i + 1] in [",", ".", "\n", "、", ";", "∶", "?",
# #                                                                                     "？"]:
# #                 seg_list_front = seg_list[:i]
# #                 seg_list_behind = seg_list[i + 2:]
# #                 seg_list_front.extend(",")
# #                 seg_list_front.extend(seg_list_behind)
# #                 seg_list = seg_list_front
# #                 break
# #             if seg_list[i] == "," and i - 1 > 0 and seg_list[i - 1] in [",", ".", "\n", "、", ";"]:
# #                 seg_list_front = seg_list[:i - 1]
# #                 seg_list_behind = seg_list[i:]
# #                 seg_list_front.extend(seg_list_behind)
# #                 seg_list = seg_list_front
# #                 break
# #             if i + 1 == len(seg_list):
# #                 seg_list_temp = 1
# #     return seg_list


# # def add_to_the_vertical(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if "垂足" in seg_list_list[i]:
# #             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             if len(seg_list_letter) == 1 and seg_list_letter[0][0] == 1:
# #                 seg_list_list[i - 1].extend("于")
# #                 seg_list_list[i - 1].extend(seg_list_letter[0][1])
# #                 seg_list_list[i] = ""
# #             else:
# #                 for j in range(len(seg_list_letter)):
# #                     seg_list_list[i - j - 1].extend("于")
# #                     seg_list_list[i - j - 1].extend(seg_list_letter[len(seg_list_letter) - 1 - j][1])
# #                 seg_list_list[i] = ""
# #     seg_list = []
# #     for i in range(len(seg_list_list)):
# #         seg_list.extend(seg_list_list[i])
# #         seg_list.extend(",")
# #     # print("^&*","".join(seg_list))
# #     return seg_list


# # # 查找当前句子的所有英文词组,返回边大小和词组
# # def find_all_letter_return_side_letter(seg_list):
# #     list_letter = []
# #     for i in range(len(seg_list)):
# #         list_letter_seg = []
# #         if if_letter(seg_list[i]) and seg_list[i].isupper():
# #             list_letter_seg.insert(len(list_letter_seg), len(seg_list[i]))
# #             list_letter_seg.insert(len(list_letter_seg), seg_list[i])
# #         # if seg_list[i] in symbol_keywords_main:
# #         #     break
# #         if len(list_letter_seg) > 0:
# #             list_letter.append(list_letter_seg)
# #     # print(list_letter)
# #     return list_letter


# # # 找到当前句子中除去字母,顿号的其他的所有字符串
# # def find_front_and_behind_other(seg_list, symbol):
# #     list_other = []
# #     if len(symbol) == 0:
# #         return seg_list
# #     # if not "、" in seg_list  \n symbol[0][1] \n elif: \n seg_list.index("、") < seg_list.index(
# #     #             symbol[0][1]) \n "、" \n else  symbol[0][1]
# #     seg_list_front = seg_list[:seg_list.index(
# #         symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
# #         seg_list_having(["、", "和"], seg_list) if seg_list.index(
# #             seg_list_having(["、", "和"], seg_list)) < seg_list.index(
# #             symbol[0][1])
# #         else symbol[0][1])]
# #     seg_list_behind = seg_list[seg_list.index(
# #         symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
# #         seg_list_having(["、", "和"], seg_list) if seg_list.index(
# #             seg_list_having(["、", "和"], seg_list)) > seg_list.index(
# #             symbol[len(symbol) - 1][1]) else
# #         symbol[len(symbol) - 1][1]) + 1:]
# #     list_other.append(seg_list_front)
# #     list_other.append(seg_list_behind)
# #     # print(list_other)
# #     return list_other


# # def find_have_d_or_slight_pause(seg_list):
# #     for i in range(len(seg_list)):
# #         if if_letter(seg_list[i]) or seg_list[i] == "、":
# #             return True
# #     return False


# # # 对交进行拼接
# # def package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
# #                         seg_list_front_behind_letter, seg_list_front_behind_other,
# #                         seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
# #                         seg_list_behind_behind_letter, seg_list_behind_behind_other, symbol):
# #     seg_list_part = []
# #     # print(seg_list_front_front_letter, end=" # ")
# #     # print(seg_list_front_front_other)
# #     # print(seg_list_front_behind_letter, end=" # ")
# #     # print(seg_list_front_behind_other)
# #     # print(seg_list_behind_front_letter, end=" # ")
# #     # print(seg_list_behind_front_other)
# #     # print(seg_list_behind_behind_letter, end=" # ")
# #     # print(seg_list_behind_behind_other)
# #     # 以下偷懒一点了，以后需要再进行更改吧
# #     # 有0111和1011和0100和0201三种情况 BE的延长线交AC于点F ，DF交 ， 四边形ABCD的两条对角线AC、BD交于点E
# #     # 存在1101和1111和1121三种情况
# #     # 存在2001一种情况

# #     # if len(seg_list_front_front_other) != 0 and (
# #     #         len(seg_list_front_front_other[0]) != 0 or seg_list_having(symbol_keywords_main,
# #     #                                                                    seg_list_front_front_other[1])):  # 清除前面的冗余句子
# #     #     for i in range(len(seg_list_front_front_letter)):
# #     #         seg_list_part.extend(seg_list_front_front_other[0])
# #     #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[i][1])
# #     #         if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
# #     #             seg_list_part.extend(seg_list_front_front_other[1])
# #     #         seg_list_part.extend(",")
# #     #     seg_list_front_front_other[0] = []
# #     #     if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
# #     #         seg_list_front_front_other[1] = []
# #     # if len(seg_list_front_behind_other) != 0 and (
# #     #         len(seg_list_front_behind_other[0]) != 0 or seg_list_having(symbol_keywords_main,
# #     #                                                                     seg_list_front_behind_other[1])):  # 清除后面的冗余句子
# #     #     for i in range(len(seg_list_front_behind_letter)):
# #     #         seg_list_part.extend(seg_list_front_behind_other[0])
# #     #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
# #     #         if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
# #     #             seg_list_part.extend(seg_list_front_behind_other[1])
# #     #         seg_list_part.extend(",")
# #     #     seg_list_front_behind_other[0] = []
# #     #     if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
# #     #         seg_list_front_behind_other[1] = []

# #     if len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 0 and len(
# #             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_part.extend(seg_list_front_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #         if "交" not in seg_list_front_front_other[1] and "分别" not in seg_list_front_front_other[1]:
# #             seg_list_part.extend(seg_list_front_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
# #             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[1][1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 0:
# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_part.extend(seg_list_front_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #         seg_list_part.extend(seg_list_front_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
# #         if seg_list_front_front_letter[0][0] == 1:
# #             seg_list_part.extend(seg_list_front_front_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #             seg_list_part.extend(seg_list_front_front_other[1])
# #             seg_list_part.insert(len(seg_list_part), "作")
# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_front_front_letter_temp = 1
# #         for i in range(2):
# #             seg_list_part.extend(seg_list_front_front_other[0])
# #             if seg_list_front_front_letter_temp == 1:
# #                 seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #                 seg_list_front_front_letter_temp += 1
# #             else:
# #                 seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #             seg_list_part.extend(seg_list_front_front_other[1])
# #             seg_list_part.insert(len(seg_list_part), "交")
# #             seg_list_part.extend(seg_list_behind_front_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #             seg_list_part.extend(seg_list_behind_front_other[1])
# #             seg_list_part.insert(len(seg_list_part), "于")
# #             seg_list_part.extend(seg_list_behind_behind_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #             seg_list_part.extend(seg_list_behind_behind_other[1])
# #             seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 2 and len(seg_list_front_behind_letter) == 0 and len(
# #             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
# #         seg_list_part.extend(seg_list_front_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_front_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[1][1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
# #             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 2:
# #         for i in range(2):
# #             seg_list_part.extend(seg_list_front_behind_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
# #             seg_list_part.extend(seg_list_front_behind_other[1])
# #             seg_list_part.insert(len(seg_list_part), "交")
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #             seg_list_part.insert(len(seg_list_part), "于")
# #             seg_list_part.extend(seg_list_behind_behind_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
# #             seg_list_part.extend(seg_list_behind_behind_other[1])
# #             seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
# #         seg_list_part.extend(seg_list_front_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
# #         seg_list_part.extend(seg_list_front_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")

# #         seg_list_part.extend(seg_list_front_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #         seg_list_part.extend(seg_list_front_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), "交")
# #         seg_list_part.extend(seg_list_behind_front_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
# #         seg_list_part.extend(seg_list_behind_front_other[1])
# #         seg_list_part.insert(len(seg_list_part), "于")
# #         seg_list_part.extend(seg_list_behind_behind_other[0])
# #         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[1][1])
# #         seg_list_part.extend(seg_list_behind_behind_other[1])
# #         seg_list_part.insert(len(seg_list_part), ",")
# #     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
# #             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
# #         for i in range(2):
# #             seg_list_part.extend(seg_list_front_behind_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
# #             seg_list_part.extend(seg_list_front_behind_other[1])
# #             seg_list_part.insert(len(seg_list_part), "交")
# #             seg_list_part.extend(seg_list_behind_front_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[i][1])
# #             seg_list_part.extend(seg_list_behind_front_other[1])
# #             seg_list_part.insert(len(seg_list_part), "于")
# #             seg_list_part.extend(seg_list_behind_behind_other[0])
# #             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
# #             seg_list_part.extend(seg_list_behind_behind_other[1])
# #             seg_list_part.insert(len(seg_list_part), ",")
# #     else:  # 其他非常规的默认输出
# #         seg_list_part = package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
# #                                      seg_list_front_behind_letter, seg_list_front_behind_other,
# #                                      seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
# #                                      seg_list_behind_behind_letter, seg_list_behind_behind_other)
# #     # print("".join(seg_list_part))
# #     return seg_list_part


# # # 连接词组
# # def package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
# #                  seg_list_front_behind_letter, seg_list_front_behind_other,
# #                  seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
# #                  seg_list_behind_behind_letter, seg_list_behind_behind_other):
# #     seg_list_max = max(len(seg_list_front_front_letter), len(seg_list_front_behind_letter),
# #                        len(seg_list_behind_front_letter), len(seg_list_behind_behind_letter))
# #     seg_list_part = []
# #     # 存在数字的相等
# #     # print("###",seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other))
# #     # print( seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other))
# #     # print(seg_list_behind_behind_letter_if_letter(seg_list_behind_behind_letter))
# #     # print(seg_list_front_front_letter)
# #     # print(seg_list_front_behind_letter)
# #     # print(seg_list_behind_front_letter)
# #     # △ABC的高AD与CE的长分别为4、6
# #     if (seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other)
# #         or seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other)) \
# #             and seg_list_behind_behind_letter_if_letter(seg_list_behind_front_letter):
# #         for i in range(len(seg_list_front_front_letter)):

# #             seg_list_part_part = []
# #             if len(seg_list_front_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[0])
# #             if len(seg_list_front_front_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
# #             elif len(seg_list_front_front_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
# #             if len(seg_list_front_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[1])

# #             if len(seg_list_behind_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_front_other[0])
# #             if len(seg_list_behind_front_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
# #             elif len(seg_list_behind_front_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
# #             if len(seg_list_behind_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_front_other[1])

# #             if len(seg_list_behind_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_behind_other[0])
# #             if len(seg_list_behind_behind_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
# #             elif len(seg_list_behind_behind_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
# #             if len(seg_list_behind_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_behind_other[1])
# #             seg_list_part.extend(seg_list_part_part)
# #             seg_list_part.extend(",")
# #         for i in range(len(seg_list_front_behind_letter)):
# #             seg_list_part_part = []
# #             if len(seg_list_front_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_behind_other[0])
# #             if len(seg_list_front_behind_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
# #             elif len(seg_list_front_behind_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
# #             if len(seg_list_front_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_behind_other[1])

# #             if len(seg_list_behind_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_front_other[0])
# #             if len(seg_list_behind_front_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part),
# #                                           seg_list_behind_front_letter[i + len(seg_list_front_front_letter)][1])
# #             elif len(seg_list_behind_front_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
# #             if len(seg_list_behind_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_front_other[1])

# #             if len(seg_list_behind_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_behind_other[0])
# #             if len(seg_list_behind_behind_letter) == seg_list_max:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
# #             elif len(seg_list_behind_behind_letter) != 0:
# #                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
# #             if len(seg_list_behind_behind_other) == 2:
# #                 seg_list_part_part.extend(seg_list_behind_behind_other[1])
# #             seg_list_part.extend(seg_list_part_part)
# #             seg_list_part.extend(",")

# #         return seg_list_part

# #     for i in range(seg_list_max):
# #         seg_list_part_part = []
# #         if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
# #             if len(seg_list_front_front_other[i]) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[i][0])
# #         else:
# #             if len(seg_list_front_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[0])
# #         # if len(seg_list_front_front_letter) == seg_list_max:
# #         #     if len(seg_list_front_front_letter[i][1]) == 1:  # 为垂足分别是兜底 ? 看不懂了
# #         #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
# #         #     else:
# #         #         seg_list_part_part.extend(seg_list_front_front_letter[i][1])
# #         # elif len(seg_list_front_front_letter) != 0:
# #         #     if len(seg_list_front_front_letter[0][1]) == 1:
# #         #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
# #         #     else:
# #         #         seg_list_part_part.extend(seg_list_front_front_letter[0][1])
# #         if len(seg_list_front_front_letter) == seg_list_max:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
# #         elif len(seg_list_front_front_letter) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])

# #         if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
# #             if len(seg_list_front_front_other[i]) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[i][1])
# #         else:
# #             if len(seg_list_front_front_other) == 2:
# #                 seg_list_part_part.extend(seg_list_front_front_other[1])

# #         if len(seg_list_part_part) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_add)
# #         if len(seg_list_front_behind_other) == 2:
# #             seg_list_part_part.extend(seg_list_front_behind_other[0])
# #         if len(seg_list_front_behind_letter) == seg_list_max:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
# #         elif len(seg_list_front_behind_letter) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
# #         if len(seg_list_front_behind_other) == 2:
# #             seg_list_part_part.extend(seg_list_front_behind_other[1])

# #         if len(seg_list_behind_front_other) == 2:
# #             seg_list_part_part.extend(seg_list_behind_front_other[0])
# #         else:  # 如果存在分别相交于
# #             if len(seg_list_behind_front_other) != 0:
# #                 seg_list_part_part.extend(seg_list_behind_front_other[0])
# #         if len(seg_list_behind_front_letter) == seg_list_max:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
# #         elif len(seg_list_behind_front_letter) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
# #         if len(seg_list_behind_front_other) == 2:
# #             seg_list_part_part.extend(seg_list_behind_front_other[1])

# #         if len(seg_list_behind_behind_letter) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_add)

# #         if len(seg_list_behind_behind_other) == 2:
# #             seg_list_part_part.extend(seg_list_behind_behind_other[0])
# #         if len(seg_list_behind_behind_letter) == seg_list_max:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
# #         elif len(seg_list_behind_behind_letter) != 0:
# #             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
# #         if len(seg_list_behind_behind_other) == 2:
# #             seg_list_part_part.extend(seg_list_behind_behind_other[1])
# #         # print("#########","".join(seg_list_part_part))
# #         seg_list_part.extend(seg_list_part_part)
# #         seg_list_part.extend(",")
# #     # print("#########","".join(seg_list_part))
# #     return seg_list_part


# # def find_the_mian_word(seg_list_list, symbol, seg_list_front_front_letter, i):
# #     for m in range(1, 5):  # 可能出现多次交
# #         if seg_list_list[i - m][0] != symbol:
# #             if re.search(".*交", "".join(seg_list_list[i - m])):
# #                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("交")]
# #             if re.search(".*与", "".join(seg_list_list[i - m])):
# #                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("与")]
# #             if re.search(".*作", "".join(seg_list_list[i - m])):
# #                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("作")]
# #             if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
# #                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
# #                 seg_list_front_front_letter = find_all_letter_return_side_letter(
# #                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
# #                 while len(seg_list_front_front_letter) > 1:
# #                     del seg_list_front_front_letter[1]
# #                 # print(seg_list_front_front_letter)
# #                 # print()
# #                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
# #                                                                          seg_list_front_front_letter)
# #             # 线AB、CD,分别交^^于^^
# #             elif seg_list_having("、", seg_list_list[i - m]):
# #                 seg_list_front_front_letter = find_all_letter_return_side_letter(
# #                     seg_list_list[i - m])
# #                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
# #                                                                          seg_list_front_front_letter)
# #             else:
# #                 for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
# #                     if if_letter(seg_list_list[i - m][k]):
# #                         for j in range(len(seg_list_front_front_letter)):
# #                             seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
# #                             seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
# #                         seg_list_front_front_other = find_front_and_behind_other(
# #                             seg_list_list[i - m],
# #                             seg_list_front_front_letter)
# #                         break  # 只提取第一个词语
# #             if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
# #                 seg_list_front_front_other[1] = []
# #             break
# #     return seg_list_front_front_letter, seg_list_front_front_other


# # # 处理分别
# # def cut_respect_is_importance(seg_list, symbol):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     seg_list_i_temp_front = 0
# #     seg_list_i_temp_behind = 0
# #     seg_list_i_temp = []  # 存储更新后的词组
# #     for i in range(len(seg_list_list)):
# #         if symbol == "交" and "交" not in seg_list_list[i]:
# #             if "相交" in seg_list_list[i]:
# #                 symbol = "相交"

# #         if symbol in seg_list_list[i]:
# #             seg_list_i_temp_front = i  # 记录当前分别的位置
# #             seg_list_front = seg_list_list[i][:seg_list_list[i].index(symbol)]
# #             seg_list_behind = seg_list_list[i][seg_list_list[i].index(symbol) + 1:]
# #             seg_list_front_front_letter = []
# #             seg_list_front_front_other = []
# #             seg_list_front_behind_letter = []
# #             seg_list_front_behind_other = []
# #             seg_list_behind_front_letter = []
# #             seg_list_behind_front_other = []
# #             seg_list_behind_behind_letter = []
# #             seg_list_behind_behind_other = []
# #             if len(seg_list_front) == 0:
# #                 # 当存在"作"的时候,可能出现于,但是不存在缺少主语,故为: 分别f-f 作 f-b 交 b-h 于 b-b
# #                 # 当不存在"作"的时候,可能出现于,但是缺少主语,故为:  主语,分别b-f 于b-b
# #                 # 主语可能出现线,三边,多边
# #                 # 此时ff是分别之后作之前
# #                 if seg_list_having(["作", "与"], seg_list_behind) and seg_list_behind.index(
# #                         seg_list_having_0(["作", "与"], seg_list_behind)) > 0:  # 防止出现分别作多判断
# #                     seg_list_front_front = seg_list_behind[
# #                                            :seg_list_behind.index(seg_list_having_0(["作", "与"], seg_list_behind))]
# #                     seg_list_front_behind = seg_list_behind[
# #                                             seg_list_behind.index(
# #                                                 seg_list_having_0(["作", "与"], seg_list_behind)) + 1:]
# #                     # 前半部分是否存在可以处理"的"
# #                     if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
# #                             seg_list_front_front[seg_list_front_front.index(
# #                                 seg_list_having_0("的", seg_list_front_front)) + 1:]):
# #                         seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
# #                             seg_list_having_0("的", seg_list_front_front)) + 1:]
# #                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
# #                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
# #                                                                                  seg_list_front_front_letter)
# #                     else:
# #                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
# #                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
# #                                                                                  seg_list_front_front_letter)

# #                     if seg_list_having(["于"], seg_list_front_behind):  # 是否有"于"或者"交于"在后半段
# #                         seg_list_behind_front = seg_list_front_behind[:seg_list_front_behind.index(
# #                             seg_list_having_0(["于"], seg_list_front_behind))]
# #                         seg_list_behind_behind = seg_list_front_behind[seg_list_front_behind.index(
# #                             seg_list_having_0(["于"], seg_list_front_behind)) + 1:]
# #                         seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
# #                         seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
# #                                                                                    seg_list_behind_behind_letter)
# #                         if seg_list_having(["交"], seg_list_behind_front):  # 是否有"交"在作后半段,于前半段,即在中间
# #                             seg_list_behind_front_front = seg_list_behind_front[:seg_list_behind_front.index(
# #                                 seg_list_having_0(["交"], seg_list_behind_front))]
# #                             seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
# #                                 seg_list_having_0(["交"], seg_list_behind_front)):]
# #                             seg_list_front_behind_letter = find_all_letter_return_side_letter(
# #                                 seg_list_behind_front_front)
# #                             seg_list_front_behind_other = find_front_and_behind_other(seg_list_behind_front_front,
# #                                                                                       seg_list_front_behind_letter)
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
# #                                 seg_list_behind_front_behind)
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_behind,
# #                                                                                       seg_list_behind_front_letter)
# #                         else:
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
# #                                                                                       seg_list_behind_front_letter)
# #                     else:
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_front_behind)
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_front_behind,
# #                                                                                   seg_list_behind_front_letter)
# #                 else:
# #                     if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
# #                         seg_list_behind_front = seg_list_behind[
# #                                                 :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
# #                         seg_list_behind_behind = seg_list_behind[
# #                                                  seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
# #                         if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
# #                                 seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
# #                                 seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
# #                                                                                       seg_list_behind_front)
# #                         else:
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
# #                                                                                       seg_list_behind_front_letter)
# #                         seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
# #                         seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
# #                                                                                    seg_list_behind_behind_letter)
# #                     else:
# #                         # 垂线   分别交三角形ABC的AB CD
# #                         if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
# #                                 seg_list_behind[seg_list_behind.index("的") + 1:]):
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
# #                                 seg_list_behind[seg_list_behind.index("的") + 1:])
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
# #                                                                                       seg_list_behind)
# #                         else:
# #                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
# #                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
# #                                                                                       seg_list_behind_front_letter)
# #                     # 如果有"于"看b-b-l字母值,否则看b-f-l值
# #                     seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
# #                         else len(seg_list_behind_front_letter)
# #                     for k in range(seg_list_b_b_l_len):
# #                         seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
# #                     for m in range(1, 5):  # 可能出现多次交
# #                         if seg_list_list[i - m][0] != symbol:
# #                             if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
# #                                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
# #                                 seg_list_front_front_letter = find_all_letter_return_side_letter(
# #                                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
# #                                 while len(seg_list_front_front_letter) > 1:
# #                                     del seg_list_front_front_letter[1]
# #                                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
# #                                                                                          seg_list_front_front_letter)
# #                             # 线AB、CD,分别交^^于^^
# #                             elif seg_list_having("、", seg_list_list[i - m]):
# #                                 seg_list_front_front_letter = find_all_letter_return_side_letter(
# #                                     seg_list_list[i - m])
# #                                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
# #                                                                                          seg_list_front_front_letter)
# #                             else:
# #                                 for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
# #                                     if if_letter(seg_list_list[i - m][k]):
# #                                         for j in range(len(seg_list_front_front_letter)):
# #                                             seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
# #                                             seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
# #                                         seg_list_front_front_other = find_front_and_behind_other(
# #                                             seg_list_list[i - m],
# #                                             seg_list_front_front_letter)
# #                                         break  # 只提取第一个词语
# #                             if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
# #                                 seg_list_front_front_other[1] = []
# #                             break

# #                 for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):
# #                     seg_list_i_temp.extend(seg_list_list[k])
# #                     seg_list_i_temp.extend(",")
# #                 if "分别" in symbol:
# #                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                         seg_list_having_0(["作", "与"], seg_list_front),
# #                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
# #                                                         seg_list_behind_front_letter, seg_list_behind_front_other,
# #                                                         seg_list_having_0("于", seg_list_behind),
# #                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
# #                 else:
# #                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                                seg_list_having_0(["作", "与"], seg_list_front),
# #                                                                seg_list_front_behind_letter,
# #                                                                seg_list_front_behind_other,
# #                                                                seg_list_behind_front_letter,
# #                                                                seg_list_behind_front_other, "于",
# #                                                                seg_list_behind_behind_letter,
# #                                                                seg_list_behind_behind_other, symbol))

# #                 seg_list_i_temp_behind = i + 1
# #                 # 分别在前面,可能出现缺主语或不缺
# #             elif len(seg_list_front) == 1 and seg_list_having_2(["垂"], seg_list_front):
# #                 if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
# #                     seg_list_behind_front = seg_list_behind[
# #                                             :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
# #                     seg_list_behind_behind = seg_list_behind[
# #                                              seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
# #                     if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
# #                             seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(
# #                             seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
# #                                                                                   seg_list_behind_front)
# #                     else:
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
# #                                                                                   seg_list_behind_front_letter)
# #                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
# #                     seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
# #                                                                                seg_list_behind_behind_letter)
# #                 else:
# #                     # 垂线分别交三角形ABC的AB CD
# #                     if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
# #                             seg_list_behind[seg_list_behind.index("的") + 1:]):
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(
# #                             seg_list_behind[seg_list_behind.index("的") + 1:])
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
# #                                                                                   seg_list_behind)
# #                     else:
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
# #                                                                                   seg_list_behind_front_letter)
# #                 seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
# #                     else len(seg_list_behind_front_letter)
# #                 s_l_b_b_temp = 0
# #                 for k in range(seg_list_b_b_l_len):
# #                     seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
# #                     seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
# #                 for k in range(seg_list_b_b_l_len):  # 如果存在"于"看b-b-l,否则看b-f-l
# #                     if seg_list_having("⊥", seg_list_list[i - k - 1]):
# #                         s_l_b_b_temp = i - k - 1
# #                         for j in range(len(seg_list_list[i - k - 1])):
# #                             if if_letter(seg_list_list[i - k - 1][j]):
# #                                 seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0] = len(
# #                                     seg_list_list[i - k - 1][j])
# #                                 seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1] = seg_list_list[i - k - 1][j]
# #                                 seg_list_front_front_letter_temp = [[[], []]]
# #                                 seg_list_front_front_letter_temp[0][0] = \
# #                                     seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0]
# #                                 seg_list_front_front_letter_temp[0][1] = \
# #                                     seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1]
# #                                 seg_list_front_front_other[seg_list_b_b_l_len - 1 - k] = find_front_and_behind_other(
# #                                     seg_list_list[i - k - 1], seg_list_front_front_letter_temp)
# #                                 break  # 只提取第一个词语
# #                 # print(seg_list_front_front_letter)
# #                 # print(package_line(seg_list_front_front_letter, "", "垂直", "", "", seg_list_behind_front_letter,
# #                 #                    seg_list_behind_front_other, "于", seg_list_behind_behind_letter,
# #                 #                    seg_list_behind_behind_other))
# #                 for k in range(seg_list_i_temp_behind, s_l_b_b_temp):
# #                     seg_list_i_temp.extend(seg_list_list[k])
# #                     seg_list_i_temp.extend(",")
# #                 seg_list_i_temp_behind = s_l_b_b_temp
# #                 if "分别" in symbol:
# #                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                         ("垂直" if seg_list_having(["垂直"],
# #                                                                                    seg_list_front) else "垂足"),
# #                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
# #                                                         seg_list_behind_front_letter, seg_list_behind_front_other,
# #                                                         seg_list_having_0("于", seg_list_behind),
# #                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
# #                 else:
# #                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                                seg_list_having_0(["作", "与"], seg_list_front),
# #                                                                seg_list_front_behind_letter,
# #                                                                seg_list_front_behind_other,
# #                                                                seg_list_behind_front_letter,
# #                                                                seg_list_behind_front_other, "于",
# #                                                                seg_list_behind_behind_letter,
# #                                                                seg_list_behind_behind_other, symbol))

# #                 seg_list_i_temp_behind = i + 1

# #             else:
# #                 # E、F分别为AD、BC的中点
# #                 seg_list_front_temp_front = []
# #                 if return_re_return([".*平分"], "".join(seg_list_front)) and seg_list_having("、", seg_list_front) \
# #                         and return_re_return([".*交"], "".join(symbol)):
# #                     seg_list_list_front = seg_list_front[:seg_list_front.index("平分线")]
# #                     seg_list_list_behind = seg_list_front[seg_list_front.index("平分线") + 1:]
# #                     seg_list_list_front_letter = find_all_letter_return_side_letter(seg_list_list_front)
# #                     seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
# #                     if len(seg_list_list_behind_letter) == len(seg_list_list_front_letter):
# #                         for j in range(len(seg_list_list_front_letter)):
# #                             if seg_list_front[seg_list_front.index(seg_list_list_front_letter[j][1]) - 1] in "∠":
# #                                 front_letter_temp = "∠"
# #                                 front_letter_temp += seg_list_list_front_letter[j][1]
# #                                 seg_list_list_front_letter[j][1] = front_letter_temp
# #                         front_letter_temp_temp = []
# #                         front_letter_temp_time = len(seg_list_list_front_letter) - 1
# #                         for j in range(len(seg_list_list_front_letter)):
# #                             front_letter_temp = []
# #                             front_letter_temp.insert(len(front_letter_temp), seg_list_list_front_letter[j][1])
# #                             front_letter_temp.extend("的")
# #                             front_letter_temp.extend("平分线")
# #                             front_letter_temp.insert(len(front_letter_temp), seg_list_list_behind_letter[j][1])
# #                             front_letter_temp = transition_divide(front_letter_temp)
# #                             front_letter_temp_list = return_seg_list_list(front_letter_temp)
# #                             for k in range(len(front_letter_temp_list)):
# #                                 if k + 1 != len(front_letter_temp_list):
# #                                     seg_list_front_temp_front.insert(len(seg_list_front_temp_front),
# #                                                                      front_letter_temp_list[k])
# #                                 else:
# #                                     front_letter_temp_temp.extend(front_letter_temp_list[k])
# #                             if front_letter_temp_time:
# #                                 front_letter_temp_temp.extend("、")
# #                                 front_letter_temp_time -= 1
# #                         seg_list_front = front_letter_temp_temp

# #                 # 单只处理平分
# #                 if return_re_return([".*平分"], "".join(seg_list_front)) and \
# #                         not return_re_return([".*与", ".*作", ".*和"], "".join(seg_list_front)) and \
# #                         not seg_list_having("、", seg_list_list[i]):

# #                     seg_list_temp = transition_divide(seg_list_front)
# #                     seg_list_temp_list = return_seg_list_list(seg_list_temp)
# #                     seg_list_front_temp = []
# #                     seg_list_front_temp_temp = []
# #                     seg_list_front_temp_front = []  # 记录平分前的关系
# #                     for j in range(len(seg_list_temp_list)):
# #                         seg_list_temp_list_letter = find_all_letter_return_side_letter(seg_list_temp_list[j])
# #                         if len(seg_list_temp_list_letter) == 1:
# #                             seg_list_front_temp.insert(len(seg_list_front_temp), seg_list_temp_list[j])
# #                         else:
# #                             seg_list_front_temp_front.insert(len(seg_list_front_temp_front), seg_list_temp_list[j])
# #                             seg_list_front_temp_front.extend(",")
# #                     if len(seg_list_front_temp) == 1:
# #                         seg_list_front_temp_temp.extend(seg_list_front_temp[0])
# #                     else:
# #                         for j in range(len(seg_list_front_temp)):
# #                             seg_list_front_temp_temp.extend(seg_list_front_temp[j])
# #                             seg_list_front_temp_temp.extend("、")
# #                     seg_list_front = seg_list_front_temp_temp

# #                 if seg_list_having(["作", "与"], seg_list_front):
# #                     seg_list_front_front = seg_list_front[
# #                                            :seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front))]
# #                     seg_list_front_behind = seg_list_front[
# #                                             seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front)) + 1:]
# #                     if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
# #                             seg_list_front_front[seg_list_front_front.index(
# #                                 seg_list_having_0("的", seg_list_front_front)) + 1:]):
# #                         seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
# #                             seg_list_having_0("的", seg_list_front_front)) + 1:]
# #                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
# #                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
# #                                                                                  seg_list_front_front_letter)
# #                     else:
# #                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
# #                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
# #                                                                                  seg_list_front_front_letter)
# #                     if seg_list_having("的", seg_list_front_behind) and find_have_d_or_slight_pause(
# #                             seg_list_front_behind[
# #                             seg_list_front_behind.index(seg_list_having_0("的", seg_list_front_behind)) + 1:]):
# #                         # 前半部分存在"的"和每一部分都有顿号或者是字母
# #                         seg_list_front_behind_behind = seg_list_front_behind[
# #                                                        seg_list_front_behind.index(
# #                                                            seg_list_having_0("的", seg_list_front_behind)) + 1:]
# #                         seg_list_front_behind_letter = find_all_letter_return_side_letter(
# #                             seg_list_front_behind_behind)  # 找出所有的词语
# #                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
# #                                                                                   seg_list_front_behind_letter)
# #                     else:
# #                         seg_list_front_behind_letter = find_all_letter_return_side_letter(
# #                             seg_list_front_behind)  # 找出所有的词语
# #                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
# #                                                                                   seg_list_front_behind_letter)
# #                 else:
# #                     if seg_list_having("的", seg_list_front) and find_have_d_or_slight_pause(
# #                             seg_list_front[seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]):
# #                         seg_list_front_behind = seg_list_front[
# #                                                 seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]
# #                         seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)
# #                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
# #                                                                                   seg_list_front_behind_letter)
# #                     else:
# #                         seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front)
# #                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
# #                                                                                   seg_list_front_behind_letter)
# #                 if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
# #                     seg_list_behind_front = seg_list_behind[
# #                                             :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
# #                     seg_list_behind_behind = seg_list_behind[
# #                                              seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]

# #                     if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
# #                             seg_list_behind_front[seg_list_behind_front.index(
# #                                 seg_list_having_0("的", seg_list_behind_front)) + 1:]):
# #                         seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
# #                             seg_list_having_0("的", seg_list_behind_front)) + 1:]
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front_behind)
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
# #                                                                                   seg_list_behind_front_letter)
# #                     else:
# #                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
# #                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
# #                                                                                   seg_list_behind_front_letter)
# #                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
# #                     seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
# #                                                                                seg_list_behind_behind_letter)
# #                 else:
# #                     seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
# #                     seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
# #                                                                               seg_list_behind_front_letter)
# #                 if (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[0]) or \
# #                         (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[1]):
# #                     seg_list_front_behind_letter = seg_list_front_behind_letter[:1]
# #                     seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
# #                                                                               seg_list_front_behind_letter)
# #                     # 去掉三角形,三角形在最前面或最后面,且前面和中间的长度不相等
# #                 if len(seg_list_behind_front_letter) != 0 and (seg_list_behind_front_letter[0][0] == 3 or
# #                                                                seg_list_behind_front_letter[
# #                                                                    len(seg_list_behind_front_letter) - 1][0]
# #                                                                == 3) and len(seg_list_front_behind_letter) != \
# #                         len(seg_list_behind_front_letter):
# #                     if seg_list_behind_front_letter[0][0] == 3:
# #                         seg_list_behind_front_letter = seg_list_behind_front_letter[1:]
# #                     else:
# #                         seg_list_behind_front_letter = seg_list_behind_front_letter[
# #                                                        :len(seg_list_behind_front_letter) - 2]
# #                 for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):  # 拼接没有处理的句子
# #                     seg_list_i_temp.extend(seg_list_list[k])
# #                     seg_list_i_temp.extend(",")
# #                 if len(seg_list_front_temp_front) != 0:
# #                     for j in range(len(seg_list_front_temp_front)):
# #                         seg_list_i_temp.extend(seg_list_front_temp_front[j])
# #                         seg_list_i_temp.extend(",")
# #                     # print(seg_list_front_other) print(seg_list_behind_front_other) print(seg_list_behind_other)
# #                     # print("".join(package_line(seg_list_front_letter, seg_list_front_other, seg_list_mid_letter,
# #                     # seg_list_behind_front_other, seg_list_beh_letter, seg_list_behind_other)))

# #                 if "分别" in symbol:
# #                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                         seg_list_having_0(["作", "与"], seg_list_front),
# #                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
# #                                                         seg_list_behind_front_letter, seg_list_behind_front_other, "于",
# #                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
# #                 else:

# #                     if (len(seg_list_front_front_letter) + len(seg_list_front_behind_letter) + len(
# #                             seg_list_behind_front_letter)) < 2:
# #                         seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"],
# #                                                                                                    seg_list_behind) \
# #                             else len(seg_list_behind_front_letter)
# #                         s_l_b_b_temp = 0
# #                         for k in range(seg_list_b_b_l_len):
# #                             seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
# #                             seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
# #                         seg_list_front_front_letter, seg_list_front_front_other = find_the_mian_word(seg_list_list,
# #                                                                                                      symbol,
# #                                                                                                      seg_list_front_front_letter,
# #                                                                                                      i)
# #                     if "平分" in seg_list_front_behind_other[0] or "平分" in seg_list_front_behind_other[1]:
# #                         for k in range(len(seg_list_front_behind_letter)):
# #                             if seg_list_front_behind_letter[k][0] != 2:
# #                                 seg_list_front_behind_letter_front = seg_list_front_behind_letter[:k]
# #                                 seg_list_front_behind_letter_front.extend(seg_list_front_behind_letter[k + 1:])
# #                                 seg_list_front_behind_letter = seg_list_front_behind_letter_front
# #                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
# #                                                                seg_list_having_0(["作", "与"], seg_list_front),
# #                                                                seg_list_front_behind_letter,
# #                                                                seg_list_front_behind_other,
# #                                                                seg_list_behind_front_letter,
# #                                                                seg_list_behind_front_other, "于",
# #                                                                seg_list_behind_behind_letter,
# #                                                                seg_list_behind_behind_other, symbol))
# #                 seg_list_i_temp_behind = i + 1
# #         if symbol == "相交":  # 将symbol还原
# #             symbol = "交"
# #     for k in range(seg_list_i_temp_behind, len(seg_list_list)):  # 拼接"分别"后面未处理的句子
# #         seg_list_i_temp.extend(seg_list_list[k])
# #         seg_list_i_temp.extend(",")
# #     return seg_list_i_temp


# # # 处理连等和相似的情况
# # def transition_equal_or_similarity(seg_list):
# #     equal_value_all = []
# #     seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
# #     seg_list = []
# #     while seg_list1 != "":
# #         if_transition = 0
# #         if seg_list_having_0(symbol_keywords_main, seg_list1):
# #             seg_list.extend(find_which_equal(seg_list1, seg_list_having_0(symbol_keywords_main, seg_list1)))
# #             if_transition = 1
# #         if if_transition == 0:
# #             seg_list.extend(seg_list1)
# #         seg_list.extend(",")
# #         seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
# #     return seg_list
# #     # if "=" in seg_list:
# #     #     equal_value_all = find_which_equal(seg_list, "=")
# #     # if "//" in seg_list:
# #     #     equal_value_all = find_which_equal(seg_list, "//")
# #     # if "⊥" in seg_list:
# #     #     equal_value_all = find_which_equal(seg_list, "⊥")
# #     # symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]


# # def transition_angle_to_angle(seg_list):
# #     for i in range(len(seg_list)):
# #         if i + 1 < len(seg_list) and seg_list[i] in "∠" and seg_list[i + 1] in "平分线":
# #             seg_list_front = seg_list[:i]
# #             seg_list_behind = seg_list[i + 1:]
# #             seg_list_front.extend("角")
# #             seg_list_front.extend(seg_list_behind)
# #             seg_list = seg_list_front
# #     return seg_list


# # def transition_triangle_symbol(seg_list, symbol):
# #     for i in range(len(seg_list)):
# #         if symbol in seg_list[i] and if_letter(seg_list[i + 1]):
# #             seg_list_front = seg_list[i][:seg_list[i].index(symbol)]
# #             seg_list_front += "△"
# #             seg_list[i] = seg_list_front
# #     return seg_list


# # def return_the_point_at_line_temp(seg_list_list_letter1, seg_list_list_letter2, seg_list_list_letter_temp):
# #     if len(seg_list_list_letter1) == 0 and len(seg_list_list_letter2) == 0:
# #         return ""
# #     if len(seg_list_list_letter1) == 1:
# #         seg_list_list_letter_A = seg_list_list_letter1
# #         seg_list_list_letter_BC = seg_list_list_letter2
# #     else:
# #         seg_list_list_letter_A = seg_list_list_letter2
# #         seg_list_list_letter_BC = seg_list_list_letter1
# #     if seg_list_list_letter_temp == "延长线":
# #         letter_point = ""
# #         letter_AB = ""
# #         letter_point = seg_list_list_letter_BC[1]
# #         letter_AB += seg_list_list_letter_BC[0]
# #         letter_AB += seg_list_list_letter_A[0]
# #         seg_list_list_letter_A = letter_point
# #         seg_list_list_letter_BC = letter_AB
# #         seg_list_list_letter_temp = ""
# #     temp = []
# #     temp.insert(len(temp), seg_list_list_letter_A)
# #     if seg_list_list_letter_temp != "中点":  # 如果是中点,修改为A是BC的中点
# #         temp.insert(len(temp), "在")
# #     else:
# #         temp.insert(len(temp), "平分")
# #     temp.insert(len(temp), seg_list_list_letter_BC)
# #     if seg_list_list_letter_temp != "中点":
# #         if seg_list_list_letter_temp != "":
# #             temp.insert(len(temp), seg_list_list_letter_temp)
# #             temp.insert(len(temp), "上")
# #         else:
# #             temp.insert(len(temp), "上")
# #     # else:
# #     #     temp.insert(len(temp), "的")
# #     #     temp.insert(len(temp), "中点")
# #     temp.insert(len(temp), ",")
# #     temp.insert(len(temp), seg_list_list_letter_A)
# #     return temp


# # def guozuoyu(clause):
# #     arr = re.split('[作于]', clause)
# #     front = re.findall('[A-Za-z]', arr[0])
# #     mid = re.findall('[A-Za-z]', arr[1])
# #     behind = re.findall('[A-Za-z]', arr[2])
# #     clause_new = ""
# #     if arr[1].find('垂线') != -1:
# #         clause_new = front[-1] + behind[0] + '⊥' + mid[0] + mid[1] + '于' + behind[0]
# #     if arr[1].find('交') != -1:
# #         clause_new += ',' + front[-1] + behind[0] + '交' + mid[2] + mid[3] + '于' + behind[0]
# #     return (clause_new)


# # def guozuo(clause):
# #     arr = clause.split('作')
# #     front = re.findall('[A-Za-z]', arr[0])
# #     behind = re.findall('[A-Za-z]', arr[1])
# #     clause_new = ""
# #     for i in range(len(map_clear_up_keywords)):
# #         if re.search(map_clear_up_keywords[i], arr[1]) and map_clear_up_keywords[i] != "线":
# #             clause_new = map_clear_up_keywords[i]
# #             for j in range(len(behind)):
# #                 clause_new += behind[j]
# #             clause_new += ","
# #             return clause_new
# #     if front[-1] == behind[0] or front[-1] == behind[1]:
# #         clause_new = ""
# #     else:
# #         if arr[1].find("延长") != -1:
# #             clause_new = front[-1] + "在" + behind[0] + behind[1] + "延长线上"
# #         else:
# #             clause_new = front[-1] + "在" + behind[0] + behind[1] + "上"
# #     if len(behind) > 2:
# #         if arr[1].find("的平行线") != -1:
# #             if front[-1] == behind[2] or front[-1] == behind[3]:
# #                 clause = ""
# #             else:
# #                 clause_new = front[-1] + "在" + behind[2] + behind[3] + "上"
# #             if clause_new != "":
# #                 clause_new += ","
# #             clause_new += behind[0] + behind[1] + '//' + behind[2] + behind[3]
# #     if len(front) > 1:
# #         if arr[0].find('中点') != -1:
# #             if clause_new != "":
# #                 clause_new += ","
# #             clause_new += front[2] + '是' + front[0] + front[1] + '中点'
# #         elif arr[0].find('上的') != -1:
# #             if clause_new != "":
# #                 clause_new += ","
# #             clause_new += front[2] + '在' + front[0] + front[1] + '上'
# #     return clause_new


# # def transition_diagonal(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if re.search(".*对角线", "".join(seg_list_list[i])):
# #             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             seg_list_list_letter_A = []
# #             seg_list_list_letter_AB = []
# #             seg_list_list_letter_ABC = []
# #             for j in range(len(seg_list_list_letter)):
# #                 if seg_list_list_letter[j][0] == 1:
# #                     seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
# #                 elif seg_list_list_letter[j][0] == 2:
# #                     seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
# #                 else:
# #                     seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
# #             seg_temp = []
# #             for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
# #                 seg_list_list_letter_symbol = seg_list_list[i][
# #                     seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
# #                 seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
# #                 seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
# #                 seg_temp.extend(",")
# #             if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):
# #                 for j in range(len(seg_list_list_letter_A)):
# #                     seg_list_list_letter_temp = ""
# #                     temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
# #                                                          seg_list_list_letter_temp)
# #                     seg_temp.extend(temp)
# #                     seg_temp.extend(",")
# #             if len(seg_list_list_letter_AB) == 1:
# #                 seg_temp.insert(len(seg_temp), seg_list_list_letter_AB[0])
# #                 seg_temp.extend(",")
# #             seg_list_list[i] = seg_temp
# #     return return_seg_list(seg_list_list)


# # def transition_point_at_side_re(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if return_re_return(
# #                 ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
# #                  "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
# #             if seg_list_having("=", seg_list_list[i]):
# #                 if seg_list_list[i][seg_list_list[i].index("=") - 2] == "∠":
# #                     seg_list_list[i].insert(seg_list_list[i].index("=") - 2, ",")
# #                 else:
# #                     seg_list_list[i].insert(seg_list_list[i].index("=") - 1, ",")
# #                 seg_list_list[i] = behind_operation(seg_list_list[i])
# #                 continue
# #             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             seg_list_list_letter_A = []
# #             seg_list_list_letter_AB = []
# #             seg_list_list_letter_ABC = []
# #             for j in range(len(seg_list_list_letter)):
# #                 if seg_list_list_letter[j][0] == 1:
# #                     seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
# #                 elif seg_list_list_letter[j][0] == 2:
# #                     seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
# #                 else:
# #                     seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
# #             seg_list_list_letter_temp = ""
# #             if return_re_return([".*中点"], "".join(seg_list_list[i])):  # 提取关键词
# #                 seg_list_list_letter_temp = "中点"
# #             elif return_re_return([".*延长"], "".join(seg_list_list[i])):
# #                 seg_list_list_letter_temp = "延长线"
# #             else:
# #                 seg_list_list_letter_temp = ""
# #             if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):  # 可能出现单独只是一个图形
# #                 seg_temp = []
# #                 for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
# #                     seg_list_list_letter_symbol = seg_list_list[i][
# #                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
# #                     seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
# #                     seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
# #                     seg_temp.extend(",")
# #                 for j in range(len(seg_list_list_letter_A)):
# #                     temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
# #                                                          seg_list_list_letter_temp)
# #                     seg_temp.extend(temp)
# #                     seg_temp.extend(",")
# #                 seg_list_list[i] = seg_temp
# #             elif len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) > 0:
# #                 seg_temp = []
# #                 for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
# #                     seg_list_list_letter_symbol = seg_list_list[i][
# #                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
# #                     seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
# #                     seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
# #                     seg_temp.extend(",")
# #                 if len(seg_list_list_letter_AB) == 1:
# #                     for j in range(len(seg_list_list_letter_A)):
# #                         temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[0],
# #                                                              seg_list_list_letter_temp)
# #                         seg_temp.extend(temp)
# #                         seg_temp.extend(",")
# #                 seg_list_list[i] = seg_temp
# #             elif re.search("一.*直线", "".join(seg_list_list[i])) is not None or re.search("任意.*点", "".join(
# #                     seg_list_list[i])) is not None:  # 共线
# #                 seg_list_list_temp = ""
# #                 seg_list_list_temp_temp = ""
# #                 seg_list_list_temp += seg_list_list_letter[0][1]
# #                 seg_list_list_temp += seg_list_list_letter[len(seg_list_list_letter) - 1][1]
# #                 seg_list_list_temp_temp = "".join(seg_list_list_temp)
# #                 seg_list_list_letter = seg_list_list_letter[1:]
# #                 seg_list_list_letter = seg_list_list_letter[:len(seg_list_list_letter) - 1]
# #                 if len(seg_list_list_letter) == 0:
# #                     seg_list_list[i] = seg_list_list_temp_temp
# #                 else:
# #                     seg_temp = []
# #                     for j in range(len(seg_list_list_letter)):
# #                         temp = return_the_point_at_line_temp(seg_list_list_letter[j][1], seg_list_list_temp_temp,
# #                                                              seg_list_list_letter_temp)
# #                         seg_temp.extend(temp)
# #                         seg_temp.extend(",")
# #                     seg_list_list[i] = seg_temp

# #             elif (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) == 0) or (
# #                     len(seg_list_list_letter_A) == 0 and len(seg_list_list_letter_AB) > 0):
# #                 seg_list_list_letter_symbol = []
# #                 for j in range(len(seg_list_list_letter_ABC)):  # 记录的图形
# #                     seg_list_list_letter_symbol.insert(len(seg_list_list_letter_symbol), seg_list_list[i][
# #                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1])
# #                 temp = []
# #                 if (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_ABC) > 0) or (
# #                         len(seg_list_list_letter_AB) > 0 and len(seg_list_list_letter_ABC) > 0):
# #                     for j in range(len(seg_list_list_letter_A if len(
# #                             seg_list_list_letter_A) > 0 else seg_list_list_letter_AB)):
# #                         if len(seg_list_list_letter_ABC) == 1:
# #                             temp.insert(len(temp), seg_list_list_letter_symbol[0])
# #                             temp.insert(len(temp), seg_list_list_letter_ABC[0])
# #                         else:
# #                             temp.insert(len(temp), seg_list_list_letter_symbol[j])
# #                             temp.insert(len(temp), seg_list_list_letter_ABC[j])
# #                         temp.extend(",")
# #                         if len(seg_list_list_letter_A) > 0:
# #                             temp.insert(len(temp), seg_list_list_letter_A[j])
# #                             temp.extend("在")
# #                             if len(seg_list_list_letter_ABC) == 1:
# #                                 # temp.insert(len(temp), seg_list_list_letter_symbol[0])
# #                                 temp.insert(len(temp), seg_list_list_letter_ABC[0])
# #                             else:
# #                                 # temp.insert(len(temp), seg_list_list_letter_symbol[j])
# #                                 temp.insert(len(temp), seg_list_list_letter_ABC[j])
# #                             temp.extend("内")
# #                         else:
# #                             temp.insert(len(temp), seg_list_list_letter_AB[j])
# #                         temp.extend(",")
# #                         if len(seg_list_list_letter_A) > 0:
# #                             temp.extend(seg_list_list_letter_A[j])
# #                         else:
# #                             temp.extend(seg_list_list_letter_AB[j])
# #                 elif len(seg_list_list_letter_A) > 0:  # 特质判断，点在斜边上
# #                     if return_re_return([".*斜"], "".join(seg_list_list[i])):
# #                         for j in range(len(seg_list_list_letter_A)):
# #                             temp.insert(len(temp), seg_list_list_letter_A[j])
# #                             temp.extend("在")
# #                             temp.extend("斜边")
# #                             temp.extend("上")
# #                             temp.extend(",")
# #                     elif return_re_return([".*侧"], "".join(seg_list_list[i])):  # 此处为补丁，点E在F左侧
# #                         temp = seg_list_list[i]
# #                 else:
# #                     temp.insert(len(temp), seg_list_list_letter_AB[0])
# #                     if seg_list_list_letter_temp == "延长线":
# #                         temp.extend("的")
# #                         temp.insert(len(temp), "延长线")
# #                 seg_list_list[i] = temp
# #             elif seg_list_having_1(["作", "做"], seg_list_list[i]):  # 特质判断，以AE为边在直线BC的上方作正方形AEFG
# #                 seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("作" if "作" in seg_list_list[i] else "做"):]
# #                 seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])

# #             else:
# #                 for j in range(len(symbol_keywords_main)):
# #                     if symbol_keywords_main[j] in seg_list_list[i]:
# #                         temp = []
# #                         letter = []
# #                         temp_int = 0
# #                         for k in range(3):
# #                             if seg_list_list[i].index(symbol_keywords_main[j]) - k >= 0 \
# #                                     and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k] in
# #                                          map_clear_up_keywords or seg_list_list[i][
# #                                              seg_list_list[i].index(symbol_keywords_main[j]) - k] in symbol_keywords or
# #                                          if_number_and_letter(
# #                                              seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])):
# #                                 temp.insert(len(temp),
# #                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])
# #                                 temp_int = k
# #                         temp.reverse()
# #                         letter = find_all_letter_return_side_letter(temp)
# #                         letter = letter[0][1]
# #                         temp.extend(symbol_keywords_main[j])
# #                         for k in range(3):
# #                             if seg_list_list[i].index(symbol_keywords_main[j]) + k < len(seg_list_list[i]) \
# #                                     and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k] in
# #                                          map_clear_up_keywords or seg_list_list[i][
# #                                              seg_list_list[i].index(symbol_keywords_main[j]) + k] in symbol_keywords or
# #                                          if_number_and_letter(
# #                                              seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])):
# #                                 temp.insert(len(temp),
# #                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])
# #                         seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index(symbol_keywords_main[j]) - temp_int]
# #                         new_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #                         for k in range(len(letter)):
# #                             for p in range(len(new_letter)):
# #                                 if letter[k] in new_letter[p][1]:
# #                                     continue
# #                                 else:
# #                                     letter = letter[k]
# #                                     break
# #                             if k + 1 == len(letter):
# #                                 letter = ""
# #                                 break
# #                         seg_list_list[i].extend("存在点")
# #                         seg_list_list[i].extend(letter)
# #                         seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])
# #                         seg_list_list[i].extend(temp)
# #     return return_seg_list(seg_list_list)


# # def transition_hand_over_temp(seg_list_list, temp, temp_temp):
# #     temp.extend(seg_list_list[len(seg_list_list) - 1])
# #     for i in range(len(seg_list_list) - 1):
# #         temp_temp.extend(seg_list_list[i])
# #         temp_temp.extend(",")
# #     return temp, temp_temp


# # def transition_hand_over(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if seg_list_having_2("交", seg_list_list[i]):
# #             seg_list_list[i] = list(jieba.cut("".join(seg_list_list[i]), cut_all=False))
# #             seg_list_list_front = seg_list_list[i][
# #                                   :seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交")]
# #             seg_list_list_mid = seg_list_list[i][
# #                                 seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交") + 1:
# #                                 seg_list_list[i].index("于")]
# #             seg_list_list_behind = seg_list_list[i][seg_list_list[i].index("于") + 1:]
# #             seg_list_list_front = behind_operation(seg_list_list_front)
# #             seg_list_list_mid = behind_operation(seg_list_list_mid)
# #             seg_list_list_behind = behind_operation(seg_list_list_behind)
# #             seg_list_list_front_temp = return_seg_list_list(seg_list_list_front)  # 查看是否有补充
# #             seg_list_list_mid_temp = return_seg_list_list(seg_list_list_mid)
# #             seg_list_list_behind_temp = return_seg_list_list(seg_list_list_behind)
# #             temp = []
# #             temp_temp = []
# #             temp, temp_temp = transition_hand_over_temp(seg_list_list_front_temp, temp, temp_temp)
# #             temp.extend("交")
# #             temp, temp_temp = transition_hand_over_temp(seg_list_list_mid_temp, temp, temp_temp)
# #             temp.extend("于")
# #             temp, temp_temp = transition_hand_over_temp(seg_list_list_behind_temp, temp, temp_temp)
# #             temp_temp.extend(temp)
# #             temp.extend(",")
# #             seg_list_list[i] = temp_temp
# #     return return_seg_list(seg_list_list)


# # def transition_zuo_in_list(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if re.search(".*作", "".join(seg_list_list[i])):
# #             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             if len(seg_list_letter) == 0:
# #                 seg_list_list[i] = ""
# #             elif len(seg_list_letter) == 1:
# #                 seg_list_list[i] = seg_list_letter[0][1]
# #             elif len(seg_list_letter) == 2:
# #                 if seg_list_having(seg_list_letter[0][1], seg_list_letter[1][1]):
# #                     seg_list_list[i] = seg_list_letter[1][1]
# #                 else:
# #                     temp = []
# #                     temp.extend("过")
# #                     temp.insert(len(temp), seg_list_letter[0][1])
# #                     temp.extend("作")
# #                     temp.insert(len(temp), seg_list_letter[1][1])
# #                     seg_list_list[i] = temp
# #             # elif len(seg_list_letter) == 3:
# #                 # print(seg_list_list[i])
# #             # else:
# #                 # print("多元关系", seg_list_list[i])
# #     return return_seg_list(seg_list_list)


# # # 返回seg_list_list
# # def return_seg_list_list(seg_list):
# #     seg_list_list = []
# #     seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
# #     while seg_list1 != "":
# #         seg_list_list.append(seg_list1)
# #         seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
# #     return seg_list_list


# # def return_seg_list(seg_list_list):
# #     seg_list = []
# #     for i in range(len(seg_list_list)):
# #         seg_list.extend(seg_list_list[i])
# #         seg_list.extend(",")
# #     return seg_list


# # def tran_wei_to_fen_bie(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if "为" in seg_list_list[i]:
# #             seg_list_list_front = seg_list_list[i][:seg_list_list[i].index("为")]
# #             seg_list_list_front.insert(len(seg_list_list_front), "分别")
# #             seg_list_list_front.extend(seg_list_list[i][seg_list_list[i].index("为"):])
# #             seg_list_list[i] = seg_list_list_front
# #     return return_seg_list(seg_list_list)


# # def delete_line_and_line(symbol, seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if seg_list_having_0(symbol, seg_list_list[i]):
# #             if not seg_list_having_2(["交", "作"], seg_list_list[i]) and len(
# #                     find_all_letter_return_side_letter(seg_list_list[i])) >= len(seg_list_list[i]) * 0.5:
# #                 seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #                 seg_temp = []
# #                 for j in range(len(seg_list_letter)):
# #                     seg_temp.insert(len(seg_temp), seg_list_letter[j][1])
# #                     seg_temp.extend(",")
# #                 seg_list_list[i] = seg_temp
# #             else:
# #                 seg_list_list_temp = seg_list_list[i][
# #                                      :seg_list_list[i].index(
# #                                          seg_list_having_0(symbol, seg_list_list[i]))]
# #                 seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(
# #                     seg_list_having_0(symbol, seg_list_list[i])) + 1:])
# #                 seg_list_list[i] = seg_list_list_temp
# #     return return_seg_list(seg_list_list)


# # def delete_have_other(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     seg_list_list_temp = []
# #     for i in range(len(seg_list_list)):
# #         for j in range(len(seg_list_list)):
# #             if j <= i:
# #                 continue
# #             else:
# #                 if seg_list_list[i] == seg_list_list[j]:
# #                     break
# #             if j + 1 >= len(seg_list_list):
# #                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
# #         if i + 1 == len(seg_list_list):
# #             seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
# #     seg_temp = []
# #     for i in range(len(seg_list_list_temp)):
# #         seg_temp.extend(seg_list_list_temp[i])
# #         seg_temp.extend(",")
# #     return seg_temp


# # def transition_divide_temp(seg_list_letter, seg_list_angle, seg_list_list_key):
# #     temp = []
# #     temp.insert(len(temp), seg_list_letter)
# #     temp.insert(len(temp), seg_list_list_key)
# #     temp.extend(seg_list_angle)
# #     temp.extend(",")
# #     temp.insert(len(temp), seg_list_letter)
# #     temp.extend(",")
# #     return temp


# # def transition_divide(seg_list):  # 平分
# #     seg_list = "".join(seg_list)
# #     seg_list = list(jieba.cut(seg_list, cut_all=False))
# #     if re.search(".*垂直平分", "".join(seg_list)):
# #         seg_list_letter = find_all_letter_return_side_letter(seg_list)
# #         if len(seg_list_letter) == 0:
# #             return ""
# #         elif len(seg_list_letter) == 1:
# #             return seg_list
# #         symbol_letter = []
# #         symbol_point = []
# #         for i in range(len(seg_list_letter)):
# #             if seg_list_letter[i][0] == 2:
# #                 symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
# #             else:
# #                 symbol_point.insert(len(symbol_point), seg_list_letter[i][1])
# #         seg_list_temp = []
# #         seg_list_temp.insert(len(seg_list_temp), symbol_letter[0])
# #         seg_list_temp.extend("⊥")
# #         seg_list_temp.insert(len(seg_list_temp), symbol_letter[1])
# #         if len(symbol_point) == 1:
# #             seg_list_temp.extend("于")
# #             seg_list_temp.insert(len(seg_list_temp), symbol_point[0])
# #         seg_list_temp.extend(",")
# #         seg_list_temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
# #         seg_list = seg_list_temp
# #     elif re.search(".*平分", "".join(seg_list)):
# #         seg_list_letter = find_all_letter_return_side_letter(seg_list)
# #         if len(seg_list_letter) == 0:
# #             return ""
# #         elif len(seg_list_letter) == 1 and seg_list_letter[0][0] == 2:
# #             return seg_list_letter[0][1]
# #         else:
# #             symbol_angle = []
# #             symbol_triangle = []
# #             symbol_letter = []
# #             for i in range(len(seg_list_letter)):
# #                 if seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in "∠":
# #                     symbol_angle_temp = ["∠"]
# #                     symbol_angle_temp.insert(len(symbol_angle_temp), seg_list_letter[i][1])
# #                     symbol_angle.insert(len(symbol_angle), symbol_angle_temp)
# #                 elif seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in map_clear_up_keywords:
# #                     symbol_triangle_temp = []
# #                     symbol_triangle_temp.insert(len(symbol_triangle_temp),
# #                                                 seg_list[seg_list.index(seg_list_letter[i][1]) - 1])
# #                     symbol_triangle_temp.insert(len(symbol_triangle_temp), seg_list_letter[i][1])
# #                     symbol_triangle.insert(len(symbol_triangle), symbol_triangle_temp)
# #                 else:
# #                     symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
# #             if len(symbol_triangle) == 0:
# #                 temp = []
# #                 if len(symbol_angle) == 0:
# #                     if return_re_return([".*互相平分"], "".join(seg_list)):
# #                         for i in range(len(symbol_letter)):
# #                             for j in range(len(symbol_letter)):
# #                                 temp.extend(transition_divide_temp(symbol_letter[i], symbol_letter[j], "平分"))
# #                     elif len(symbol_letter) == 2:
# #                         temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
# #                 else:
# #                     if len(symbol_angle) == len(symbol_letter):
# #                         for i in range(len(symbol_angle)):
# #                             temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
# #                     else:
# #                         for i in range(len(symbol_letter)):
# #                             temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[0], "平分"))
# #                 if len(temp) == 0:  # 此处为补丁，即出现∠CAB的平分线
# #                     temp = seg_list
# #                 seg_list = temp
# #             else:
# #                 temp = []
# #                 if len(symbol_angle) == len(symbol_letter):
# #                     for i in range(len(symbol_triangle)):
# #                         temp.insert(len(temp), symbol_triangle[i][0])
# #                         temp.insert(len(temp), symbol_triangle[i][1])
# #                         temp.extend(",")
# #                     for i in range(len(symbol_angle)):
# #                         temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
# #                 elif len(symbol_triangle) == 1 and len(symbol_letter) == 1:
# #                     seg_list_temp = seg_list_having_0(symbol_letter[0], symbol_triangle[0][1])
# #                     temp.extend(symbol_triangle[0])
# #                     temp.extend(",")
# #                     temp.extend(symbol_letter)
# #                     temp.extend("平分")
# #                     temp.extend("∠")
# #                     temp.extend(seg_list_temp)
# #                     temp.extend(",")
# #                     temp.extend(symbol_letter)
# #                 seg_list = temp
# #     return seg_list


# # def transition_S_C(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         seg_temp = []
# #         if return_re_return([".*面积", ".*周长"], "".join(seg_list_list[i])):
# #             seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             symbol_ = []
# #             seg_list_list_temp = []
# #             for j in range(len(seg_letter)):  # 求主要的图形
# #                 if seg_letter[j][0] >= 3 and \
# #                         seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1] in map_clear_up_keywords:
# #                     symbol_.insert(len(symbol_), seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1])
# #                     symbol_.insert(len(symbol_), seg_letter[j][1])
# #                     seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index(seg_letter[j][1]) - 1]
# #                     seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) + 1:])
# #             seg_letter = find_all_letter_return_side_letter(seg_list_list_temp)
# #             seg_num = []
# #             for j in range(len(seg_list_list_temp)):
# #                 if if_number(seg_list_list_temp[j]) or if_letter(seg_list_list_temp[j]) or \
# #                         seg_list_list_temp[j] in symbol_keywords:
# #                     seg_num.insert(len(seg_num), seg_list_list_temp[j])
# #                     # if j + 1 < len(seg_list_list_temp) and seg_list_list_temp[j + 1] in ["cm", "dm", "m", "km"]:
# #                     #     seg_num.insert(len(seg_num),seg_list_list_temp[j + 1])
# #             if re.search(".*面积", "".join(seg_list_list[i])):
# #                 seg_temp.insert(len(seg_temp), "S")
# #             elif re.search(".*周长", "".join(seg_list_list[i])):
# #                 seg_temp.insert(len(seg_temp), "C")
# #             seg_temp.extend(symbol_)
# #             if len(seg_num) != 0:
# #                 seg_temp.extend("=")
# #                 seg_temp.extend(seg_num)
# #             seg_list_list[i] = seg_temp
# #         elif seg_list_having("长", seg_list_list[i]):
# #             seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             seg_symbol = seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]):]
# #             seg_num = []
# #             for j in range(len(seg_list_list[i])):
# #                 if if_number(seg_list_list[i][j]):
# #                     seg_num.insert(len(seg_num), seg_list_list[i][j])
# #                     if j + 1 < len(seg_list_list[i]) and seg_list_list[i][j + 1] in ["cm", "dm", "m", "km"]:
# #                         seg_num.insert(len(seg_num), seg_list_list[i][j + 1])
# #             seg_temp.insert(len(seg_temp), "l")
# #             seg_temp.insert(len(seg_temp), seg_letter[0][1])
# #             if len(seg_num) != 0:
# #                 seg_temp.extend("=")
# #                 seg_temp.extend(seg_num)
# #             seg_list_list[i] = seg_temp

# #     return return_seg_list(seg_list_list)


# # def transition_parallel(seg_list):
# #     seg_list_letter = find_all_letter_return_side_letter(seg_list)
# #     if len(seg_list_letter) == 2:
# #         seg_list_temp = []
# #         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[0][1])
# #         seg_list_temp.insert(len(seg_list_temp), "//")
# #         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
# #         seg_list_temp.extend(",")
# #         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
# #         seg_list = seg_list_temp
# #     return seg_list


# # def transition_parallel_tran(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if "//" in seg_list_list[i]:
# #             seg_temp = seg_list_list[i][:seg_list_list[i].index("//")]
# #             seg_temp.insert(len(seg_temp), "平行")
# #             seg_temp.extend(seg_list_list[i][seg_list_list[i].index("//") + 1])
# #             seg_list_list[i] = seg_temp
# #     seg_temp = []
# #     for i in range(len(seg_list_list)):
# #         seg_temp.extend(seg_list_list[i])
# #         seg_temp.extend(",")
# #     return seg_temp


# # def transition_pause(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if re.search(".*、", "".join(seg_list_list[i])):
# #             seg_list_list_temp = []
# #             seg_list_list_behind = []
# #             seg_list_list_front = seg_list_list[i]
# #             while re.search(".*、", "".join(seg_list_list_front)):
# #                 seg_list_list_behind = seg_list_list_front[:seg_list_list_front.index("、")]
# #                 seg_list_list_front = seg_list_list_front[seg_list_list_front.index("、") + 1:]
# #                 seg_list_list_behind = behind_operation(seg_list_list_behind)
# #                 seg_list_list_temp.extend(seg_list_list_behind)
# #                 seg_list_list_temp.extend(",")
# #             seg_list_list_behind = behind_operation(seg_list_list_behind)
# #             seg_list_list_temp.extend(seg_list_list_behind)
# #             seg_list_list_temp.extend(",")
# #             seg_list_list[i] = seg_list_list_temp
# #     return return_seg_list(seg_list_list)


# # def return_re_return(input_list, seg_list_list):
# #     for i in range(len(input_list)):
# #         if re.search(input_list[i], "".join(seg_list_list)) is not None:
# #             return True
# #     return False


# # # 切割后续处理的“和”
# # def cut_seg_list_and(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if re.search(".*和", "".join(seg_list_list[i])):
# #             seg_front = seg_list_list[i][:seg_list_list[i].index("和")]
# #             seg_behind = seg_list_list[i][seg_list_list[i].index("和") + 1:]
# #             seg_front = behind_operation(seg_front)
# #             seg_behind = behind_operation(seg_behind)
# #             seg_list_list_temp = seg_front
# #             seg_list_list_temp.extend(",")
# #             seg_list_list_temp.extend(seg_behind)
# #             seg_list_list[i] = seg_list_list_temp
# #     return return_seg_list(seg_list_list)


# # def behind_operation(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #         if len(seg_list_letter) == 0:  # 不存在关系
# #             if seg_list_having("∠", seg_list_list[i]):
# #                 for j in range(len(seg_list_list)):
# #                     seg_list_list[j] = ""
# #             else:
# #                 seg_list_list[i] = ""
# #         if return_re_return([".*作"], seg_list_list[i]):
# #             if re.search(".*于", "".join(seg_list_list[i])) is None:
# #                 seg_list_list[i] = guozuo("".join(seg_list_list[i]))
# #             else:
# #                 seg_list_list[i] = guozuoyu("".join(seg_list_list[i]))
# #             seg_list_list[i] = list(jieba.cut(seg_list_list[i], cut_all=False))  # 精确模式切割词句
# #         elif re.search(".*交", "".join(seg_list_list[i])) is not None:
# #             seg_list_list[i] = transition_hand_over(seg_list_list[i])  # 交
# #         elif return_re_return(
# #                 ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
# #                  "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
# #             seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])  # 借助re处理点在线上
# #         elif seg_list_having("点", seg_list_list[i]):
# #             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             if len(seg_list_list_letter) == 1:
# #                 seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("点") + 1:]
# #         elif seg_list_having_0(["连接", "连结", "链接", "线段", "若", "设", "直线"], seg_list_list[i]):
# #             seg_list_list[i] = delete_line_and_line(["连接", "连结", "链接", "线段", "若", "设", "直线"],
# #                                                     seg_list_list[i])  # 将连接AB删除
# #         elif return_re_return([".*平行"], seg_list_list[i]):
# #             seg_list_list[i] = transition_parallel(seg_list_list[i])
# #         elif re.search(".*平分", "".join(seg_list_list[i])):
# #             seg_list_list[i] = transition_divide(seg_list_list[i])
# #         elif re.search(".*、", "".join(seg_list_list[i])):
# #             seg_list_list[i] = transition_pause(seg_list_list[i])
# #         elif re.search(".*对角线", "".join(seg_list_list[i])):
# #             seg_list_list[i] = transition_diagonal(seg_list_list[i])
# #         elif re.search(".*和", "".join(seg_list_list[i])):
# #             seg_list_list[i] = cut_seg_list_and(seg_list_list[i])
# #         elif return_re_return([".*面积", ".*周长"], seg_list_list[i]) or seg_list_having("长", seg_list_list[i]):
# #             seg_list_list[i] = transition_S_C(seg_list_list[i])  # 处理面积和周长
# #         elif re.search("的度数", "".join(seg_list_list[i])):
# #             seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index("的")]
# #         elif re.search(".*高", "".join(seg_list_list[i])):
# #             seg_list_list[i] = transition_high(seg_list_list[i])
# #         elif seg_list_having(["中"], seg_list_list[i]):
# #             seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("中")]
# #             seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("中") + 1:])
# #             seg_list_list[i] = seg_list_list_temp
# #         elif return_re_return([".*两点"], "".join(seg_list_list[i])):
# #             seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("两点")]
# #             seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("两点") + 1:])
# #             seg_list_list[i] = seg_list_list_temp
# #         elif return_re_return([".*中点"], "".join(seg_list_list[i])):
# #             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             if len(seg_list_letter) == 2:
# #                 seg_list_list[i] = return_the_point_at_line_temp(seg_list_letter[0][1], seg_list_letter[1][1], "中点")
# #         elif return_re_return(["垂直.*于"], "".join(seg_list_list[i])):
# #             for j in range(len(seg_list_list[i])):
# #                 if seg_list_list[i][j] == "垂直":
# #                     seg_list_list[i][j] = "⊥"

# #     seg_list = return_seg_list(seg_list_list)
# #     while len(seg_list) != 0 and seg_list[len(seg_list) - 1] == ",":
# #         seg_list = seg_list[:len(seg_list) - 1]
# #     return seg_list


# # def delete_other_point_line(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #         seg_long = 0
# #         for j in range(len(seg_letter)):
# #             seg_long += seg_letter[j][0]
# #         if seg_long == len("".join(seg_list_list[i])):
# #             seg_list_list[i] = ""
# #         if return_re_return([".*的长", ".*的延长线"], "".join(seg_list_list[i])) and len(seg_letter) == 1:
# #             seg_list_list[i] = ""
# #         if len(seg_letter) == 1 and seg_letter[0][1] in seg_list_list[i] and \
# #                 seg_list_list[i].index(seg_letter[0][1]) - 1 >= 0 \
# #                 and seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]) - 1] in ["∠", "l"] and \
# #                 seg_list_list[i].index(seg_letter[0][1]) + 1 == len(seg_list_list[i]):  # 只有单独的角
# #             seg_list_list[i] = ""
# #         if "∠" in seg_list_list[i] and seg_list_list[i].index("∠") + 1 < len(seg_list_list[i]) and if_number(
# #                 seg_list_list[i][seg_list_list[i].index("∠") + 1]):
# #             return ""
# #     seg_temp = []
# #     for i in range(len(seg_list_list)):
# #         seg_temp.extend(seg_list_list[i])
# #         seg_temp.extend(",")
# #     return seg_temp


# # # 处理高
# # def transition_high(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     seg_list_temp = []
# #     for i in range(len(seg_list_list)):
# #         if re.search(".*高", "".join(seg_list_list[i])):
# #             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #             seg_list_list_temp = []
# #             for j in range(len(seg_list_all_triangle)):
# #                 if (len(seg_list_list_letter) == 2 and seg_list_list_letter[0][0] == 2 and
# #                         seg_list_having_all(seg_list_list_letter[0][1], seg_list_all_triangle[j][1])):
# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
# #                     seg_list_list_temp.extend("是")
# #                     seg_list_list_temp.extend(seg_list_all_triangle[j])
# #                     seg_list_list_temp.extend("的")
# #                     seg_list_list_temp.extend("高")
# #                     seg_list_list_temp.extend(",")
# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
# #                     seg_list_list_temp.extend(",")
# #                 elif len(seg_list_list_letter) == 2 and seg_list_list_letter[1][0] == 2 and \
# #                         seg_list_having_all(seg_list_list_letter[1][1], seg_list_all_triangle[j][1]):
# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
# #                     seg_list_list_temp.extend("是")
# #                     seg_list_list_temp.extend(seg_list_all_triangle[j])
# #                     seg_list_list_temp.extend("的")
# #                     seg_list_list_temp.extend("高")
# #                     seg_list_list_temp.extend(",")
# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
# #                     seg_list_list_temp.extend(",")
# #                 elif len(seg_list_list_letter) == 1 and seg_list_list_letter[0][0] == 2:
# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
# #                     seg_list_list_temp.extend("是")
# #                     seg_list_list_temp.extend(seg_list_all_triangle[0])
# #                     seg_list_list_temp.extend("的")
# #                     seg_list_list_temp.extend("高")
# #                     seg_list_list_temp.extend(",")
# #                     if "=" in seg_list_list[i]:
# #                         seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
# #                         seg_list_list_temp.extend("=")
# #                         for j in range(len(seg_list_list[i])):
# #                             if if_number(seg_list_list[i][j]):
# #                                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][j])
# #                         seg_list_list_temp.extend(",")

# #                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
# #                     seg_list_list_temp.extend(",")
# #             seg_list_list[i] = seg_list_list_temp
# #     seg_temp = []
# #     for i in range(len(seg_list_list)):
# #         seg_temp.extend(seg_list_list[i])
# #         seg_temp.extend(",")
# #     return seg_temp


# # def find_all_triangle(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #         for j in range(len(seg_list_list_letter)):
# #             if seg_list_list_letter[j][0] >= 3 and seg_list_list[i].index(seg_list_list_letter[j][1]) - 1 >= 0 and \
# #                     seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1] in map_clear_up_keywords:
# #                 seg_list_temp_temp = []
# #                 seg_list_temp_temp.insert(len(seg_list_temp_temp),
# #                                           seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1])
# #                 seg_list_temp_temp.insert(len(seg_list_temp_temp), seg_list_list_letter[j][1])
# #                 if seg_list_temp_temp not in seg_list_all_triangle:  # 防止重复
# #                     seg_list_all_triangle.insert(len(seg_list_all_triangle), seg_list_temp_temp)
# #     return seg_list_all_triangle


# # def dispose_waist_and_diagonal(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     seg_list_list_letter_ABC = []
# #     for i in range(len(seg_list_list)):
# #         seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
# #         seg_list_list_letter_A = []
# #         seg_list_list_letter_AB = []
# #         for j in range(len(seg_list_list_letter)):
# #             if seg_list_list_letter[j][0] == 2:
# #                 seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
# #             elif seg_list_list_letter[j][0] == 1:
# #                 seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
# #             else:
# #                 seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
# #         if re.search(".*对角线", "".join(seg_list_list[i])):
# #             if len(seg_list_list_letter_AB) == 0:
# #                 seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
# #                 if len(seg_list_list_letter_ABC_1) == 4:
# #                     wei_temp = seg_list_list[i].index("对角线") + 1
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = "、"
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[3]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     # print(seg_list_list[i])
# #         if seg_list_having("腰", seg_list_list[i]):
# #             if len(seg_list_list_letter_AB) == 0:
# #                 seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
# #                 if len(seg_list_list_letter_ABC_1) == 3:
# #                     wei_temp = re.search(".*对角线", "".join(seg_list_list[i])).end()
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[1]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = "、"
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     # print(seg_list_list[i])

# #                 if len(seg_list_list_letter_ABC_1) == 4:
# #                     wei_temp = seg_list_list[i].index("腰") + 1
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[3]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = "、"
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[2]
# #                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
# #                     # print(seg_list_list[i])
# #     seg_list = return_seg_list(seg_list_list)
# #     return seg_list


# # def clean_all_triangle():
# #     seg_list_all_triangle.clear()


# # def delete_other_line(seg_list):
# #     seg_list_list = return_seg_list_list(seg_list)
# #     for i in range(len(seg_list_list)):
# #         if len(seg_list_list[i]) < 3:
# #             for j in range(0, i):
# #                 if seg_list_having(seg_list_list[i], seg_list_list[i-j]):
# #                     seg_list_list[i] = ""
# #                     break
# #     seg_list = return_seg_list(seg_list_list)
# #     return seg_list


# # def cut_word(txt_data):
# #     point = []  # 点
# #     line = []  # 线
# #     triangle = []  # 三角形
# #     map_ = []  # 多边形
# #     seg_list = list(jieba.cut(txt_data, cut_all=False))  # 精确模式切割词句
# #     # print("".join(seg_list))
# #     # seg_list = is_half_angle(seg_list)#全角转半角
# #     seg_list = conversion_parallel(seg_list)  # 对//进行处理
# #     seg_list = remove_pause(seg_list)  # 去除前面的序号
# #     seg_list = find_if_have_parallel_and_equal(seg_list)  # 特殊值判断是否有平行且相等
# #     seg_list = conversion_symbols(seg_list)  # 将转换为文字
# #     seg_list = list(jieba.cut("".join(seg_list), cut_all=False))
# #     seg_list = conversion_parallel(seg_list)  # 对//进行处理
# #     seg_list = seg_list_transition_side(seg_list)  # lAB = 5 --转变---> 边AB = 5
# #     seg_list = delete_prove(seg_list)  # 删除“求证”
# #     seg_list = handles_greater_or_less(seg_list)  # 将<=或者>=进行规范化处理
# #     seg_list = delete_blank(seg_list)  # 删除空格
# #     seg_list = add_de_to_side(seg_list)  # 给长宽高前适当的加"的"
# #     seg_list = transition_side(seg_list)  # 将三边等转换成具体字母
# #     seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
# #     # print("####分别####\t:", "".join(seg_list))
# #     seg_list = add_all_shape(seg_list)  # 给所有超过三个字母的字母添加基础形状
# #     seg_list = delete_repetition_symbol(seg_list)  # 去除重复的图形
# #     seg_list = add_all_letter(seg_list)  # 将单独出现的三角形补全字母
# #     seg_list = dispose_waist_and_diagonal(seg_list)  # 处理对角线与腰
# #     seg_list = add_all_shape_at_front(seg_list)  # 防止出现三角形ABC\DEF\GHZ   #处理形状在前面
# #     seg_list = add_all_shape_at_behind(seg_list)  # 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH   #处理形状在后面
# #     seg_list = transition_equal_or_similarity(seg_list)  # 处理连等的情况
# #     seg_list = dispose_shi_and_symbol(seg_list)  # 处理四边形ABCD是正方形的情况
# #     find_all_triangle(seg_list)  # 记录所有的多边形
# #     seg_list = transition_litter_to_super(seg_list)  # 将小写转换为大写(三角形,角)
# #     seg_list = add_comma_at_equal(seg_list)  # 在连等后面加上逗号，清除垂足为或者垂足于  AB⊥BD,垂足是B点 -- >  AB⊥BD于B
# #     seg_list = cut_zuo_from_seg_list(seg_list)  # 将作从（过A 左AS垂直于DF)提取出来
# #     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
# #     seg_list = add_to_the_vertical(seg_list)  # 将垂足于A,添加到前一步的句子中
# #     # print("".join(seg_list))
# #     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
# #     seg_list = cut_respect_is_importance(seg_list, "交")  # 处理交
# #     # seg_list = transition_S_C(seg_list)  # 处理面积和周长
# #     seg_list = tran_wei_to_fen_bie(seg_list)  # 将为转变为 分别为
# #     seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
# #     seg_list = delete_blank(seg_list)  # 删除空格
# #     seg_list = transition_angle_to_angle(seg_list)  # 将符号角平分线更改为角平分线

# #     seg_list = behind_operation(seg_list)  # 后续操作
# #     seg_list = transition_parallel_tran(seg_list)  # 将//转换为平行
# #     seg_list = seg_list_complement(seg_list)  # 补全 角的字母
# #     seg_list = transition_triangle_symbol(seg_list, "三角形")  # 将三角形转换为符号

# #     seg_list = delete_have_other(seg_list)  # 去重
# #     seg_list = delete_other_line(seg_list)  # 去重
# #     # seg_list = delete_other_point_line(seg_list)  # 删去单独的点和线与角
# #     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
# #     seg_list = add_end_punctuation(seg_list)  # 给末尾加上;
# #     clean_all_triangle()  # 清除记录的多边形
# #     with open(txt_output, "a", encoding="utf-8") as fw:
# #         fw.write("".join(seg_list))
# #         fw.write("\n")
# #     fw.close()
# #     # print("".join(seg_list))

# # def setDir(filepath):
# #     #没有文件夹就创建，有就清空
# #     if not os.path.exists(filepath):
# #         os.makedirs(filepath)
# #     else:
# #         shutil.rmtree(filepath)
# #         os.mkdir(filepath)
# # def process():
# #     setDir(txt_output[:-12])
# #     for word in map_keywords:
# #         jieba.add_word(word)  # 分词时添加关键词
# #     for word in jieba_have_delete:
# #         jieba.del_word(word)
# #     file = open(txt_input, 'r', encoding="utf-8", errors="ignore")  # 打开文件
# #     data = " "
# #     while data:
# #         data = file.readline()
# #         # data = data[:-1]  # 逐行读取文件，也就是提取出每一题
# #         if data != "" and data != "\n":
# #             cut_word(data)
# #             # print(data)

# #     file.close()  # 确保文件被关闭

# import re
# import jieba
# import jieba.posseg as pseg
# import sys
# import numpy
# from jieba import analyse
# import shutil
# import os
# from config import *
# # txt_input = "D://Desktop//题目.txt"
# # txt_output = "D://Desktop//disposed.txt"

# jieba_have_delete = ["于点", "交于", "中高", "外作", "相交于", "上且", "腰交于", "线交", "边交于", "交边", "交作",
#                      "边于", "线于", "点作"]
# map_keywords = ["线", "三角形", "△", "Rt△", "rt△", "直角三角形", "直角△", "等腰三角形", "等腰△", "等边三角形", "等边△",
#                 "等腰直角三角形", "等腰直角△",
#                 "等腰Rt△", "四边形", "矩形", "正方形", "长方形", "▭", "平行四边形", "▱", "▰", "梯形", "等腰梯形",
#                 "直角梯形", "等腰直角梯形", "菱形", "◇",
#                 "◆", "多边形", "凸多边形", "平行且相等", "<>", "平行于"]  # 有坑不等于
# map_clear_up_keywords = ["线", "三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形", "矩形",
#                          "正方形", "长方形", "平行四边形",
#                          "梯形", "等腰梯形", "直角梯形", "菱形", "多边形", "凸多边形", "五边形", "六边形", "七边形",
#                          "高"]
# map_clear_up_keywords_value = [0, 1, 2.01, 2.02, 2.03, 4.03, 5, 8.01, 8.04, 8.03, 10.02, 6.01, 7.02, 7.03, 10.01, 9, 10,
#                                11, 12, 13]
# map_clear_up_keywords_error = [14.02, 14.04, 14.05, 14.05, 15.03, 15.04, 15.05, 15.06, 15.06, 15.07, 16.02, 16.03,
#                                17.03, 17.04, 17.04, 17.05, 18.02, 18.03, 23, 24, 25, 0]  # 当权值相加时不可能出现这类情况
# # print(sorted(list(map_clear_up_keywords_error)))
# symbol_keywords = ["∠", "°", "+", "-", "/", "*", "·", "^", "'", "√", "≤", "≥"]
# symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]  # 留坑 三角形的全等无法实现
# side = ["三边", "四边", "五边", "六边"]
# the_capital_form_of_a_chinese_number = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
# seg_list_all_triangle = []


# def if_letter(seg_list):  # 检查是否为英文
#     return seg_list.encode('utf-8').isalpha()


# def if_number(num):  # 检测是否为数字
#     if len(num) == 0:
#         return False
#     for i in range(len(num)):
#         if '0' <= num[i] <= '9' or num[i] == ".":
#             continue
#         else:
#             return False
#     return True


# def if_number_and_letter(seg_list):
#     for i in range(len(seg_list)):
#         if if_letter(seg_list[i]) or if_number(seg_list[i]):
#             continue
#         else:
#             return False
#     return True


# def delete_blank(seg_list):  # 删除空格
#     j = 0
#     while j == 0:
#         if len(seg_list) == 0:
#             break
#         for i in range(len(seg_list)):
#             if seg_list[i] == " " or seg_list[i] == "":
#                 seg_list1 = seg_list[i + 1:]
#                 seg_list2 = seg_list[:i]
#                 seg_list = seg_list2 + seg_list1
#                 break
#             i += 1
#             if i >= (len(seg_list) - 1):
#                 j += 1
#     return seg_list


# def conversion_parallel(seg_list):  # 对//进行处理
#     j = 0
#     while j == 0:
#         for i in range(len(seg_list) - 1):
#             if seg_list[i] == "/" and seg_list[i + 1] == "/":
#                 seg_list1 = seg_list[i + 2:]
#                 seg_list2 = seg_list[:i]
#                 seg_list = seg_list2 + ["//"] + seg_list1
#                 break
#             if seg_list[i] == "\\" and seg_list[i + 1] == "\\":
#                 seg_list1 = seg_list[i + 2:]
#                 seg_list2 = seg_list[:i]
#                 seg_list = seg_list2 + ["//"] + seg_list1
#                 break
#             i += 1
#             if i >= (len(seg_list) - 1):
#                 j += 1
#     return seg_list


# # 将三边\四边给去掉
# def transition_side(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if seg_list_having(side, seg_list_list[i]):
#             seg_list_temp = return_how_many_side(seg_list_having_0(side, seg_list_list[i]))
#             seg_anger_temp = []
#             for j in range(seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i]))):
#                 # 从后面往前面找
#                 if if_letter(
#                         seg_list_list[i][seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]):
#                     seg_list_anger = seg_list_list[i][
#                         seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]
#                     if len(seg_list_anger) == seg_list_temp:
#                         seg_anger = []
#                         for k in range(len(seg_list_anger)):
#                             seg_anger.insert(len(seg_list_anger), seg_list_anger[k])
#                         for k in range(len(seg_list_anger)):
#                             seg_list_anger_temp = ""
#                             if k + 1 != len(seg_list_anger):
#                                 seg_list_anger_temp += seg_list_anger[k]
#                                 seg_list_anger_temp += seg_list_anger[k + 1]
#                                 seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
#                             else:
#                                 seg_list_anger_temp += seg_list_anger[0]
#                                 seg_list_anger_temp += seg_list_anger[k]
#                                 seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
#                             if len(seg_anger_temp) != len(seg_list_anger) * 2 - 1:
#                                 seg_anger_temp.insert(len(seg_anger_temp), "、")

#             seg_list_ = seg_list_list[i]
#             seg_list_front = seg_list_[:seg_list_.index(seg_list_having_0(side, seg_list_))]
#             seg_list_behind = seg_list_[seg_list_.index(seg_list_having_0(side, seg_list_)) + 1:]
#             seg_list_front.extend(",")
#             seg_list_front.extend(seg_anger_temp)
#             seg_list_front.extend(seg_list_behind)
#             seg_list_list[i] = seg_list_front
#     seg_list_t = []
#     for i in range(len(seg_list_list)):
#         seg_list_t.extend(seg_list_list[i])
#         seg_list_t.extend(",")
#     return seg_list_t


# def conversion_symbols(seg_list):  # 将图形转换为汉字
#     for i in range(len(seg_list)):
#         temp = seg_list[i]
#         if seg_list[i] in ["Rt", "rt"] and seg_list[i + 1] in ["△", "三角形"]:
#             temp = "".join("直角")
#         elif seg_list[i] in ["Rt△", "rt△"]:
#             temp = "".join("直角三角形")
#         elif seg_list[i] in ["▱", "▰"]:
#             temp = "".join("平行四边形")
#         elif seg_list[i] in ["▭", "▯", "▮"]:
#             temp = "".join("长方形")
#         elif seg_list[i] in ["□", "■", "▪", "▫", "◻", "◼", "◽", "◾"]:
#             temp = "".join("正方形")
#         elif seg_list[i] in ["◇", "◆"]:
#             temp = "".join("菱形")
#         elif seg_list[i] in ["⊿"]:
#             temp = "".join("直角三角形")
#         elif seg_list[i] in ["！"]:
#             temp = "".join("!")
#         elif seg_list[i] in ["＜"]:
#             temp = "".join("<")
#         elif seg_list[i] in ["＝"]:
#             temp = "".join("=")
#         elif seg_list[i] in ["≦", "≮"]:
#             temp = "".join("≤")
#         elif seg_list[i] in ["≧", "≯"]:
#             temp = "".join("≥")
#         elif seg_list[i] in ["△"]:
#             temp = "".join("三角形")
#         elif seg_list[i] in ["角"]:
#             temp = "".join("∠")
#         elif seg_list[i] in ["等腰直角梯形"]:
#             temp = "".join("长方形")
#         elif seg_list[i] in ["等于"]:
#             temp = "".join("=")
#         elif seg_list[i] in ["度"] and if_number(seg_list[i - 1]):
#             temp = "".join("°")
#         elif seg_list[i] in ["正三角形"]:
#             temp = "".join("等边三角形")
#         elif seg_list[i] in ["想交"]:
#             temp = "".join("相交")
#         elif seg_list[i] in ["想交于"]:
#             temp = "".join("相交于")
#         elif seg_list[i] in ["重点"]:
#             temp = "".join("中点")
#         elif seg_list[i] in ["均"]:
#             temp = "".join("都")
#         elif seg_list[i] in ["各"]:
#             temp = "".join("分别")
#         elif seg_list[i] in ["读"]:
#             temp = "".join("°")
#         elif seg_list[i] in ["∥", "平行于"]:
#             temp = "".join("//")
#         elif seg_list[i] in ["已知", "使得", "使", "且有", "并且", "满足", "且", "截取", "∶", "：", "，", "。", "；", "?",
#                              "？", "(",
#                              ")", "（", "）", ";"]:
#             # 将毫无意义的词组删去 将中文符号修改为英文的逗号
#             temp = "".join(",")
#         elif seg_list[i] in ["μm"]:
#             temp = "".join("微米")
#         elif seg_list[i] in ["nm"]:
#             temp = "".join("纳米")
#         elif seg_list[i] in ["mm"]:
#             temp = "".join("毫米")
#         elif seg_list[i] in ["cm"]:
#             temp = "".join("厘米")
#         elif seg_list[i] in ["dm"]:
#             temp = "".join("分米")
#         elif seg_list[i] in ["km"]:
#             temp = "".join("千米")
#         elif seg_list[i] in ["m"]:
#             temp = "".join("米")
#         seg_list[i] = temp
#     return seg_list


# # 将角和三角形等的字母大写
# def transition_litter_to_super(seg_list):
#     for i in range(len(seg_list)):
#         if if_letter(seg_list[i]) and len(seg_list[i]) > 2 and (
#                 seg_list[i - 1] in "∠" or seg_list[i - 1] in map_clear_up_keywords):
#             seg_list_letter = str(seg_list[i])
#             seg_list_letter = seg_list_letter.upper()
#             seg_list[i] = seg_list_letter
#     return seg_list


# # 补全交的符号
# def seg_list_complement(seg_list):
#     seg_list_list_temp = []  # 记录三角形的个数
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         # 查询所有的三角形以上的图形，并且合并同类项
#         if seg_list_having_0(map_clear_up_keywords, seg_list_list[i]):
#             seg_list_list_i_1 = seg_list_list[i].index(seg_list_having_0(map_clear_up_keywords, seg_list_list[i]))
#             if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
#                     seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) > 2 and \
#                     seg_list_list[i][seg_list_list_i_1 + 1] not in seg_list_list_temp:
#                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][seg_list_list_i_1 + 1])
#     if len(seg_list_list_temp) == 0:
#         return seg_list  # 无三角形等图形，无法进行识别 补全
#     else:
#         for i in range(len(seg_list_list)):
#             if "∠" in seg_list_list[i]:  # 如果存在∠且∠后的字母长度为1
#                 seg_list_list_i_1 = seg_list_list[i].index("∠")
#                 if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
#                         seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) == 1:
#                     angele_if_in_two_symbol = 0  # 判断是否存在多个图形里面
#                     angele_in_this_symbol = 0  # 记录当前字母所在的图形的下标
#                     for j in range(len(seg_list_list_temp)):
#                         if seg_list_list[i][seg_list_list_i_1 + 1] in seg_list_list_temp[j]:
#                             if angele_if_in_two_symbol != 0:
#                                 angele_if_in_two_symbol += 1
#                                 break  # 如果同时出现在多个图形中也无法 补全
#                             else:
#                                 angele_if_in_two_symbol += 1
#                                 angele_in_this_symbol = j
#                     if angele_if_in_two_symbol != 1:  # 可能出现角不在前面出现的图形中，也无法处理
#                         continue
#                     else:
#                         tran_angle = ""
#                         letter = re.findall('[A-Za-z]', seg_list_list_temp[angele_in_this_symbol])
#                         if seg_list_list[i][seg_list_list_i_1 + 1] in letter:
#                             if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1 < 0:  # 最前面
#                                 tran_angle += letter[len(letter) - 1]
#                             else:
#                                 tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1]
#                             tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1])]
#                             if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1 >= len(letter):  # 最后面
#                                 tran_angle += letter[0]
#                             else:
#                                 tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1]
#                         seg_list_list[i][seg_list_list_i_1 + 1] = tran_angle
#     return return_seg_list(seg_list_list)


# # lAB = 5 --转变---> 边AB = 5 暂时不知道有什么用
# def seg_list_transition_side(seg_list):
#     seg_list_temp = 0
#     while seg_list_temp == 0:
#         for i in range(len(seg_list)):
#             if len(seg_list[i]) == 3 and if_letter(seg_list[i]) and seg_list[i][0] == "l":  # lAB
#                 seg_list_behind = seg_list[i][1:]  # AB
#                 seg_list[i] = seg_list_behind
#                 seg_list_front = seg_list[:i]
#                 seg_list_behind = seg_list[i:]
#                 seg_list_front.extend("边")
#                 seg_list_front.extend(seg_list_behind)
#                 seg_list = seg_list_front
#                 break
#             if i + 1 == len(seg_list):
#                 seg_list_temp += 1
#     # print("".join(seg_list))
#     return seg_list


# # 去除序号
# def remove_pause(seg_list):
#     for i in range(len(seg_list) - 1):
#         if seg_list[i] == "、" and if_number(seg_list[i - 1]) and i <= 2:
#             seg_list1 = seg_list[i + 1:]
#             return seg_list1
#     return seg_list


# # 删除求证
# def delete_prove(seg_list):
#     seg_list_front = []
#     seg_txt = ["证明", "求解", "求证", "求", "有", "如图", "如图所示"]
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if seg_list_having(seg_txt, seg_list_list[i]):
#             seg_list_list_wei = seg_list_having_0(seg_txt, seg_list_list[i])
#             seg_list_front = seg_list_list[i][:seg_list_list[i].index(seg_list_list_wei)]
#             seg_list_front.extend(",")
#             if seg_list_list[i].index(seg_list_list_wei) + 1 < len(seg_list_list[i]) and \
#                     if_number(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1]):
#                 seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 2:])
#             else:
#                 seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1:])
#             seg_list_list[i] = seg_list_front
#     return return_seg_list(seg_list_list)


# # 将大于或者小于或者不等于归一化   <=  --->  ≤
# def handles_greater_or_less(seg_list):
#     seg_temp = 0
#     while seg_temp == 0:
#         for i in range(len(seg_list)):
#             if seg_list[i] in ["<", ">", "!"] and i + 1 < len(seg_list) and seg_list[i + 1] in "=":
#                 seg_list_front = seg_list[:i]
#                 seg_list_behind = seg_list[i + 2:]
#                 if seg_list[i] in "<":
#                     seg_list_front.insert(len(seg_list_front), "≤")
#                 elif seg_list[i] in ">":
#                     seg_list_front.insert(len(seg_list_front), "≥")
#                 elif seg_list[i] in "!":
#                     seg_list_front.insert(len(seg_list_front), "!=")
#                 seg_list_front.extend(seg_list_behind)
#                 seg_list = seg_list_front
#                 break
#             if i + 1 == len(seg_list):
#                 seg_temp = 1
#     return seg_list


# # 给末尾加上;
# def add_end_punctuation(seg_list):
#     for i in range(len(seg_list)):
#         if seg_list[len(seg_list) - 1 - i] in [".", ",", ";", "?", "？"] and \
#                 seg_list[len(seg_list) - 2 - i] in [".", ",", ";", "?", "？"]:
#             continue
#         else:
#             seg_list = seg_list[:len(seg_list) - 1 - i]
#             seg_list.append(";")
#             return seg_list
#     return seg_list


# # 按照逗号或者句号分句
# def cut_clause(seg_list):
#     for i in range(len(seg_list) - 1):
#         if seg_list[i] in [",", ".", "，", "。"]:
#             seg_list1 = seg_list[
#                         i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ['.', ','] else len(seg_list)]
#             seg_list2 = seg_list[:i]
#             return seg_list2, seg_list1
#     return seg_list, ""


# # 对顿号进行切割
# def cut_clause_slight_pause(seg_list):
#     for i in range(len(seg_list) - 1):
#         if seg_list[i] in ["、", "和", "与", "."]:
#             seg_list1 = seg_list[
#                         i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ["、", "和", "与", "."] else len(
#                             seg_list)]
#             seg_list2 = seg_list[:i]
#             return seg_list2, seg_list1
#     return seg_list, ""


# # 给长宽高边长面积周长前适当加"的"
# def add_de_to_side(seg_list):
#     seg_temp = 0
#     while seg_temp == 0:
#         for i in range(len(seg_list)):
#             if seg_list[i] in ["长", "宽", "高", "边长", "周长", "面积"]:
#                 if i == 0 or seg_list[i - 1] in [",", "."] or seg_list[i - 1] in ["的"] or seg_list[i - 1] in ["是"]:
#                     continue
#                 elif i > 1 and if_letter(seg_list[i - 1]) and len(seg_list[i - 1]) > 1:  # ABC长AD为
#                     seg_list_front = seg_list[:i]
#                     seg_list_front.insert(i, "的")
#                     seg_list_front.extend(seg_list[i:])
#                     seg_list = seg_list_front
#                     break
#                 elif i > 2 and (seg_list[i - 1] in ["中"] and if_letter(seg_list[i - 2])) and len(seg_list[i - 2]) > 1:
#                     seg_list_front = seg_list[:i]
#                     seg_list_front.insert(i, "的")
#                     seg_list_front.extend(seg_list[i:])
#                     seg_list = seg_list_front
#                     break
#             if i + 1 == len(seg_list):
#                 seg_temp = 1
#     # print(seg_list)
#     return seg_list


# # 将作从（过A 作AS垂直于DF)提取出来
# def cut_zuo_from_seg_list(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if seg_list_having(symbol_keywords_main, seg_list_list[i]) and "作" in seg_list_list[i]:
#             seg_list_front = seg_list_list[i][
#                              :seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i]))]  # 垂直之前
#             seg_list_behind = seg_list_list[i][
#                               seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i])):]  # 垂直之后
#             seg_list_front_behind = seg_list_front[seg_list_front.index("作"):]  # 作之后，找后面的一个词组
#             seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)  # 找到词组
#             seg_list_front.extend(",")  # 过A 作AS，
#             seg_list_front.insert(len(seg_list_front), seg_list_front_behind_letter[0][1])  # 过A 作AS，AS
#             seg_list_front.extend(seg_list_behind)  # 过A 作AS，AS垂直DF
#             seg_list_list_front = seg_list_list[:i]
#             seg_list_list_behind = seg_list_list[i + 1:]
#             seg_list_list_front.insert(len(seg_list_list_front), seg_list_front)
#             seg_list_list_front.extend(seg_list_list_behind)
#             seg_list_list = seg_list_list_front
#     seg_list = []
#     for i in range(len(seg_list_list)):
#         seg_list.extend(seg_list_list[i])
#         seg_list.extend(",")
#     # print("".join(seg_list))
#     return seg_list


# # 将垂直后加一个逗号切分
# def add_comma_at_equal(seg_list):
#     seg_list_temp = 0
#     while seg_list_temp == 0:
#         for i in range(len(seg_list)):
#             if i + 1 == len(seg_list):
#                 seg_list_temp = 1
#             if seg_list[i] in symbol_keywords_main:
#                 for j in range(1, 3):
#                     if i + j > len(seg_list):
#                         break
#                     if seg_list[i + j] not in map_clear_up_keywords and seg_list[
#                         i + j] not in symbol_keywords and not if_number_and_letter(seg_list[i + j]) and seg_list[
#                         i + j] not in ["于", "点"]:

#                         if seg_list[i + j] != ",":
#                             seg_list_front = seg_list[:i + j]
#                             seg_list_behind = seg_list[i + j:]
#                             seg_list_front.extend(",")
#                             seg_list_front.extend(seg_list_behind)
#                             seg_list_temp1 = 1
#                             seg_list = seg_list_front
#                             break
#                         else:
#                             break
#     return seg_list


# # 根据输入不同的symbol进行类似连等的分割
# def find_which_equal(seg_list, symbol):
#     equal_value = []  # 存储当前段落的所有的等式的元素
#     seg_list1_front = []
#     seg_list2_front = []
#     seg_list2_behind = []
#     seg_list_behind_behind_letter = []
#     seg_list_behind_behind_other = []
#     seg_list_front_front_other = []
#     seg_list_front_behind_other = []
#     seg_list1 = seg_list[:seg_list.index(symbol)]
#     # 梯形ABCD的面积=EF·AB
#     if len(seg_list1) > 2:
#         if "作" in seg_list:  # 作三角形ABC的AD垂直CV
#             seg_list1_front = seg_list1[:seg_list1.index("作")]
#             seg_list1_behind = seg_list1[seg_list1.index("作"):]
#             if "的" in seg_list1_behind:
#                 seg_list_behind_front = seg_list1_behind[:seg_list1_behind.index("的")]
#                 seg_list1_behind_behind = seg_list1_behind[seg_list1_behind.index("的"):]
#                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
#                 if len(seg_list_behind_behind_letter) == 0:
#                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#                 seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
#             else:
#                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind)
#                 seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
#         elif "的" in seg_list1:
#             seg_list_behind_front = seg_list1[:seg_list1.index("的")]
#             seg_list1_behind_behind = seg_list1[seg_list1.index("的"):]
#             seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
#             if len(seg_list_behind_behind_letter) == 0:
#                 seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#             seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
#         else:
#             seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1)
#             seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
#         seg_list_front_front_other = seg_list_behind_behind_other[0]  # 存储前半部分的其他部分
#         seg_list_front_behind_other = seg_list_behind_behind_other[1]  # 存储字母后半部分的其他部分
#     seg_list2 = seg_list[seg_list.index(symbol) + 1:]
#     if len(seg_list_behind_behind_letter) > 0:
#         equal_value.append(dispose_cut_front_equal(seg_list_behind_behind_letter[0][1]))  # 处理等号前半段
#     else:
#         equal_value.append(dispose_cut_front_equal(seg_list1))
#     while symbol in seg_list2:
#         seg_list0 = seg_list2.copy()
#         seg_list1 = seg_list0[:seg_list0.index(symbol)]  # 等号前半段
#         seg_list2 = seg_list0[seg_list0.index(symbol) + 1:]  # 取等号后半段
#         equal_value.append(dispose_cut_front_equal(seg_list1))  # 处理等号前半段
#     if len(seg_list2) > 1:  # 过D作DE⊥BC于E
#         for i in range(len(seg_list2)):
#             if if_number_and_letter(seg_list2[i]):
#                 seg_list2_letter = seg_list2[i]
#                 seg_list2_front = seg_list2[:i]
#                 seg_list2_behind = seg_list2[i + 1:]
#                 seg_list2 = seg_list2_letter
#                 break

#     equal_value.append(dispose_cut_front_equal(seg_list2))  # 处理等号后半段
#     equal_value_all = []
#     for i in range(len(equal_value) - 1):
#         j = i + 1
#         while j < len(equal_value):
#             equal_value_all.extend(seg_list_front_front_other)
#             equal_value_all.extend(equal_value[i])
#             equal_value_all.extend(seg_list_front_behind_other)
#             equal_value_all.append(symbol)
#             if j + 1 == len(equal_value):
#                 equal_value_all.extend(seg_list2_front)
#             equal_value_all.extend(equal_value[j])
#             if j + 1 == len(equal_value):
#                 equal_value_all.extend(seg_list2_behind)
#             equal_value_all.append(",")
#             j += 1
#     return equal_value_all


# # 处理使用等号分出来的前半段,存在角\边\点种情况
# def dispose_cut_front_equal(seg_list1):
#     Str_value = [""]
#     for i in range(len(seg_list1)):
#         if seg_list1[i] in symbol_keywords or if_number_and_letter(seg_list1[i]) or seg_list1[i] \
#                 in map_clear_up_keywords:
#             if if_letter(seg_list1[i]) and if_letter(Str_value[len(Str_value) - 1]) and len(Str_value) > 0:
#                 Str_value[len(Str_value) - 1] += (seg_list1[i])
#             else:
#                 Str_value.append(seg_list1[i])
#     Str_value = delete_blank(Str_value)
#     return Str_value


# # 提取当前段落的所有英文字母
# def dispose_cut_front_equal_letter(seg_list1):
#     Str_value = [""]
#     for i in range(len(seg_list1)):
#         if if_letter(seg_list1[i]):
#             Str_value.append(seg_list1[i])
#     Str_value_true = "".join(Str_value)
#     return Str_value_true


# # 查询当前符号symbol是否在语句seg_list中
# def seg_list_having(symbol, seg_list):
#     if len(seg_list) == 0:
#         return False
#     for i in range(len(symbol)):
#         if symbol[i] in seg_list:
#             return symbol[i]
#     return False


# # 查看字符symbol是否有任意一个在字符串中,如果没有返回空字符,否则存在字符.
# def seg_list_having_0(symbol, seg_list):
#     if len(seg_list) == 0:
#         return ""
#     for i in range(len(symbol)):
#         if symbol[i] in seg_list:
#             return symbol[i]
#     return ""


# # seg_list[][]中有一点在symbol中的一个值
# def seg_list_having_1(symbol, seg_list):
#     if len(seg_list) == 0:
#         return False
#     for i in range(len(seg_list)):
#         for j in range(len(seg_list[i])):
#             if seg_list[i][j] in symbol:
#                 return True
#     return False


# # symbol与seg_list[][]中存在很小一点的相等
# def seg_list_having_2(symbol, seg_list):
#     if len(seg_list) == 0:
#         return False
#     for i in range(len(symbol)):
#         for j in range(len(seg_list)):
#             for k in range(len(seg_list[j])):
#                 if symbol[i] == seg_list[j][k]:
#                     return True
#     return False


# def seg_list_having_all(symbol, seg_list):
#     if len(seg_list) == 0:
#         return False
#     for i in range(len(symbol)):
#         if symbol[i] in seg_list:
#             continue
#         else:
#             return False
#     return True


# # 在处理分别中的辅助函数,查看b-b-l的低2列是否是数字
# def seg_list_behind_behind_letter_if_letter(seg_letter):
#     for i in range(len(seg_letter)):
#         if not if_number(seg_letter[i][1]):
#             break
#         if i + 1 == len(seg_letter):
#             return True
#     return False


# # 判断是几边形的图形
# def match_how_many_side(seg_list):
#     len_seg_list = len(seg_list)
#     if len_seg_list == 1:
#         return "点"
#     elif len_seg_list == 2:
#         return "边"
#     elif len_seg_list == 3:
#         return "三角形"
#     elif len_seg_list == 4:
#         return "四边形"
#     elif len_seg_list == 5:
#         return "五边形"
#     elif len_seg_list == 6:
#         return "六边形"
#     else:
#         return "多边形"


# # 返回两个三角形的边数
# def return_how_many_side_symbol(symbol1, symbol2):
#     triangle = ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形"]
#     quadrangle = ["四边形", "矩形", "正方形", "长方形", "平行四边形", "梯形", "等腰梯形", "直角梯形", "菱形"]
#     polygon = ["五边形", "六边形", "七边形", "多边形", "凸多边形"]
#     symbol1_angle = 0
#     symbol2_angle = 0
#     if symbol1 in triangle:
#         symbol1_angle = 3
#     elif symbol1 in quadrangle:
#         symbol1_angle = 4
#     else:
#         symbol1_angle = 10
#     if symbol2 in triangle:
#         symbol2_angle = 3
#     elif symbol2 in quadrangle:
#         symbol2_angle = 4
#     else:
#         symbol2_angle = 10
#     return symbol1_angle, symbol2_angle


# def return_how_many_side(symbol1):
#     side = ["三边", "四边", "五边", "六边", "七边"]
#     symbol1_angle = 0
#     symbol2_angle = 0
#     if symbol1 in "三边":
#         symbol1_angle = 3
#     elif symbol1 in "四边":
#         symbol1_angle = 4
#     elif symbol1 in "五边":
#         symbol1_angle = 5
#     elif symbol1 in "六边":
#         symbol1_angle = 6
#     elif symbol1 in "七边":
#         symbol1_angle = 7
#     else:
#         symbol1_angle = 10

#     return symbol1_angle


# def return_how_many_number(symbol, the_capital_form_of_a_chinese_number):
#     return the_capital_form_of_a_chinese_number.index(symbol) + 1


# # 查询当前语句是否存在形状,并且形状位置在字母前面
# def seg_list_having_symbol_letter(symbol, seg_list, letter):
#     for i in range(len(seg_list)):
#         if seg_list[i] in symbol and i + 1 == seg_list.index(letter):
#             return symbol[symbol.index(seg_list[i])]
#     return ""


# # 特征值判断是否存在平行且相等的情况
# def find_if_have_parallel_and_equal(seg_list):
#     Str = [""]
#     if "平行且相等" in seg_list:
#         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
#         while seg_list1 != "":
#             if "平行且相等" in seg_list1:  # 如果平行且相等在当前分句里面
#                 seg_list00 = seg_list1.copy()
#                 seg_list01 = seg_list00[:seg_list00.index("平行且相等")]
#                 seg_list02 = seg_list00[seg_list00.index("平行且相等") + 1:]
#                 seg_list_value_front = dispose_cut_front_equal_letter(seg_list01)
#                 seg_list_value_behind = dispose_cut_front_equal_letter(seg_list02)
#                 seg_list1 = [seg_list_value_front, "//", seg_list_value_behind, ",", seg_list_value_front, "=",
#                              seg_list_value_behind, ","]
#             Str.extend(seg_list1)
#             Str.extend(",")
#             if "平行且相等" not in seg_list2:
#                 Str.extend(seg_list2)
#                 return Str
#             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
#     return seg_list


# # 对字母进行形状配对,当形状在前面时
# def add_all_shape_at_front(seg_list):
#     len_seg_list = len(seg_list)
#     Str = []
#     seg_list_temp_overall = []
#     seg_list_temp_front = []
#     type_temp = []  # 储存形状
#     type_value = []  # 储存字母
#     if seg_list_having("、", seg_list):
#         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
#         while seg_list1 != "":
#             if seg_list_having("、", seg_list1) and len(seg_list1[seg_list1.index("、") - 1]) > 2:  # 顿号前的字母长度大于三才处理
#                 seg_list10, seg_list11 = cut_clause_slight_pause(seg_list1)  # 按照顿号进行切割           #可能出现三个字母的代码,露马脚了

#                 while seg_list10 != "":
#                     type_value.insert(len(type_value), dispose_cut_front_equal_letter(seg_list10))  # 提取英文字母
#                     type_temp.insert(len(type_temp), seg_list_having_symbol_letter(map_clear_up_keywords, seg_list10,
#                                                                                    dispose_cut_front_equal_letter(
#                                                                                        seg_list10)))  # 提取字母类型
#                     seg_list10, seg_list11 = cut_clause_slight_pause(seg_list11)  # 按照顿号进行切割
#                 if len(type_temp[0]) > 0:  # 有标签的情况下
#                     seg_list_temp_front = seg_list1[:seg_list1.index(type_value[0]) - 1]
#                     seg_list_temp_behind = seg_list1[seg_list1.index(type_value[len(type_value) - 1]) + 1:]
#                     for i in range(len(type_temp)):
#                         if len(type_temp[i]) > 0:
#                             seg_list_temp_front.insert(len(seg_list_temp_front),
#                                                        find_the_max_symbol(type_temp[0], type_temp[i], type_value[i]))
#                         else:
#                             seg_list_temp_front.insert(len(seg_list_temp_front), type_temp[0])
#                         seg_list_temp_front.insert(len(seg_list_temp_front), type_value[i])
#                         if i < len(type_temp) - 1:
#                             seg_list_temp_front.insert(len(seg_list_temp_front), "、")
#                     seg_list_temp_front.extend(seg_list_temp_behind)  # 将三角形ABC、DEF、GHZ,拼接
#                     # print(seg_list_temp_front)
#             if len(seg_list_temp_front) > 0:
#                 seg_list_temp_overall.extend(seg_list_temp_front)
#                 seg_list_temp_front = []
#             else:
#                 seg_list_temp_overall.extend(seg_list1)
#             seg_list_temp_overall.extend(",")
#             # print(dispose_cut_front_equal_letter(seg_list1))
#             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
#         # print("seg_list_temp_overall",seg_list_temp_overall)
#         # print("".join(seg_list_temp_overall))
#         return seg_list_temp_overall
#     return seg_list


# # 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH
# def add_all_shape_at_behind(seg_list):
#     Str = []
#     seg_list_temp = []
#     type_temp = []
#     type_value = []
#     if seg_list_having(["均为", "都"], seg_list):
#         seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
#         while seg_list1 != "":
#             if seg_list_having(["均为", "都"], seg_list1):
#                 seg_list_symbol_1 = seg_list_having(["均为", "都"], seg_list1)
#                 seg_list00 = seg_list1[:seg_list1.index(seg_list_symbol_1)]  # 提取"都"前面的句子进入循环
#                 seg_list20 = seg_list1[seg_list1.index(seg_list_symbol_1) + 1:]  # 提取都后面的句子
#                 seg_list_symbol_behind = seg_list_having(map_clear_up_keywords, seg_list20)  # 提出"均为"后的图形
#                 seg_list_letter20 = dispose_cut_front_equal_letter(seg_list20)  # 查看图形后面是否跟着字母
#                 seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list00)
#                 while seg_list1_0 != "":
#                     seg_list_symbol_front = seg_list_having_0(map_clear_up_keywords, seg_list1_0)  # 提出第一个图形的类型
#                     type_temp.insert(len(type_temp), seg_list_symbol_front)
#                     seg_list_letter10 = dispose_cut_front_equal_letter(seg_list1_0)
#                     type_value.insert(len(type_value), seg_list_letter10)
#                     seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list1_1)
#                 for i in range(len(type_temp)):
#                     Str.insert(len(Str), type_temp[i])
#                     Str.insert(len(Str), type_value[i])
#                     Str.insert(len(Str), "是")
#                     Str.insert(len(Str), seg_list_symbol_behind)
#                     Str.insert(len(Str), seg_list_letter20)
#                     Str.insert(len(Str), ",")
#                 seg_list_temp.extend(Str)
#             else:
#                 seg_list_temp.extend(seg_list1)
#                 seg_list_temp.extend(",")
#             seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照顿号与"与"分段
#         return seg_list_temp
#     else:
#         return seg_list


# def add_all_letter(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     temp = []
#     for i in range(len(seg_list_list)):
#         for j in range(len(seg_list_list[i])):
#             if if_letter(seg_list_list[i][j]) and len(seg_list_list[i][j]) > 2 and seg_list_list[i][j - 1] != "∠":
#                 temp.insert(len(temp), seg_list_list[i][j])
#             if seg_list_list[i][j] in ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形",
#                                        "矩形", "正方形", "长方形", "平行四边形",
#                                        "梯形", "等腰梯形", "直角梯形", "菱形"] and j + 1 < len(seg_list_list[i]) and \
#                     not if_letter(seg_list_list[i][j + 1]):
#                 if seg_list_having_2("三", seg_list_list[i][j]):
#                     for k in range(len(temp)):
#                         if len(temp[len(temp) - 1 - k]) == 3:
#                             seg_list_list_temp = seg_list_list[i][:j + 1]
#                             seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
#                             seg_list_list_temp.extend(seg_list_list[i][j + 1:])
#                             seg_list_list[i] = seg_list_list_temp
#                             break
#                 else:
#                     for k in range(len(temp)):
#                         if len(temp[len(temp) - 1 - k]) > 3:
#                             seg_list_list_temp = seg_list_list[i][:j + 1]
#                             seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
#                             seg_list_list_temp.extend(seg_list_list[i][j + 1:])
#                             seg_list_list[i] = seg_list_list_temp
#                             break
#                 break
#     return return_seg_list(seg_list_list)


# # 对其余的所有的多个连续字母进行基础形状赋值
# def add_all_shape(seg_list):
#     seg_list_if = 0
#     while seg_list_if == 0:
#         seg_list_temp = []
#         for i in range(len(seg_list)):
#             if if_letter(seg_list[i]) and len(seg_list[i]) > 2:
#                 seg_list_front = seg_list[:i]
#                 seg_list_behind = seg_list[i + 1:]
#                 if len(seg_list_front) == 0:  # ABC打头
#                     seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
#                     seg_list_temp.insert(len(seg_list_temp), seg_list[i])
#                     seg_list_temp.extend(seg_list_behind)
#                     seg_list = seg_list_temp
#                     seg_list_temp = []
#                     break
#                 else:
#                     if seg_list[i - 1] in map_clear_up_keywords or seg_list[i - 1] == "∠":  # 字母前面有形状或者有角
#                         continue
#                     else:
#                         seg_list_temp.extend(seg_list_front)
#                         seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
#                         seg_list_temp.insert(len(seg_list_temp), seg_list[i])
#                         seg_list_temp.extend(seg_list_behind)
#                         seg_list = seg_list_temp
#                         seg_list_temp = []
#                         break

#             if i == len(seg_list) - 1:
#                 seg_list_if = 1
#     return seg_list


# # 输出两个图形的权值的最大一个形状
# def find_the_max_symbol(symbol1, symbol2):
#     x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
#     x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
#     y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
#     y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
#     if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
#         return ""
#     elif (y1 + y2) in map_clear_up_keywords_value:
#         seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
#         return seg_list_temp
#     else:
#         if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
#             return symbol1
#         else:
#             return symbol2


# # 形状 形状 ABC ,如果前两个的图形的边相等,所以判断谁的权值大,否则,就有一个图形是错误的,需要舍弃,如果都错误,那么给予ABC基础图形
# def find_the_max_symbol(symbol1, symbol2, seg_list):
#     symbol1_angle, symbol2_angle = return_how_many_side_symbol(symbol1, symbol2)
#     if symbol1_angle == symbol2_angle:
#         x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
#         x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
#         y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
#         y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
#         if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
#             return ""
#         elif (y1 + y2) in map_clear_up_keywords_value:
#             seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
#             return seg_list_temp
#         else:
#             if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
#                 return symbol1
#             else:
#                 return symbol2
#     else:
#         if len(seg_list) == symbol1_angle:
#             return symbol1
#         elif len(seg_list) == symbol2_angle:
#             return symbol2
#         else:
#             return match_how_many_side(seg_list)


# # 除去重复的形状
# def delete_repetition_symbol(seg_list):
#     seg_temp = 0

#     while seg_temp == 0:
#         for i in range(len(seg_list)):
#             if seg_list[i] in map_clear_up_keywords and i + 1 < len(seg_list) and \
#                     seg_list[i + 1] in map_clear_up_keywords:  # 当前形状和下一个值都是形状
#                 seg_list_front = seg_list[:i]
#                 seg_list_behind = seg_list[i + 2:]
#                 seg_list_front.insert(len(seg_list_front), find_the_max_symbol(seg_list[i], seg_list[i + 1]))
#                 seg_list_front.extend(seg_list_behind)
#                 seg_list = seg_list_front
#                 break
#             if i + 1 == len(seg_list):
#                 seg_temp = 1
#     return seg_list


# # 处理四边形ABCD是正方形的情况
# def dispose_shi_and_symbol(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         for j in range(len(seg_list_list[i])):
#             if seg_list_list[i][j] in map_clear_up_keywords and j + 1 < len(seg_list_list[i]) and if_letter(
#                     seg_list_list[i][j + 1]):  # 四边形abcd
#                 subject = seg_list_list[i][j]  # 当前主语为abcd
#                 if j + 3 < len(seg_list_list[i]) and seg_list_list[i][j + 2] in ["是", "为"] and \
#                         seg_list_list[i][j + 3] in map_clear_up_keywords:  # 特殊值判断 四边形ABCD为长方形
#                     seg_list_list_front = seg_list_list[i][:j]
#                     seg_list_list_behind = seg_list_list[i][j + 4:]
#                     seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
#                     seg_list_list_front.insert(len(seg_list_list_front),
#                                                find_the_max_symbol(seg_list_list[i][j], seg_list_list[i][j + 3],
#                                                                    seg_list_list[i][j + 1]))
#                     seg_list_list_front.insert(len(seg_list_list_front), seg_list_list[i][j + 1])
#                     if len(seg_list_list_behind_letter) == 1 and seg_list_list_behind_letter[0][1] != seg_list_list[i][
#                         j + 1]:
#                         seg_list_list_front.extend(seg_list_list_behind)
#                     seg_list_list[i] = seg_list_list_front
#                     break
#     seg_list = []
#     for i in range(len(seg_list_list)):
#         seg_list.extend(seg_list_list[i])
#         seg_list.extend(",")
#     # print("^&*","".join(seg_list))
#     return seg_list


# # 删去多余的逗号
# def delete_unnecessary_comma(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if len(seg_list_list[i]) > 0 and seg_list_list[i][0] == ":":
#             seg_list_list[i] = seg_list_list[i][1:]
#     seg_list = return_seg_list(seg_list_list)
#     seg_list_temp = 0
#     while seg_list_temp == 0:
#         if len(seg_list) == 0:
#             break
#         for i in range(len(seg_list)):
#             if seg_list[i] == "," and i == 0:
#                 seg_list = seg_list[1:]
#                 break
#             if seg_list[i] == "," and i + 2 < len(seg_list) and seg_list[i + 1] in [",", ".", "\n", "、", ";", "∶", "?",
#                                                                                     "？"]:
#                 seg_list_front = seg_list[:i]
#                 seg_list_behind = seg_list[i + 2:]
#                 seg_list_front.extend(",")
#                 seg_list_front.extend(seg_list_behind)
#                 seg_list = seg_list_front
#                 break
#             if seg_list[i] == "," and i - 1 > 0 and seg_list[i - 1] in [",", ".", "\n", "、", ";"]:
#                 seg_list_front = seg_list[:i - 1]
#                 seg_list_behind = seg_list[i:]
#                 seg_list_front.extend(seg_list_behind)
#                 seg_list = seg_list_front
#                 break
#             if i + 1 == len(seg_list):
#                 seg_list_temp = 1
#     return seg_list


# def add_to_the_vertical(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if "垂足" in seg_list_list[i]:
#             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             if len(seg_list_letter) == 1 and seg_list_letter[0][0] == 1:
#                 seg_list_list[i - 1].extend("于")
#                 seg_list_list[i - 1].extend(seg_list_letter[0][1])
#                 seg_list_list[i] = ""
#             else:
#                 for j in range(len(seg_list_letter)):
#                     seg_list_list[i - j - 1].extend("于")
#                     seg_list_list[i - j - 1].extend(seg_list_letter[len(seg_list_letter) - 1 - j][1])
#                 seg_list_list[i] = ""
#     seg_list = []
#     for i in range(len(seg_list_list)):
#         seg_list.extend(seg_list_list[i])
#         seg_list.extend(",")
#     # print("^&*","".join(seg_list))
#     return seg_list


# # 查找当前句子的所有英文词组,返回边大小和词组
# def find_all_letter_return_side_letter(seg_list):
#     list_letter = []
#     for i in range(len(seg_list)):
#         list_letter_seg = []
#         if if_letter(seg_list[i]) and seg_list[i].isupper():
#             list_letter_seg.insert(len(list_letter_seg), len(seg_list[i]))
#             list_letter_seg.insert(len(list_letter_seg), seg_list[i])
#         # if seg_list[i] in symbol_keywords_main:
#         #     break
#         if len(list_letter_seg) > 0:
#             list_letter.append(list_letter_seg)
#     # print(list_letter)
#     return list_letter


# # 找到当前句子中除去字母,顿号的其他的所有字符串
# def find_front_and_behind_other(seg_list, symbol):
#     list_other = []
#     if len(symbol) == 0:
#         return seg_list
#     # if not "、" in seg_list  \n symbol[0][1] \n elif: \n seg_list.index("、") < seg_list.index(
#     #             symbol[0][1]) \n "、" \n else  symbol[0][1]
#     seg_list_front = seg_list[:seg_list.index(
#         symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
#         seg_list_having(["、", "和"], seg_list) if seg_list.index(
#             seg_list_having(["、", "和"], seg_list)) < seg_list.index(
#             symbol[0][1])
#         else symbol[0][1])]
#     seg_list_behind = seg_list[seg_list.index(
#         symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
#         seg_list_having(["、", "和"], seg_list) if seg_list.index(
#             seg_list_having(["、", "和"], seg_list)) > seg_list.index(
#             symbol[len(symbol) - 1][1]) else
#         symbol[len(symbol) - 1][1]) + 1:]
#     list_other.append(seg_list_front)
#     list_other.append(seg_list_behind)
#     # print(list_other)
#     return list_other


# def find_have_d_or_slight_pause(seg_list):
#     for i in range(len(seg_list)):
#         if if_letter(seg_list[i]) or seg_list[i] == "、":
#             return True
#     return False


# # 对交进行拼接
# def package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
#                         seg_list_front_behind_letter, seg_list_front_behind_other,
#                         seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
#                         seg_list_behind_behind_letter, seg_list_behind_behind_other, symbol):
#     seg_list_part = []
#     # print(seg_list_front_front_letter, end=" # ")
#     # print(seg_list_front_front_other)
#     # print(seg_list_front_behind_letter, end=" # ")
#     # print(seg_list_front_behind_other)
#     # print(seg_list_behind_front_letter, end=" # ")
#     # print(seg_list_behind_front_other)
#     # print(seg_list_behind_behind_letter, end=" # ")
#     # print(seg_list_behind_behind_other)
#     # 以下偷懒一点了，以后需要再进行更改吧
#     # 有0111和1011和0100和0201三种情况 BE的延长线交AC于点F ，DF交 ， 四边形ABCD的两条对角线AC、BD交于点E
#     # 存在1101和1111和1121三种情况
#     # 存在2001一种情况

#     # if len(seg_list_front_front_other) != 0 and (
#     #         len(seg_list_front_front_other[0]) != 0 or seg_list_having(symbol_keywords_main,
#     #                                                                    seg_list_front_front_other[1])):  # 清除前面的冗余句子
#     #     for i in range(len(seg_list_front_front_letter)):
#     #         seg_list_part.extend(seg_list_front_front_other[0])
#     #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[i][1])
#     #         if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
#     #             seg_list_part.extend(seg_list_front_front_other[1])
#     #         seg_list_part.extend(",")
#     #     seg_list_front_front_other[0] = []
#     #     if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
#     #         seg_list_front_front_other[1] = []
#     # if len(seg_list_front_behind_other) != 0 and (
#     #         len(seg_list_front_behind_other[0]) != 0 or seg_list_having(symbol_keywords_main,
#     #                                                                     seg_list_front_behind_other[1])):  # 清除后面的冗余句子
#     #     for i in range(len(seg_list_front_behind_letter)):
#     #         seg_list_part.extend(seg_list_front_behind_other[0])
#     #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
#     #         if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
#     #             seg_list_part.extend(seg_list_front_behind_other[1])
#     #         seg_list_part.extend(",")
#     #     seg_list_front_behind_other[0] = []
#     #     if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
#     #         seg_list_front_behind_other[1] = []

#     if len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#         seg_list_part.extend(seg_list_behind_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 0 and len(
#             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_part.extend(seg_list_front_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#         if "交" not in seg_list_front_front_other[1] and "分别" not in seg_list_front_front_other[1]:
#             seg_list_part.extend(seg_list_front_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#         seg_list_part.extend(seg_list_behind_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
#             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[1][1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 0:
#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_part.extend(seg_list_front_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#         seg_list_part.extend(seg_list_front_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
#         if seg_list_front_front_letter[0][0] == 1:
#             seg_list_part.extend(seg_list_front_front_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#             seg_list_part.extend(seg_list_front_front_other[1])
#             seg_list_part.insert(len(seg_list_part), "作")
#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#         seg_list_part.extend(seg_list_behind_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_front_front_letter_temp = 1
#         for i in range(2):
#             seg_list_part.extend(seg_list_front_front_other[0])
#             if seg_list_front_front_letter_temp == 1:
#                 seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#                 seg_list_front_front_letter_temp += 1
#             else:
#                 seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#             seg_list_part.extend(seg_list_front_front_other[1])
#             seg_list_part.insert(len(seg_list_part), "交")
#             seg_list_part.extend(seg_list_behind_front_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#             seg_list_part.extend(seg_list_behind_front_other[1])
#             seg_list_part.insert(len(seg_list_part), "于")
#             seg_list_part.extend(seg_list_behind_behind_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#             seg_list_part.extend(seg_list_behind_behind_other[1])
#             seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 2 and len(seg_list_front_behind_letter) == 0 and len(
#             seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
#         seg_list_part.extend(seg_list_front_front_other[1])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_front_front_other[1])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[1][1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
#             seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 2:
#         for i in range(2):
#             seg_list_part.extend(seg_list_front_behind_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
#             seg_list_part.extend(seg_list_front_behind_other[1])
#             seg_list_part.insert(len(seg_list_part), "交")
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#             seg_list_part.insert(len(seg_list_part), "于")
#             seg_list_part.extend(seg_list_behind_behind_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
#             seg_list_part.extend(seg_list_behind_behind_other[1])
#             seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
#         seg_list_part.extend(seg_list_front_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
#         seg_list_part.extend(seg_list_front_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
#         seg_list_part.extend(seg_list_behind_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")

#         seg_list_part.extend(seg_list_front_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#         seg_list_part.extend(seg_list_front_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), "交")
#         seg_list_part.extend(seg_list_behind_front_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
#         seg_list_part.extend(seg_list_behind_front_other[1])
#         seg_list_part.insert(len(seg_list_part), "于")
#         seg_list_part.extend(seg_list_behind_behind_other[0])
#         seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[1][1])
#         seg_list_part.extend(seg_list_behind_behind_other[1])
#         seg_list_part.insert(len(seg_list_part), ",")
#     elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
#             seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
#         for i in range(2):
#             seg_list_part.extend(seg_list_front_behind_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
#             seg_list_part.extend(seg_list_front_behind_other[1])
#             seg_list_part.insert(len(seg_list_part), "交")
#             seg_list_part.extend(seg_list_behind_front_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[i][1])
#             seg_list_part.extend(seg_list_behind_front_other[1])
#             seg_list_part.insert(len(seg_list_part), "于")
#             seg_list_part.extend(seg_list_behind_behind_other[0])
#             seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
#             seg_list_part.extend(seg_list_behind_behind_other[1])
#             seg_list_part.insert(len(seg_list_part), ",")
#     else:  # 其他非常规的默认输出
#         seg_list_part = package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
#                                      seg_list_front_behind_letter, seg_list_front_behind_other,
#                                      seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
#                                      seg_list_behind_behind_letter, seg_list_behind_behind_other)
#     # print("".join(seg_list_part))
#     return seg_list_part


# # 连接词组
# def package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
#                  seg_list_front_behind_letter, seg_list_front_behind_other,
#                  seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
#                  seg_list_behind_behind_letter, seg_list_behind_behind_other):
#     seg_list_max = max(len(seg_list_front_front_letter), len(seg_list_front_behind_letter),
#                        len(seg_list_behind_front_letter), len(seg_list_behind_behind_letter))
#     seg_list_part = []
#     # 存在数字的相等
#     # print("###",seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other))
#     # print( seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other))
#     # print(seg_list_behind_behind_letter_if_letter(seg_list_behind_behind_letter))
#     # print(seg_list_front_front_letter)
#     # print(seg_list_front_behind_letter)
#     # print(seg_list_behind_front_letter)
#     # △ABC的高AD与CE的长分别为4、6
#     if (seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other)
#         or seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other)) \
#             and seg_list_behind_behind_letter_if_letter(seg_list_behind_front_letter):
#         for i in range(len(seg_list_front_front_letter)):

#             seg_list_part_part = []
#             if len(seg_list_front_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[0])
#             if len(seg_list_front_front_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
#             elif len(seg_list_front_front_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
#             if len(seg_list_front_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[1])

#             if len(seg_list_behind_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_front_other[0])
#             if len(seg_list_behind_front_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
#             elif len(seg_list_behind_front_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
#             if len(seg_list_behind_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_front_other[1])

#             if len(seg_list_behind_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_behind_other[0])
#             if len(seg_list_behind_behind_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
#             elif len(seg_list_behind_behind_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
#             if len(seg_list_behind_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_behind_other[1])
#             seg_list_part.extend(seg_list_part_part)
#             seg_list_part.extend(",")
#         for i in range(len(seg_list_front_behind_letter)):
#             seg_list_part_part = []
#             if len(seg_list_front_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_behind_other[0])
#             if len(seg_list_front_behind_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
#             elif len(seg_list_front_behind_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
#             if len(seg_list_front_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_behind_other[1])

#             if len(seg_list_behind_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_front_other[0])
#             if len(seg_list_behind_front_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part),
#                                           seg_list_behind_front_letter[i + len(seg_list_front_front_letter)][1])
#             elif len(seg_list_behind_front_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
#             if len(seg_list_behind_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_front_other[1])

#             if len(seg_list_behind_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_behind_other[0])
#             if len(seg_list_behind_behind_letter) == seg_list_max:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
#             elif len(seg_list_behind_behind_letter) != 0:
#                 seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
#             if len(seg_list_behind_behind_other) == 2:
#                 seg_list_part_part.extend(seg_list_behind_behind_other[1])
#             seg_list_part.extend(seg_list_part_part)
#             seg_list_part.extend(",")

#         return seg_list_part

#     for i in range(seg_list_max):
#         seg_list_part_part = []
#         if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
#             if len(seg_list_front_front_other[i]) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[i][0])
#         else:
#             if len(seg_list_front_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[0])
#         # if len(seg_list_front_front_letter) == seg_list_max:
#         #     if len(seg_list_front_front_letter[i][1]) == 1:  # 为垂足分别是兜底 ? 看不懂了
#         #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
#         #     else:
#         #         seg_list_part_part.extend(seg_list_front_front_letter[i][1])
#         # elif len(seg_list_front_front_letter) != 0:
#         #     if len(seg_list_front_front_letter[0][1]) == 1:
#         #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
#         #     else:
#         #         seg_list_part_part.extend(seg_list_front_front_letter[0][1])
#         if len(seg_list_front_front_letter) == seg_list_max:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
#         elif len(seg_list_front_front_letter) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])

#         if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
#             if len(seg_list_front_front_other[i]) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[i][1])
#         else:
#             if len(seg_list_front_front_other) == 2:
#                 seg_list_part_part.extend(seg_list_front_front_other[1])

#         if len(seg_list_part_part) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_add)
#         if len(seg_list_front_behind_other) == 2:
#             seg_list_part_part.extend(seg_list_front_behind_other[0])
#         if len(seg_list_front_behind_letter) == seg_list_max:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
#         elif len(seg_list_front_behind_letter) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
#         if len(seg_list_front_behind_other) == 2:
#             seg_list_part_part.extend(seg_list_front_behind_other[1])

#         if len(seg_list_behind_front_other) == 2:
#             seg_list_part_part.extend(seg_list_behind_front_other[0])
#         else:  # 如果存在分别相交于
#             if len(seg_list_behind_front_other) != 0:
#                 seg_list_part_part.extend(seg_list_behind_front_other[0])
#         if len(seg_list_behind_front_letter) == seg_list_max:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
#         elif len(seg_list_behind_front_letter) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
#         if len(seg_list_behind_front_other) == 2:
#             seg_list_part_part.extend(seg_list_behind_front_other[1])

#         if len(seg_list_behind_behind_letter) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_add)

#         if len(seg_list_behind_behind_other) == 2:
#             seg_list_part_part.extend(seg_list_behind_behind_other[0])
#         if len(seg_list_behind_behind_letter) == seg_list_max:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
#         elif len(seg_list_behind_behind_letter) != 0:
#             seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
#         if len(seg_list_behind_behind_other) == 2:
#             seg_list_part_part.extend(seg_list_behind_behind_other[1])
#         # print("#########","".join(seg_list_part_part))
#         seg_list_part.extend(seg_list_part_part)
#         seg_list_part.extend(",")
#     # print("#########","".join(seg_list_part))
#     return seg_list_part


# def find_the_mian_word(seg_list_list, symbol, seg_list_front_front_letter, i):
#     for m in range(1, 5):  # 可能出现多次交
#         if seg_list_list[i - m][0] != symbol:
#             if re.search(".*交", "".join(seg_list_list[i - m])):
#                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("交")]
#             if re.search(".*与", "".join(seg_list_list[i - m])):
#                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("与")]
#             if re.search(".*作", "".join(seg_list_list[i - m])):
#                 seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("作")]
#             if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
#                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
#                 seg_list_front_front_letter = find_all_letter_return_side_letter(
#                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
#                 while len(seg_list_front_front_letter) > 1:
#                     del seg_list_front_front_letter[1]
#                 # print(seg_list_front_front_letter)
#                 # print()
#                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
#                                                                          seg_list_front_front_letter)
#             # 线AB、CD,分别交^^于^^
#             elif seg_list_having("、", seg_list_list[i - m]):
#                 seg_list_front_front_letter = find_all_letter_return_side_letter(
#                     seg_list_list[i - m])
#                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
#                                                                          seg_list_front_front_letter)
#             else:
#                 for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
#                     if if_letter(seg_list_list[i - m][k]):
#                         for j in range(len(seg_list_front_front_letter)):
#                             seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
#                             seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
#                         seg_list_front_front_other = find_front_and_behind_other(
#                             seg_list_list[i - m],
#                             seg_list_front_front_letter)
#                         break  # 只提取第一个词语
#             if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
#                 seg_list_front_front_other[1] = []
#             break
#     return seg_list_front_front_letter, seg_list_front_front_other


# # 处理分别
# def cut_respect_is_importance(seg_list, symbol):
#     seg_list_list = return_seg_list_list(seg_list)
#     seg_list_i_temp_front = 0
#     seg_list_i_temp_behind = 0
#     seg_list_i_temp = []  # 存储更新后的词组
#     for i in range(len(seg_list_list)):
#         if symbol == "交" and "交" not in seg_list_list[i]:
#             if "相交" in seg_list_list[i]:
#                 symbol = "相交"

#         if symbol in seg_list_list[i]:
#             seg_list_i_temp_front = i  # 记录当前分别的位置
#             seg_list_front = seg_list_list[i][:seg_list_list[i].index(symbol)]
#             seg_list_behind = seg_list_list[i][seg_list_list[i].index(symbol) + 1:]
#             seg_list_front_front_letter = []
#             seg_list_front_front_other = []
#             seg_list_front_behind_letter = []
#             seg_list_front_behind_other = []
#             seg_list_behind_front_letter = []
#             seg_list_behind_front_other = []
#             seg_list_behind_behind_letter = []
#             seg_list_behind_behind_other = []
#             if len(seg_list_front) == 0:
#                 # 当存在"作"的时候,可能出现于,但是不存在缺少主语,故为: 分别f-f 作 f-b 交 b-h 于 b-b
#                 # 当不存在"作"的时候,可能出现于,但是缺少主语,故为:  主语,分别b-f 于b-b
#                 # 主语可能出现线,三边,多边
#                 # 此时ff是分别之后作之前
#                 if seg_list_having(["作", "与"], seg_list_behind) and seg_list_behind.index(
#                         seg_list_having_0(["作", "与"], seg_list_behind)) > 0:  # 防止出现分别作多判断
#                     seg_list_front_front = seg_list_behind[
#                                            :seg_list_behind.index(seg_list_having_0(["作", "与"], seg_list_behind))]
#                     seg_list_front_behind = seg_list_behind[
#                                             seg_list_behind.index(
#                                                 seg_list_having_0(["作", "与"], seg_list_behind)) + 1:]
#                     # 前半部分是否存在可以处理"的"
#                     if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
#                             seg_list_front_front[seg_list_front_front.index(
#                                 seg_list_having_0("的", seg_list_front_front)) + 1:]):
#                         seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
#                             seg_list_having_0("的", seg_list_front_front)) + 1:]
#                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
#                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
#                                                                                  seg_list_front_front_letter)
#                     else:
#                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
#                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
#                                                                                  seg_list_front_front_letter)

#                     if seg_list_having(["于"], seg_list_front_behind):  # 是否有"于"或者"交于"在后半段
#                         seg_list_behind_front = seg_list_front_behind[:seg_list_front_behind.index(
#                             seg_list_having_0(["于"], seg_list_front_behind))]
#                         seg_list_behind_behind = seg_list_front_behind[seg_list_front_behind.index(
#                             seg_list_having_0(["于"], seg_list_front_behind)) + 1:]
#                         seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
#                         seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
#                                                                                    seg_list_behind_behind_letter)
#                         if seg_list_having(["交"], seg_list_behind_front):  # 是否有"交"在作后半段,于前半段,即在中间
#                             seg_list_behind_front_front = seg_list_behind_front[:seg_list_behind_front.index(
#                                 seg_list_having_0(["交"], seg_list_behind_front))]
#                             seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
#                                 seg_list_having_0(["交"], seg_list_behind_front)):]
#                             seg_list_front_behind_letter = find_all_letter_return_side_letter(
#                                 seg_list_behind_front_front)
#                             seg_list_front_behind_other = find_front_and_behind_other(seg_list_behind_front_front,
#                                                                                       seg_list_front_behind_letter)
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
#                                 seg_list_behind_front_behind)
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_behind,
#                                                                                       seg_list_behind_front_letter)
#                         else:
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
#                                                                                       seg_list_behind_front_letter)
#                     else:
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_front_behind)
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_front_behind,
#                                                                                   seg_list_behind_front_letter)
#                 else:
#                     if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
#                         seg_list_behind_front = seg_list_behind[
#                                                 :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
#                         seg_list_behind_behind = seg_list_behind[
#                                                  seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
#                         if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
#                                 seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
#                                 seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
#                                                                                       seg_list_behind_front)
#                         else:
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
#                                                                                       seg_list_behind_front_letter)
#                         seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
#                         seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
#                                                                                    seg_list_behind_behind_letter)
#                     else:
#                         # 垂线   分别交三角形ABC的AB CD
#                         if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
#                                 seg_list_behind[seg_list_behind.index("的") + 1:]):
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(
#                                 seg_list_behind[seg_list_behind.index("的") + 1:])
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
#                                                                                       seg_list_behind)
#                         else:
#                             seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
#                             seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
#                                                                                       seg_list_behind_front_letter)
#                     # 如果有"于"看b-b-l字母值,否则看b-f-l值
#                     seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
#                         else len(seg_list_behind_front_letter)
#                     for k in range(seg_list_b_b_l_len):
#                         seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
#                     for m in range(1, 5):  # 可能出现多次交
#                         if seg_list_list[i - m][0] != symbol:
#                             if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
#                                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
#                                 seg_list_front_front_letter = find_all_letter_return_side_letter(
#                                     seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
#                                 while len(seg_list_front_front_letter) > 1:
#                                     del seg_list_front_front_letter[1]
#                                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
#                                                                                          seg_list_front_front_letter)
#                             # 线AB、CD,分别交^^于^^
#                             elif seg_list_having("、", seg_list_list[i - m]):
#                                 seg_list_front_front_letter = find_all_letter_return_side_letter(
#                                     seg_list_list[i - m])
#                                 seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
#                                                                                          seg_list_front_front_letter)
#                             else:
#                                 for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
#                                     if if_letter(seg_list_list[i - m][k]):
#                                         for j in range(len(seg_list_front_front_letter)):
#                                             seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
#                                             seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
#                                         seg_list_front_front_other = find_front_and_behind_other(
#                                             seg_list_list[i - m],
#                                             seg_list_front_front_letter)
#                                         break  # 只提取第一个词语
#                             if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
#                                 seg_list_front_front_other[1] = []
#                             break

#                 for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):
#                     seg_list_i_temp.extend(seg_list_list[k])
#                     seg_list_i_temp.extend(",")
#                 if "分别" in symbol:
#                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
#                                                         seg_list_having_0(["作", "与"], seg_list_front),
#                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
#                                                         seg_list_behind_front_letter, seg_list_behind_front_other,
#                                                         seg_list_having_0("于", seg_list_behind),
#                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
#                 else:
#                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
#                                                                seg_list_having_0(["作", "与"], seg_list_front),
#                                                                seg_list_front_behind_letter,
#                                                                seg_list_front_behind_other,
#                                                                seg_list_behind_front_letter,
#                                                                seg_list_behind_front_other, "于",
#                                                                seg_list_behind_behind_letter,
#                                                                seg_list_behind_behind_other, symbol))

#                 seg_list_i_temp_behind = i + 1
#                 # 分别在前面,可能出现缺主语或不缺
#             elif len(seg_list_front) == 1 and seg_list_having_2(["垂"], seg_list_front):
#                 if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
#                     seg_list_behind_front = seg_list_behind[
#                                             :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
#                     seg_list_behind_behind = seg_list_behind[
#                                              seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
#                     if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
#                             seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(
#                             seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
#                                                                                   seg_list_behind_front)
#                     else:
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
#                                                                                   seg_list_behind_front_letter)
#                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
#                     seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
#                                                                                seg_list_behind_behind_letter)
#                 else:
#                     # 垂线分别交三角形ABC的AB CD
#                     if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
#                             seg_list_behind[seg_list_behind.index("的") + 1:]):
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(
#                             seg_list_behind[seg_list_behind.index("的") + 1:])
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
#                                                                                   seg_list_behind)
#                     else:
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
#                                                                                   seg_list_behind_front_letter)
#                 seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
#                     else len(seg_list_behind_front_letter)
#                 s_l_b_b_temp = 0
#                 for k in range(seg_list_b_b_l_len):
#                     seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
#                     seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
#                 for k in range(seg_list_b_b_l_len):  # 如果存在"于"看b-b-l,否则看b-f-l
#                     if seg_list_having("⊥", seg_list_list[i - k - 1]):
#                         s_l_b_b_temp = i - k - 1
#                         for j in range(len(seg_list_list[i - k - 1])):
#                             if if_letter(seg_list_list[i - k - 1][j]):
#                                 seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0] = len(
#                                     seg_list_list[i - k - 1][j])
#                                 seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1] = seg_list_list[i - k - 1][j]
#                                 seg_list_front_front_letter_temp = [[[], []]]
#                                 seg_list_front_front_letter_temp[0][0] = \
#                                     seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0]
#                                 seg_list_front_front_letter_temp[0][1] = \
#                                     seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1]
#                                 seg_list_front_front_other[seg_list_b_b_l_len - 1 - k] = find_front_and_behind_other(
#                                     seg_list_list[i - k - 1], seg_list_front_front_letter_temp)
#                                 break  # 只提取第一个词语
#                 # print(seg_list_front_front_letter)
#                 # print(package_line(seg_list_front_front_letter, "", "垂直", "", "", seg_list_behind_front_letter,
#                 #                    seg_list_behind_front_other, "于", seg_list_behind_behind_letter,
#                 #                    seg_list_behind_behind_other))
#                 for k in range(seg_list_i_temp_behind, s_l_b_b_temp):
#                     seg_list_i_temp.extend(seg_list_list[k])
#                     seg_list_i_temp.extend(",")
#                 seg_list_i_temp_behind = s_l_b_b_temp
#                 if "分别" in symbol:
#                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
#                                                         ("垂直" if seg_list_having(["垂直"],
#                                                                                    seg_list_front) else "垂足"),
#                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
#                                                         seg_list_behind_front_letter, seg_list_behind_front_other,
#                                                         seg_list_having_0("于", seg_list_behind),
#                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
#                 else:
#                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
#                                                                seg_list_having_0(["作", "与"], seg_list_front),
#                                                                seg_list_front_behind_letter,
#                                                                seg_list_front_behind_other,
#                                                                seg_list_behind_front_letter,
#                                                                seg_list_behind_front_other, "于",
#                                                                seg_list_behind_behind_letter,
#                                                                seg_list_behind_behind_other, symbol))

#                 seg_list_i_temp_behind = i + 1

#             else:
#                 # E、F分别为AD、BC的中点
#                 seg_list_front_temp_front = []
#                 if return_re_return([".*平分"], "".join(seg_list_front)) and seg_list_having("、", seg_list_front) \
#                         and return_re_return([".*交"], "".join(symbol)):
#                     seg_list_list_front = seg_list_front[:seg_list_front.index("平分线")]
#                     seg_list_list_behind = seg_list_front[seg_list_front.index("平分线") + 1:]
#                     seg_list_list_front_letter = find_all_letter_return_side_letter(seg_list_list_front)
#                     seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
#                     if len(seg_list_list_behind_letter) == len(seg_list_list_front_letter):
#                         for j in range(len(seg_list_list_front_letter)):
#                             if seg_list_front[seg_list_front.index(seg_list_list_front_letter[j][1]) - 1] in "∠":
#                                 front_letter_temp = "∠"
#                                 front_letter_temp += seg_list_list_front_letter[j][1]
#                                 seg_list_list_front_letter[j][1] = front_letter_temp
#                         front_letter_temp_temp = []
#                         front_letter_temp_time = len(seg_list_list_front_letter) - 1
#                         for j in range(len(seg_list_list_front_letter)):
#                             front_letter_temp = []
#                             front_letter_temp.insert(len(front_letter_temp), seg_list_list_front_letter[j][1])
#                             front_letter_temp.extend("的")
#                             front_letter_temp.extend("平分线")
#                             front_letter_temp.insert(len(front_letter_temp), seg_list_list_behind_letter[j][1])
#                             front_letter_temp = transition_divide(front_letter_temp)
#                             front_letter_temp_list = return_seg_list_list(front_letter_temp)
#                             for k in range(len(front_letter_temp_list)):
#                                 if k + 1 != len(front_letter_temp_list):
#                                     seg_list_front_temp_front.insert(len(seg_list_front_temp_front),
#                                                                      front_letter_temp_list[k])
#                                 else:
#                                     front_letter_temp_temp.extend(front_letter_temp_list[k])
#                             if front_letter_temp_time:
#                                 front_letter_temp_temp.extend("、")
#                                 front_letter_temp_time -= 1
#                         seg_list_front = front_letter_temp_temp

#                 # 单只处理平分
#                 if return_re_return([".*平分"], "".join(seg_list_front)) and \
#                         not return_re_return([".*与", ".*作", ".*和"], "".join(seg_list_front)) and \
#                         not seg_list_having("、", seg_list_list[i]):

#                     seg_list_temp = transition_divide(seg_list_front)
#                     seg_list_temp_list = return_seg_list_list(seg_list_temp)
#                     seg_list_front_temp = []
#                     seg_list_front_temp_temp = []
#                     seg_list_front_temp_front = []  # 记录平分前的关系
#                     for j in range(len(seg_list_temp_list)):
#                         seg_list_temp_list_letter = find_all_letter_return_side_letter(seg_list_temp_list[j])
#                         if len(seg_list_temp_list_letter) == 1:
#                             seg_list_front_temp.insert(len(seg_list_front_temp), seg_list_temp_list[j])
#                         else:
#                             seg_list_front_temp_front.insert(len(seg_list_front_temp_front), seg_list_temp_list[j])
#                             seg_list_front_temp_front.extend(",")
#                     if len(seg_list_front_temp) == 1:
#                         seg_list_front_temp_temp.extend(seg_list_front_temp[0])
#                     else:
#                         for j in range(len(seg_list_front_temp)):
#                             seg_list_front_temp_temp.extend(seg_list_front_temp[j])
#                             seg_list_front_temp_temp.extend("、")
#                     seg_list_front = seg_list_front_temp_temp

#                 if seg_list_having(["作", "与"], seg_list_front):
#                     seg_list_front_front = seg_list_front[
#                                            :seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front))]
#                     seg_list_front_behind = seg_list_front[
#                                             seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front)) + 1:]
#                     if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
#                             seg_list_front_front[seg_list_front_front.index(
#                                 seg_list_having_0("的", seg_list_front_front)) + 1:]):
#                         seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
#                             seg_list_having_0("的", seg_list_front_front)) + 1:]
#                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
#                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
#                                                                                  seg_list_front_front_letter)
#                     else:
#                         seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
#                         seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
#                                                                                  seg_list_front_front_letter)
#                     if seg_list_having("的", seg_list_front_behind) and find_have_d_or_slight_pause(
#                             seg_list_front_behind[
#                             seg_list_front_behind.index(seg_list_having_0("的", seg_list_front_behind)) + 1:]):
#                         # 前半部分存在"的"和每一部分都有顿号或者是字母
#                         seg_list_front_behind_behind = seg_list_front_behind[
#                                                        seg_list_front_behind.index(
#                                                            seg_list_having_0("的", seg_list_front_behind)) + 1:]
#                         seg_list_front_behind_letter = find_all_letter_return_side_letter(
#                             seg_list_front_behind_behind)  # 找出所有的词语
#                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
#                                                                                   seg_list_front_behind_letter)
#                     else:
#                         seg_list_front_behind_letter = find_all_letter_return_side_letter(
#                             seg_list_front_behind)  # 找出所有的词语
#                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
#                                                                                   seg_list_front_behind_letter)
#                 else:
#                     if seg_list_having("的", seg_list_front) and find_have_d_or_slight_pause(
#                             seg_list_front[seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]):
#                         seg_list_front_behind = seg_list_front[
#                                                 seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]
#                         seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)
#                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
#                                                                                   seg_list_front_behind_letter)
#                     else:
#                         seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front)
#                         seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
#                                                                                   seg_list_front_behind_letter)
#                 if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
#                     seg_list_behind_front = seg_list_behind[
#                                             :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
#                     seg_list_behind_behind = seg_list_behind[
#                                              seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]

#                     if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
#                             seg_list_behind_front[seg_list_behind_front.index(
#                                 seg_list_having_0("的", seg_list_behind_front)) + 1:]):
#                         seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
#                             seg_list_having_0("的", seg_list_behind_front)) + 1:]
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front_behind)
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
#                                                                                   seg_list_behind_front_letter)
#                     else:
#                         seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
#                         seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
#                                                                                   seg_list_behind_front_letter)
#                     seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
#                     seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
#                                                                                seg_list_behind_behind_letter)
#                 else:
#                     seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
#                     seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
#                                                                               seg_list_behind_front_letter)
#                 if (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[0]) or \
#                         (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[1]):
#                     seg_list_front_behind_letter = seg_list_front_behind_letter[:1]
#                     seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
#                                                                               seg_list_front_behind_letter)
#                     # 去掉三角形,三角形在最前面或最后面,且前面和中间的长度不相等
#                 if len(seg_list_behind_front_letter) != 0 and (seg_list_behind_front_letter[0][0] == 3 or
#                                                                seg_list_behind_front_letter[
#                                                                    len(seg_list_behind_front_letter) - 1][0]
#                                                                == 3) and len(seg_list_front_behind_letter) != \
#                         len(seg_list_behind_front_letter):
#                     if seg_list_behind_front_letter[0][0] == 3:
#                         seg_list_behind_front_letter = seg_list_behind_front_letter[1:]
#                     else:
#                         seg_list_behind_front_letter = seg_list_behind_front_letter[
#                                                        :len(seg_list_behind_front_letter) - 2]
#                 for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):  # 拼接没有处理的句子
#                     seg_list_i_temp.extend(seg_list_list[k])
#                     seg_list_i_temp.extend(",")
#                 if len(seg_list_front_temp_front) != 0:
#                     for j in range(len(seg_list_front_temp_front)):
#                         seg_list_i_temp.extend(seg_list_front_temp_front[j])
#                         seg_list_i_temp.extend(",")
#                     # print(seg_list_front_other) print(seg_list_behind_front_other) print(seg_list_behind_other)
#                     # print("".join(package_line(seg_list_front_letter, seg_list_front_other, seg_list_mid_letter,
#                     # seg_list_behind_front_other, seg_list_beh_letter, seg_list_behind_other)))

#                 if "分别" in symbol:
#                     seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
#                                                         seg_list_having_0(["作", "与"], seg_list_front),
#                                                         seg_list_front_behind_letter, seg_list_front_behind_other,
#                                                         seg_list_behind_front_letter, seg_list_behind_front_other, "于",
#                                                         seg_list_behind_behind_letter, seg_list_behind_behind_other))
#                 else:

#                     if (len(seg_list_front_front_letter) + len(seg_list_front_behind_letter) + len(
#                             seg_list_behind_front_letter)) < 2:
#                         seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"],
#                                                                                                    seg_list_behind) \
#                             else len(seg_list_behind_front_letter)
#                         s_l_b_b_temp = 0
#                         for k in range(seg_list_b_b_l_len):
#                             seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
#                             seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
#                         seg_list_front_front_letter, seg_list_front_front_other = find_the_mian_word(seg_list_list,
#                                                                                                      symbol,
#                                                                                                      seg_list_front_front_letter,
#                                                                                                      i)
#                     if "平分" in seg_list_front_behind_other[0] or "平分" in seg_list_front_behind_other[1]:
#                         for k in range(len(seg_list_front_behind_letter)):
#                             if seg_list_front_behind_letter[k][0] != 2:
#                                 seg_list_front_behind_letter_front = seg_list_front_behind_letter[:k]
#                                 seg_list_front_behind_letter_front.extend(seg_list_front_behind_letter[k + 1:])
#                                 seg_list_front_behind_letter = seg_list_front_behind_letter_front
#                     seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
#                                                                seg_list_having_0(["作", "与"], seg_list_front),
#                                                                seg_list_front_behind_letter,
#                                                                seg_list_front_behind_other,
#                                                                seg_list_behind_front_letter,
#                                                                seg_list_behind_front_other, "于",
#                                                                seg_list_behind_behind_letter,
#                                                                seg_list_behind_behind_other, symbol))
#                 seg_list_i_temp_behind = i + 1
#         if symbol == "相交":  # 将symbol还原
#             symbol = "交"
#     for k in range(seg_list_i_temp_behind, len(seg_list_list)):  # 拼接"分别"后面未处理的句子
#         seg_list_i_temp.extend(seg_list_list[k])
#         seg_list_i_temp.extend(",")
#     return seg_list_i_temp


# # 处理连等和相似的情况
# def transition_equal_or_similarity(seg_list):
#     equal_value_all = []
#     seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
#     seg_list = []
#     while seg_list1 != "":
#         if_transition = 0
#         if seg_list_having_0(symbol_keywords_main, seg_list1):
#             seg_list.extend(find_which_equal(seg_list1, seg_list_having_0(symbol_keywords_main, seg_list1)))
#             if_transition = 1
#         if if_transition == 0:
#             seg_list.extend(seg_list1)
#         seg_list.extend(",")
#         seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
#     return seg_list
#     # if "=" in seg_list:
#     #     equal_value_all = find_which_equal(seg_list, "=")
#     # if "//" in seg_list:
#     #     equal_value_all = find_which_equal(seg_list, "//")
#     # if "⊥" in seg_list:
#     #     equal_value_all = find_which_equal(seg_list, "⊥")
#     # symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]


# def transition_angle_to_angle(seg_list):
#     for i in range(len(seg_list)):
#         if i + 1 < len(seg_list) and seg_list[i] in "∠" and seg_list[i + 1] in "平分线":
#             seg_list_front = seg_list[:i]
#             seg_list_behind = seg_list[i + 1:]
#             seg_list_front.extend("角")
#             seg_list_front.extend(seg_list_behind)
#             seg_list = seg_list_front
#     return seg_list


# def transition_triangle_symbol(seg_list, symbol):
#     for i in range(len(seg_list)):
#         if symbol in seg_list[i] and if_letter(seg_list[i + 1]):
#             seg_list_front = seg_list[i][:seg_list[i].index(symbol)]
#             seg_list_front += "△"
#             seg_list[i] = seg_list_front
#     return seg_list


# def return_the_point_at_line_temp(seg_list_list_letter1, seg_list_list_letter2, seg_list_list_letter_temp):
#     if len(seg_list_list_letter1) == 0 and len(seg_list_list_letter2) == 0:
#         return ""
#     if len(seg_list_list_letter1) == 1:
#         seg_list_list_letter_A = seg_list_list_letter1
#         seg_list_list_letter_BC = seg_list_list_letter2
#     else:
#         seg_list_list_letter_A = seg_list_list_letter2
#         seg_list_list_letter_BC = seg_list_list_letter1
#     if seg_list_list_letter_temp == "延长线":
#         letter_point = ""
#         letter_AB = ""
#         letter_point = seg_list_list_letter_BC[1]
#         letter_AB += seg_list_list_letter_BC[0]
#         letter_AB += seg_list_list_letter_A[0]
#         seg_list_list_letter_A = letter_point
#         seg_list_list_letter_BC = letter_AB
#         seg_list_list_letter_temp = ""
#     temp = []
#     temp.insert(len(temp), seg_list_list_letter_A)
#     if seg_list_list_letter_temp != "中点":  # 如果是中点,修改为A是BC的中点
#         temp.insert(len(temp), "在")
#     else:
#         temp.insert(len(temp), "平分")
#     temp.insert(len(temp), seg_list_list_letter_BC)
#     if seg_list_list_letter_temp != "中点":
#         if seg_list_list_letter_temp != "":
#             temp.insert(len(temp), seg_list_list_letter_temp)
#             temp.insert(len(temp), "上")
#         else:
#             temp.insert(len(temp), "上")
#     # else:
#     #     temp.insert(len(temp), "的")
#     #     temp.insert(len(temp), "中点")
#     temp.insert(len(temp), ",")
#     temp.insert(len(temp), seg_list_list_letter_A)
#     return temp


# def guozuoyu(clause):
#     arr = re.split('[作于]', clause)
#     front = re.findall('[A-Za-z]', arr[0])
#     mid = re.findall('[A-Za-z]', arr[1])
#     behind = re.findall('[A-Za-z]', arr[2])
#     clause_new = ""
#     if arr[1].find('垂线') != -1:
#         clause_new = front[-1] + behind[0] + '⊥' + mid[0] + mid[1] + '于' + behind[0]
#     if arr[1].find('交') != -1:
#         clause_new += ',' + front[-1] + behind[0] + '交' + mid[2] + mid[3] + '于' + behind[0]
#     return (clause_new)


# def guozuo(clause):
#     arr = clause.split('作')
#     front = re.findall('[A-Za-z]', arr[0])
#     behind = re.findall('[A-Za-z]', arr[1])
#     clause_new = ""
#     for i in range(len(map_clear_up_keywords)):
#         if re.search(map_clear_up_keywords[i], arr[1]) and map_clear_up_keywords[i] != "线":
#             clause_new = map_clear_up_keywords[i]
#             for j in range(len(behind)):
#                 clause_new += behind[j]
#             clause_new += ","
#             return clause_new
#     if front[-1] == behind[0] or front[-1] == behind[1]:
#         clause_new = ""
#     else:
#         if arr[1].find("延长") != -1:
#             clause_new = front[-1] + "在" + behind[0] + behind[1] + "延长线上"
#         else:
#             clause_new = front[-1] + "在" + behind[0] + behind[1] + "上"
#     if len(behind) > 2:
#         if arr[1].find("的平行线") != -1:
#             if front[-1] == behind[2] or front[-1] == behind[3]:
#                 clause = ""
#             else:
#                 clause_new = front[-1] + "在" + behind[2] + behind[3] + "上"
#             if clause_new != "":
#                 clause_new += ","
#             clause_new += behind[0] + behind[1] + '//' + behind[2] + behind[3]
#     if len(front) > 1:
#         if arr[0].find('中点') != -1:
#             if clause_new != "":
#                 clause_new += ","
#             clause_new += front[2] + '是' + front[0] + front[1] + '中点'
#         elif arr[0].find('上的') != -1:
#             if clause_new != "":
#                 clause_new += ","
#             clause_new += front[2] + '在' + front[0] + front[1] + '上'
#     return clause_new


# def transition_diagonal(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if re.search(".*对角线", "".join(seg_list_list[i])):
#             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             seg_list_list_letter_A = []
#             seg_list_list_letter_AB = []
#             seg_list_list_letter_ABC = []
#             for j in range(len(seg_list_list_letter)):
#                 if seg_list_list_letter[j][0] == 1:
#                     seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
#                 elif seg_list_list_letter[j][0] == 2:
#                     seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
#                 else:
#                     seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
#             seg_temp = []
#             for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
#                 seg_list_list_letter_symbol = seg_list_list[i][
#                     seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
#                 seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
#                 seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
#                 seg_temp.extend(",")
#             if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):
#                 for j in range(len(seg_list_list_letter_A)):
#                     seg_list_list_letter_temp = ""
#                     temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
#                                                          seg_list_list_letter_temp)
#                     seg_temp.extend(temp)
#                     seg_temp.extend(",")
#             if len(seg_list_list_letter_AB) == 1:
#                 seg_temp.insert(len(seg_temp), seg_list_list_letter_AB[0])
#                 seg_temp.extend(",")
#             seg_list_list[i] = seg_temp
#     return return_seg_list(seg_list_list)


# def transition_point_at_side_re(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if return_re_return(
#                 ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
#                  "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
#             if seg_list_having("=", seg_list_list[i]):
#                 if seg_list_list[i][seg_list_list[i].index("=") - 2] == "∠":
#                     seg_list_list[i].insert(seg_list_list[i].index("=") - 2, ",")
#                 else:
#                     seg_list_list[i].insert(seg_list_list[i].index("=") - 1, ",")
#                 seg_list_list[i] = behind_operation(seg_list_list[i])
#                 continue
#             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             seg_list_list_letter_A = []
#             seg_list_list_letter_AB = []
#             seg_list_list_letter_ABC = []
#             for j in range(len(seg_list_list_letter)):
#                 if seg_list_list_letter[j][0] == 1:
#                     seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
#                 elif seg_list_list_letter[j][0] == 2:
#                     seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
#                 else:
#                     seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
#             seg_list_list_letter_temp = ""
#             if return_re_return([".*中点"], "".join(seg_list_list[i])):  # 提取关键词
#                 seg_list_list_letter_temp = "中点"
#             elif return_re_return([".*延长"], "".join(seg_list_list[i])):
#                 seg_list_list_letter_temp = "延长线"
#             else:
#                 seg_list_list_letter_temp = ""
#             if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):  # 可能出现单独只是一个图形
#                 seg_temp = []
#                 for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
#                     seg_list_list_letter_symbol = seg_list_list[i][
#                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
#                     seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
#                     seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
#                     seg_temp.extend(",")
#                 for j in range(len(seg_list_list_letter_A)):
#                     temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
#                                                          seg_list_list_letter_temp)
#                     seg_temp.extend(temp)
#                     seg_temp.extend(",")
#                 seg_list_list[i] = seg_temp
#             elif len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) > 0:
#                 seg_temp = []
#                 for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
#                     seg_list_list_letter_symbol = seg_list_list[i][
#                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
#                     seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
#                     seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
#                     seg_temp.extend(",")
#                 if len(seg_list_list_letter_AB) == 1:
#                     for j in range(len(seg_list_list_letter_A)):
#                         temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[0],
#                                                              seg_list_list_letter_temp)
#                         seg_temp.extend(temp)
#                         seg_temp.extend(",")
#                 seg_list_list[i] = seg_temp
#             elif re.search("一.*直线", "".join(seg_list_list[i])) is not None or re.search("任意.*点", "".join(
#                     seg_list_list[i])) is not None:  # 共线
#                 seg_list_list_temp = ""
#                 seg_list_list_temp_temp = ""
#                 seg_list_list_temp += seg_list_list_letter[0][1]
#                 seg_list_list_temp += seg_list_list_letter[len(seg_list_list_letter) - 1][1]
#                 seg_list_list_temp_temp = "".join(seg_list_list_temp)
#                 seg_list_list_letter = seg_list_list_letter[1:]
#                 seg_list_list_letter = seg_list_list_letter[:len(seg_list_list_letter) - 1]
#                 if len(seg_list_list_letter) == 0:
#                     seg_list_list[i] = seg_list_list_temp_temp
#                 else:
#                     seg_temp = []
#                     for j in range(len(seg_list_list_letter)):
#                         temp = return_the_point_at_line_temp(seg_list_list_letter[j][1], seg_list_list_temp_temp,
#                                                              seg_list_list_letter_temp)
#                         seg_temp.extend(temp)
#                         seg_temp.extend(",")
#                     seg_list_list[i] = seg_temp

#             elif (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) == 0) or (
#                     len(seg_list_list_letter_A) == 0 and len(seg_list_list_letter_AB) > 0):
#                 seg_list_list_letter_symbol = []
#                 for j in range(len(seg_list_list_letter_ABC)):  # 记录的图形
#                     seg_list_list_letter_symbol.insert(len(seg_list_list_letter_symbol), seg_list_list[i][
#                         seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1])
#                 temp = []
#                 if (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_ABC) > 0) or (
#                         len(seg_list_list_letter_AB) > 0 and len(seg_list_list_letter_ABC) > 0):
#                     for j in range(len(seg_list_list_letter_A if len(
#                             seg_list_list_letter_A) > 0 else seg_list_list_letter_AB)):
#                         if len(seg_list_list_letter_ABC) == 1:
#                             temp.insert(len(temp), seg_list_list_letter_symbol[0])
#                             temp.insert(len(temp), seg_list_list_letter_ABC[0])
#                         else:
#                             temp.insert(len(temp), seg_list_list_letter_symbol[j])
#                             temp.insert(len(temp), seg_list_list_letter_ABC[j])
#                         temp.extend(",")
#                         if len(seg_list_list_letter_A) > 0:
#                             temp.insert(len(temp), seg_list_list_letter_A[j])
#                             temp.extend("在")
#                             if len(seg_list_list_letter_ABC) == 1:
#                                 # temp.insert(len(temp), seg_list_list_letter_symbol[0])
#                                 temp.insert(len(temp), seg_list_list_letter_ABC[0])
#                             else:
#                                 # temp.insert(len(temp), seg_list_list_letter_symbol[j])
#                                 temp.insert(len(temp), seg_list_list_letter_ABC[j])
#                             temp.extend("内")
#                         else:
#                             temp.insert(len(temp), seg_list_list_letter_AB[j])
#                         temp.extend(",")
#                         if len(seg_list_list_letter_A) > 0:
#                             temp.extend(seg_list_list_letter_A[j])
#                         else:
#                             temp.extend(seg_list_list_letter_AB[j])
#                 elif len(seg_list_list_letter_A) > 0:  # 特质判断，点在斜边上
#                     if return_re_return([".*斜"], "".join(seg_list_list[i])):
#                         for j in range(len(seg_list_list_letter_A)):
#                             temp.insert(len(temp), seg_list_list_letter_A[j])
#                             temp.extend("在")
#                             temp.extend("斜边")
#                             temp.extend("上")
#                             temp.extend(",")
#                     elif return_re_return([".*侧"], "".join(seg_list_list[i])):  # 此处为补丁，点E在F左侧
#                         temp = seg_list_list[i]
#                 else:
#                     temp.insert(len(temp), seg_list_list_letter_AB[0])
#                     if seg_list_list_letter_temp == "延长线":
#                         temp.extend("的")
#                         temp.insert(len(temp), "延长线")
#                 seg_list_list[i] = temp
#             elif seg_list_having_1(["作", "做"], seg_list_list[i]):  # 特质判断，以AE为边在直线BC的上方作正方形AEFG
#                 seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("作" if "作" in seg_list_list[i] else "做"):]
#                 seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])

#             else:
#                 for j in range(len(symbol_keywords_main)):
#                     if symbol_keywords_main[j] in seg_list_list[i]:
#                         temp = []
#                         letter = []
#                         temp_int = 0
#                         for k in range(3):
#                             if seg_list_list[i].index(symbol_keywords_main[j]) - k >= 0 \
#                                     and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k] in
#                                          map_clear_up_keywords or seg_list_list[i][
#                                              seg_list_list[i].index(symbol_keywords_main[j]) - k] in symbol_keywords or
#                                          if_number_and_letter(
#                                              seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])):
#                                 temp.insert(len(temp),
#                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])
#                                 temp_int = k
#                         temp.reverse()
#                         letter = find_all_letter_return_side_letter(temp)
#                         letter = letter[0][1]
#                         temp.extend(symbol_keywords_main[j])
#                         for k in range(3):
#                             if seg_list_list[i].index(symbol_keywords_main[j]) + k < len(seg_list_list[i]) \
#                                     and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k] in
#                                          map_clear_up_keywords or seg_list_list[i][
#                                              seg_list_list[i].index(symbol_keywords_main[j]) + k] in symbol_keywords or
#                                          if_number_and_letter(
#                                              seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])):
#                                 temp.insert(len(temp),
#                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])
#                         seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index(symbol_keywords_main[j]) - temp_int]
#                         new_letter = find_all_letter_return_side_letter(seg_list_list[i])
#                         for k in range(len(letter)):
#                             for p in range(len(new_letter)):
#                                 if letter[k] in new_letter[p][1]:
#                                     continue
#                                 else:
#                                     letter = letter[k]
#                                     break
#                             if k + 1 == len(letter):
#                                 letter = ""
#                                 break
#                         seg_list_list[i].extend("存在点")
#                         seg_list_list[i].extend(letter)
#                         seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])
#                         seg_list_list[i].extend(temp)
#     return return_seg_list(seg_list_list)


# def transition_hand_over_temp(seg_list_list, temp, temp_temp):
#     temp.extend(seg_list_list[len(seg_list_list) - 1])
#     for i in range(len(seg_list_list) - 1):
#         temp_temp.extend(seg_list_list[i])
#         temp_temp.extend(",")
#     return temp, temp_temp


# def transition_hand_over(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if seg_list_having_2("交", seg_list_list[i]):
#             seg_list_list[i] = list(jieba.cut("".join(seg_list_list[i]), cut_all=False))
#             seg_list_list_front = seg_list_list[i][
#                                   :seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交")]
#             seg_list_list_mid = seg_list_list[i][
#                                 seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交") + 1:
#                                 seg_list_list[i].index("于")]
#             seg_list_list_behind = seg_list_list[i][seg_list_list[i].index("于") + 1:]
#             seg_list_list_front = behind_operation(seg_list_list_front)
#             seg_list_list_mid = behind_operation(seg_list_list_mid)
#             seg_list_list_behind = behind_operation(seg_list_list_behind)
#             seg_list_list_front_temp = return_seg_list_list(seg_list_list_front)  # 查看是否有补充
#             seg_list_list_mid_temp = return_seg_list_list(seg_list_list_mid)
#             seg_list_list_behind_temp = return_seg_list_list(seg_list_list_behind)
#             temp = []
#             temp_temp = []
#             temp, temp_temp = transition_hand_over_temp(seg_list_list_front_temp, temp, temp_temp)
#             temp.extend("交")
#             temp, temp_temp = transition_hand_over_temp(seg_list_list_mid_temp, temp, temp_temp)
#             temp.extend("于")
#             temp, temp_temp = transition_hand_over_temp(seg_list_list_behind_temp, temp, temp_temp)
#             temp_temp.extend(temp)
#             temp.extend(",")
#             seg_list_list[i] = temp_temp
#     return return_seg_list(seg_list_list)


# def transition_zuo_in_list(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if re.search(".*作", "".join(seg_list_list[i])):
#             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             if len(seg_list_letter) == 0:
#                 seg_list_list[i] = ""
#             elif len(seg_list_letter) == 1:
#                 seg_list_list[i] = seg_list_letter[0][1]
#             elif len(seg_list_letter) == 2:
#                 if seg_list_having(seg_list_letter[0][1], seg_list_letter[1][1]):
#                     seg_list_list[i] = seg_list_letter[1][1]
#                 else:
#                     temp = []
#                     temp.extend("过")
#                     temp.insert(len(temp), seg_list_letter[0][1])
#                     temp.extend("作")
#                     temp.insert(len(temp), seg_list_letter[1][1])
#                     seg_list_list[i] = temp
#             elif len(seg_list_letter) == 3:
#                 print(seg_list_list[i])
#             else:
#                 print("多元关系", seg_list_list[i])
#     return return_seg_list(seg_list_list)


# # 返回seg_list_list
# def return_seg_list_list(seg_list):
#     seg_list_list = []
#     seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
#     while seg_list1 != "":
#         seg_list_list.append(seg_list1)
#         seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
#     return seg_list_list


# def return_seg_list(seg_list_list):
#     seg_list = []
#     for i in range(len(seg_list_list)):
#         seg_list.extend(seg_list_list[i])
#         seg_list.extend(",")
#     return seg_list


# def tran_wei_to_fen_bie(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if "为" in seg_list_list[i]:
#             seg_list_list_front = seg_list_list[i][:seg_list_list[i].index("为")]
#             seg_list_list_front.insert(len(seg_list_list_front), "分别")
#             seg_list_list_front.extend(seg_list_list[i][seg_list_list[i].index("为"):])
#             seg_list_list[i] = seg_list_list_front
#     return return_seg_list(seg_list_list)


# def delete_line_and_line(symbol, seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if seg_list_having_0(symbol, seg_list_list[i]):
#             if not seg_list_having_2(["交", "作"], seg_list_list[i]) and len(
#                     find_all_letter_return_side_letter(seg_list_list[i])) >= len(seg_list_list[i]) * 0.5:
#                 seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#                 seg_temp = []
#                 for j in range(len(seg_list_letter)):
#                     seg_temp.insert(len(seg_temp), seg_list_letter[j][1])
#                     seg_temp.extend(",")
#                 seg_list_list[i] = seg_temp
#             else:
#                 seg_list_list_temp = seg_list_list[i][
#                                      :seg_list_list[i].index(
#                                          seg_list_having_0(symbol, seg_list_list[i]))]
#                 seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(
#                     seg_list_having_0(symbol, seg_list_list[i])) + 1:])
#                 seg_list_list[i] = seg_list_list_temp
#     return return_seg_list(seg_list_list)


# def delete_have_other(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     seg_list_list_temp = []
#     for i in range(len(seg_list_list)):
#         for j in range(len(seg_list_list)):
#             if j <= i:
#                 continue
#             else:
#                 if seg_list_list[i] == seg_list_list[j]:
#                     break
#             if j + 1 >= len(seg_list_list):
#                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
#         if i + 1 == len(seg_list_list):
#             seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
#     seg_temp = []
#     for i in range(len(seg_list_list_temp)):
#         seg_temp.extend(seg_list_list_temp[i])
#         seg_temp.extend(",")
#     return seg_temp


# def transition_divide_temp(seg_list_letter, seg_list_angle, seg_list_list_key):
#     temp = []
#     temp.insert(len(temp), seg_list_letter)
#     temp.insert(len(temp), seg_list_list_key)
#     temp.extend(seg_list_angle)
#     temp.extend(",")
#     temp.insert(len(temp), seg_list_letter)
#     temp.extend(",")
#     return temp


# def transition_divide(seg_list):  # 平分
#     seg_list = "".join(seg_list)
#     seg_list = list(jieba.cut(seg_list, cut_all=False))
#     if re.search(".*垂直平分", "".join(seg_list)):
#         seg_list_letter = find_all_letter_return_side_letter(seg_list)
#         if len(seg_list_letter) == 0:
#             return ""
#         elif len(seg_list_letter) == 1:
#             return seg_list
#         symbol_letter = []
#         symbol_point = []
#         for i in range(len(seg_list_letter)):
#             if seg_list_letter[i][0] == 2:
#                 symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
#             else:
#                 symbol_point.insert(len(symbol_point), seg_list_letter[i][1])
#         seg_list_temp = []
#         seg_list_temp.insert(len(seg_list_temp), symbol_letter[0])
#         seg_list_temp.extend("⊥")
#         seg_list_temp.insert(len(seg_list_temp), symbol_letter[1])
#         if len(symbol_point) == 1:
#             seg_list_temp.extend("于")
#             seg_list_temp.insert(len(seg_list_temp), symbol_point[0])
#         seg_list_temp.extend(",")
#         seg_list_temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
#         seg_list = seg_list_temp
#     elif re.search(".*平分", "".join(seg_list)):
#         seg_list_letter = find_all_letter_return_side_letter(seg_list)
#         if len(seg_list_letter) == 0:
#             return ""
#         elif len(seg_list_letter) == 1 and seg_list_letter[0][0] == 2:
#             return seg_list_letter[0][1]
#         else:
#             symbol_angle = []
#             symbol_triangle = []
#             symbol_letter = []
#             for i in range(len(seg_list_letter)):
#                 if seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in "∠":
#                     symbol_angle_temp = ["∠"]
#                     symbol_angle_temp.insert(len(symbol_angle_temp), seg_list_letter[i][1])
#                     symbol_angle.insert(len(symbol_angle), symbol_angle_temp)
#                 elif seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in map_clear_up_keywords:
#                     symbol_triangle_temp = []
#                     symbol_triangle_temp.insert(len(symbol_triangle_temp),
#                                                 seg_list[seg_list.index(seg_list_letter[i][1]) - 1])
#                     symbol_triangle_temp.insert(len(symbol_triangle_temp), seg_list_letter[i][1])
#                     symbol_triangle.insert(len(symbol_triangle), symbol_triangle_temp)
#                 else:
#                     symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
#             if len(symbol_triangle) == 0:
#                 temp = []
#                 if len(symbol_angle) == 0:
#                     if return_re_return([".*互相平分"], "".join(seg_list)):
#                         for i in range(len(symbol_letter)):
#                             for j in range(len(symbol_letter)):
#                                 temp.extend(transition_divide_temp(symbol_letter[i], symbol_letter[j], "平分"))
#                     elif len(symbol_letter) == 2:
#                         temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
#                 else:
#                     if len(symbol_angle) == len(symbol_letter):
#                         for i in range(len(symbol_angle)):
#                             temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
#                     else:
#                         for i in range(len(symbol_letter)):
#                             temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[0], "平分"))
#                 if len(temp) == 0:  # 此处为补丁，即出现∠CAB的平分线
#                     temp = seg_list
#                 seg_list = temp
#             else:
#                 temp = []
#                 if len(symbol_angle) == len(symbol_letter):
#                     for i in range(len(symbol_triangle)):
#                         temp.insert(len(temp), symbol_triangle[i][0])
#                         temp.insert(len(temp), symbol_triangle[i][1])
#                         temp.extend(",")
#                     for i in range(len(symbol_angle)):
#                         temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
#                 elif len(symbol_triangle) == 1 and len(symbol_letter) == 1:
#                     seg_list_temp = seg_list_having_0(symbol_letter[0], symbol_triangle[0][1])
#                     temp.extend(symbol_triangle[0])
#                     temp.extend(",")
#                     temp.extend(symbol_letter)
#                     temp.extend("平分")
#                     temp.extend("∠")
#                     temp.extend(seg_list_temp)
#                     temp.extend(",")
#                     temp.extend(symbol_letter)
#                 seg_list = temp
#     return seg_list


# def transition_S_C(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         seg_temp = []
#         if return_re_return([".*面积", ".*周长"], "".join(seg_list_list[i])):
#             seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             symbol_ = []
#             seg_list_list_temp = []
#             for j in range(len(seg_letter)):  # 求主要的图形
#                 if seg_letter[j][0] >= 3 and \
#                         seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1] in map_clear_up_keywords:
#                     symbol_.insert(len(symbol_), seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1])
#                     symbol_.insert(len(symbol_), seg_letter[j][1])
#                     seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index(seg_letter[j][1]) - 1]
#                     seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) + 1:])
#             seg_letter = find_all_letter_return_side_letter(seg_list_list_temp)
#             seg_num = []
#             for j in range(len(seg_list_list_temp)):
#                 if if_number(seg_list_list_temp[j]) or if_letter(seg_list_list_temp[j]) or \
#                         seg_list_list_temp[j] in symbol_keywords:
#                     seg_num.insert(len(seg_num), seg_list_list_temp[j])
#                     # if j + 1 < len(seg_list_list_temp) and seg_list_list_temp[j + 1] in ["cm", "dm", "m", "km"]:
#                     #     seg_num.insert(len(seg_num),seg_list_list_temp[j + 1])
#             if re.search(".*面积", "".join(seg_list_list[i])):
#                 seg_temp.insert(len(seg_temp), "S")
#             elif re.search(".*周长", "".join(seg_list_list[i])):
#                 seg_temp.insert(len(seg_temp), "C")
#             seg_temp.extend(symbol_)
#             if len(seg_num) != 0:
#                 seg_temp.extend("=")
#                 seg_temp.extend(seg_num)
#             seg_list_list[i] = seg_temp
#         elif seg_list_having("长", seg_list_list[i]):
#             seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             seg_symbol = seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]):]
#             seg_num = []
#             for j in range(len(seg_list_list[i])):
#                 if if_number(seg_list_list[i][j]):
#                     seg_num.insert(len(seg_num), seg_list_list[i][j])
#                     if j + 1 < len(seg_list_list[i]) and seg_list_list[i][j + 1] in ["cm", "dm", "m", "km"]:
#                         seg_num.insert(len(seg_num), seg_list_list[i][j + 1])
#             seg_temp.insert(len(seg_temp), "l")
#             seg_temp.insert(len(seg_temp), seg_letter[0][1])
#             if len(seg_num) != 0:
#                 seg_temp.extend("=")
#                 seg_temp.extend(seg_num)
#             seg_list_list[i] = seg_temp

#     return return_seg_list(seg_list_list)


# def transition_parallel(seg_list):
#     seg_list_letter = find_all_letter_return_side_letter(seg_list)
#     if len(seg_list_letter) == 2:
#         seg_list_temp = []
#         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[0][1])
#         seg_list_temp.insert(len(seg_list_temp), "//")
#         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
#         seg_list_temp.extend(",")
#         seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
#         seg_list = seg_list_temp
#     return seg_list


# def transition_parallel_tran(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if "//" in seg_list_list[i]:
#             seg_temp = seg_list_list[i][:seg_list_list[i].index("//")]
#             seg_temp.insert(len(seg_temp), "平行")
#             seg_temp.extend(seg_list_list[i][seg_list_list[i].index("//") + 1])
#             seg_list_list[i] = seg_temp
#     seg_temp = []
#     for i in range(len(seg_list_list)):
#         seg_temp.extend(seg_list_list[i])
#         seg_temp.extend(",")
#     return seg_temp


# def transition_pause(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if re.search(".*、", "".join(seg_list_list[i])):
#             seg_list_list_temp = []
#             seg_list_list_behind = []
#             seg_list_list_front = seg_list_list[i]
#             while re.search(".*、", "".join(seg_list_list_front)):
#                 seg_list_list_behind = seg_list_list_front[:seg_list_list_front.index("、")]
#                 seg_list_list_front = seg_list_list_front[seg_list_list_front.index("、") + 1:]
#                 seg_list_list_behind = behind_operation(seg_list_list_behind)
#                 seg_list_list_temp.extend(seg_list_list_behind)
#                 seg_list_list_temp.extend(",")
#             seg_list_list_behind = behind_operation(seg_list_list_behind)
#             seg_list_list_temp.extend(seg_list_list_behind)
#             seg_list_list_temp.extend(",")
#             seg_list_list[i] = seg_list_list_temp
#     return return_seg_list(seg_list_list)


# def return_re_return(input_list, seg_list_list):
#     for i in range(len(input_list)):
#         if re.search(input_list[i], "".join(seg_list_list)) is not None:
#             return True
#     return False


# # 切割后续处理的“和”
# def cut_seg_list_and(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if re.search(".*和", "".join(seg_list_list[i])):
#             seg_front = seg_list_list[i][:seg_list_list[i].index("和")]
#             seg_behind = seg_list_list[i][seg_list_list[i].index("和") + 1:]
#             seg_front = behind_operation(seg_front)
#             seg_behind = behind_operation(seg_behind)
#             seg_list_list_temp = seg_front
#             seg_list_list_temp.extend(",")
#             seg_list_list_temp.extend(seg_behind)
#             seg_list_list[i] = seg_list_list_temp
#     return return_seg_list(seg_list_list)


# def behind_operation(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#         if len(seg_list_letter) == 0:  # 不存在关系
#             if seg_list_having("∠", seg_list_list[i]):
#                 for j in range(len(seg_list_list)):
#                     seg_list_list[j] = ""
#             else:
#                 seg_list_list[i] = ""
#         if return_re_return([".*作"], seg_list_list[i]):
#             if re.search(".*于", "".join(seg_list_list[i])) is None:
#                 seg_list_list[i] = guozuo("".join(seg_list_list[i]))
#             else:
#                 seg_list_list[i] = guozuoyu("".join(seg_list_list[i]))
#             seg_list_list[i] = list(jieba.cut(seg_list_list[i], cut_all=False))  # 精确模式切割词句
#         elif re.search(".*交", "".join(seg_list_list[i])) is not None:
#             seg_list_list[i] = transition_hand_over(seg_list_list[i])  # 交
#         elif return_re_return(
#                 ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
#                  "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
#             seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])  # 借助re处理点在线上
#         elif seg_list_having("点", seg_list_list[i]):
#             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             if len(seg_list_list_letter) == 1:
#                 seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("点") + 1:]
#         elif seg_list_having_0(["连接", "连结", "链接", "线段", "若", "设", "直线"], seg_list_list[i]):
#             seg_list_list[i] = delete_line_and_line(["连接", "连结", "链接", "线段", "若", "设", "直线"],
#                                                     seg_list_list[i])  # 将连接AB删除
#         elif return_re_return([".*平行"], seg_list_list[i]):
#             seg_list_list[i] = transition_parallel(seg_list_list[i])
#         elif re.search(".*平分", "".join(seg_list_list[i])):
#             seg_list_list[i] = transition_divide(seg_list_list[i])
#         elif re.search(".*、", "".join(seg_list_list[i])):
#             seg_list_list[i] = transition_pause(seg_list_list[i])
#         elif re.search(".*对角线", "".join(seg_list_list[i])):
#             seg_list_list[i] = transition_diagonal(seg_list_list[i])
#         elif re.search(".*和", "".join(seg_list_list[i])):
#             seg_list_list[i] = cut_seg_list_and(seg_list_list[i])
#         elif return_re_return([".*面积", ".*周长"], seg_list_list[i]) or seg_list_having("长", seg_list_list[i]):
#             seg_list_list[i] = transition_S_C(seg_list_list[i])  # 处理面积和周长
#         elif re.search("的度数", "".join(seg_list_list[i])):
#             seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index("的")]
#         elif re.search(".*高", "".join(seg_list_list[i])):
#             seg_list_list[i] = transition_high(seg_list_list[i])
#         elif seg_list_having(["中"], seg_list_list[i]):
#             seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("中")]
#             seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("中") + 1:])
#             seg_list_list[i] = seg_list_list_temp
#         elif return_re_return([".*两点"], "".join(seg_list_list[i])):
#             seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("两点")]
#             seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("两点") + 1:])
#             seg_list_list[i] = seg_list_list_temp
#         elif return_re_return([".*中点"], "".join(seg_list_list[i])):
#             seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             if len(seg_list_letter) == 2:
#                 seg_list_list[i] = return_the_point_at_line_temp(seg_list_letter[0][1], seg_list_letter[1][1], "中点")
#         elif return_re_return(["垂直.*于"], "".join(seg_list_list[i])):
#             for j in range(len(seg_list_list[i])):
#                 if seg_list_list[i][j] == "垂直":
#                     seg_list_list[i][j] = "⊥"
#         elif len(seg_list_letter) == 1 and not seg_list_having(map_clear_up_keywords, seg_list_list[i]) and \
#                 not seg_list_having(symbol_keywords_main, seg_list_list[i]) and \
#                 not seg_list_having(symbol_keywords, seg_list_list[i]):
#             seg_list_list[i] = seg_list_letter[0][1]

#     seg_list = return_seg_list(seg_list_list)
#     while len(seg_list) != 0 and seg_list[len(seg_list) - 1] == ",":
#         seg_list = seg_list[:len(seg_list) - 1]
#     return seg_list


# def delete_other_point_line(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
#         seg_long = 0
#         for j in range(len(seg_letter)):
#             seg_long += seg_letter[j][0]
#         if seg_long == len("".join(seg_list_list[i])):
#             seg_list_list[i] = ""
#         if return_re_return([".*的长", ".*的延长线"], "".join(seg_list_list[i])) and len(seg_letter) == 1:
#             seg_list_list[i] = ""
#         if len(seg_letter) == 1 and seg_letter[0][1] in seg_list_list[i] and \
#                 seg_list_list[i].index(seg_letter[0][1]) - 1 >= 0 \
#                 and seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]) - 1] in ["∠", "l"] and \
#                 seg_list_list[i].index(seg_letter[0][1]) + 1 == len(seg_list_list[i]):  # 只有单独的角
#             seg_list_list[i] = ""
#         if "∠" in seg_list_list[i] and seg_list_list[i].index("∠") + 1 < len(seg_list_list[i]) and if_number(
#                 seg_list_list[i][seg_list_list[i].index("∠") + 1]):
#             return ""
#     seg_temp = []
#     for i in range(len(seg_list_list)):
#         seg_temp.extend(seg_list_list[i])
#         seg_temp.extend(",")
#     return seg_temp


# # 处理高
# def transition_high(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     seg_list_temp = []
#     for i in range(len(seg_list_list)):
#         if re.search(".*高", "".join(seg_list_list[i])):
#             seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#             seg_list_list_temp = []
#             for j in range(len(seg_list_all_triangle)):
#                 if (len(seg_list_list_letter) == 2 and seg_list_list_letter[0][0] == 2 and
#                         seg_list_having_all(seg_list_list_letter[0][1], seg_list_all_triangle[j][1])):
#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
#                     seg_list_list_temp.extend("是")
#                     seg_list_list_temp.extend(seg_list_all_triangle[j])
#                     seg_list_list_temp.extend("的")
#                     seg_list_list_temp.extend("高")
#                     seg_list_list_temp.extend(",")
#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
#                     seg_list_list_temp.extend(",")
#                 elif len(seg_list_list_letter) == 2 and seg_list_list_letter[1][0] == 2 and \
#                         seg_list_having_all(seg_list_list_letter[1][1], seg_list_all_triangle[j][1]):
#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
#                     seg_list_list_temp.extend("是")
#                     seg_list_list_temp.extend(seg_list_all_triangle[j])
#                     seg_list_list_temp.extend("的")
#                     seg_list_list_temp.extend("高")
#                     seg_list_list_temp.extend(",")
#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
#                     seg_list_list_temp.extend(",")
#                 elif len(seg_list_list_letter) == 1 and seg_list_list_letter[0][0] == 2:
#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
#                     seg_list_list_temp.extend("是")
#                     seg_list_list_temp.extend(seg_list_all_triangle[0])
#                     seg_list_list_temp.extend("的")
#                     seg_list_list_temp.extend("高")
#                     seg_list_list_temp.extend(",")
#                     if "=" in seg_list_list[i]:
#                         seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
#                         seg_list_list_temp.extend("=")
#                         for j in range(len(seg_list_list[i])):
#                             if if_number(seg_list_list[i][j]):
#                                 seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][j])
#                         seg_list_list_temp.extend(",")

#                     seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
#                     seg_list_list_temp.extend(",")
#             seg_list_list[i] = seg_list_list_temp
#     seg_temp = []
#     for i in range(len(seg_list_list)):
#         seg_temp.extend(seg_list_list[i])
#         seg_temp.extend(",")
#     return seg_temp


# def find_all_triangle(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#         for j in range(len(seg_list_list_letter)):
#             if seg_list_list_letter[j][0] >= 3 and seg_list_list[i].index(seg_list_list_letter[j][1]) - 1 >= 0 and \
#                     seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1] in map_clear_up_keywords:
#                 seg_list_temp_temp = []
#                 seg_list_temp_temp.insert(len(seg_list_temp_temp),
#                                           seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1])
#                 seg_list_temp_temp.insert(len(seg_list_temp_temp), seg_list_list_letter[j][1])
#                 if seg_list_temp_temp not in seg_list_all_triangle:  # 防止重复
#                     seg_list_all_triangle.insert(len(seg_list_all_triangle), seg_list_temp_temp)
#     return seg_list_all_triangle


# def dispose_waist_and_diagonal(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     seg_list_list_letter_ABC = []
#     for i in range(len(seg_list_list)):
#         seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
#         seg_list_list_letter_A = []
#         seg_list_list_letter_AB = []
#         for j in range(len(seg_list_list_letter)):
#             if seg_list_list_letter[j][0] == 2:
#                 seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
#             elif seg_list_list_letter[j][0] == 1:
#                 seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
#             else:
#                 seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
#         if re.search(".*对角线", "".join(seg_list_list[i])):
#             if len(seg_list_list_letter_AB) == 0:
#                 seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
#                 if len(seg_list_list_letter_ABC_1) == 4:
#                     wei_temp = seg_list_list[i].index("对角线") + 1
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = "、"
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[3]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     print(seg_list_list[i])
#         if seg_list_having("腰", seg_list_list[i]):
#             if len(seg_list_list_letter_AB) == 0:
#                 seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
#                 if len(seg_list_list_letter_ABC_1) == 3:
#                     wei_temp = re.search(".*对角线", "".join(seg_list_list[i])).end()
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[1]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = "、"
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     print(seg_list_list[i])

#                 if len(seg_list_list_letter_ABC_1) == 4:
#                     wei_temp = seg_list_list[i].index("腰") + 1
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[3]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = "、"
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[2]
#                     seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
#                     print(seg_list_list[i])
#     seg_list = return_seg_list(seg_list_list)
#     return seg_list


# def clean_all_triangle():
#     seg_list_all_triangle.clear()


# def delete_other_line(seg_list):
#     seg_list_list = return_seg_list_list(seg_list)
#     for i in range(len(seg_list_list)):
#         if len(seg_list_list[i]) < 2:
#             for j in range(0, i):
#                 if seg_list_having(seg_list_list[i], seg_list_list[i - j - 1]):
#                     seg_list_list[i] = ""
#                     break
#     seg_list = return_seg_list(seg_list_list)
#     return seg_list


# def cut_word(txt_data):
#     point = []  # 点
#     line = []  # 线
#     triangle = []  # 三角形
#     map_ = []  # 多边形
#     seg_list = list(jieba.cut(txt_data, cut_all=False))  # 精确模式切割词句
#     # print("".join(seg_list))
#     # seg_list = is_half_angle(seg_list)#全角转半角
#     seg_list = conversion_parallel(seg_list)  # 对//进行处理
#     seg_list = remove_pause(seg_list)  # 去除前面的序号
#     seg_list = find_if_have_parallel_and_equal(seg_list)  # 特殊值判断是否有平行且相等
#     seg_list = conversion_symbols(seg_list)  # 将转换为文字
#     seg_list = list(jieba.cut("".join(seg_list), cut_all=False))
#     seg_list = conversion_parallel(seg_list)  # 对//进行处理
#     seg_list = seg_list_transition_side(seg_list)  # lAB = 5 --转变---> 边AB = 5
#     seg_list = delete_prove(seg_list)  # 删除“求证”
#     seg_list = handles_greater_or_less(seg_list)  # 将<=或者>=进行规范化处理
#     seg_list = delete_blank(seg_list)  # 删除空格
#     seg_list = add_de_to_side(seg_list)  # 给长宽高前适当的加"的"
#     seg_list = transition_side(seg_list)  # 将三边等转换成具体字母
#     seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
#     # print("####分别####\t:", "".join(seg_list))
#     seg_list = add_all_shape(seg_list)  # 给所有超过三个字母的字母添加基础形状
#     seg_list = delete_repetition_symbol(seg_list)  # 去除重复的图形
#     seg_list = add_all_letter(seg_list)  # 将单独出现的三角形补全字母
#     seg_list = dispose_waist_and_diagonal(seg_list)  # 处理对角线与腰
#     seg_list = add_all_shape_at_front(seg_list)  # 防止出现三角形ABC\DEF\GHZ   #处理形状在前面
#     seg_list = add_all_shape_at_behind(seg_list)  # 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH   #处理形状在后面
#     seg_list = transition_equal_or_similarity(seg_list)  # 处理连等的情况
#     seg_list = dispose_shi_and_symbol(seg_list)  # 处理四边形ABCD是正方形的情况
#     find_all_triangle(seg_list)  # 记录所有的多边形
#     seg_list = transition_litter_to_super(seg_list)  # 将小写转换为大写(三角形,角)
#     seg_list = add_comma_at_equal(seg_list)  # 在连等后面加上逗号，清除垂足为或者垂足于  AB⊥BD,垂足是B点 -- >  AB⊥BD于B
#     seg_list = cut_zuo_from_seg_list(seg_list)  # 将作从（过A 左AS垂直于DF)提取出来
#     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
#     seg_list = add_to_the_vertical(seg_list)  # 将垂足于A,添加到前一步的句子中
#     # print("".join(seg_list))
#     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
#     seg_list = cut_respect_is_importance(seg_list, "交")  # 处理交
#     # seg_list = transition_S_C(seg_list)  # 处理面积和周长
#     seg_list = tran_wei_to_fen_bie(seg_list)  # 将为转变为 分别为
#     seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
#     seg_list = delete_blank(seg_list)  # 删除空格
#     seg_list = transition_angle_to_angle(seg_list)  # 将符号角平分线更改为角平分线

#     seg_list = behind_operation(seg_list)  # 后续操作
#     seg_list = transition_parallel_tran(seg_list)  # 将//转换为平行
#     seg_list = seg_list_complement(seg_list)  # 补全 角的字母
#     seg_list = transition_triangle_symbol(seg_list, "三角形")  # 将三角形转换为符号

#     # seg_list = delete_have_other(seg_list)  # 去重
#     seg_list = delete_other_line(seg_list)  # 去重
#     # seg_list = delete_other_point_line(seg_list)  # 删去单独的点和线与角
#     seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
#     seg_list = add_end_punctuation(seg_list)  # 给末尾加上;
#     clean_all_triangle()  # 清除记录的多边形

#     with open(txt_output, "a", encoding="utf-8") as fw:
#         fw.write("".join(seg_list))
#         fw.write("\n")
#     print("".join(seg_list))

# def process():
#     setDir(txt_output[:-12])
#     for word in map_keywords:
#         jieba.add_word(word)  # 分词时添加关键词
#     for word in jieba_have_delete:
#         jieba.del_word(word)
#     file = open(txt_input, 'r', encoding="utf-8", errors="ignore")  # 打开文件
#     data = " "
#     while data:
#         data = file.readline()
#         # data = data[:-1]  # 逐行读取文件，也就是提取出每一题
#         if data != "" and data != "\n":
#             t=cut_word(data)
#             # print(data)
#             if(t==False):
#                 file.close()  # 确保文件被关闭
#                 return False
#     file.close()  # 确保文件被关闭


# def setDir(filepath):
#     #没有文件夹就创建，有就清空
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)
#     else:
#         shutil.rmtree(filepath)
#         os.mkdir(filepath)

# def process_text(data):
#     setDir(txt_output[:-12])
#     cut_word(data)



# 以下是2023.2.20的新版本


import re
import jieba
import jieba.posseg as pseg
import sys
import numpy
from jieba import analyse
from config import *
import traceback

jieba_have_delete = ["于点", "交于", "中高", "外作", "相交于", "上且", "腰交于", "线交", "边交于", "交边", "交作",
                     "边于", "线于", "点作"]
map_keywords = ["线", "三角形", "△", "Rt△", "rt△", "直角三角形", "直角△", "等腰三角形", "等腰△", "等边三角形", "等边△",
                "等腰直角三角形", "等腰直角△",
                "等腰Rt△", "四边形", "矩形", "正方形", "长方形", "▭", "平行四边形", "▱", "▰", "梯形", "等腰梯形",
                "直角梯形", "等腰直角梯形", "菱形", "◇",
                "◆", "多边形", "凸多边形", "平行且相等", "<>", "平行于"]  # 有坑不等于
map_clear_up_keywords = ["线", "三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形", "矩形",
                         "正方形", "长方形", "平行四边形",
                         "梯形", "等腰梯形", "直角梯形", "菱形", "多边形", "凸多边形", "五边形", "六边形", "七边形",
                         "高"]
map_clear_up_keywords_value = [0, 1, 2.01, 2.02, 2.03, 4.03, 5, 8.01, 8.04, 8.03, 10.02, 6.01, 7.02, 7.03, 10.01, 9, 10,
                               11, 12, 13]
map_clear_up_keywords_error = [14.02, 14.04, 14.05, 14.05, 15.03, 15.04, 15.05, 15.06, 15.06, 15.07, 16.02, 16.03,
                               17.03, 17.04, 17.04, 17.05, 18.02, 18.03, 23, 24, 25, 0]  # 当权值相加时不可能出现这类情况
# print(sorted(list(map_clear_up_keywords_error)))
symbol_keywords = ["∠", "°", "+", "-", "/", "*", "·", "^", "'", "√", "≤", "≥"]
symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]  # 留坑 三角形的全等无法实现
side = ["三边", "四边", "五边", "六边"]
the_capital_form_of_a_chinese_number = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
seg_list_all_triangle = []


def if_letter(seg_list):  # 检查是否为英文
    return seg_list.encode('utf-8').isalpha()


def if_number(num):  # 检测是否为数字
    if len(num) == 0:
        return False
    for i in range(len(num)):
        if '0' <= num[i] <= '9' or num[i] == ".":
            continue
        else:
            return False
    return True


def if_number_and_letter(seg_list):
    for i in range(len(seg_list)):
        if if_letter(seg_list[i]) or if_number(seg_list[i]):
            continue
        else:
            return False
    return True


def delete_blank(seg_list):  # 删除空格
    j = 0
    while j == 0:
        if len(seg_list) == 0:
            break
        for i in range(len(seg_list)):
            if seg_list[i] == " " or seg_list[i] == "":
                seg_list1 = seg_list[i + 1:]
                seg_list2 = seg_list[:i]
                seg_list = seg_list2 + seg_list1
                break
            i += 1
            if i >= (len(seg_list) - 1):
                j += 1
    return seg_list


def conversion_parallel(seg_list):  # 对//进行处理
    j = 0
    while j == 0:
        for i in range(len(seg_list) - 1):
            if seg_list[i] == "/" and seg_list[i + 1] == "/":
                seg_list1 = seg_list[i + 2:]
                seg_list2 = seg_list[:i]
                seg_list = seg_list2 + ["//"] + seg_list1
                break
            if seg_list[i] == "\\" and seg_list[i + 1] == "\\":
                seg_list1 = seg_list[i + 2:]
                seg_list2 = seg_list[:i]
                seg_list = seg_list2 + ["//"] + seg_list1
                break
            i += 1
            if i >= (len(seg_list) - 1):
                j += 1
    return seg_list


# 将三边\四边给去掉
def transition_side(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if seg_list_having(side, seg_list_list[i]):
            seg_list_temp = return_how_many_side(seg_list_having_0(side, seg_list_list[i]))
            seg_anger_temp = []
            for j in range(seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i]))):
                # 从后面往前面找
                if if_letter(
                        seg_list_list[i][seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]):
                    seg_list_anger = seg_list_list[i][
                        seg_list_list[i].index(seg_list_having_0(side, seg_list_list[i])) - 1 - j]
                    if len(seg_list_anger) == seg_list_temp:
                        seg_anger = []
                        for k in range(len(seg_list_anger)):
                            seg_anger.insert(len(seg_list_anger), seg_list_anger[k])
                        for k in range(len(seg_list_anger)):
                            seg_list_anger_temp = ""
                            if k + 1 != len(seg_list_anger):
                                seg_list_anger_temp += seg_list_anger[k]
                                seg_list_anger_temp += seg_list_anger[k + 1]
                                seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
                            else:
                                seg_list_anger_temp += seg_list_anger[0]
                                seg_list_anger_temp += seg_list_anger[k]
                                seg_anger_temp.insert(len(seg_anger_temp), seg_list_anger_temp)
                            if len(seg_anger_temp) != len(seg_list_anger) * 2 - 1:
                                seg_anger_temp.insert(len(seg_anger_temp), "、")

            seg_list_ = seg_list_list[i]
            seg_list_front = seg_list_[:seg_list_.index(seg_list_having_0(side, seg_list_))]
            seg_list_behind = seg_list_[seg_list_.index(seg_list_having_0(side, seg_list_)) + 1:]
            seg_list_front.extend(",")
            seg_list_front.extend(seg_anger_temp)
            seg_list_front.extend(seg_list_behind)
            seg_list_list[i] = seg_list_front
    seg_list_t = []
    for i in range(len(seg_list_list)):
        seg_list_t.extend(seg_list_list[i])
        seg_list_t.extend(",")
    return seg_list_t


def conversion_symbols(seg_list):  # 将图形转换为汉字
    for i in range(len(seg_list)):
        temp = seg_list[i]
        if seg_list[i] in ["Rt", "rt"] and seg_list[i + 1] in ["△", "三角形"]:
            temp = "".join("直角")
        elif seg_list[i] in ["Rt△", "rt△"]:
            temp = "".join("直角三角形")
        elif seg_list[i] in ["▱", "▰"]:
            temp = "".join("平行四边形")
        elif seg_list[i] in ["▭", "▯", "▮"]:
            temp = "".join("长方形")
        elif seg_list[i] in ["□", "■", "▪", "▫", "◻", "◼", "◽", "◾"]:
            temp = "".join("正方形")
        elif seg_list[i] in ["◇", "◆"]:
            temp = "".join("菱形")
        elif seg_list[i] in ["⊿"]:
            temp = "".join("直角三角形")
        elif seg_list[i] in ["！"]:
            temp = "".join("!")
        elif seg_list[i] in ["＜"]:
            temp = "".join("<")
        elif seg_list[i] in ["＝"]:
            temp = "".join("=")
        elif seg_list[i] in ["≦", "≮"]:
            temp = "".join("≤")
        elif seg_list[i] in ["≧", "≯"]:
            temp = "".join("≥")
        elif seg_list[i] in ["△"]:
            temp = "".join("三角形")
        elif seg_list[i] in ["角"]:
            temp = "".join("∠")
        elif seg_list[i] in ["等腰直角梯形"]:
            temp = "".join("长方形")
        elif seg_list[i] in ["等于"]:
            temp = "".join("=")
        elif seg_list[i] in ["度"] and if_number(seg_list[i - 1]):
            temp = "".join("°")
        elif seg_list[i] in ["正三角形"]:
            temp = "".join("等边三角形")
        elif seg_list[i] in ["想交"]:
            temp = "".join("相交")
        elif seg_list[i] in ["想交于"]:
            temp = "".join("相交于")
        elif seg_list[i] in ["重点"]:
            temp = "".join("中点")
        elif seg_list[i] in ["均"]:
            temp = "".join("都")
        elif seg_list[i] in ["各"]:
            temp = "".join("分别")
        elif seg_list[i] in ["读"]:
            temp = "".join("°")
        elif seg_list[i] in ["∥", "平行于"]:
            temp = "".join("//")
        elif seg_list[i] in ["已知", "使得", "使", "且有", "并且", "满足", "且", "截取", "∶", "：", "，", "。", "；", "?",
                             "？", "(",
                             ")", "（", "）", ";"]:
            # 将毫无意义的词组删去 将中文符号修改为英文的逗号
            temp = "".join(",")
        elif seg_list[i] in ["μm"]:
            temp = "".join("微米")
        elif seg_list[i] in ["nm"]:
            temp = "".join("纳米")
        elif seg_list[i] in ["mm"]:
            temp = "".join("毫米")
        elif seg_list[i] in ["cm"]:
            temp = "".join("厘米")
        elif seg_list[i] in ["dm"]:
            temp = "".join("分米")
        elif seg_list[i] in ["km"]:
            temp = "".join("千米")
        elif seg_list[i] in ["m"]:
            temp = "".join("米")
        seg_list[i] = temp
    return seg_list


# 将角和三角形等的字母大写
def transition_litter_to_super(seg_list):
    for i in range(len(seg_list)):
        if if_letter(seg_list[i]) and len(seg_list[i]) > 2 and (
                seg_list[i - 1] in "∠" or seg_list[i - 1] in map_clear_up_keywords):
            seg_list_letter = str(seg_list[i])
            seg_list_letter = seg_list_letter.upper()
            seg_list[i] = seg_list_letter
    return seg_list


# 补全交的符号
def seg_list_complement(seg_list):
    seg_list_list_temp = []  # 记录三角形的个数
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        # 查询所有的三角形以上的图形，并且合并同类项
        if seg_list_having_0(map_clear_up_keywords, seg_list_list[i]):
            seg_list_list_i_1 = seg_list_list[i].index(seg_list_having_0(map_clear_up_keywords, seg_list_list[i]))
            if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
                    seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) > 2 and \
                    seg_list_list[i][seg_list_list_i_1 + 1] not in seg_list_list_temp:
                seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][seg_list_list_i_1 + 1])
    if len(seg_list_list_temp) == 0:
        return seg_list  # 无三角形等图形，无法进行识别 补全
    else:
        for i in range(len(seg_list_list)):
            if "∠" in seg_list_list[i]:  # 如果存在∠且∠后的字母长度为1
                seg_list_list_i_1 = seg_list_list[i].index("∠")
                if seg_list_list_i_1 + 1 < len(seg_list_list[i]) and if_letter(
                        seg_list_list[i][seg_list_list_i_1 + 1]) and len(seg_list_list[i][seg_list_list_i_1 + 1]) == 1:
                    angele_if_in_two_symbol = 0  # 判断是否存在多个图形里面
                    angele_in_this_symbol = 0  # 记录当前字母所在的图形的下标
                    for j in range(len(seg_list_list_temp)):
                        if seg_list_list[i][seg_list_list_i_1 + 1] in seg_list_list_temp[j]:
                            if angele_if_in_two_symbol != 0:
                                angele_if_in_two_symbol += 1
                                break  # 如果同时出现在多个图形中也无法 补全
                            else:
                                angele_if_in_two_symbol += 1
                                angele_in_this_symbol = j
                    if angele_if_in_two_symbol != 1:  # 可能出现角不在前面出现的图形中，也无法处理
                        continue
                    else:
                        tran_angle = ""
                        letter = re.findall('[A-Za-z]', seg_list_list_temp[angele_in_this_symbol])
                        if seg_list_list[i][seg_list_list_i_1 + 1] in letter:
                            if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1 < 0:  # 最前面
                                tran_angle += letter[len(letter) - 1]
                            else:
                                tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) - 1]
                            tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1])]
                            if letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1 >= len(letter):  # 最后面
                                tran_angle += letter[0]
                            else:
                                tran_angle += letter[letter.index(seg_list_list[i][seg_list_list_i_1 + 1]) + 1]
                        seg_list_list[i][seg_list_list_i_1 + 1] = tran_angle
    return return_seg_list(seg_list_list)


# lAB = 5 --转变---> 边AB = 5 暂时不知道有什么用
def seg_list_transition_side(seg_list):
    seg_list_temp = 0
    while seg_list_temp == 0:
        for i in range(len(seg_list)):
            if len(seg_list[i]) == 3 and if_letter(seg_list[i]) and seg_list[i][0] == "l":  # lAB
                seg_list_behind = seg_list[i][1:]  # AB
                seg_list[i] = seg_list_behind
                seg_list_front = seg_list[:i]
                seg_list_behind = seg_list[i:]
                seg_list_front.extend("边")
                seg_list_front.extend(seg_list_behind)
                seg_list = seg_list_front
                break
            if i + 1 == len(seg_list):
                seg_list_temp += 1
    # print("".join(seg_list))
    return seg_list


# 去除序号
def remove_pause(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        seg_list_list_temp = seg_list_list[i]
        if_change = 1
        for j in range(len(seg_list_list[i])):
            if if_number(seg_list_list[i][j]) or seg_list_list[i][j] in ["提", "题"]:
                seg_list_list_temp = seg_list_list_temp[j + 1:] if j >= len(seg_list_list[i]) - 1 else ","
            else:
                if_change = 0
                break
        if if_change == 1:
            seg_list_list[i] = seg_list_list_temp
    seg_list = []
    for i in range(len(seg_list_list)):
        seg_list.extend(seg_list_list[i])
        seg_list.extend(",")
    return seg_list


# 删除求证
def delete_prove(seg_list):
    seg_list_front = []
    seg_txt = ["证明", "求解", "求证", "求", "有", "如图", "如图所示"]
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if seg_list_having(seg_txt, seg_list_list[i]):
            seg_list_list_wei = seg_list_having_0(seg_txt, seg_list_list[i])
            seg_list_front = seg_list_list[i][:seg_list_list[i].index(seg_list_list_wei)]
            seg_list_front.extend(",")
            if seg_list_list[i].index(seg_list_list_wei) + 1 < len(seg_list_list[i]) and \
                    if_number(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1]):
                seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 2:])
            else:
                seg_list_front.extend(seg_list_list[i][seg_list_list[i].index(seg_list_list_wei) + 1:])
            seg_list_list[i] = seg_list_front
    return return_seg_list(seg_list_list)


# 将大于或者小于或者不等于归一化   <=  --->  ≤
def handles_greater_or_less(seg_list):
    seg_temp = 0
    while seg_temp == 0:
        for i in range(len(seg_list)):
            if seg_list[i] in ["<", ">", "!"] and i + 1 < len(seg_list) and seg_list[i + 1] in "=":
                seg_list_front = seg_list[:i]
                seg_list_behind = seg_list[i + 2:]
                if seg_list[i] in "<":
                    seg_list_front.insert(len(seg_list_front), "≤")
                elif seg_list[i] in ">":
                    seg_list_front.insert(len(seg_list_front), "≥")
                elif seg_list[i] in "!":
                    seg_list_front.insert(len(seg_list_front), "!=")
                seg_list_front.extend(seg_list_behind)
                seg_list = seg_list_front
                break
            if i + 1 == len(seg_list):
                seg_temp = 1
    return seg_list


# 给末尾加上;
def add_end_punctuation(seg_list):
    for i in range(len(seg_list)):
        if seg_list[len(seg_list) - 1 - i] in [".", ",", ";", "?", "？"] and \
                seg_list[len(seg_list) - 2 - i] in [".", ",", ";", "?", "？"]:
            continue
        else:
            seg_list = seg_list[:len(seg_list) - 1 - i]
            seg_list.append(";")
            return seg_list
    return seg_list


# 按照逗号或者句号分句
def cut_clause(seg_list):
    for i in range(len(seg_list) - 1):
        if seg_list[i] in [",", ".", "，", "。", ":", "：", "、"]:
            seg_list1 = seg_list[
                        i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ['.', ','] else len(seg_list)]
            seg_list2 = seg_list[:i]
            return seg_list2, seg_list1
    return seg_list, ""


# 对顿号进行切割
def cut_clause_slight_pause(seg_list):
    for i in range(len(seg_list) - 1):
        if seg_list[i] in ["、", "和", "与", "."]:
            seg_list1 = seg_list[
                        i + 1:len(seg_list) - 1 if seg_list[len(seg_list) - 1] in ["、", "和", "与", "."] else len(
                            seg_list)]
            seg_list2 = seg_list[:i]
            return seg_list2, seg_list1
    return seg_list, ""


# 给长宽高边长面积周长前适当加"的"
def add_de_to_side(seg_list):
    seg_temp = 0
    while seg_temp == 0:
        for i in range(len(seg_list)):
            if seg_list[i] in ["长", "宽", "高", "边长", "周长", "面积"]:
                if i == 0 or seg_list[i - 1] in [",", "."] or seg_list[i - 1] in ["的"] or seg_list[i - 1] in ["是"]:
                    continue
                elif i > 1 and if_letter(seg_list[i - 1]) and len(seg_list[i - 1]) > 1:  # ABC长AD为
                    seg_list_front = seg_list[:i]
                    seg_list_front.insert(i, "的")
                    seg_list_front.extend(seg_list[i:])
                    seg_list = seg_list_front
                    break
                elif i > 2 and (seg_list[i - 1] in ["中"] and if_letter(seg_list[i - 2])) and len(seg_list[i - 2]) > 1:
                    seg_list_front = seg_list[:i]
                    seg_list_front.insert(i, "的")
                    seg_list_front.extend(seg_list[i:])
                    seg_list = seg_list_front
                    break
            if i + 1 == len(seg_list):
                seg_temp = 1
    # print(seg_list)
    return seg_list


# 将作从（过A 作AS垂直于DF)提取出来
def cut_zuo_from_seg_list(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if seg_list_having(symbol_keywords_main, seg_list_list[i]) and "作" in seg_list_list[i]:
            seg_list_front = seg_list_list[i][
                             :seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i]))]  # 垂直之前
            seg_list_behind = seg_list_list[i][
                              seg_list_list[i].index(seg_list_having(symbol_keywords_main, seg_list_list[i])):]  # 垂直之后
            seg_list_front_behind = seg_list_front[seg_list_front.index("作"):]  # 作之后，找后面的一个词组
            seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)  # 找到词组
            seg_list_front.extend(",")  # 过A 作AS，
            seg_list_front.insert(len(seg_list_front), seg_list_front_behind_letter[0][1])  # 过A 作AS，AS
            seg_list_front.extend(seg_list_behind)  # 过A 作AS，AS垂直DF
            seg_list_list_front = seg_list_list[:i]
            seg_list_list_behind = seg_list_list[i + 1:]
            seg_list_list_front.insert(len(seg_list_list_front), seg_list_front)
            seg_list_list_front.extend(seg_list_list_behind)
            seg_list_list = seg_list_list_front
    seg_list = []
    for i in range(len(seg_list_list)):
        seg_list.extend(seg_list_list[i])
        seg_list.extend(",")
    # print("".join(seg_list))
    return seg_list


# 将垂直后加一个逗号切分
def add_comma_at_equal(seg_list):
    seg_list_temp = 0
    while seg_list_temp == 0:
        for i in range(len(seg_list)):
            if i + 1 == len(seg_list):
                seg_list_temp = 1
            if seg_list[i] in symbol_keywords_main:
                for j in range(1, 3):
                    if i + j > len(seg_list):
                        break
                    if seg_list[i + j] not in map_clear_up_keywords and seg_list[
                        i + j] not in symbol_keywords and not if_number_and_letter(seg_list[i + j]) and seg_list[
                        i + j] not in ["于", "点"]:

                        if seg_list[i + j] != ",":
                            seg_list_front = seg_list[:i + j]
                            seg_list_behind = seg_list[i + j:]
                            seg_list_front.extend(",")
                            seg_list_front.extend(seg_list_behind)
                            seg_list_temp1 = 1
                            seg_list = seg_list_front
                            break
                        else:
                            break
    return seg_list


# 根据输入不同的symbol进行类似连等的分割
def find_which_equal(seg_list, symbol):
    equal_value = []  # 存储当前段落的所有的等式的元素
    seg_list1_front = []
    seg_list2_front = []
    seg_list2_behind = []
    seg_list_behind_behind_letter = []
    seg_list_behind_behind_other = []
    seg_list_front_front_other = []
    seg_list_front_behind_other = []
    seg_list1 = seg_list[:seg_list.index(symbol)]
    # 梯形ABCD的面积=EF·AB
    if len(seg_list1) > 2:
        if "作" in seg_list:  # 作三角形ABC的AD垂直CV
            seg_list1_front = seg_list1[:seg_list1.index("作")]
            seg_list1_behind = seg_list1[seg_list1.index("作"):]
            if "的" in seg_list1_behind:
                seg_list_behind_front = seg_list1_behind[:seg_list1_behind.index("的")]
                seg_list1_behind_behind = seg_list1_behind[seg_list1_behind.index("的"):]
                seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
                if len(seg_list_behind_behind_letter) == 0:
                    seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
                seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
            else:
                seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind)
                seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
        elif "的" in seg_list1:
            seg_list_behind_front = seg_list1[:seg_list1.index("的")]
            seg_list1_behind_behind = seg_list1[seg_list1.index("的"):]
            seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1_behind_behind)
            if len(seg_list_behind_behind_letter) == 0:
                seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_front)
            seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
        else:
            seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list1)
            seg_list_behind_behind_other = find_front_and_behind_other(seg_list1, seg_list_behind_behind_letter)
        seg_list_front_front_other = seg_list_behind_behind_other[0]  # 存储前半部分的其他部分
        seg_list_front_behind_other = seg_list_behind_behind_other[1]  # 存储字母后半部分的其他部分
    seg_list2 = seg_list[seg_list.index(symbol) + 1:]
    if len(seg_list_behind_behind_letter) > 0:
        equal_value.append(dispose_cut_front_equal(seg_list_behind_behind_letter[0][1]))  # 处理等号前半段
    else:
        equal_value.append(dispose_cut_front_equal(seg_list1))
    while symbol in seg_list2:
        seg_list0 = seg_list2.copy()
        seg_list1 = seg_list0[:seg_list0.index(symbol)]  # 等号前半段
        seg_list2 = seg_list0[seg_list0.index(symbol) + 1:]  # 取等号后半段
        equal_value.append(dispose_cut_front_equal(seg_list1))  # 处理等号前半段
    if len(seg_list2) > 1:  # 过D作DE⊥BC于E
        for i in range(len(seg_list2)):
            if if_number_and_letter(seg_list2[i]):
                seg_list2_letter = seg_list2[i]
                seg_list2_front = seg_list2[:i]
                seg_list2_behind = seg_list2[i + 1:]
                seg_list2 = seg_list2_letter
                break

    equal_value.append(dispose_cut_front_equal(seg_list2))  # 处理等号后半段
    equal_value_all = []
    for i in range(len(equal_value) - 1):
        j = i + 1
        while j < len(equal_value):
            equal_value_all.extend(seg_list_front_front_other)
            equal_value_all.extend(equal_value[i])
            equal_value_all.extend(seg_list_front_behind_other)
            equal_value_all.append(symbol)
            if j + 1 == len(equal_value):
                equal_value_all.extend(seg_list2_front)
            equal_value_all.extend(equal_value[j])
            if j + 1 == len(equal_value):
                equal_value_all.extend(seg_list2_behind)
            equal_value_all.append(",")
            j += 1
    return equal_value_all


# 处理使用等号分出来的前半段,存在角\边\点种情况
def dispose_cut_front_equal(seg_list1):
    Str_value = [""]
    for i in range(len(seg_list1)):
        if seg_list1[i] in symbol_keywords or if_number_and_letter(seg_list1[i]) or seg_list1[i] \
                in map_clear_up_keywords:
            if if_letter(seg_list1[i]) and if_letter(Str_value[len(Str_value) - 1]) and len(Str_value) > 0:
                Str_value[len(Str_value) - 1] += (seg_list1[i])
            else:
                Str_value.append(seg_list1[i])
    Str_value = delete_blank(Str_value)
    return Str_value


# 提取当前段落的所有英文字母
def dispose_cut_front_equal_letter(seg_list1):
    Str_value = [""]
    for i in range(len(seg_list1)):
        if if_letter(seg_list1[i]):
            Str_value.append(seg_list1[i])
    Str_value_true = "".join(Str_value)
    return Str_value_true


# 查询当前符号symbol是否在语句seg_list中
def seg_list_having(symbol, seg_list):
    if len(seg_list) == 0:
        return False
    for i in range(len(symbol)):
        if symbol[i] in seg_list:
            return symbol[i]
    return False


# 查看字符symbol是否有任意一个在字符串中,如果没有返回空字符,否则存在字符.
def seg_list_having_0(symbol, seg_list):
    if len(seg_list) == 0:
        return ""
    for i in range(len(symbol)):
        if symbol[i] in seg_list:
            return symbol[i]
    return ""


# seg_list[][]中有一点在symbol中的一个值
def seg_list_having_1(symbol, seg_list):
    if len(seg_list) == 0:
        return False
    for i in range(len(seg_list)):
        for j in range(len(seg_list[i])):
            if seg_list[i][j] in symbol:
                return True
    return False


# symbol与seg_list[][]中存在很小一点的相等
def seg_list_having_2(symbol, seg_list):
    if len(seg_list) == 0:
        return False
    for i in range(len(symbol)):
        for j in range(len(seg_list)):
            for k in range(len(seg_list[j])):
                if symbol[i] == seg_list[j][k]:
                    return True
    return False


def seg_list_having_all(symbol, seg_list):
    if len(seg_list) == 0:
        return False
    for i in range(len(symbol)):
        if symbol[i] in seg_list:
            continue
        else:
            return False
    return True


# 在处理分别中的辅助函数,查看b-b-l的低2列是否是数字
def seg_list_behind_behind_letter_if_letter(seg_letter):
    for i in range(len(seg_letter)):
        if not if_number(seg_letter[i][1]):
            break
        if i + 1 == len(seg_letter):
            return True
    return False


# 判断是几边形的图形
def match_how_many_side(seg_list):
    len_seg_list = len(seg_list)
    if len_seg_list == 1:
        return "点"
    elif len_seg_list == 2:
        return "边"
    elif len_seg_list == 3:
        return "三角形"
    elif len_seg_list == 4:
        return "四边形"
    elif len_seg_list == 5:
        return "五边形"
    elif len_seg_list == 6:
        return "六边形"
    else:
        return "多边形"


# 返回两个三角形的边数
def return_how_many_side_symbol(symbol1, symbol2):
    triangle = ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形"]
    quadrangle = ["四边形", "矩形", "正方形", "长方形", "平行四边形", "梯形", "等腰梯形", "直角梯形", "菱形"]
    polygon = ["五边形", "六边形", "七边形", "多边形", "凸多边形"]
    symbol1_angle = 0
    symbol2_angle = 0
    if symbol1 in triangle:
        symbol1_angle = 3
    elif symbol1 in quadrangle:
        symbol1_angle = 4
    else:
        symbol1_angle = 10
    if symbol2 in triangle:
        symbol2_angle = 3
    elif symbol2 in quadrangle:
        symbol2_angle = 4
    else:
        symbol2_angle = 10
    return symbol1_angle, symbol2_angle


def return_how_many_side(symbol1):
    side = ["三边", "四边", "五边", "六边", "七边"]
    symbol1_angle = 0
    symbol2_angle = 0
    if symbol1 in "三边":
        symbol1_angle = 3
    elif symbol1 in "四边":
        symbol1_angle = 4
    elif symbol1 in "五边":
        symbol1_angle = 5
    elif symbol1 in "六边":
        symbol1_angle = 6
    elif symbol1 in "七边":
        symbol1_angle = 7
    else:
        symbol1_angle = 10

    return symbol1_angle


def return_how_many_number(symbol, the_capital_form_of_a_chinese_number):
    return the_capital_form_of_a_chinese_number.index(symbol) + 1


# 查询当前语句是否存在形状,并且形状位置在字母前面
def seg_list_having_symbol_letter(symbol, seg_list, letter):
    for i in range(len(seg_list)):
        if seg_list[i] in symbol and i + 1 == seg_list.index(letter):
            return symbol[symbol.index(seg_list[i])]
    return ""


# 特征值判断是否存在平行且相等的情况
def find_if_have_parallel_and_equal(seg_list):
    Str = [""]
    if "平行且相等" in seg_list:
        seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
        while seg_list1 != "":
            if "平行且相等" in seg_list1:  # 如果平行且相等在当前分句里面
                seg_list00 = seg_list1.copy()
                seg_list01 = seg_list00[:seg_list00.index("平行且相等")]
                seg_list02 = seg_list00[seg_list00.index("平行且相等") + 1:]
                seg_list_value_front = dispose_cut_front_equal_letter(seg_list01)
                seg_list_value_behind = dispose_cut_front_equal_letter(seg_list02)
                seg_list1 = [seg_list_value_front, "//", seg_list_value_behind, ",", seg_list_value_front, "=",
                             seg_list_value_behind, ","]
            Str.extend(seg_list1)
            Str.extend(",")
            if "平行且相等" not in seg_list2:
                Str.extend(seg_list2)
                return Str
            seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
    return seg_list


# 对字母进行形状配对,当形状在前面时
def add_all_shape_at_front(seg_list):
    len_seg_list = len(seg_list)
    Str = []
    seg_list_temp_overall = []
    seg_list_temp_front = []
    type_temp = []  # 储存形状
    type_value = []  # 储存字母
    if seg_list_having("、", seg_list):
        seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
        while seg_list1 != "":
            if seg_list_having("、", seg_list1) and len(seg_list1[seg_list1.index("、") - 1]) > 2:  # 顿号前的字母长度大于三才处理
                seg_list10, seg_list11 = cut_clause_slight_pause(seg_list1)  # 按照顿号进行切割           #可能出现三个字母的代码,露马脚了

                while seg_list10 != "":
                    type_value.insert(len(type_value), dispose_cut_front_equal_letter(seg_list10))  # 提取英文字母
                    type_temp.insert(len(type_temp), seg_list_having_symbol_letter(map_clear_up_keywords, seg_list10,
                                                                                   dispose_cut_front_equal_letter(
                                                                                       seg_list10)))  # 提取字母类型
                    seg_list10, seg_list11 = cut_clause_slight_pause(seg_list11)  # 按照顿号进行切割
                if len(type_temp[0]) > 0:  # 有标签的情况下
                    seg_list_temp_front = seg_list1[:seg_list1.index(type_value[0]) - 1]
                    seg_list_temp_behind = seg_list1[seg_list1.index(type_value[len(type_value) - 1]) + 1:]
                    for i in range(len(type_temp)):
                        if len(type_temp[i]) > 0:
                            seg_list_temp_front.insert(len(seg_list_temp_front),
                                                       find_the_max_symbol(type_temp[0], type_temp[i], type_value[i]))
                        else:
                            seg_list_temp_front.insert(len(seg_list_temp_front), type_temp[0])
                        seg_list_temp_front.insert(len(seg_list_temp_front), type_value[i])
                        if i < len(type_temp) - 1:
                            seg_list_temp_front.insert(len(seg_list_temp_front), "、")
                    seg_list_temp_front.extend(seg_list_temp_behind)  # 将三角形ABC、DEF、GHZ,拼接
                    # print(seg_list_temp_front)
            if len(seg_list_temp_front) > 0:
                seg_list_temp_overall.extend(seg_list_temp_front)
                seg_list_temp_front = []
            else:
                seg_list_temp_overall.extend(seg_list1)
            seg_list_temp_overall.extend(",")
            # print(dispose_cut_front_equal_letter(seg_list1))
            seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
        # print("seg_list_temp_overall",seg_list_temp_overall)
        # print("".join(seg_list_temp_overall))
        return seg_list_temp_overall
    return seg_list


# 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH
def add_all_shape_at_behind(seg_list):
    Str = []
    seg_list_temp = []
    type_temp = []
    type_value = []
    if seg_list_having(["均为", "都"], seg_list):
        seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
        while seg_list1 != "":
            if seg_list_having(["均为", "都"], seg_list1):
                seg_list_symbol_1 = seg_list_having(["均为", "都"], seg_list1)
                seg_list00 = seg_list1[:seg_list1.index(seg_list_symbol_1)]  # 提取"都"前面的句子进入循环
                seg_list20 = seg_list1[seg_list1.index(seg_list_symbol_1) + 1:]  # 提取都后面的句子
                seg_list_symbol_behind = seg_list_having(map_clear_up_keywords, seg_list20)  # 提出"均为"后的图形
                seg_list_letter20 = dispose_cut_front_equal_letter(seg_list20)  # 查看图形后面是否跟着字母
                seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list00)
                while seg_list1_0 != "":
                    seg_list_symbol_front = seg_list_having_0(map_clear_up_keywords, seg_list1_0)  # 提出第一个图形的类型
                    type_temp.insert(len(type_temp), seg_list_symbol_front)
                    seg_list_letter10 = dispose_cut_front_equal_letter(seg_list1_0)
                    type_value.insert(len(type_value), seg_list_letter10)
                    seg_list1_0, seg_list1_1 = cut_clause_slight_pause(seg_list1_1)
                for i in range(len(type_temp)):
                    Str.insert(len(Str), type_temp[i])
                    Str.insert(len(Str), type_value[i])
                    Str.insert(len(Str), "是")
                    Str.insert(len(Str), seg_list_symbol_behind)
                    Str.insert(len(Str), seg_list_letter20)
                    Str.insert(len(Str), ",")
                seg_list_temp.extend(Str)
            else:
                seg_list_temp.extend(seg_list1)
                seg_list_temp.extend(",")
            seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照顿号与"与"分段
        return seg_list_temp
    else:
        return seg_list


def add_all_letter(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    temp = []
    for i in range(len(seg_list_list)):
        for j in range(len(seg_list_list[i])):
            if if_letter(seg_list_list[i][j]) and len(seg_list_list[i][j]) > 2 and seg_list_list[i][j - 1] != "∠":
                temp.insert(len(temp), seg_list_list[i][j])
            if seg_list_list[i][j] in ["三角形", "直角三角形", "等腰三角形", "等边三角形", "等腰直角三角形", "四边形",
                                       "矩形", "正方形", "长方形", "平行四边形",
                                       "梯形", "等腰梯形", "直角梯形", "菱形"] and j + 1 < len(seg_list_list[i]) and \
                    not if_letter(seg_list_list[i][j + 1]):
                if seg_list_having_2("三", seg_list_list[i][j]):
                    for k in range(len(temp)):
                        if len(temp[len(temp) - 1 - k]) == 3:
                            seg_list_list_temp = seg_list_list[i][:j + 1]
                            seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
                            seg_list_list_temp.extend(seg_list_list[i][j + 1:])
                            seg_list_list[i] = seg_list_list_temp
                            break
                else:
                    for k in range(len(temp)):
                        if len(temp[len(temp) - 1 - k]) > 3:
                            seg_list_list_temp = seg_list_list[i][:j + 1]
                            seg_list_list_temp.insert(len(seg_list_list_temp), temp[len(temp) - 1 - k])
                            seg_list_list_temp.extend(seg_list_list[i][j + 1:])
                            seg_list_list[i] = seg_list_list_temp
                            break
                break
    return return_seg_list(seg_list_list)


# 对其余的所有的多个连续字母进行基础形状赋值
def add_all_shape(seg_list):
    seg_list_if = 0
    while seg_list_if == 0:
        seg_list_temp = []
        for i in range(len(seg_list)):
            if if_letter(seg_list[i]) and len(seg_list[i]) > 2:
                seg_list_front = seg_list[:i]
                seg_list_behind = seg_list[i + 1:]
                if len(seg_list_front) == 0:  # ABC打头
                    seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
                    seg_list_temp.insert(len(seg_list_temp), seg_list[i])
                    seg_list_temp.extend(seg_list_behind)
                    seg_list = seg_list_temp
                    seg_list_temp = []
                    break
                else:
                    if seg_list[i - 1] in map_clear_up_keywords or seg_list[i - 1] == "∠":  # 字母前面有形状或者有角
                        continue
                    else:
                        seg_list_temp.extend(seg_list_front)
                        seg_list_temp.insert(len(seg_list_temp), match_how_many_side(seg_list[i]))
                        seg_list_temp.insert(len(seg_list_temp), seg_list[i])
                        seg_list_temp.extend(seg_list_behind)
                        seg_list = seg_list_temp
                        seg_list_temp = []
                        break

            if i == len(seg_list) - 1:
                seg_list_if = 1
    return seg_list


# 输出两个图形的权值的最大一个形状
def find_the_max_symbol(symbol1, symbol2):
    x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
    x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
    y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
    y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
    if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
        return ""
    elif (y1 + y2) in map_clear_up_keywords_value:
        seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
        return seg_list_temp
    else:
        if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
            return symbol1
        else:
            return symbol2


# 形状 形状 ABC ,如果前两个的图形的边相等,所以判断谁的权值大,否则,就有一个图形是错误的,需要舍弃,如果都错误,那么给予ABC基础图形
def find_the_max_symbol(symbol1, symbol2, seg_list):
    symbol1_angle, symbol2_angle = return_how_many_side_symbol(symbol1, symbol2)
    if symbol1_angle == symbol2_angle:
        x1 = map_clear_up_keywords.index(symbol1)  # 前一个图形的形状
        x2 = map_clear_up_keywords.index(symbol2)  # 后一个形状
        y1 = map_clear_up_keywords_value[x1]  # 前一个图形的权值
        y2 = map_clear_up_keywords_value[x2]  # 后一个图形的权值
        if (y1 + y2) in map_clear_up_keywords_error:  # 寻找当前的关系是否存在,例如可能出现梯形abcd是长方形
            return ""
        elif (y1 + y2) in map_clear_up_keywords_value:
            seg_list_temp = map_clear_up_keywords[map_clear_up_keywords_value.index(y1 + y2)]
            return seg_list_temp
        else:
            if y1 > y2:  # 规则:俩多边形的对应的值相加,如果存在,则更新为对应值的多边形,否则判断原来俩个多边形的大小,取值大的一个
                return symbol1
            else:
                return symbol2
    else:
        if len(seg_list) == symbol1_angle:
            return symbol1
        elif len(seg_list) == symbol2_angle:
            return symbol2
        else:
            return match_how_many_side(seg_list)


# 除去重复的形状
def delete_repetition_symbol(seg_list):
    seg_temp = 0

    while seg_temp == 0:
        for i in range(len(seg_list)):
            if seg_list[i] in map_clear_up_keywords and i + 1 < len(seg_list) and \
                    seg_list[i + 1] in map_clear_up_keywords:  # 当前形状和下一个值都是形状
                seg_list_front = seg_list[:i]
                seg_list_behind = seg_list[i + 2:]
                seg_list_front.insert(len(seg_list_front), find_the_max_symbol(seg_list[i], seg_list[i + 1]))
                seg_list_front.extend(seg_list_behind)
                seg_list = seg_list_front
                break
            if i + 1 == len(seg_list):
                seg_temp = 1
    return seg_list


# 处理四边形ABCD是正方形的情况
def dispose_shi_and_symbol(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        for j in range(len(seg_list_list[i])):
            if seg_list_list[i][j] in map_clear_up_keywords and j + 1 < len(seg_list_list[i]) and if_letter(
                    seg_list_list[i][j + 1]):  # 四边形abcd
                subject = seg_list_list[i][j]  # 当前主语为abcd
                if j + 3 < len(seg_list_list[i]) and seg_list_list[i][j + 2] in ["是", "为"] and \
                        seg_list_list[i][j + 3] in map_clear_up_keywords:  # 特殊值判断 四边形ABCD为长方形
                    seg_list_list_front = seg_list_list[i][:j]
                    seg_list_list_behind = seg_list_list[i][j + 4:]
                    seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
                    seg_list_list_front.insert(len(seg_list_list_front),
                                               find_the_max_symbol(seg_list_list[i][j], seg_list_list[i][j + 3],
                                                                   seg_list_list[i][j + 1]))
                    seg_list_list_front.insert(len(seg_list_list_front), seg_list_list[i][j + 1])
                    if len(seg_list_list_behind_letter) == 1 and seg_list_list_behind_letter[0][1] != seg_list_list[i][
                        j + 1]:
                        seg_list_list_front.extend(seg_list_list_behind)
                    seg_list_list[i] = seg_list_list_front
                    break
    seg_list = []
    for i in range(len(seg_list_list)):
        seg_list.extend(seg_list_list[i])
        seg_list.extend(",")
    # print("^&*","".join(seg_list))
    return seg_list


# 删去多余的逗号
def delete_unnecessary_comma(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if len(seg_list_list[i]) > 0 and seg_list_list[i][0] == ":":
            seg_list_list[i] = seg_list_list[i][1:]
    seg_list = return_seg_list(seg_list_list)
    seg_list_temp = 0
    while seg_list_temp == 0:
        if len(seg_list) == 0:
            break
        for i in range(len(seg_list)):
            if seg_list[i] == "," and i == 0:
                seg_list = seg_list[1:]
                break
            if seg_list[i] == "," and i + 2 < len(seg_list) and seg_list[i + 1] in [",", ".", "\n", "、", ";", "∶", "?",
                                                                                    "？"]:
                seg_list_front = seg_list[:i]
                seg_list_behind = seg_list[i + 2:]
                seg_list_front.extend(",")
                seg_list_front.extend(seg_list_behind)
                seg_list = seg_list_front
                break
            if seg_list[i] == "," and i - 1 > 0 and seg_list[i - 1] in [",", ".", "\n", "、", ";"]:
                seg_list_front = seg_list[:i - 1]
                seg_list_behind = seg_list[i:]
                seg_list_front.extend(seg_list_behind)
                seg_list = seg_list_front
                break
            if i + 1 == len(seg_list):
                seg_list_temp = 1
    return seg_list


def add_to_the_vertical(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if "垂足" in seg_list_list[i]:
            seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            if len(seg_list_letter) == 1 and seg_list_letter[0][0] == 1:
                seg_list_list[i - 1].extend("于")
                seg_list_list[i - 1].extend(seg_list_letter[0][1])
                seg_list_list[i] = ""
            else:
                for j in range(len(seg_list_letter)):
                    seg_list_list[i - j - 1].extend("于")
                    seg_list_list[i - j - 1].extend(seg_list_letter[len(seg_list_letter) - 1 - j][1])
                seg_list_list[i] = ""
    seg_list = []
    for i in range(len(seg_list_list)):
        seg_list.extend(seg_list_list[i])
        seg_list.extend(",")
    # print("^&*","".join(seg_list))
    return seg_list


# 查找当前句子的所有英文词组,返回边大小和词组
def find_all_letter_return_side_letter(seg_list):
    list_letter = []
    for i in range(len(seg_list)):
        list_letter_seg = []
        if if_letter(seg_list[i]) and seg_list[i].isupper():
            list_letter_seg.insert(len(list_letter_seg), len(seg_list[i]))
            list_letter_seg.insert(len(list_letter_seg), seg_list[i])
        # if seg_list[i] in symbol_keywords_main:
        #     break
        if len(list_letter_seg) > 0:
            list_letter.append(list_letter_seg)
    # print(list_letter)
    return list_letter


# 找到当前句子中除去字母,顿号的其他的所有字符串
def find_front_and_behind_other(seg_list, symbol):
    list_other = []
    if len(symbol) == 0:
        return seg_list
    # if not "、" in seg_list  \n symbol[0][1] \n elif: \n seg_list.index("、") < seg_list.index(
    #             symbol[0][1]) \n "、" \n else  symbol[0][1]
    seg_list_front = seg_list[:seg_list.index(
        symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
        seg_list_having(["、", "和"], seg_list) if seg_list.index(
            seg_list_having(["、", "和"], seg_list)) < seg_list.index(
            symbol[0][1])
        else symbol[0][1])]
    seg_list_behind = seg_list[seg_list.index(
        symbol[0][1] if not seg_list_having(["、", "和"], seg_list) else
        seg_list_having(["、", "和"], seg_list) if seg_list.index(
            seg_list_having(["、", "和"], seg_list)) > seg_list.index(
            symbol[len(symbol) - 1][1]) else
        symbol[len(symbol) - 1][1]) + 1:]
    list_other.append(seg_list_front)
    list_other.append(seg_list_behind)
    # print(list_other)
    return list_other


def find_have_d_or_slight_pause(seg_list):
    for i in range(len(seg_list)):
        if if_letter(seg_list[i]) or seg_list[i] == "、":
            return True
    return False


# 对交进行拼接
def package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
                        seg_list_front_behind_letter, seg_list_front_behind_other,
                        seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
                        seg_list_behind_behind_letter, seg_list_behind_behind_other, symbol):
    seg_list_part = []
    # print(seg_list_front_front_letter, end=" # ")
    # print(seg_list_front_front_other)
    # print(seg_list_front_behind_letter, end=" # ")
    # print(seg_list_front_behind_other)
    # print(seg_list_behind_front_letter, end=" # ")
    # print(seg_list_behind_front_other)
    # print(seg_list_behind_behind_letter, end=" # ")
    # print(seg_list_behind_behind_other)
    # 以下偷懒一点了，以后需要再进行更改吧
    # 有0111和1011和0100和0201三种情况 BE的延长线交AC于点F ，DF交 ， 四边形ABCD的两条对角线AC、BD交于点E
    # 存在1101和1111和1121三种情况
    # 存在2001一种情况

    # if len(seg_list_front_front_other) != 0 and (
    #         len(seg_list_front_front_other[0]) != 0 or seg_list_having(symbol_keywords_main,
    #                                                                    seg_list_front_front_other[1])):  # 清除前面的冗余句子
    #     for i in range(len(seg_list_front_front_letter)):
    #         seg_list_part.extend(seg_list_front_front_other[0])
    #         seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[i][1])
    #         if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
    #             seg_list_part.extend(seg_list_front_front_other[1])
    #         seg_list_part.extend(",")
    #     seg_list_front_front_other[0] = []
    #     if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
    #         seg_list_front_front_other[1] = []
    # if len(seg_list_front_behind_other) != 0 and (
    #         len(seg_list_front_behind_other[0]) != 0 or seg_list_having(symbol_keywords_main,
    #                                                                     seg_list_front_behind_other[1])):  # 清除后面的冗余句子
    #     for i in range(len(seg_list_front_behind_letter)):
    #         seg_list_part.extend(seg_list_front_behind_other[0])
    #         seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
    #         if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
    #             seg_list_part.extend(seg_list_front_behind_other[1])
    #         seg_list_part.extend(",")
    #     seg_list_front_behind_other[0] = []
    #     if seg_list_having(symbol_keywords_main, seg_list_front_behind_other[1]):
    #         seg_list_front_behind_other[1] = []

    if len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
        seg_list_part.extend(seg_list_behind_front_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 0 and len(
            seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
        seg_list_part.extend(seg_list_front_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
        if "交" not in seg_list_front_front_other[1] and "分别" not in seg_list_front_front_other[1]:
            seg_list_part.extend(seg_list_front_front_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
        seg_list_part.extend(seg_list_behind_front_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
            seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[1][1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 0:
        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
        seg_list_part.extend(seg_list_front_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
        seg_list_part.extend(seg_list_front_front_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 1:
        if seg_list_front_front_letter[0][0] == 1:
            seg_list_part.extend(seg_list_front_front_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
            seg_list_part.extend(seg_list_front_front_other[1])
            seg_list_part.insert(len(seg_list_part), "作")
        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
        seg_list_part.extend(seg_list_behind_front_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 1:
        seg_list_front_front_letter_temp = 1
        for i in range(2):
            seg_list_part.extend(seg_list_front_front_other[0])
            if seg_list_front_front_letter_temp == 1:
                seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
                seg_list_front_front_letter_temp += 1
            else:
                seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
            seg_list_part.extend(seg_list_front_front_other[1])
            seg_list_part.insert(len(seg_list_part), "交")
            seg_list_part.extend(seg_list_behind_front_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
            seg_list_part.extend(seg_list_behind_front_other[1])
            seg_list_part.insert(len(seg_list_part), "于")
            seg_list_part.extend(seg_list_behind_behind_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
            seg_list_part.extend(seg_list_behind_behind_other[1])
            seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 2 and len(seg_list_front_behind_letter) == 0 and len(
            seg_list_behind_front_letter) == 0 and len(seg_list_behind_behind_letter) == 1:
        seg_list_part.extend(seg_list_front_front_other[1])
        seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_front_front_other[1])
        seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[1][1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 2 and len(
            seg_list_behind_front_letter) == 1 and len(seg_list_behind_behind_letter) == 2:
        for i in range(2):
            seg_list_part.extend(seg_list_front_behind_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[i][1])
            seg_list_part.extend(seg_list_front_behind_other[1])
            seg_list_part.insert(len(seg_list_part), "交")
            seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
            seg_list_part.insert(len(seg_list_part), "于")
            seg_list_part.extend(seg_list_behind_behind_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
            seg_list_part.extend(seg_list_behind_behind_other[1])
            seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 1 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
        seg_list_part.extend(seg_list_front_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_front_letter[0][1])
        seg_list_part.extend(seg_list_front_front_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[0][1])
        seg_list_part.extend(seg_list_behind_front_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[0][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")

        seg_list_part.extend(seg_list_front_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
        seg_list_part.extend(seg_list_front_behind_other[1])
        seg_list_part.insert(len(seg_list_part), "交")
        seg_list_part.extend(seg_list_behind_front_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[1][1])
        seg_list_part.extend(seg_list_behind_front_other[1])
        seg_list_part.insert(len(seg_list_part), "于")
        seg_list_part.extend(seg_list_behind_behind_other[0])
        seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[1][1])
        seg_list_part.extend(seg_list_behind_behind_other[1])
        seg_list_part.insert(len(seg_list_part), ",")
    elif len(seg_list_front_front_letter) == 0 and len(seg_list_front_behind_letter) == 1 and len(
            seg_list_behind_front_letter) == 2 and len(seg_list_behind_behind_letter) == 2:
        for i in range(2):
            seg_list_part.extend(seg_list_front_behind_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_front_behind_letter[0][1])
            seg_list_part.extend(seg_list_front_behind_other[1])
            seg_list_part.insert(len(seg_list_part), "交")
            seg_list_part.extend(seg_list_behind_front_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_behind_front_letter[i][1])
            seg_list_part.extend(seg_list_behind_front_other[1])
            seg_list_part.insert(len(seg_list_part), "于")
            seg_list_part.extend(seg_list_behind_behind_other[0])
            seg_list_part.insert(len(seg_list_part), seg_list_behind_behind_letter[i][1])
            seg_list_part.extend(seg_list_behind_behind_other[1])
            seg_list_part.insert(len(seg_list_part), ",")
    else:  # 其他非常规的默认输出
        seg_list_part = package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
                                     seg_list_front_behind_letter, seg_list_front_behind_other,
                                     seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
                                     seg_list_behind_behind_letter, seg_list_behind_behind_other)
    # print("".join(seg_list_part))
    return seg_list_part


# 连接词组
def package_line(seg_list_front_front_letter, seg_list_front_front_other, seg_list_front_add,
                 seg_list_front_behind_letter, seg_list_front_behind_other,
                 seg_list_behind_front_letter, seg_list_behind_front_other, seg_list_behind_add,
                 seg_list_behind_behind_letter, seg_list_behind_behind_other):
    seg_list_max = max(len(seg_list_front_front_letter), len(seg_list_front_behind_letter),
                       len(seg_list_behind_front_letter), len(seg_list_behind_behind_letter))
    seg_list_part = []
    # 存在数字的相等
    # print("###",seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other))
    # print( seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other))
    # print(seg_list_behind_behind_letter_if_letter(seg_list_behind_behind_letter))
    # print(seg_list_front_front_letter)
    # print(seg_list_front_behind_letter)
    # print(seg_list_behind_front_letter)
    # △ABC的高AD与CE的长分别为4、6
    if (seg_list_having_1(["长", "宽", "高"], seg_list_front_front_other)
        or seg_list_having_1(["长", "宽", "高"], seg_list_front_behind_other)) \
            and seg_list_behind_behind_letter_if_letter(seg_list_behind_front_letter):
        for i in range(len(seg_list_front_front_letter)):

            seg_list_part_part = []
            if len(seg_list_front_front_other) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[0])
            if len(seg_list_front_front_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
            elif len(seg_list_front_front_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
            if len(seg_list_front_front_other) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[1])

            if len(seg_list_behind_front_other) == 2:
                seg_list_part_part.extend(seg_list_behind_front_other[0])
            if len(seg_list_behind_front_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
            elif len(seg_list_behind_front_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
            if len(seg_list_behind_front_other) == 2:
                seg_list_part_part.extend(seg_list_behind_front_other[1])

            if len(seg_list_behind_behind_other) == 2:
                seg_list_part_part.extend(seg_list_behind_behind_other[0])
            if len(seg_list_behind_behind_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
            elif len(seg_list_behind_behind_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
            if len(seg_list_behind_behind_other) == 2:
                seg_list_part_part.extend(seg_list_behind_behind_other[1])
            seg_list_part.extend(seg_list_part_part)
            seg_list_part.extend(",")
        for i in range(len(seg_list_front_behind_letter)):
            seg_list_part_part = []
            if len(seg_list_front_behind_other) == 2:
                seg_list_part_part.extend(seg_list_front_behind_other[0])
            if len(seg_list_front_behind_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
            elif len(seg_list_front_behind_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
            if len(seg_list_front_behind_other) == 2:
                seg_list_part_part.extend(seg_list_front_behind_other[1])

            if len(seg_list_behind_front_other) == 2:
                seg_list_part_part.extend(seg_list_behind_front_other[0])
            if len(seg_list_behind_front_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part),
                                          seg_list_behind_front_letter[i + len(seg_list_front_front_letter)][1])
            elif len(seg_list_behind_front_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
            if len(seg_list_behind_front_other) == 2:
                seg_list_part_part.extend(seg_list_behind_front_other[1])

            if len(seg_list_behind_behind_other) == 2:
                seg_list_part_part.extend(seg_list_behind_behind_other[0])
            if len(seg_list_behind_behind_letter) == seg_list_max:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
            elif len(seg_list_behind_behind_letter) != 0:
                seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
            if len(seg_list_behind_behind_other) == 2:
                seg_list_part_part.extend(seg_list_behind_behind_other[1])
            seg_list_part.extend(seg_list_part_part)
            seg_list_part.extend(",")

        return seg_list_part

    for i in range(seg_list_max):
        seg_list_part_part = []
        if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
            if len(seg_list_front_front_other[i]) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[i][0])
        else:
            if len(seg_list_front_front_other) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[0])
        # if len(seg_list_front_front_letter) == seg_list_max:
        #     if len(seg_list_front_front_letter[i][1]) == 1:  # 为垂足分别是兜底 ? 看不懂了
        #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
        #     else:
        #         seg_list_part_part.extend(seg_list_front_front_letter[i][1])
        # elif len(seg_list_front_front_letter) != 0:
        #     if len(seg_list_front_front_letter[0][1]) == 1:
        #         seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])
        #     else:
        #         seg_list_part_part.extend(seg_list_front_front_letter[0][1])
        if len(seg_list_front_front_letter) == seg_list_max:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[i][1])
        elif len(seg_list_front_front_letter) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_front_letter[0][1])

        if "垂直" in seg_list_front_add or "垂足" in seg_list_front_add:
            if len(seg_list_front_front_other[i]) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[i][1])
        else:
            if len(seg_list_front_front_other) == 2:
                seg_list_part_part.extend(seg_list_front_front_other[1])

        if len(seg_list_part_part) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_add)
        if len(seg_list_front_behind_other) == 2:
            seg_list_part_part.extend(seg_list_front_behind_other[0])
        if len(seg_list_front_behind_letter) == seg_list_max:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[i][1])
        elif len(seg_list_front_behind_letter) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_front_behind_letter[0][1])
        if len(seg_list_front_behind_other) == 2:
            seg_list_part_part.extend(seg_list_front_behind_other[1])

        if len(seg_list_behind_front_other) == 2:
            seg_list_part_part.extend(seg_list_behind_front_other[0])
        else:  # 如果存在分别相交于
            if len(seg_list_behind_front_other) != 0:
                seg_list_part_part.extend(seg_list_behind_front_other[0])
        if len(seg_list_behind_front_letter) == seg_list_max:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[i][1])
        elif len(seg_list_behind_front_letter) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_front_letter[0][1])
        if len(seg_list_behind_front_other) == 2:
            seg_list_part_part.extend(seg_list_behind_front_other[1])

        if len(seg_list_behind_behind_letter) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_add)

        if len(seg_list_behind_behind_other) == 2:
            seg_list_part_part.extend(seg_list_behind_behind_other[0])
        if len(seg_list_behind_behind_letter) == seg_list_max:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[i][1])
        elif len(seg_list_behind_behind_letter) != 0:
            seg_list_part_part.insert(len(seg_list_part_part), seg_list_behind_behind_letter[0][1])
        if len(seg_list_behind_behind_other) == 2:
            seg_list_part_part.extend(seg_list_behind_behind_other[1])
        # print("#########","".join(seg_list_part_part))
        seg_list_part.extend(seg_list_part_part)
        seg_list_part.extend(",")
    # print("#########","".join(seg_list_part))
    return seg_list_part


def find_the_mian_word(seg_list_list, symbol, seg_list_front_front_letter, i):
    for m in range(1, 5):  # 可能出现多次交
        if seg_list_list[i - m][0] != symbol:
            if re.search(".*交", "".join(seg_list_list[i - m])):
                seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("交")]
            if re.search(".*与", "".join(seg_list_list[i - m])):
                seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("与")]
            if re.search(".*作", "".join(seg_list_list[i - m])):
                seg_list_list[i - m] = seg_list_list[i - m][:seg_list_list[i - m].index("作")]
            if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
                    seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
                seg_list_front_front_letter = find_all_letter_return_side_letter(
                    seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
                while len(seg_list_front_front_letter) > 1:
                    del seg_list_front_front_letter[1]
                # print(seg_list_front_front_letter)
                # print()
                seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
                                                                         seg_list_front_front_letter)
            # 线AB、CD,分别交^^于^^
            elif seg_list_having("、", seg_list_list[i - m]):
                seg_list_front_front_letter = find_all_letter_return_side_letter(
                    seg_list_list[i - m])
                seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
                                                                         seg_list_front_front_letter)
            else:
                for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
                    if if_letter(seg_list_list[i - m][k]):
                        for j in range(len(seg_list_front_front_letter)):
                            seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
                            seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
                        seg_list_front_front_other = find_front_and_behind_other(
                            seg_list_list[i - m],
                            seg_list_front_front_letter)
                        break  # 只提取第一个词语
            if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
                seg_list_front_front_other[1] = []
            break
    return seg_list_front_front_letter, seg_list_front_front_other


# 处理分别
def cut_respect_is_importance(seg_list, symbol):
    seg_list_list = return_seg_list_list(seg_list)
    seg_list_i_temp_front = 0
    seg_list_i_temp_behind = 0
    seg_list_i_temp = []  # 存储更新后的词组
    for i in range(len(seg_list_list)):
        if symbol == "交" and "交" not in seg_list_list[i]:
            if "相交" in seg_list_list[i]:
                symbol = "相交"

        if symbol in seg_list_list[i]:
            seg_list_i_temp_front = i  # 记录当前分别的位置
            seg_list_front = seg_list_list[i][:seg_list_list[i].index(symbol)]
            seg_list_behind = seg_list_list[i][seg_list_list[i].index(symbol) + 1:]
            seg_list_front_front_letter = []
            seg_list_front_front_other = []
            seg_list_front_behind_letter = []
            seg_list_front_behind_other = []
            seg_list_behind_front_letter = []
            seg_list_behind_front_other = []
            seg_list_behind_behind_letter = []
            seg_list_behind_behind_other = []
            if len(seg_list_front) == 0:
                # 当存在"作"的时候,可能出现于,但是不存在缺少主语,故为: 分别f-f 作 f-b 交 b-h 于 b-b
                # 当不存在"作"的时候,可能出现于,但是缺少主语,故为:  主语,分别b-f 于b-b
                # 主语可能出现线,三边,多边
                # 此时ff是分别之后作之前
                if seg_list_having(["作", "与"], seg_list_behind) and seg_list_behind.index(
                        seg_list_having_0(["作", "与"], seg_list_behind)) > 0:  # 防止出现分别作多判断
                    seg_list_front_front = seg_list_behind[
                                           :seg_list_behind.index(seg_list_having_0(["作", "与"], seg_list_behind))]
                    seg_list_front_behind = seg_list_behind[
                                            seg_list_behind.index(
                                                seg_list_having_0(["作", "与"], seg_list_behind)) + 1:]
                    # 前半部分是否存在可以处理"的"
                    if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
                            seg_list_front_front[seg_list_front_front.index(
                                seg_list_having_0("的", seg_list_front_front)) + 1:]):
                        seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
                            seg_list_having_0("的", seg_list_front_front)) + 1:]
                        seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
                        seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
                                                                                 seg_list_front_front_letter)
                    else:
                        seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
                        seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
                                                                                 seg_list_front_front_letter)

                    if seg_list_having(["于"], seg_list_front_behind):  # 是否有"于"或者"交于"在后半段
                        seg_list_behind_front = seg_list_front_behind[:seg_list_front_behind.index(
                            seg_list_having_0(["于"], seg_list_front_behind))]
                        seg_list_behind_behind = seg_list_front_behind[seg_list_front_behind.index(
                            seg_list_having_0(["于"], seg_list_front_behind)) + 1:]
                        seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
                        seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
                                                                                   seg_list_behind_behind_letter)
                        if seg_list_having(["交"], seg_list_behind_front):  # 是否有"交"在作后半段,于前半段,即在中间
                            seg_list_behind_front_front = seg_list_behind_front[:seg_list_behind_front.index(
                                seg_list_having_0(["交"], seg_list_behind_front))]
                            seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
                                seg_list_having_0(["交"], seg_list_behind_front)):]
                            seg_list_front_behind_letter = find_all_letter_return_side_letter(
                                seg_list_behind_front_front)
                            seg_list_front_behind_other = find_front_and_behind_other(seg_list_behind_front_front,
                                                                                      seg_list_front_behind_letter)
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(
                                seg_list_behind_front_behind)
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_behind,
                                                                                      seg_list_behind_front_letter)
                        else:
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
                                                                                      seg_list_behind_front_letter)
                    else:
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_front_behind)
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_front_behind,
                                                                                  seg_list_behind_front_letter)
                else:
                    if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
                        seg_list_behind_front = seg_list_behind[
                                                :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
                        seg_list_behind_behind = seg_list_behind[
                                                 seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
                        if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
                                seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(
                                seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
                                                                                      seg_list_behind_front)
                        else:
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
                                                                                      seg_list_behind_front_letter)
                        seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
                        seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
                                                                                   seg_list_behind_behind_letter)
                    else:
                        # 垂线   分别交三角形ABC的AB CD
                        if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
                                seg_list_behind[seg_list_behind.index("的") + 1:]):
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(
                                seg_list_behind[seg_list_behind.index("的") + 1:])
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
                                                                                      seg_list_behind)
                        else:
                            seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
                            seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
                                                                                      seg_list_behind_front_letter)
                    # 如果有"于"看b-b-l字母值,否则看b-f-l值
                    seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
                        else len(seg_list_behind_front_letter)
                    for k in range(seg_list_b_b_l_len):
                        seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
                    for m in range(1, 5):  # 可能出现多次交
                        if seg_list_list[i - m][0] != symbol:
                            if seg_list_having("的", seg_list_list[i - m]) and find_have_d_or_slight_pause(
                                    seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:]):
                                seg_list_front_front_letter = find_all_letter_return_side_letter(
                                    seg_list_list[i - m][seg_list_list[i - m].index("的") + 1:])
                                while len(seg_list_front_front_letter) > 1:
                                    del seg_list_front_front_letter[1]
                                seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
                                                                                         seg_list_front_front_letter)
                            # 线AB、CD,分别交^^于^^
                            elif seg_list_having("、", seg_list_list[i - m]):
                                seg_list_front_front_letter = find_all_letter_return_side_letter(
                                    seg_list_list[i - m])
                                seg_list_front_front_other = find_front_and_behind_other(seg_list_list[i - m],
                                                                                         seg_list_front_front_letter)
                            else:
                                for k in range(len(seg_list_list[i - m])):  # 提取前一句的主语
                                    if if_letter(seg_list_list[i - m][k]):
                                        for j in range(len(seg_list_front_front_letter)):
                                            seg_list_front_front_letter[j][0] = len(seg_list_list[i - m][k])
                                            seg_list_front_front_letter[j][1] = seg_list_list[i - m][k]
                                        seg_list_front_front_other = find_front_and_behind_other(
                                            seg_list_list[i - m],
                                            seg_list_front_front_letter)
                                        break  # 只提取第一个词语
                            if seg_list_having(symbol_keywords_main, seg_list_front_front_other[1]):
                                seg_list_front_front_other[1] = []
                            break

                for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):
                    seg_list_i_temp.extend(seg_list_list[k])
                    seg_list_i_temp.extend(",")
                if "分别" in symbol:
                    seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
                                                        seg_list_having_0(["作", "与"], seg_list_front),
                                                        seg_list_front_behind_letter, seg_list_front_behind_other,
                                                        seg_list_behind_front_letter, seg_list_behind_front_other,
                                                        seg_list_having_0("于", seg_list_behind),
                                                        seg_list_behind_behind_letter, seg_list_behind_behind_other))
                else:
                    seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
                                                               seg_list_having_0(["作", "与"], seg_list_front),
                                                               seg_list_front_behind_letter,
                                                               seg_list_front_behind_other,
                                                               seg_list_behind_front_letter,
                                                               seg_list_behind_front_other, "于",
                                                               seg_list_behind_behind_letter,
                                                               seg_list_behind_behind_other, symbol))

                seg_list_i_temp_behind = i + 1
                # 分别在前面,可能出现缺主语或不缺
            elif len(seg_list_front) == 1 and seg_list_having_2(["垂"], seg_list_front):
                if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
                    seg_list_behind_front = seg_list_behind[
                                            :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
                    seg_list_behind_behind = seg_list_behind[
                                             seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]
                    if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
                            seg_list_behind_front[seg_list_behind_front.index("的") + 1:]):
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(
                            seg_list_behind_front[seg_list_behind_front.index("的") + 1:])
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
                                                                                  seg_list_behind_front)
                    else:
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
                                                                                  seg_list_behind_front_letter)
                    seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
                    seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
                                                                               seg_list_behind_behind_letter)
                else:
                    # 垂线分别交三角形ABC的AB CD
                    if seg_list_having("的", seg_list_behind) and find_have_d_or_slight_pause(
                            seg_list_behind[seg_list_behind.index("的") + 1:]):
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(
                            seg_list_behind[seg_list_behind.index("的") + 1:])
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front_letter,
                                                                                  seg_list_behind)
                    else:
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
                                                                                  seg_list_behind_front_letter)
                seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"], seg_list_behind) \
                    else len(seg_list_behind_front_letter)
                s_l_b_b_temp = 0
                for k in range(seg_list_b_b_l_len):
                    seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
                    seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
                for k in range(seg_list_b_b_l_len):  # 如果存在"于"看b-b-l,否则看b-f-l
                    if seg_list_having("⊥", seg_list_list[i - k - 1]):
                        s_l_b_b_temp = i - k - 1
                        for j in range(len(seg_list_list[i - k - 1])):
                            if if_letter(seg_list_list[i - k - 1][j]):
                                seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0] = len(
                                    seg_list_list[i - k - 1][j])
                                seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1] = seg_list_list[i - k - 1][j]
                                seg_list_front_front_letter_temp = [[[], []]]
                                seg_list_front_front_letter_temp[0][0] = \
                                    seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][0]
                                seg_list_front_front_letter_temp[0][1] = \
                                    seg_list_front_front_letter[seg_list_b_b_l_len - 1 - k][1]
                                seg_list_front_front_other[seg_list_b_b_l_len - 1 - k] = find_front_and_behind_other(
                                    seg_list_list[i - k - 1], seg_list_front_front_letter_temp)
                                break  # 只提取第一个词语
                # print(seg_list_front_front_letter)
                # print(package_line(seg_list_front_front_letter, "", "垂直", "", "", seg_list_behind_front_letter,
                #                    seg_list_behind_front_other, "于", seg_list_behind_behind_letter,
                #                    seg_list_behind_behind_other))
                for k in range(seg_list_i_temp_behind, s_l_b_b_temp):
                    seg_list_i_temp.extend(seg_list_list[k])
                    seg_list_i_temp.extend(",")
                seg_list_i_temp_behind = s_l_b_b_temp
                if "分别" in symbol:
                    seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
                                                        ("垂直" if seg_list_having(["垂直"],
                                                                                   seg_list_front) else "垂足"),
                                                        seg_list_front_behind_letter, seg_list_front_behind_other,
                                                        seg_list_behind_front_letter, seg_list_behind_front_other,
                                                        seg_list_having_0("于", seg_list_behind),
                                                        seg_list_behind_behind_letter, seg_list_behind_behind_other))
                else:
                    seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
                                                               seg_list_having_0(["作", "与"], seg_list_front),
                                                               seg_list_front_behind_letter,
                                                               seg_list_front_behind_other,
                                                               seg_list_behind_front_letter,
                                                               seg_list_behind_front_other, "于",
                                                               seg_list_behind_behind_letter,
                                                               seg_list_behind_behind_other, symbol))

                seg_list_i_temp_behind = i + 1

            else:
                # E、F分别为AD、BC的中点
                seg_list_front_temp_front = []
                if return_re_return([".*平分"], "".join(seg_list_front)) and seg_list_having("、", seg_list_front) \
                        and return_re_return([".*交"], "".join(symbol)):
                    seg_list_list_front = seg_list_front[:seg_list_front.index("平分线")]
                    seg_list_list_behind = seg_list_front[seg_list_front.index("平分线") + 1:]
                    seg_list_list_front_letter = find_all_letter_return_side_letter(seg_list_list_front)
                    seg_list_list_behind_letter = find_all_letter_return_side_letter(seg_list_list_behind)
                    if len(seg_list_list_behind_letter) == len(seg_list_list_front_letter):
                        for j in range(len(seg_list_list_front_letter)):
                            if seg_list_front[seg_list_front.index(seg_list_list_front_letter[j][1]) - 1] in "∠":
                                front_letter_temp = "∠"
                                front_letter_temp += seg_list_list_front_letter[j][1]
                                seg_list_list_front_letter[j][1] = front_letter_temp
                        front_letter_temp_temp = []
                        front_letter_temp_time = len(seg_list_list_front_letter) - 1
                        for j in range(len(seg_list_list_front_letter)):
                            front_letter_temp = []
                            front_letter_temp.insert(len(front_letter_temp), seg_list_list_front_letter[j][1])
                            front_letter_temp.extend("的")
                            front_letter_temp.extend("平分线")
                            front_letter_temp.insert(len(front_letter_temp), seg_list_list_behind_letter[j][1])
                            front_letter_temp = transition_divide(front_letter_temp)
                            front_letter_temp_list = return_seg_list_list(front_letter_temp)
                            for k in range(len(front_letter_temp_list)):
                                if k + 1 != len(front_letter_temp_list):
                                    seg_list_front_temp_front.insert(len(seg_list_front_temp_front),
                                                                     front_letter_temp_list[k])
                                else:
                                    front_letter_temp_temp.extend(front_letter_temp_list[k])
                            if front_letter_temp_time:
                                front_letter_temp_temp.extend("、")
                                front_letter_temp_time -= 1
                        seg_list_front = front_letter_temp_temp

                # 单只处理平分
                if return_re_return([".*平分"], "".join(seg_list_front)) and \
                        not return_re_return([".*与", ".*作", ".*和"], "".join(seg_list_front)) and \
                        not seg_list_having("、", seg_list_list[i]):

                    seg_list_temp = transition_divide(seg_list_front)
                    seg_list_temp_list = return_seg_list_list(seg_list_temp)
                    seg_list_front_temp = []
                    seg_list_front_temp_temp = []
                    seg_list_front_temp_front = []  # 记录平分前的关系
                    for j in range(len(seg_list_temp_list)):
                        seg_list_temp_list_letter = find_all_letter_return_side_letter(seg_list_temp_list[j])
                        if len(seg_list_temp_list_letter) == 1:
                            seg_list_front_temp.insert(len(seg_list_front_temp), seg_list_temp_list[j])
                        else:
                            seg_list_front_temp_front.insert(len(seg_list_front_temp_front), seg_list_temp_list[j])
                            seg_list_front_temp_front.extend(",")
                    if len(seg_list_front_temp) == 1:
                        seg_list_front_temp_temp.extend(seg_list_front_temp[0])
                    else:
                        for j in range(len(seg_list_front_temp)):
                            seg_list_front_temp_temp.extend(seg_list_front_temp[j])
                            seg_list_front_temp_temp.extend("、")
                    seg_list_front = seg_list_front_temp_temp

                if seg_list_having(["作", "与"], seg_list_front):
                    seg_list_front_front = seg_list_front[
                                           :seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front))]
                    seg_list_front_behind = seg_list_front[
                                            seg_list_front.index(seg_list_having_0(["作", "与"], seg_list_front)) + 1:]
                    if seg_list_having("的", seg_list_front_front) and find_have_d_or_slight_pause(
                            seg_list_front_front[seg_list_front_front.index(
                                seg_list_having_0("的", seg_list_front_front)) + 1:]):
                        seg_list_front_front_behind = seg_list_front_front[seg_list_front_front.index(
                            seg_list_having_0("的", seg_list_front_front)) + 1:]
                        seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front_behind)
                        seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
                                                                                 seg_list_front_front_letter)
                    else:
                        seg_list_front_front_letter = find_all_letter_return_side_letter(seg_list_front_front)
                        seg_list_front_front_other = find_front_and_behind_other(seg_list_front_front,
                                                                                 seg_list_front_front_letter)
                    if seg_list_having("的", seg_list_front_behind) and find_have_d_or_slight_pause(
                            seg_list_front_behind[
                            seg_list_front_behind.index(seg_list_having_0("的", seg_list_front_behind)) + 1:]):
                        # 前半部分存在"的"和每一部分都有顿号或者是字母
                        seg_list_front_behind_behind = seg_list_front_behind[
                                                       seg_list_front_behind.index(
                                                           seg_list_having_0("的", seg_list_front_behind)) + 1:]
                        seg_list_front_behind_letter = find_all_letter_return_side_letter(
                            seg_list_front_behind_behind)  # 找出所有的词语
                        seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
                                                                                  seg_list_front_behind_letter)
                    else:
                        seg_list_front_behind_letter = find_all_letter_return_side_letter(
                            seg_list_front_behind)  # 找出所有的词语
                        seg_list_front_behind_other = find_front_and_behind_other(seg_list_front_behind,
                                                                                  seg_list_front_behind_letter)
                else:
                    if seg_list_having("的", seg_list_front) and find_have_d_or_slight_pause(
                            seg_list_front[seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]):
                        seg_list_front_behind = seg_list_front[
                                                seg_list_front.index(seg_list_having_0("的", seg_list_front)) + 1:]
                        seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front_behind)
                        seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
                                                                                  seg_list_front_behind_letter)
                    else:
                        seg_list_front_behind_letter = find_all_letter_return_side_letter(seg_list_front)
                        seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
                                                                                  seg_list_front_behind_letter)
                if seg_list_having(["于"], seg_list_behind):  # 是否有"于"或者"交于"在后半段
                    seg_list_behind_front = seg_list_behind[
                                            :seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind))]
                    seg_list_behind_behind = seg_list_behind[
                                             seg_list_behind.index(seg_list_having_0(["于"], seg_list_behind)) + 1:]

                    if seg_list_having("的", seg_list_behind_front) and find_have_d_or_slight_pause(
                            seg_list_behind_front[seg_list_behind_front.index(
                                seg_list_having_0("的", seg_list_behind_front)) + 1:]):
                        seg_list_behind_front_behind = seg_list_behind_front[seg_list_behind_front.index(
                            seg_list_having_0("的", seg_list_behind_front)) + 1:]
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front_behind)
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
                                                                                  seg_list_behind_front_letter)
                    else:
                        seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind_front)
                        seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind_front,
                                                                                  seg_list_behind_front_letter)
                    seg_list_behind_behind_letter = find_all_letter_return_side_letter(seg_list_behind_behind)
                    seg_list_behind_behind_other = find_front_and_behind_other(seg_list_behind_behind,
                                                                               seg_list_behind_behind_letter)
                else:
                    seg_list_behind_front_letter = find_all_letter_return_side_letter(seg_list_behind)
                    seg_list_behind_front_other = find_front_and_behind_other(seg_list_behind,
                                                                              seg_list_behind_front_letter)
                if (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[0]) or \
                        (len(seg_list_front_behind_other) > 0 and "垂直平分" in seg_list_front_behind_other[1]):
                    seg_list_front_behind_letter = seg_list_front_behind_letter[:1]
                    seg_list_front_behind_other = find_front_and_behind_other(seg_list_front,
                                                                              seg_list_front_behind_letter)
                    # 去掉三角形,三角形在最前面或最后面,且前面和中间的长度不相等
                if len(seg_list_behind_front_letter) != 0 and (seg_list_behind_front_letter[0][0] == 3 or
                                                               seg_list_behind_front_letter[
                                                                   len(seg_list_behind_front_letter) - 1][0]
                                                               == 3) and len(seg_list_front_behind_letter) != \
                        len(seg_list_behind_front_letter):
                    if seg_list_behind_front_letter[0][0] == 3:
                        seg_list_behind_front_letter = seg_list_behind_front_letter[1:]
                    else:
                        seg_list_behind_front_letter = seg_list_behind_front_letter[
                                                       :len(seg_list_behind_front_letter) - 2]
                for k in range(seg_list_i_temp_behind, seg_list_i_temp_front):  # 拼接没有处理的句子
                    seg_list_i_temp.extend(seg_list_list[k])
                    seg_list_i_temp.extend(",")
                if len(seg_list_front_temp_front) != 0:
                    for j in range(len(seg_list_front_temp_front)):
                        seg_list_i_temp.extend(seg_list_front_temp_front[j])
                        seg_list_i_temp.extend(",")
                    # print(seg_list_front_other) print(seg_list_behind_front_other) print(seg_list_behind_other)
                    # print("".join(package_line(seg_list_front_letter, seg_list_front_other, seg_list_mid_letter,
                    # seg_list_behind_front_other, seg_list_beh_letter, seg_list_behind_other)))

                if "分别" in symbol:
                    seg_list_i_temp.extend(package_line(seg_list_front_front_letter, seg_list_front_front_other,
                                                        seg_list_having_0(["作", "与"], seg_list_front),
                                                        seg_list_front_behind_letter, seg_list_front_behind_other,
                                                        seg_list_behind_front_letter, seg_list_behind_front_other, "于",
                                                        seg_list_behind_behind_letter, seg_list_behind_behind_other))
                else:

                    if (len(seg_list_front_front_letter) + len(seg_list_front_behind_letter) + len(
                            seg_list_behind_front_letter)) < 2:
                        seg_list_b_b_l_len = len(seg_list_behind_behind_letter) if seg_list_having(["于"],
                                                                                                   seg_list_behind) \
                            else len(seg_list_behind_front_letter)
                        s_l_b_b_temp = 0
                        for k in range(seg_list_b_b_l_len):
                            seg_list_front_front_letter.insert(len(seg_list_front_front_letter), [[], []])
                            seg_list_front_front_other.insert(len(seg_list_front_front_other), [[], []])
                        seg_list_front_front_letter, seg_list_front_front_other = find_the_mian_word(seg_list_list,
                                                                                                     symbol,
                                                                                                     seg_list_front_front_letter,
                                                                                                     i)
                    if "平分" in seg_list_front_behind_other[0] or "平分" in seg_list_front_behind_other[1]:
                        for k in range(len(seg_list_front_behind_letter)):
                            if seg_list_front_behind_letter[k][0] != 2:
                                seg_list_front_behind_letter_front = seg_list_front_behind_letter[:k]
                                seg_list_front_behind_letter_front.extend(seg_list_front_behind_letter[k + 1:])
                                seg_list_front_behind_letter = seg_list_front_behind_letter_front
                    seg_list_i_temp.extend(package_line_symbol(seg_list_front_front_letter, seg_list_front_front_other,
                                                               seg_list_having_0(["作", "与"], seg_list_front),
                                                               seg_list_front_behind_letter,
                                                               seg_list_front_behind_other,
                                                               seg_list_behind_front_letter,
                                                               seg_list_behind_front_other, "于",
                                                               seg_list_behind_behind_letter,
                                                               seg_list_behind_behind_other, symbol))
                seg_list_i_temp_behind = i + 1
        if symbol == "相交":  # 将symbol还原
            symbol = "交"
    for k in range(seg_list_i_temp_behind, len(seg_list_list)):  # 拼接"分别"后面未处理的句子
        seg_list_i_temp.extend(seg_list_list[k])
        seg_list_i_temp.extend(",")
    return seg_list_i_temp


# 处理连等和相似的情况
def transition_equal_or_similarity(seg_list):
    equal_value_all = []
    seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
    seg_list = []
    while seg_list1 != "":
        if_transition = 0
        if seg_list_having_0(symbol_keywords_main, seg_list1):
            seg_list.extend(find_which_equal(seg_list1, seg_list_having_0(symbol_keywords_main, seg_list1)))
            if_transition = 1
        if if_transition == 0:
            seg_list.extend(seg_list1)
        seg_list.extend(",")
        seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
    return seg_list
    # if "=" in seg_list:
    #     equal_value_all = find_which_equal(seg_list, "=")
    # if "//" in seg_list:
    #     equal_value_all = find_which_equal(seg_list, "//")
    # if "⊥" in seg_list:
    #     equal_value_all = find_which_equal(seg_list, "⊥")
    # symbol_keywords_main = ["=", "//", "⊥", "≠", "≈", "∽", "!=", "≌"]


def transition_angle_to_angle(seg_list):
    for i in range(len(seg_list)):
        if i + 1 < len(seg_list) and seg_list[i] in "∠" and seg_list[i + 1] in "平分线":
            seg_list_front = seg_list[:i]
            seg_list_behind = seg_list[i + 1:]
            seg_list_front.extend("角")
            seg_list_front.extend(seg_list_behind)
            seg_list = seg_list_front
    return seg_list


def transition_triangle_symbol(seg_list, symbol):
    for i in range(len(seg_list)):
        if symbol in seg_list[i] and if_letter(seg_list[i + 1]):
            seg_list_front = seg_list[i][:seg_list[i].index(symbol)]
            seg_list_front += "△"
            seg_list[i] = seg_list_front
    return seg_list


def return_the_point_at_line_temp(seg_list_list_letter1, seg_list_list_letter2, seg_list_list_letter_temp):
    if len(seg_list_list_letter1) == 0 and len(seg_list_list_letter2) == 0:
        return ""
    if len(seg_list_list_letter1) == 1:
        seg_list_list_letter_A = seg_list_list_letter1
        seg_list_list_letter_BC = seg_list_list_letter2
    else:
        seg_list_list_letter_A = seg_list_list_letter2
        seg_list_list_letter_BC = seg_list_list_letter1
    if seg_list_list_letter_temp == "延长线":
        letter_point = ""
        letter_AB = ""
        letter_point = seg_list_list_letter_BC[1]
        letter_AB += seg_list_list_letter_BC[0]
        letter_AB += seg_list_list_letter_A[0]
        seg_list_list_letter_A = letter_point
        seg_list_list_letter_BC = letter_AB
        seg_list_list_letter_temp = ""
    temp = []
    temp.insert(len(temp), seg_list_list_letter_A)
    if seg_list_list_letter_temp != "中点":  # 如果是中点,修改为A是BC的中点
        temp.insert(len(temp), "在")
    else:
        temp.insert(len(temp), "平分")
    temp.insert(len(temp), seg_list_list_letter_BC)
    if seg_list_list_letter_temp != "中点":
        if seg_list_list_letter_temp != "":
            temp.insert(len(temp), seg_list_list_letter_temp)
            temp.insert(len(temp), "上")
        else:
            temp.insert(len(temp), "上")
    # else:
    #     temp.insert(len(temp), "的")
    #     temp.insert(len(temp), "中点")
    temp.insert(len(temp), ",")
    temp.insert(len(temp), seg_list_list_letter_A)
    return temp


def guozuoyu(clause):
    arr = re.split('[作于]', clause)
    front = re.findall('[A-Za-z]', arr[0])
    mid = re.findall('[A-Za-z]', arr[1])
    behind = re.findall('[A-Za-z]', arr[2])
    clause_new = ""
    if arr[1].find('垂线') != -1:
        clause_new = front[-1] + behind[0] + '⊥' + mid[0] + mid[1] + '于' + behind[0]
    if arr[1].find('交') != -1:
        clause_new += ',' + front[-1] + behind[0] + '交' + mid[2] + mid[3] + '于' + behind[0]
    return (clause_new)


def guozuo(clause):
    arr = clause.split('作')
    front = re.findall('[A-Za-z]', arr[0])
    behind = re.findall('[A-Za-z]', arr[1])
    clause_new = ""
    for i in range(len(map_clear_up_keywords)):
        if re.search(map_clear_up_keywords[i], arr[1]) and map_clear_up_keywords[i] != "线":
            clause_new = map_clear_up_keywords[i]
            for j in range(len(behind)):
                clause_new += behind[j]
            clause_new += ","
            return clause_new
    if front[-1] == behind[0] or front[-1] == behind[1]:
        clause_new = ""
    else:
        if arr[1].find("延长") != -1:
            clause_new = front[-1] + "在" + behind[0] + behind[1] + "延长线上"
        else:
            clause_new = front[-1] + "在" + behind[0] + behind[1] + "上"
    if len(behind) > 2:
        if arr[1].find("的平行线") != -1:
            if front[-1] == behind[2] or front[-1] == behind[3]:
                clause = ""
            else:
                clause_new = front[-1] + "在" + behind[2] + behind[3] + "上"
            if clause_new != "":
                clause_new += ","
            clause_new += behind[0] + behind[1] + '//' + behind[2] + behind[3]
    if len(front) > 1:
        if arr[0].find('中点') != -1:
            if clause_new != "":
                clause_new += ","
            clause_new += front[2] + '是' + front[0] + front[1] + '中点'
        elif arr[0].find('上的') != -1:
            if clause_new != "":
                clause_new += ","
            clause_new += front[2] + '在' + front[0] + front[1] + '上'
    return clause_new


def transition_diagonal(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if re.search(".*对角线", "".join(seg_list_list[i])):
            seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            seg_list_list_letter_A = []
            seg_list_list_letter_AB = []
            seg_list_list_letter_ABC = []
            for j in range(len(seg_list_list_letter)):
                if seg_list_list_letter[j][0] == 1:
                    seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
                elif seg_list_list_letter[j][0] == 2:
                    seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
                else:
                    seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
            seg_temp = []
            for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
                seg_list_list_letter_symbol = seg_list_list[i][
                    seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
                seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
                seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
                seg_temp.extend(",")
            if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):
                for j in range(len(seg_list_list_letter_A)):
                    seg_list_list_letter_temp = ""
                    temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
                                                         seg_list_list_letter_temp)
                    seg_temp.extend(temp)
                    seg_temp.extend(",")
            if len(seg_list_list_letter_AB) == 1:
                seg_temp.insert(len(seg_temp), seg_list_list_letter_AB[0])
                seg_temp.extend(",")
            seg_list_list[i] = seg_temp
    return return_seg_list(seg_list_list)


def transition_point_at_side_re(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if return_re_return(
                ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
                 "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
            if seg_list_having("=", seg_list_list[i]):
                if seg_list_list[i][seg_list_list[i].index("=") - 2] == "∠":
                    seg_list_list[i].insert(seg_list_list[i].index("=") - 2, ",")
                else:
                    seg_list_list[i].insert(seg_list_list[i].index("=") - 1, ",")
                seg_list_list[i] = behind_operation(seg_list_list[i])
                continue
            seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            seg_list_list_letter_A = []
            seg_list_list_letter_AB = []
            seg_list_list_letter_ABC = []
            for j in range(len(seg_list_list_letter)):
                if seg_list_list_letter[j][0] == 1:
                    seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
                elif seg_list_list_letter[j][0] == 2:
                    seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
                else:
                    seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
            seg_list_list_letter_temp = ""
            if return_re_return([".*中点"], "".join(seg_list_list[i])):  # 提取关键词
                seg_list_list_letter_temp = "中点"
            elif return_re_return([".*延长"], "".join(seg_list_list[i])):
                seg_list_list_letter_temp = "延长线"
            else:
                seg_list_list_letter_temp = ""
            if len(seg_list_list_letter_A) == len(seg_list_list_letter_AB):  # 可能出现单独只是一个图形
                seg_temp = []
                for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
                    seg_list_list_letter_symbol = seg_list_list[i][
                        seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
                    seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
                    seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
                    seg_temp.extend(",")
                for j in range(len(seg_list_list_letter_A)):
                    temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[j],
                                                         seg_list_list_letter_temp)
                    seg_temp.extend(temp)
                    seg_temp.extend(",")
                seg_list_list[i] = seg_temp
            elif len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) > 0:
                seg_temp = []
                for j in range(len(seg_list_list_letter_ABC)):  # 处理多余的图形
                    seg_list_list_letter_symbol = seg_list_list[i][
                        seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1]
                    seg_temp.insert(len(seg_temp), seg_list_list_letter_symbol)
                    seg_temp.insert(len(seg_temp), seg_list_list_letter_ABC[j])
                    seg_temp.extend(",")
                if len(seg_list_list_letter_AB) == 1:
                    for j in range(len(seg_list_list_letter_A)):
                        temp = return_the_point_at_line_temp(seg_list_list_letter_A[j], seg_list_list_letter_AB[0],
                                                             seg_list_list_letter_temp)
                        seg_temp.extend(temp)
                        seg_temp.extend(",")
                seg_list_list[i] = seg_temp
            elif re.search("一.*直线", "".join(seg_list_list[i])) is not None or re.search("任意.*点", "".join(
                    seg_list_list[i])) is not None:  # 共线
                seg_list_list_temp = ""
                seg_list_list_temp_temp = ""
                seg_list_list_temp += seg_list_list_letter[0][1]
                seg_list_list_temp += seg_list_list_letter[len(seg_list_list_letter) - 1][1]
                seg_list_list_temp_temp = "".join(seg_list_list_temp)
                seg_list_list_letter = seg_list_list_letter[1:]
                seg_list_list_letter = seg_list_list_letter[:len(seg_list_list_letter) - 1]
                if len(seg_list_list_letter) == 0:
                    seg_list_list[i] = seg_list_list_temp_temp
                else:
                    seg_temp = []
                    for j in range(len(seg_list_list_letter)):
                        temp = return_the_point_at_line_temp(seg_list_list_letter[j][1], seg_list_list_temp_temp,
                                                             seg_list_list_letter_temp)
                        seg_temp.extend(temp)
                        seg_temp.extend(",")
                    seg_list_list[i] = seg_temp

            elif (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_AB) == 0) or (
                    len(seg_list_list_letter_A) == 0 and len(seg_list_list_letter_AB) > 0):
                seg_list_list_letter_symbol = []
                for j in range(len(seg_list_list_letter_ABC)):  # 记录的图形
                    seg_list_list_letter_symbol.insert(len(seg_list_list_letter_symbol), seg_list_list[i][
                        seg_list_list[i].index(seg_list_list_letter_ABC[j]) - 1])
                temp = []
                if (len(seg_list_list_letter_A) > 0 and len(seg_list_list_letter_ABC) > 0) or (
                        len(seg_list_list_letter_AB) > 0 and len(seg_list_list_letter_ABC) > 0):
                    for j in range(len(seg_list_list_letter_A if len(
                            seg_list_list_letter_A) > 0 else seg_list_list_letter_AB)):
                        if len(seg_list_list_letter_ABC) == 1:
                            temp.insert(len(temp), seg_list_list_letter_symbol[0])
                            temp.insert(len(temp), seg_list_list_letter_ABC[0])
                        else:
                            temp.insert(len(temp), seg_list_list_letter_symbol[j])
                            temp.insert(len(temp), seg_list_list_letter_ABC[j])
                        temp.extend(",")
                        if len(seg_list_list_letter_A) > 0:
                            temp.insert(len(temp), seg_list_list_letter_A[j])
                            temp.extend("在")
                            if len(seg_list_list_letter_ABC) == 1:
                                # temp.insert(len(temp), seg_list_list_letter_symbol[0])
                                temp.insert(len(temp), seg_list_list_letter_ABC[0])
                            else:
                                # temp.insert(len(temp), seg_list_list_letter_symbol[j])
                                temp.insert(len(temp), seg_list_list_letter_ABC[j])
                            temp.extend("内")
                        else:
                            temp.insert(len(temp), seg_list_list_letter_AB[j])
                        temp.extend(",")
                        if len(seg_list_list_letter_A) > 0:
                            temp.extend(seg_list_list_letter_A[j])
                        else:
                            temp.extend(seg_list_list_letter_AB[j])
                elif len(seg_list_list_letter_A) > 0:  # 特质判断，点在斜边上
                    if return_re_return([".*斜"], "".join(seg_list_list[i])):
                        for j in range(len(seg_list_list_letter_A)):
                            temp.insert(len(temp), seg_list_list_letter_A[j])
                            temp.extend("在")
                            temp.extend("斜边")
                            temp.extend("上")
                            temp.extend(",")
                    elif return_re_return([".*侧"], "".join(seg_list_list[i])):  # 此处为补丁，点E在F左侧
                        temp = seg_list_list[i]
                else:
                    temp.insert(len(temp), seg_list_list_letter_AB[0])
                    if seg_list_list_letter_temp == "延长线":
                        temp.extend("的")
                        temp.insert(len(temp), "延长线")
                seg_list_list[i] = temp
            elif seg_list_having_1(["作", "做"], seg_list_list[i]):  # 特质判断，以AE为边在直线BC的上方作正方形AEFG
                seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("作" if "作" in seg_list_list[i] else "做"):]
                seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])

            else:
                for j in range(len(symbol_keywords_main)):
                    if symbol_keywords_main[j] in seg_list_list[i]:
                        temp = []
                        letter = []
                        temp_int = 0
                        for k in range(3):
                            if seg_list_list[i].index(symbol_keywords_main[j]) - k >= 0 \
                                    and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k] in
                                         map_clear_up_keywords or seg_list_list[i][
                                             seg_list_list[i].index(symbol_keywords_main[j]) - k] in symbol_keywords or
                                         if_number_and_letter(
                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])):
                                temp.insert(len(temp),
                                            seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) - k])
                                temp_int = k
                        temp.reverse()
                        letter = find_all_letter_return_side_letter(temp)
                        letter = letter[0][1]
                        temp.extend(symbol_keywords_main[j])
                        for k in range(3):
                            if seg_list_list[i].index(symbol_keywords_main[j]) + k < len(seg_list_list[i]) \
                                    and (seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k] in
                                         map_clear_up_keywords or seg_list_list[i][
                                             seg_list_list[i].index(symbol_keywords_main[j]) + k] in symbol_keywords or
                                         if_number_and_letter(
                                             seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])):
                                temp.insert(len(temp),
                                            seg_list_list[i][seg_list_list[i].index(symbol_keywords_main[j]) + k])
                        seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index(symbol_keywords_main[j]) - temp_int]
                        new_letter = find_all_letter_return_side_letter(seg_list_list[i])
                        for k in range(len(letter)):
                            for p in range(len(new_letter)):
                                if letter[k] in new_letter[p][1]:
                                    continue
                                else:
                                    letter = letter[k]
                                    break
                            if k + 1 == len(letter):
                                letter = ""
                                break
                        seg_list_list[i].extend("存在点")
                        seg_list_list[i].extend(letter)
                        seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])
                        seg_list_list[i].extend(temp)
    return return_seg_list(seg_list_list)


def transition_hand_over_temp(seg_list_list, temp, temp_temp):
    temp.extend(seg_list_list[len(seg_list_list) - 1])
    for i in range(len(seg_list_list) - 1):
        temp_temp.extend(seg_list_list[i])
        temp_temp.extend(",")
    return temp, temp_temp


def transition_hand_over(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if seg_list_having_2("交", seg_list_list[i]):
            seg_list_list[i] = list(jieba.cut("".join(seg_list_list[i]), cut_all=False))
            seg_list_list_front = seg_list_list[i][
                                  :seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交")]
            seg_list_list_mid = seg_list_list[i][
                                seg_list_list[i].index("交" if seg_list_having("交", seg_list_list[i]) else "相交") + 1:
                                seg_list_list[i].index("于")]
            seg_list_list_behind = seg_list_list[i][seg_list_list[i].index("于") + 1:]
            seg_list_list_front = behind_operation(seg_list_list_front)
            seg_list_list_mid = behind_operation(seg_list_list_mid)
            seg_list_list_behind = behind_operation(seg_list_list_behind)
            seg_list_list_front_temp = return_seg_list_list(seg_list_list_front)  # 查看是否有补充
            seg_list_list_mid_temp = return_seg_list_list(seg_list_list_mid)
            seg_list_list_behind_temp = return_seg_list_list(seg_list_list_behind)
            temp = []
            temp_temp = []
            temp, temp_temp = transition_hand_over_temp(seg_list_list_front_temp, temp, temp_temp)
            temp.extend("交")
            temp, temp_temp = transition_hand_over_temp(seg_list_list_mid_temp, temp, temp_temp)
            temp.extend("于")
            temp, temp_temp = transition_hand_over_temp(seg_list_list_behind_temp, temp, temp_temp)
            temp_temp.extend(temp)
            temp.extend(",")
            seg_list_list[i] = temp_temp
    return return_seg_list(seg_list_list)


def transition_zuo_in_list(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if re.search(".*作", "".join(seg_list_list[i])):
            seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            if len(seg_list_letter) == 0:
                seg_list_list[i] = ""
            elif len(seg_list_letter) == 1:
                seg_list_list[i] = seg_list_letter[0][1]
            elif len(seg_list_letter) == 2:
                if seg_list_having(seg_list_letter[0][1], seg_list_letter[1][1]):
                    seg_list_list[i] = seg_list_letter[1][1]
                else:
                    temp = []
                    temp.extend("过")
                    temp.insert(len(temp), seg_list_letter[0][1])
                    temp.extend("作")
                    temp.insert(len(temp), seg_list_letter[1][1])
                    seg_list_list[i] = temp
            elif len(seg_list_letter) == 3:
                print(seg_list_list[i])
            else:
                print("多元关系", seg_list_list[i])
    return return_seg_list(seg_list_list)


# 返回seg_list_list
def return_seg_list_list(seg_list):
    seg_list_list = []
    seg_list1, seg_list2 = cut_clause(seg_list)  # 按照","，"."，"，"，"。"分段
    while seg_list1 != "":
        seg_list_list.append(seg_list1)
        seg_list1, seg_list2 = cut_clause(seg_list2)  # 按照","，"."，"，"，"。"分段
    return seg_list_list


def return_seg_list(seg_list_list):
    seg_list = []
    for i in range(len(seg_list_list)):
        seg_list.extend(seg_list_list[i])
        seg_list.extend(",")
    return seg_list


def tran_wei_to_fen_bie(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if "为" in seg_list_list[i]:
            seg_list_list_front = seg_list_list[i][:seg_list_list[i].index("为")]
            seg_list_list_front.insert(len(seg_list_list_front), "分别")
            seg_list_list_front.extend(seg_list_list[i][seg_list_list[i].index("为"):])
            seg_list_list[i] = seg_list_list_front
    return return_seg_list(seg_list_list)


def delete_line_and_line(symbol, seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if seg_list_having_0(symbol, seg_list_list[i]):
            if not seg_list_having_2(["交", "作"], seg_list_list[i]) and len(
                    find_all_letter_return_side_letter(seg_list_list[i])) >= len(seg_list_list[i]) * 0.5:
                seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
                seg_temp = []
                for j in range(len(seg_list_letter)):
                    seg_temp.insert(len(seg_temp), seg_list_letter[j][1])
                    seg_temp.extend(",")
                seg_list_list[i] = seg_temp
            else:
                seg_list_list_temp = seg_list_list[i][
                                     :seg_list_list[i].index(
                                         seg_list_having_0(symbol, seg_list_list[i]))]
                seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(
                    seg_list_having_0(symbol, seg_list_list[i])) + 1:])
                seg_list_list[i] = seg_list_list_temp
    return return_seg_list(seg_list_list)


def delete_have_other(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    seg_list_list_temp = []
    for i in range(len(seg_list_list)):
        if i == 0:
            seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
        for j in range(len(seg_list_list_temp)):
            if seg_list_list[i] == seg_list_list_temp[j]:
                break
            if j + 1 >= len(seg_list_list_temp):
                seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i])
    seg_temp = []
    for i in range(len(seg_list_list_temp)):
        seg_temp.extend(seg_list_list_temp[i])
        seg_temp.extend(",")
    return seg_temp


def transition_divide_temp(seg_list_letter, seg_list_angle, seg_list_list_key):
    temp = []
    temp.insert(len(temp), seg_list_letter)
    temp.insert(len(temp), seg_list_list_key)
    temp.extend(seg_list_angle)
    temp.extend(",")
    temp.insert(len(temp), seg_list_letter)
    temp.extend(",")
    return temp


def transition_divide(seg_list):  # 平分
    seg_list = "".join(seg_list)
    seg_list = list(jieba.cut(seg_list, cut_all=False))
    if re.search(".*垂直平分", "".join(seg_list)):
        seg_list_letter = find_all_letter_return_side_letter(seg_list)
        if len(seg_list_letter) == 0:
            return ""
        elif len(seg_list_letter) == 1:
            return seg_list
        symbol_letter = []
        symbol_point = []
        for i in range(len(seg_list_letter)):
            if seg_list_letter[i][0] == 2:
                symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
            else:
                symbol_point.insert(len(symbol_point), seg_list_letter[i][1])
        seg_list_temp = []
        seg_list_temp.insert(len(seg_list_temp), symbol_letter[0])
        seg_list_temp.extend("⊥")
        seg_list_temp.insert(len(seg_list_temp), symbol_letter[1])
        if len(symbol_point) == 1:
            seg_list_temp.extend("于")
            seg_list_temp.insert(len(seg_list_temp), symbol_point[0])
        seg_list_temp.extend(",")
        seg_list_temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
        seg_list = seg_list_temp
    elif re.search(".*平分", "".join(seg_list)):
        seg_list_letter = find_all_letter_return_side_letter(seg_list)
        if len(seg_list_letter) == 0:
            return ""
        elif len(seg_list_letter) == 1 and seg_list_letter[0][0] == 2:
            return seg_list_letter[0][1]
        else:
            symbol_angle = []
            symbol_triangle = []
            symbol_letter = []
            for i in range(len(seg_list_letter)):
                if seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in "∠":
                    symbol_angle_temp = ["∠"]
                    symbol_angle_temp.insert(len(symbol_angle_temp), seg_list_letter[i][1])
                    symbol_angle.insert(len(symbol_angle), symbol_angle_temp)
                elif seg_list[seg_list.index(seg_list_letter[i][1]) - 1] in map_clear_up_keywords:
                    symbol_triangle_temp = []
                    symbol_triangle_temp.insert(len(symbol_triangle_temp),
                                                seg_list[seg_list.index(seg_list_letter[i][1]) - 1])
                    symbol_triangle_temp.insert(len(symbol_triangle_temp), seg_list_letter[i][1])
                    symbol_triangle.insert(len(symbol_triangle), symbol_triangle_temp)
                else:
                    symbol_letter.insert(len(symbol_letter), seg_list_letter[i][1])
            if len(symbol_triangle) == 0:
                temp = []
                if len(symbol_angle) == 0:
                    if return_re_return([".*互相平分"], "".join(seg_list)):
                        for i in range(len(symbol_letter)):
                            for j in range(len(symbol_letter)):
                                temp.extend(transition_divide_temp(symbol_letter[i], symbol_letter[j], "平分"))
                    elif len(symbol_letter) == 2:
                        temp.extend(transition_divide_temp(symbol_letter[0], symbol_letter[1], "平分"))
                else:
                    if len(symbol_angle) == len(symbol_letter):
                        for i in range(len(symbol_angle)):
                            temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
                    else:
                        for i in range(len(symbol_letter)):
                            temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[0], "平分"))
                if len(temp) == 0:  # 此处为补丁，即出现∠CAB的平分线
                    temp = seg_list
                seg_list = temp
            else:
                temp = []
                if len(symbol_angle) == len(symbol_letter):
                    for i in range(len(symbol_triangle)):
                        temp.insert(len(temp), symbol_triangle[i][0])
                        temp.insert(len(temp), symbol_triangle[i][1])
                        temp.extend(",")
                    for i in range(len(symbol_angle)):
                        temp.extend(transition_divide_temp(symbol_letter[i], symbol_angle[i], "平分"))
                elif len(symbol_triangle) == 1 and len(symbol_letter) == 1:
                    seg_list_temp = seg_list_having_0(symbol_letter[0], symbol_triangle[0][1])
                    temp.extend(symbol_triangle[0])
                    temp.extend(",")
                    temp.extend(symbol_letter)
                    temp.extend("平分")
                    temp.extend("∠")
                    temp.extend(seg_list_temp)
                    temp.extend(",")
                    temp.extend(symbol_letter)
                seg_list = temp
    return seg_list


def transition_S_C(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        seg_temp = []
        if return_re_return([".*面积", ".*周长"], "".join(seg_list_list[i])):
            seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
            symbol_ = []
            seg_list_list_temp = []
            for j in range(len(seg_letter)):  # 求主要的图形
                if seg_letter[j][0] >= 3 and \
                        seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1] in map_clear_up_keywords:
                    symbol_.insert(len(symbol_), seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) - 1])
                    symbol_.insert(len(symbol_), seg_letter[j][1])
                    seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index(seg_letter[j][1]) - 1]
                    seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index(seg_letter[j][1]) + 1:])
            seg_letter = find_all_letter_return_side_letter(seg_list_list_temp)
            seg_num = []
            for j in range(len(seg_list_list_temp)):
                if if_number(seg_list_list_temp[j]) or if_letter(seg_list_list_temp[j]) or \
                        seg_list_list_temp[j] in symbol_keywords:
                    seg_num.insert(len(seg_num), seg_list_list_temp[j])
                    # if j + 1 < len(seg_list_list_temp) and seg_list_list_temp[j + 1] in ["cm", "dm", "m", "km"]:
                    #     seg_num.insert(len(seg_num),seg_list_list_temp[j + 1])
            if re.search(".*面积", "".join(seg_list_list[i])):
                seg_temp.insert(len(seg_temp), "S")
            elif re.search(".*周长", "".join(seg_list_list[i])):
                seg_temp.insert(len(seg_temp), "C")
            seg_temp.extend(symbol_)
            if len(seg_num) != 0:
                seg_temp.extend("=")
                seg_temp.extend(seg_num)
            seg_list_list[i] = seg_temp
        elif seg_list_having("长", seg_list_list[i]):
            seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
            seg_symbol = seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]):]
            seg_num = []
            for j in range(len(seg_list_list[i])):
                if if_number(seg_list_list[i][j]):
                    seg_num.insert(len(seg_num), seg_list_list[i][j])
                    if j + 1 < len(seg_list_list[i]) and seg_list_list[i][j + 1] in ["cm", "dm", "m", "km"]:
                        seg_num.insert(len(seg_num), seg_list_list[i][j + 1])
            seg_temp.insert(len(seg_temp), "l")
            seg_temp.insert(len(seg_temp), seg_letter[0][1])
            if len(seg_num) != 0:
                seg_temp.extend("=")
                seg_temp.extend(seg_num)
            seg_list_list[i] = seg_temp

    return return_seg_list(seg_list_list)


def transition_parallel(seg_list):
    seg_list_letter = find_all_letter_return_side_letter(seg_list)
    if len(seg_list_letter) == 2:
        seg_list_temp = []
        seg_list_temp.insert(len(seg_list_temp), seg_list_letter[0][1])
        seg_list_temp.insert(len(seg_list_temp), "//")
        seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
        seg_list_temp.extend(",")
        seg_list_temp.insert(len(seg_list_temp), seg_list_letter[1][1])
        seg_list = seg_list_temp
    return seg_list


def transition_parallel_tran(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if "//" in seg_list_list[i]:
            seg_temp = seg_list_list[i][:seg_list_list[i].index("//")]
            seg_temp.insert(len(seg_temp), "平行")
            seg_temp.extend(seg_list_list[i][seg_list_list[i].index("//") + 1])
            seg_list_list[i] = seg_temp
    seg_temp = []
    for i in range(len(seg_list_list)):
        seg_temp.extend(seg_list_list[i])
        seg_temp.extend(",")
    return seg_temp


def transition_pause(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if re.search(".*、", "".join(seg_list_list[i])):
            seg_list_list_temp = []
            seg_list_list_behind = []
            seg_list_list_front = seg_list_list[i]
            while re.search(".*、", "".join(seg_list_list_front)):
                seg_list_list_behind = seg_list_list_front[:seg_list_list_front.index("、")]
                seg_list_list_front = seg_list_list_front[seg_list_list_front.index("、") + 1:]
                seg_list_list_behind = behind_operation(seg_list_list_behind)
                seg_list_list_temp.extend(seg_list_list_behind)
                seg_list_list_temp.extend(",")
            seg_list_list_behind = behind_operation(seg_list_list_behind)
            seg_list_list_temp.extend(seg_list_list_behind)
            seg_list_list_temp.extend(",")
            seg_list_list[i] = seg_list_list_temp
    return return_seg_list(seg_list_list)


def return_re_return(input_list, seg_list_list):
    for i in range(len(input_list)):
        if re.search(input_list[i], "".join(seg_list_list)) is not None:
            return True
    return False


# 切割后续处理的“和”
def cut_seg_list_and(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if re.search(".*和", "".join(seg_list_list[i])):
            seg_front = seg_list_list[i][:seg_list_list[i].index("和")]
            seg_behind = seg_list_list[i][seg_list_list[i].index("和") + 1:]
            seg_front = behind_operation(seg_front)
            seg_behind = behind_operation(seg_behind)
            seg_list_list_temp = seg_front
            seg_list_list_temp.extend(",")
            seg_list_list_temp.extend(seg_behind)
            seg_list_list[i] = seg_list_list_temp
    return return_seg_list(seg_list_list)


def behind_operation(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
        if len(seg_list_letter) == 0:  # 不存在关系
            if seg_list_having("∠", seg_list_list[i]):
                for j in range(len(seg_list_list)):
                    seg_list_list[j] = ""
            else:
                seg_list_list[i] = ""
        if return_re_return([".*作"], seg_list_list[i]):
            if re.search(".*于", "".join(seg_list_list[i])) is None:
                seg_list_list[i] = guozuo("".join(seg_list_list[i]))
            else:
                seg_list_list[i] = guozuoyu("".join(seg_list_list[i]))
            seg_list_list[i] = list(jieba.cut(seg_list_list[i], cut_all=False))  # 精确模式切割词句
        elif re.search(".*交", "".join(seg_list_list[i])) is not None:
            seg_list_list[i] = transition_hand_over(seg_list_list[i])  # 交
        elif return_re_return(
                ["在.*上", "是.*点", "为.*点", "取.*点", "在.*中", ".*共线", "延长.*点", "任意.*点", "过.*点",
                 "在.*内", ".*延长", "点.*在", "时.*点", "在.*的"], seg_list_list[i]):
            seg_list_list[i] = transition_point_at_side_re(seg_list_list[i])  # 借助re处理点在线上
        elif seg_list_having("点", seg_list_list[i]):
            seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            if len(seg_list_list_letter) == 1:
                seg_list_list[i] = seg_list_list[i][seg_list_list[i].index("点") + 1:]
        elif seg_list_having_0(["连接", "连结", "链接", "线段", "若", "设", "直线"], seg_list_list[i]):
            seg_list_list[i] = delete_line_and_line(["连接", "连结", "链接", "线段", "若", "设", "直线"],
                                                    seg_list_list[i])  # 将连接AB删除
        elif return_re_return([".*平行"], seg_list_list[i]):
            seg_list_list[i] = transition_parallel(seg_list_list[i])
        elif re.search(".*平分", "".join(seg_list_list[i])):
            seg_list_list[i] = transition_divide(seg_list_list[i])
        elif re.search(".*、", "".join(seg_list_list[i])):
            seg_list_list[i] = transition_pause(seg_list_list[i])
        elif re.search(".*对角线", "".join(seg_list_list[i])):
            seg_list_list[i] = transition_diagonal(seg_list_list[i])
        elif re.search(".*和", "".join(seg_list_list[i])):
            seg_list_list[i] = cut_seg_list_and(seg_list_list[i])
        elif return_re_return([".*面积", ".*周长"], seg_list_list[i]) or seg_list_having("长", seg_list_list[i]):
            seg_list_list[i] = transition_S_C(seg_list_list[i])  # 处理面积和周长
        elif re.search("的度数", "".join(seg_list_list[i])):
            seg_list_list[i] = seg_list_list[i][:seg_list_list[i].index("的")]
        elif re.search(".*高", "".join(seg_list_list[i])):
            seg_list_list[i] = transition_high(seg_list_list[i])
        elif seg_list_having(["中"], seg_list_list[i]):
            seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("中")]
            seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("中") + 1:])
            seg_list_list[i] = seg_list_list_temp
        elif return_re_return([".*两点"], "".join(seg_list_list[i])):
            seg_list_list_temp = seg_list_list[i][:seg_list_list[i].index("两点")]
            seg_list_list_temp.extend(seg_list_list[i][seg_list_list[i].index("两点") + 1:])
            seg_list_list[i] = seg_list_list_temp
        elif return_re_return([".*中点"], "".join(seg_list_list[i])):
            seg_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            if len(seg_list_letter) == 2:
                seg_list_list[i] = return_the_point_at_line_temp(seg_list_letter[0][1], seg_list_letter[1][1], "中点")
        elif return_re_return(["垂直.*于"], "".join(seg_list_list[i])):
            for j in range(len(seg_list_list[i])):
                if seg_list_list[i][j] == "垂直":
                    seg_list_list[i][j] = "⊥"
        elif len(seg_list_letter) == 1 and not seg_list_having(map_clear_up_keywords, seg_list_list[i]) and \
                not seg_list_having(symbol_keywords_main, seg_list_list[i]) and \
                not seg_list_having(symbol_keywords, seg_list_list[i]):
            seg_list_list[i] = seg_list_letter[0][1]

    seg_list = return_seg_list(seg_list_list)
    while len(seg_list) != 0 and seg_list[len(seg_list) - 1] == ",":
        seg_list = seg_list[:len(seg_list) - 1]
    return seg_list


def delete_other_point_line(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        seg_letter = find_all_letter_return_side_letter(seg_list_list[i])
        seg_long = 0
        for j in range(len(seg_letter)):
            seg_long += seg_letter[j][0]
        if seg_long == len("".join(seg_list_list[i])):
            seg_list_list[i] = ""
        if return_re_return([".*的长", ".*的延长线"], "".join(seg_list_list[i])) and len(seg_letter) == 1:
            seg_list_list[i] = ""
        if len(seg_letter) == 1 and seg_letter[0][1] in seg_list_list[i] and \
                seg_list_list[i].index(seg_letter[0][1]) - 1 >= 0 \
                and seg_list_list[i][seg_list_list[i].index(seg_letter[0][1]) - 1] in ["∠", "l"] and \
                seg_list_list[i].index(seg_letter[0][1]) + 1 == len(seg_list_list[i]):  # 只有单独的角
            seg_list_list[i] = ""
        if "∠" in seg_list_list[i] and seg_list_list[i].index("∠") + 1 < len(seg_list_list[i]) and if_number(
                seg_list_list[i][seg_list_list[i].index("∠") + 1]):
            return ""
    seg_temp = []
    for i in range(len(seg_list_list)):
        seg_temp.extend(seg_list_list[i])
        seg_temp.extend(",")
    return seg_temp


# 处理高
def transition_high(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    seg_list_temp = []
    for i in range(len(seg_list_list)):
        if re.search(".*高", "".join(seg_list_list[i])):
            seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
            seg_list_list_temp = []
            for j in range(len(seg_list_all_triangle)):
                if (len(seg_list_list_letter) == 2 and seg_list_list_letter[0][0] == 2 and
                        seg_list_having_all(seg_list_list_letter[0][1], seg_list_all_triangle[j][1])):
                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
                    seg_list_list_temp.extend("是")
                    seg_list_list_temp.extend(seg_list_all_triangle[j])
                    seg_list_list_temp.extend("的")
                    seg_list_list_temp.extend("高")
                    seg_list_list_temp.extend(",")
                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[1][1])
                    seg_list_list_temp.extend(",")
                elif len(seg_list_list_letter) == 2 and seg_list_list_letter[1][0] == 2 and \
                        seg_list_having_all(seg_list_list_letter[1][1], seg_list_all_triangle[j][1]):
                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
                    seg_list_list_temp.extend("是")
                    seg_list_list_temp.extend(seg_list_all_triangle[j])
                    seg_list_list_temp.extend("的")
                    seg_list_list_temp.extend("高")
                    seg_list_list_temp.extend(",")
                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
                    seg_list_list_temp.extend(",")
                elif len(seg_list_list_letter) == 1 and seg_list_list_letter[0][0] == 2:
                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
                    seg_list_list_temp.extend("是")
                    seg_list_list_temp.extend(seg_list_all_triangle[0])
                    seg_list_list_temp.extend("的")
                    seg_list_list_temp.extend("高")
                    seg_list_list_temp.extend(",")
                    if "=" in seg_list_list[i]:
                        seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
                        seg_list_list_temp.extend("=")
                        for j in range(len(seg_list_list[i])):
                            if if_number(seg_list_list[i][j]):
                                seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list[i][j])
                        seg_list_list_temp.extend(",")

                    seg_list_list_temp.insert(len(seg_list_list_temp), seg_list_list_letter[0][1])
                    seg_list_list_temp.extend(",")
            seg_list_list[i] = seg_list_list_temp
    seg_temp = []
    for i in range(len(seg_list_list)):
        seg_temp.extend(seg_list_list[i])
        seg_temp.extend(",")
    return seg_temp


def find_all_triangle(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
        for j in range(len(seg_list_list_letter)):
            if seg_list_list_letter[j][0] >= 3 and seg_list_list[i].index(seg_list_list_letter[j][1]) - 1 >= 0 and \
                    seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1] in map_clear_up_keywords:
                seg_list_temp_temp = []
                seg_list_temp_temp.insert(len(seg_list_temp_temp),
                                          seg_list_list[i][seg_list_list[i].index(seg_list_list_letter[j][1]) - 1])
                seg_list_temp_temp.insert(len(seg_list_temp_temp), seg_list_list_letter[j][1])
                if seg_list_temp_temp not in seg_list_all_triangle:  # 防止重复
                    seg_list_all_triangle.insert(len(seg_list_all_triangle), seg_list_temp_temp)
    return seg_list_all_triangle


def dispose_waist_and_diagonal(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    seg_list_list_letter_ABC = []
    for i in range(len(seg_list_list)):
        seg_list_list_letter = find_all_letter_return_side_letter(seg_list_list[i])
        seg_list_list_letter_A = []
        seg_list_list_letter_AB = []
        for j in range(len(seg_list_list_letter)):
            if seg_list_list_letter[j][0] == 2:
                seg_list_list_letter_AB.insert(len(seg_list_list_letter_AB), seg_list_list_letter[j][1])
            elif seg_list_list_letter[j][0] == 1:
                seg_list_list_letter_A.insert(len(seg_list_list_letter_A), seg_list_list_letter[j][1])
            else:
                seg_list_list_letter_ABC.insert(len(seg_list_list_letter_ABC), seg_list_list_letter[j][1])
        if re.search(".*对角线", "".join(seg_list_list[i])):
            if len(seg_list_list_letter_AB) == 0:
                seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
                if len(seg_list_list_letter_ABC_1) == 4:
                    wei_temp = seg_list_list[i].index("对角线") + 1
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = "、"
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[3]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    print(seg_list_list[i])
        if seg_list_having("腰", seg_list_list[i]):
            if len(seg_list_list_letter_AB) == 0:
                seg_list_list_letter_ABC_1 = seg_list_list_letter_ABC[len(seg_list_list_letter_ABC) - 1]  # 最后一个图形
                if len(seg_list_list_letter_ABC_1) == 3:
                    wei_temp = re.search(".*对角线", "".join(seg_list_list[i])).end()
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[1]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = "、"
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[2]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    print(seg_list_list[i])

                if len(seg_list_list_letter_ABC_1) == 4:
                    wei_temp = seg_list_list[i].index("腰") + 1
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[0] + seg_list_list_letter_ABC_1[3]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = "、"
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    seg_list_list_letter_AB_temp = seg_list_list_letter_ABC_1[1] + seg_list_list_letter_ABC_1[2]
                    seg_list_list[i].insert(wei_temp, seg_list_list_letter_AB_temp)
                    print(seg_list_list[i])
    seg_list = return_seg_list(seg_list_list)
    return seg_list


def clean_all_triangle():
    seg_list_all_triangle.clear()


def delete_other_line(seg_list):
    seg_list_list = return_seg_list_list(seg_list)
    for i in range(len(seg_list_list)):
        if len(seg_list_list[i]) < 2:
            for j in range(0, i):
                if seg_list_having(seg_list_list[i], seg_list_list[i - j - 1]):
                    seg_list_list[i] = ""
                    break
    seg_list = return_seg_list(seg_list_list)
    return seg_list


def cut_word(txt_data):
    try:
        seg_list = list(jieba.cut(txt_data, cut_all=False))  # 精确模式切割词句
        # print("".join(seg_list))
        # seg_list = is_half_angle(seg_list)#全角转半角
        seg_list = conversion_parallel(seg_list)  # 对//进行处理
        seg_list = remove_pause(seg_list)  # 去除前面的序号
        seg_list = find_if_have_parallel_and_equal(seg_list)  # 特殊值判断是否有平行且相等
        seg_list = conversion_symbols(seg_list)  # 将转换为文字
        seg_list = list(jieba.cut("".join(seg_list), cut_all=False))
        seg_list = conversion_parallel(seg_list)  # 对//进行处理
        seg_list = seg_list_transition_side(seg_list)  # lAB = 5 --转变---> 边AB = 5
        seg_list = delete_prove(seg_list)  # 删除“求证”
        seg_list = handles_greater_or_less(seg_list)  # 将<=或者>=进行规范化处理
        seg_list = delete_blank(seg_list)  # 删除空格
        seg_list = add_de_to_side(seg_list)  # 给长宽高前适当的加"的"
        seg_list = transition_side(seg_list)  # 将三边等转换成具体字母
        seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
        # print("####分别####\t:", "".join(seg_list))
        seg_list = add_all_shape(seg_list)  # 给所有超过三个字母的字母添加基础形状
        seg_list = delete_repetition_symbol(seg_list)  # 去除重复的图形
        seg_list = add_all_letter(seg_list)  # 将单独出现的三角形补全字母
        seg_list = dispose_waist_and_diagonal(seg_list)  # 处理对角线与腰
        seg_list = add_all_shape_at_front(seg_list)  # 防止出现三角形ABC\DEF\GHZ   #处理形状在前面
        seg_list = add_all_shape_at_behind(seg_list)  # 将四边形ABCD\EFGH都是正方形分开为正方形ABCD\正方形EFGH   #处理形状在后面
        seg_list = transition_equal_or_similarity(seg_list)  # 处理连等的情况
        seg_list = dispose_shi_and_symbol(seg_list)  # 处理四边形ABCD是正方形的情况
        find_all_triangle(seg_list)  # 记录所有的多边形
        seg_list = transition_litter_to_super(seg_list)  # 将小写转换为大写(三角形,角)
        seg_list = add_comma_at_equal(seg_list)  # 在连等后面加上逗号，清除垂足为或者垂足于  AB⊥BD,垂足是B点 -- >  AB⊥BD于B
        seg_list = cut_zuo_from_seg_list(seg_list)  # 将作从（过A 左AS垂直于DF)提取出来
        seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
        seg_list = add_to_the_vertical(seg_list)  # 将垂足于A,添加到前一步的句子中
        # print("".join(seg_list))
        seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
        seg_list = cut_respect_is_importance(seg_list, "交")  # 处理交
        # seg_list = transition_S_C(seg_list)  # 处理面积和周长
        seg_list = tran_wei_to_fen_bie(seg_list)  # 将为转变为 分别为
        seg_list = cut_respect_is_importance(seg_list, "分别")  # 处理分别
        seg_list = delete_blank(seg_list)  # 删除空格
        seg_list = transition_angle_to_angle(seg_list)  # 将符号角平分线更改为角平分线

        seg_list = behind_operation(seg_list)  # 后续操作
        seg_list = transition_parallel_tran(seg_list)  # 将//转换为平行
        seg_list = seg_list_complement(seg_list)  # 补全 角的字母
        seg_list = transition_triangle_symbol(seg_list, "三角形")  # 将三角形转换为符号

        seg_list = delete_have_other(seg_list)  # 去重
        seg_list = delete_other_line(seg_list)  # 去重
        # seg_list = delete_other_point_line(seg_list)  # 删去单独的点和线与角
        seg_list = delete_unnecessary_comma(seg_list)  # 去除不必要的逗号
        seg_list = add_end_punctuation(seg_list)  # 给末尾加上;
        clean_all_triangle()  # 清除记录的多边形
        with open(txt_output, "a", encoding="utf-8") as fw:
            fw.write("".join(seg_list))
            fw.write("\n")
        print("".join(seg_list))
        if len(seg_list)<1:
            return "error"
    except:
        traceback.print_exc()
        return "error"

def process():
    setDir(txt_output[:-12])
    for word in map_keywords:
        jieba.add_word(word)  # 分词时添加关键词
    for word in jieba_have_delete:
        jieba.del_word(word)
    file = open(txt_input, 'r', encoding="utf-8", errors="ignore")  # 打开文件
    data = " "
    while data:
        data = file.readline()
        # data = data[:-1]  # 逐行读取文件，也就是提取出每一题
        if data != "" and data != "\n":
            t=cut_word(data)
            # print(data)
            if(t==False):
                file.close()  # 确保文件被关闭
                return False
    file.close()  # 确保文件被关闭


def setDir(filepath):
    #没有文件夹就创建，有就清空
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

def process_text(data):
    setDir(txt_output[:-12])
    for word in map_keywords:
        jieba.add_word(word)  # 分词时添加关键词
    for word in jieba_have_delete:
        jieba.del_word(word)
    cut_word(data)












