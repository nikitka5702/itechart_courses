import unittest

from hw2.f1 import Department


BudgetError = Department.BudgetError


class DepartmentTestClass(unittest.TestCase):
    def test_get_budget_plan(self):
        d1 = Department(
            'TestDepartment1',
            {
                'u1': 13,
                'u2': 5.2,
                'u3': 4.6
            },
            120
        )
        d2 = Department(
            'TestDepartment2',
            {
                'u1': 13,
                'u2': 5.2,
                'u3': 4.6
            },
            20
        )
        self.assertEqual(97.2, d1.get_budget_plan())
        with self.assertRaises(BudgetError):
            d2.get_budget_plan()
    
    def test_average_salary(self):
        d1 = Department(
            'TestDepartment1',
            {
                'u1': 13,
                'u2': 5.2,
                'u3': 4.6
            },
            120
        )
        d2 = Department(
            'TestDepartment2',
            {
                'u1': 13,
                'u2': 19,
                'u3': 27.5
            },
            260
        )
        self.assertFalse(callable(Department.average_salary))
        self.assertEqual(7.6, d1.average_salary)
        self.assertEqual(19.83, d2.average_salary)
    
    def test_merge_departments(self):
        d1 = Department(
            'TestDepartment1',
            {
                'u1': 13,
                'u2': 5.2,
                'u3': 4.6
            },
            120
        )
        d2 = Department(
            'TestDepartment2',
            {
                'u1': 13,
                'u2': 19,
                'u3': 27.5
            },
            260
        )

        self.assertEqual('TestDepartment1 (3 - 7.6, 120)', str(d1))
        self.assertEqual('TestDepartment2 - TestDepartment1 (3 - 7.6, 380)', str(Department.merge_departments(d1, d2)))
        self.assertEqual('TestDepartment2 - TestDepartment1 (3 - 7.6, 380)', str(d1 + d2))
