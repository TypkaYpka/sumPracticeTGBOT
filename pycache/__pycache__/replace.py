from tasks_checker import TaskChecker

def func(list1):
      
 try:
      index = list1.index(5)
      list1[index] = 8
 except ValueError:
      print("Элемент не найден")
 return list1

user_solution = 'func(list1): \n return list1'

test_cases = [
    ([0,1,2,3], [0,1,2,3]),
    ([0,1,2,5,8,9],[0,1,2,8,8,9]),
    ([5,5,7,3],[8,5,7,3]),
]

print(TaskChecker(user_solution, test_cases).check())

