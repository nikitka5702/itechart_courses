class Department:
    class BudgetError(ValueError):
        pass

    def __init__(
            self,
            name: str,
            employees: dict,
            budget: int
    ):
        self.name = name
        self.employees = employees
        self.budget = budget

    def get_budget_plan(self):
        val = self.budget - sum(self.employees.values())
        if val < 0:
            raise Department.BudgetError
        return val

    @property
    def average_salary(self):
        return round(sum(self.employees.values()) / len(self.employees), 2)

    @staticmethod
    def merge_departments(*deps):
        deps = sorted(deps, key=lambda x: (-x.average_salary, x.name))
        obj = Department(
            ' - '.join(d.name for d in deps),
            {k: v for d in deps for k, v in d.employees.items()},
            sum(d.budget for d in deps)
        )
        try:
            obj.get_budget_plan()
        except Department.BudgetError:
            raise
        return obj

    def __add__(self, other):
        return Department.merge_departments(self, other)

    def __str__(self):
        return '{name} ({employees} - {avg}, {budget})'.format(
            name=self.name,
            employees=len(self.employees),
            avg=self.average_salary,
            budget=self.budget
        )

    def __or__(self, other):
        try:
            p1, p2 = self.get_budget_plan(), other.get_budget_plan()
        except Department.BudgetError:
            raise
        return self if p1 >= p2 else other
