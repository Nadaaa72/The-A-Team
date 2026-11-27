# Inference engine

def is_var(value):
    return isinstance(value, str) and value.startswith("?")


def fmt_fact(fact):
    args = []
    for value in fact[1:]:
        args.append(str(value))

    return fact[0] + "(" + ", ".join(args) + ")"


def check_guard(guard, bindings):
    variable = guard[0]
    operator = guard[1]
    value = guard[2]

    x = bindings[variable]

    if operator == ">=":
        return x >= value
    elif operator == ">":
        return x > value
    elif operator == "==":
        return x == value
    elif operator == "in":
        return x in value

    raise ValueError("Unknown guard operator: " + str(operator))


class Rule:
    def __init__(self, name, conditions, then, description="", guards=None):
        self.name = name
        self.conditions = conditions
        self.then = then
        self.description = description

        if guards is None:
            self.guards = []
        else:
            self.guards = guards


class Justification:
    def __init__(self, fact, rule, bindings, premises, round_number):
        self.fact = fact
        self.rule = rule
        self.bindings = bindings
        self.premises = premises
        self.round_number = round_number


class ProofNode:
    def __init__(self, goal, rule_name, description, children):
        self.goal = goal
        self.rule_name = rule_name
        self.description = description
        self.children = children


def match(pattern, fact, bindings):
    if len(pattern) != len(fact) or pattern[0] != fact[0]:
        return None

    new_bindings = dict(bindings)

    for p, value in zip(pattern[1:], fact[1:]):
        if is_var(p):
            if p in new_bindings and new_bindings[p] != value:
                return None

            new_bindings[p] = value

        elif p != value:
            return None

    return new_bindings


def substitute(pattern, bindings):
    result = []

    for term in pattern:
        if is_var(term):
            if term not in bindings:
                raise KeyError("Unbound variable " + term)

            result.append(bindings[term])
        else:
            result.append(term)

    return tuple(result)


class InferenceEngine:
    def __init__(self, rules):
        self.rules = list(rules)
        self.facts = {}
        self.given = set()
        self.rounds = [[]]
        self.firings = []
        self.fired = set()

    # Working memory

    def assert_fact(self, fact):
        fact = tuple(fact)

        if fact in self.facts:
            return False

        self.facts[fact] = [
            Justification(fact, None, {}, (), 0)
        ]

        self.given.add(fact)
        self.rounds[0].append(fact)

        return True

    def assert_facts(self, facts):
        for fact in facts:
            self.assert_fact(fact)

    def assert_derived(self, fact, label, description, premises=()):
        fact = tuple(fact)
        rule = Rule(label, [], [fact], description)

        justification = Justification(
            fact, rule, {}, tuple(premises), len(self.rounds)
        )

        added = self.add_fact(fact, justification)

        if added:
            self.rounds.append([fact])
            self.firings.append(justification)

        return added

    def holds(self, fact):
        return tuple(fact) in self.facts

    def facts_with(self, predicate):
        found = []

        for fact in self.facts:
            if fact[0] == predicate:
                found.append(fact)

        return found

    def query(self, pattern):
        found = []

        for fact in self.facts_with(pattern[0]):
            if match(pattern, fact, {}) is not None:
                found.append(fact)

        found.sort(key=str)

        return found

    def add_fact(self, fact, justification):
        if fact in self.facts:
            already_added = False

            for existing in self.facts[fact]:
                if existing.rule is justification.rule:
                    already_added = True
                    break

            if not already_added:
                self.facts[fact].append(justification)

            return False

        self.facts[fact] = [justification]

        return True

    # Forward chaining

    def find_matches(self, rule):
        results = []
        self.extend_match(rule, 0, {}, (), results)

        return results

    def extend_match(self, rule, i, bindings, premises, results):
        if i == len(rule.conditions):
            for guard in rule.guards:
                if not check_guard(guard, bindings):
                    return

            results.append((bindings, premises))
            return

        pattern = rule.conditions[i]

        for fact in self.facts_with(pattern[0]):
            new_bindings = match(pattern, fact, bindings)

            if new_bindings is not None:
                self.extend_match(
                    rule,
                    i + 1,
                    new_bindings,
                    premises + (fact,),
                    results
                )

    def step(self):
        pending = []

        for rule in self.rules:
            matches = self.find_matches(rule)

            for bindings, premises in matches:
                fired_key = (rule.name, tuple(sorted(bindings.items())))

                if fired_key in self.fired:
                    continue

                self.fired.add(fired_key)

                for conclusion in rule.then:
                    new_fact = substitute(conclusion, bindings)

                    justification = Justification(
                        new_fact,
                        rule,
                        bindings,
                        premises,
                        len(self.rounds)
                    )

                    pending.append((new_fact, justification))

        new_facts = []

        for fact, justification in pending:
            if self.add_fact(fact, justification):
                new_facts.append(fact)
                self.firings.append(justification)

        if len(new_facts) > 0:
            self.rounds.append(new_facts)

        return new_facts

    def run(self):
        while self.step():
            pass

        return self

    def rules_fired(self):
        names = []

        for justification in self.firings:
            if justification.rule.name not in names:
                names.append(justification.rule.name)

        return names

    # Backward chaining

    def ask(self, goal):
        return self.prove(tuple(goal), [])

    def prove(self, goal, path):
        if goal in self.given:
            return ProofNode(goal, None, "given", [])

        if goal in path:
            return None

        if goal not in self.facts:
            return None

        for justification in self.facts[goal]:
            if justification.rule is None:
                continue

            children = []
            all_proved = True

            for premise in justification.premises:
                child = self.prove(premise, path + [goal])

                if child is None:
                    all_proved = False
                    break

                children.append(child)

            if all_proved:
                return ProofNode(
                    goal,
                    justification.rule.name,
                    justification.rule.description,
                    children
                )

        return None

    # Explanations

    def explain(self, fact, indent=0, seen=None):
        if seen is None:
            seen = set()

        spaces = "  " * indent

        if fact not in self.facts:
            return [spaces + fmt_fact(fact) + "  [not derived]"]

        justifications = self.facts[fact]
        first = justifications[0]

        if first.rule is None:
            return [spaces + fmt_fact(fact) + "  [given]"]

        if fact in seen:
            return [spaces + fmt_fact(fact) + "  [explained above]"]

        seen.add(fact)

        lines = [
            spaces + fmt_fact(fact) + "  <= " +
            first.rule.name + ": " + first.rule.description
        ]

        for premise in first.premises:
            lines = lines + self.explain(premise, indent + 1, seen)

        other_rules = []

        for justification in justifications[1:]:
            if justification.rule is not None:
                name = justification.rule.name

                if name not in other_rules:
                    other_rules.append(name)

        if len(other_rules) > 0:
            other_rules.sort()

            lines.append(
                spaces + "  (also supported by: " +
                ", ".join(other_rules) + ")"
            )

        return lines


def explain_proof(node, indent=0):
    spaces = "  " * indent

    if node.rule_name is None:
        return [spaces + fmt_fact(node.goal) + "  [given]"]

    lines = [
        spaces + fmt_fact(node.goal) + "  <= " +
        node.rule_name + ": " + node.description
    ]

    for child in node.children:
        lines = lines + explain_proof(child, indent + 1)

    return lines

