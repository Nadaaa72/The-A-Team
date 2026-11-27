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