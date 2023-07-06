from tasks_checker import TaskChecker

def my_max(list):
	m = list[0]
	for i in list:
		if i > m:
			m=i
	return m


user_solution = 'my_max(list): \n return m(list)'

test_cases = [
    ([75,45,67,12], 75),
    ([-99,-1,-10,-8], -1),
    ([7,45,67,12], 67),
]

print(TaskChecker(user_solution, test_cases).check())