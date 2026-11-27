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