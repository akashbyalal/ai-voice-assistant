import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import OFFLINE_KB_PATH


class OfflineEngine:
    def __init__(self):
        with open(OFFLINE_KB_PATH, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

        # ✅ Use BOTH keys + values for stronger matching
        self.keys = [k.lower() for k in self.kb.keys()]
        self.docs = [v.lower() for v in self.kb.values()]

        # ✅ Merge key + value so the model understands meaning + name
        self.combined_docs = [
            self.keys[i] + " " + self.docs[i]
            for i in range(len(self.keys))
        ]

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vecs = self.vectorizer.fit_transform(self.combined_docs)

    def query(self, text):
        text = text.lower().strip()

        # ✅ First: Direct keyword hit (fast + accurate)
        for i, key in enumerate(self.keys):
            if key in text:
                return self.kb[self.keys[i]]

        # ✅ Second: Semantic similarity (TF-IDF)
        q_vec = self.vectorizer.transform([text])
        sims = cosine_similarity(q_vec, self.doc_vecs)[0]
        idx = sims.argmax()

        # ✅ Increased threshold for fewer false positives
        if sims[idx] < 0.18:
            return "Sorry, I don't have this ECE concept in my knowledge base yet."

        return self.kb[self.keys[idx]]
