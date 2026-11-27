from src.inference_engine import is_var

class KnowledgeGraph:
    def __init__(self, triples=None):
        # Relationships stored as subject, predicate and object
        self.triples = set()

        if triples is not None:
            for subject, predicate, obj in triples:
                self.add(subject, predicate, obj)

    def copy(self):
        return KnowledgeGraph(self.triples)

    def add(self, s, p, o):
        self.triples.add((s, p, o))
        
    def match(self, s=None, p=None, o=None):
        # None allows any value to match
        found = []

        for triple in self.triples:
            if s is not None and triple[0] != s:
                continue

            if p is not None and triple[1] != p:
                continue

            if o is not None and triple[2] != o:
                continue

            found.append(triple)

        found.sort()
        return found

    def objects(self, s, p):
        return [triple[2] for triple in self.match(s, p)]
    
        # Graph queries

    def select(self, patterns):
        results = [{}]

        for pattern in patterns:
            new_results = []

            for bindings in results:
                query = []

                for term in pattern:
                    if is_var(term) and term in bindings:
                        query.append(bindings[term])
                    else:
                        query.append(term)

                wanted = []

                for term in query:
                    if is_var(term):
                        wanted.append(None)
                    else:
                        wanted.append(term)

                for triple in self.match(wanted[0], wanted[1], wanted[2]):
                    new_bindings = dict(bindings)
                    valid = True

                    for term, value in zip(pattern, triple):
                        if is_var(term):
                            if term in new_bindings and new_bindings[term] != value:
                                valid = False
                                break

                            new_bindings[term] = value

                    if valid:
                        new_results.append(new_bindings)

            results = new_results
    # Graph traversal

    def bfs_path(self, start, goal, predicates=None):
        if start == goal:
            return []

        parent = {}
        queue = [start]
        visited = {start}

        while queue:
            node = queue.pop(0)

            for triple in self.match(s=node):
                predicate = triple[1]
                next_node = triple[2]

                if predicates is not None and predicate not in predicates:
                    continue

                if next_node in visited:
                    continue

                visited.add(next_node)
                parent[next_node] = (node, triple)

                if next_node == goal:
                    path = []
                    current = next_node

                    while current != start:
                        previous, edge = parent[current]
                        path.append(edge)
                        current = previous

                    path.reverse()
                    return path

                queue.append(next_node)

        return None
    
        return results