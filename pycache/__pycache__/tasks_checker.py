import re

class TaskChecker:
    ''' Class for check users python code.
        Attributes
        ----------
        solution : string
            users function code for checking
        test_cases : list of tuples
            each tuples consist test and correct anwer 
        Methods
        -------
        check()
    '''


    def __init__(self, solution, test_cases):
        self.solution = solution
        self.test_cases = test_cases


    def check(self):
        """ Execute users function and check with test cases.
        Return -1882779 if code crashed,  else
        procent of correct test runs.
        """


        function_name = re.findall(
            r'def\s+(\w+)\s*\(', 
            self.solution
            )[0]
        exec(self.solution, globals())
        func = globals()[function_name]

        num_passed_tests = 0

        for test_input, expected_output in self.test_cases:
            try:
                user_output = func(test_input)
                if user_output == expected_output:
                    num_passed_tests += 1
            except Exception:
                num_passed_tests = -1 

        if num_passed_tests > 0:
            num_passed_tests = num_passed_tests / len(self.test_cases) * 100

        return num_passed_tests