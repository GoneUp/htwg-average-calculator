import json
from enum import Enum


class Operators(Enum):
    EQ = 0,
    GT = 1,
    LT = 2,
    CONTAINS = 3

class Rule:
    def __init__(self, field, operator, operand):
        self.field = field
        self.operand = operand
        if self.operand == "None":
            self.operand = None

        if operator == "eq":
            self.operator = Operators.EQ
        elif operator == "gt":
            self.operator = Operators.GT
        elif operator == "lt":
            self.operator = Operators.LT
        elif operator == "contains":
            self.operator = Operators.CONTAINS
        else:
            print(f"Operator {operator} is unknown!")

    def __str__(self):
        return f"Field {self.field}, Operator {self.operator}, Operand {self.operand}"



class CourseRules():
    def __init__(self, name):
        self.name = name
        self.mode = ""
        self.rules = list()

    def __str__(self):
         return f"Name {self.name}, Mode {self.mode}, Rules {self.rules}"

def load_ruleset(course, debug):
    ruleset = dict()

    try:
        with(open("ruleset")) as fp:
            lines = fp.readlines()
            final_str = str(u"")

            for line in lines:
                if line.startswith("#") or line.isspace():
                    continue
                final_str += line

            rules = json.loads(final_str)

            if debug:
                print(rules)

            for config in rules['configs']:
                obj = CourseRules(config)
                obj.mode = rules['configs'][config]['mode']

                for json_rule in rules['configs'][config]['rules']:
                    rule = Rule(json_rule['field'], json_rule['operator'], json_rule['operand'])
                    obj.rules.append(rule)

                if debug:
                    print(obj)
                    for x in obj.rules:
                        print(x)


                ruleset[config] = obj


        return ruleset[course]
    except Exception as err:
        print(err)
        exit(1)


def rule_matches(rule, graderow):
    value = None

    if rule.field == "STG":
        value = graderow.STG
    elif rule.field == "number":
        value = graderow.number
    elif rule.field == "text":
        value = graderow.text
    elif rule.field == "semester":
        value = graderow.semester
    elif rule.field == "etcs":
        value = graderow.etcs
    else:
        print(f"Invalid rule field: {rule.field}")
        exit(1)

    if rule.field == "number" or rule.field == "etcs":
        if rule.operand is not None:
            rule.operand = int(rule.operand)

    if rule.operator == Operators.EQ:
        return value == rule.operand
    elif rule.operator == Operators.LT:
        return  value < rule.operand
    elif rule.operator == Operators.GT:
        return value > rule.operand
    elif rule.operand == Operators.CONTAINS:
        return rule.operand in value
    else:
        print(f"Unknown operator {rule.operator}")
        exit(1)


    # Fields STG number text semester etcs

