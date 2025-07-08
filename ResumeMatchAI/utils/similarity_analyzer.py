import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from typing import List, Tuple
import re

class SimilarityAnalyzer:
    """
    Class for computing semantic similarity between text documents using TF-IDF vectorization.
    """
    
    def __init__(self, model_name: str = 'tfidf'):
        """
        Initialize the similarity analyzer.
        
        Args:
            model_name: Name of the vectorization method to use ('tfidf' for TF-IDF)
        """
        self.model_name = model_name
        self.vectorizer = None
        self._load_model()
    
    @st.cache_resource
    def _load_model(_self):
        """Load the TF-IDF vectorizer (cached)."""
        try:
            # Create TF-IDF vectorizer with optimized parameters
            vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True,
                min_df=1,
                max_df=0.95
            )
            return vectorizer
        except Exception as e:
            st.error(f"Error loading TF-IDF vectorizer: {str(e)}")
            return None
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better similarity computation.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?]', ' ', text)
        
        # Remove extra spaces
        text = text.strip()
        
        return text
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts using TF-IDF.
        
        Args:
            text1: First text (e.g., resume)
            text2: Second text (e.g., job description)
            
        Returns:
            Similarity score as percentage (0-100)
        """
        if not self.vectorizer:
            self.vectorizer = self._load_model()
            
        if not self.vectorizer:
            st.error("Could not load TF-IDF vectorizer")
            return 0.0
        
        try:
            # Preprocess texts
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            if not processed_text1 or not processed_text2:
                return 0.0
            
            # Create corpus with both texts
            corpus = [processed_text1, processed_text2]
            
            # Generate TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Compute cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity = similarity_matrix[0][0]
            
            # Convert to percentage and ensure it's between 0 and 100
            similarity_percentage = max(0, min(100, similarity * 100))
            
            return similarity_percentage
            
        except Exception as e:
            st.error(f"Error computing similarity: {str(e)}")
            return 0.0
    
    def compute_section_similarities(self, resume_text: str, job_description: str) -> dict:
        """
        Compute similarities between different sections of resume and job description.
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            
        Returns:
            Dictionary with section-wise similarities
        """
        if not self.vectorizer:
            self.vectorizer = self._load_model()
            
        if not self.vectorizer:
            return {}
        
        try:
            # Extract sections from resume
            resume_sections = self._extract_sections(resume_text)
            
            # Extract sections from job description
            job_sections = self._extract_sections(job_description)
            
            similarities = {}
            
            for resume_section, resume_content in resume_sections.items():
                for job_section, job_content in job_sections.items():
                    if resume_content and job_content:
                        similarity = self.compute_similarity(resume_content, job_content)
                        similarities[f"{resume_section}_vs_{job_section}"] = similarity
            
            return similarities
            
        except Exception as e:
            st.error(f"Error computing section similarities: {str(e)}")
            return {}
    
    def _extract_sections(self, text: str) -> dict:
        """
        Extract different sections from text based on common patterns.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with section names and content
        """
        sections = {
            'experience': '',
            'skills': '',
            'education': '',
            'summary': ''
        }
        
        # Convert to lowercase for pattern matching
        text_lower = text.lower()
        
        # Define section patterns
        patterns = {
            'experience': [
                r'work\s+experience.*?(?=education|skills|summary|$)',
                r'experience.*?(?=education|skills|summary|$)',
                r'employment.*?(?=education|skills|summary|$)',
                r'professional\s+experience.*?(?=education|skills|summary|$)'
            ],
            'skills': [
                r'skills.*?(?=experience|education|summary|$)',
                r'technical\s+skills.*?(?=experience|education|summary|$)',
                r'competencies.*?(?=experience|education|summary|$)'
            ],
            'education': [
                r'education.*?(?=experience|skills|summary|$)',
                r'academic.*?(?=experience|skills|summary|$)',
                r'qualifications.*?(?=experience|skills|summary|$)'
            ],
            'summary': [
                r'summary.*?(?=experience|skills|education|$)',
                r'objective.*?(?=experience|skills|education|$)',
                r'profile.*?(?=experience|skills|education|$)'
            ]
        }
        
        for section, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section] = match.group(0)
                    break
        
        return sections
    
    def batch_similarity(self, texts1: List[str], text2: str) -> List[float]:
        """
        Compute similarity between multiple texts and a single reference text.
        
        Args:
            texts1: List of texts to compare
            text2: Reference text
            
        Returns:
            List of similarity scores
        """
        if not self.vectorizer:
            self.vectorizer = self._load_model()
            
        if not self.vectorizer:
            return [0.0] * len(texts1)
        
        try:
            similarities = []
            
            for text1 in texts1:
                similarity = self.compute_similarity(text1, text2)
                similarities.append(similarity)
            
            return similarities
            
        except Exception as e:
            st.error(f"Error computing batch similarities: {str(e)}")
            return [0.0] * len(texts1)
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded vectorizer.
        
        Returns:
            Dictionary with vectorizer information
        """
        if not self.vectorizer:
            return {'status': 'not_loaded'}
        
        return {
            'status': 'loaded',
            'model_name': self.model_name,
            'vectorizer_type': 'TF-IDF',
            'max_features': getattr(self.vectorizer, 'max_features', 'unknown'),
            'ngram_range': getattr(self.vectorizer, 'ngram_range', 'unknown')
        }
