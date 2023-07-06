from tasks_checker import TaskChecker

def func(aList):
	aList = aList[::-1]
	return aList

user_solution = 'func(list): \n return aList(list)'

test_cases = [
    ([75,45,67,12], [12,67,45,75]),
    ([10,7,8,12], [12,8,7,10]),
    ([89,30,6,31], [31,6,30,89]),
]

print(TaskChecker(user_solution, test_cases).check())


