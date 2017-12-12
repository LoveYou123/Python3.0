import copy

# person =['name',['saving',100]]

# '''#浅copy
# p1 = copy.copy(person)
# p2 = person[:]
# p3 = list(person)
# print(p3)
# '''
# #深copy
# p1 = person[:]
# p2 = person[:]
# p1[0] ='alex'
# p2[0] = 'fengjie'
# print(p1)
# print(p2)

#shopping list

product_list = [
    ('iphone',5800),
    ('Mac Pro',9800),
    ('Bike',800),
    ('Watch',10600),
    ('coffee',31),
    ('Alex Python',120)
]
shopping_list =[]
salary = input('请输入你当前的薪水：')
if salary.isdigit():
    salary = int(salary)
    while True:
        for index,item in enumerate(product_list):
            # print(product_list.index(item),item)
            print(index,item)

        user_choice = input('选择要买的商品>>>:')
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(product_list) and user_choice >-1:
                P_item = product_list[user_choice]
                if P_item[1] <= salary:
                    shopping_list.append(P_item)
                    salary -= P_item[1]
                    print("Added %s into shopping card,your current balance is \033[31;1m %s\033[0m"%(P_item,salary))
                else:
                    print('\033[41;1m 余额只剩下[%s]元，请充值！ \033[0m'%salary)
            else:
                print("不存在商品%s"%user_choice)


        elif user_choice =='q':
            print('==========以下是所购买的商品列表===========')

            for p in shopping_list:
                print(p)
            print('您当前余额为:',salary)
            exit()
        else:
            print('Invalid option')







