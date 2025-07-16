"""
Query Processor for Module 3: Question-Answering Engine

This module handles the preprocessing and understanding of user queries.
It normalizes questions, extracts key terms, and prepares them for retrieval.
"""

import re
import string
from typing import Dict, List, Tuple
from collections import Counter

# --- Static English stopwords set ---
ENGLISH_STOPWORDS = set('''
a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
'''.split())

# --- Simple regex-based tokenizer ---
def simple_tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())

class QueryProcessor:
    """
    Processes and understands user queries for the QA system.
    Features:
    - Query normalization and cleaning
    - Keyword extraction
    - Intent recognition
    - Query expansion
    """
    def __init__(self):
        self.stop_words = ENGLISH_STOPWORDS
        self.question_words = {
            'what', 'when', 'where', 'who', 'why', 'how', 'which', 'whose'
        }
        self.question_patterns = {
            'definition': r'\b(what is|what are|define|definition of)\b',
            'comparison': r'\b(compare|difference between|similarities|versus|vs)\b',
            'process': r'\b(how to|how does|steps to|process of)\b',
            'cause_effect': r'\b(why|because|reason|cause|effect)\b',
            'example': r'\b(example|instance|case|illustration)\b'
        }

    def normalize_query(self, query: str) -> str:
        query = query.lower().strip()
        query = re.sub(r'\s+', ' ', query)
        query = re.sub(r'[^\w\s\?]', '', query)
        return query

    def extract_keywords(self, query: str) -> List[str]:
        tokens = simple_tokenize(query)
        keywords = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        return keywords

    def recognize_intent(self, query: str) -> Dict[str, any]:
        intent_info = {
            'question_type': 'general',
            'question_word': None,
            'intent_category': 'information',
            'confidence': 0.5
        }
        words = query.lower().split()
        for word in words:
            if word in self.question_words:
                intent_info['question_word'] = word
                break
        for pattern_name, pattern in self.question_patterns.items():
            if re.search(pattern, query.lower()):
                intent_info['intent_category'] = pattern_name
                intent_info['confidence'] = 0.8
                break
        if intent_info['question_word']:
            if intent_info['question_word'] in ['what', 'which']:
                intent_info['question_type'] = 'definition'
            elif intent_info['question_word'] in ['how']:
                intent_info['question_type'] = 'process'
            elif intent_info['question_word'] in ['why']:
                intent_info['question_type'] = 'cause_effect'
            elif intent_info['question_word'] in ['when', 'where']:
                intent_info['question_type'] = 'factual'
            elif intent_info['question_word'] in ['who']:
                intent_info['question_type'] = 'person'
        return intent_info

    def expand_query(self, query: str, keywords: List[str]) -> List[str]:
        variations = [query]
        if keywords:
            keyword_query = ' '.join(keywords[:3])
            if keyword_query != query:
                variations.append(keyword_query)
        synonym_map = {
            'ai': ['artificial intelligence', 'machine learning'],
            'ml': ['machine learning', 'artificial intelligence'],
            'nlp': ['natural language processing', 'text processing'],
            'deep learning': ['neural networks', 'ai'],
            'algorithm': ['method', 'technique', 'approach'],
            'research centres': ['research organizations', 'AI labs', 'institutes', 'research labs'],
            'research centers': ['research organizations', 'AI labs', 'institutes', 'research labs'],
            'research organizations': ['research centres', 'AI labs', 'institutes', 'research labs'],
            'labs': ['research centres', 'research organizations', 'institutes', 'AI labs']
        }
        for keyword in keywords:
            if keyword in synonym_map:
                for synonym in synonym_map[keyword]:
                    variation = query.replace(keyword, synonym)
                    if variation not in variations:
                        variations.append(variation)
        return variations

    def process_query(self, query: str) -> Dict[str, any]:
        normalized_query = self.normalize_query(query)
        keywords = self.extract_keywords(normalized_query)
        intent_info = self.recognize_intent(normalized_query)
        query_variations = self.expand_query(normalized_query, keywords)
        return {
            'original_query': query,
            'normalized_query': normalized_query,
            'keywords': keywords,
            'intent': intent_info,
            'query_variations': query_variations,
            'processed_at': '2024-01-01T00:00:00Z'
        }

    def get_query_statistics(self, query: str) -> Dict[str, any]:
        processed = self.process_query(query)
        return {
            'query_length': len(query),
            'word_count': len(query.split()),
            'keyword_count': len(processed['keywords']),
            'intent_confidence': processed['intent']['confidence'],
            'variations_count': len(processed['query_variations'])
        }


# Example usage and testing
if __name__ == "__main__":
    processor = QueryProcessor()
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Compare AI and ML.",
        "Why is deep learning important?",
        "Give an example of NLP."
    ]
    
    for q in test_queries:
        print(f"Query: {q}")
        print(processor.process_query(q))
        print() 