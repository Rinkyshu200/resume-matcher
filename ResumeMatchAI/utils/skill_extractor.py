import spacy
import re
from typing import List, Tuple, Set
import streamlit as st

class SkillExtractor:
    """
    Class for extracting and comparing skills from text documents.
    """
    
    def __init__(self):
        """Initialize the skill extractor."""
        self.nlp = None
        self._load_nlp_model()
        self._initialize_skill_patterns()
    
    @st.cache_resource
    def _load_nlp_model(_self):
        """Load spaCy model (cached)."""
        try:
            # Try to load the English model
            nlp = spacy.load("en_core_web_sm")
            return nlp
        except OSError:
            try:
                # Fallback: try to load without language model
                nlp = spacy.blank("en")
                return nlp
            except Exception as e:
                st.warning(f"Could not load spaCy model: {str(e)}. Using basic pattern matching.")
                return None
    
    def _initialize_skill_patterns(self):
        """Initialize predefined skill patterns and categories."""
        # Technical skills patterns
        self.technical_skills = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'r', 'scala', 'kotlin',
                'swift', 'go', 'rust', 'php', 'ruby', 'typescript', 'matlab', 'perl'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'bootstrap', 'jquery', 'sass', 'less'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
                'oracle', 'sqlite', 'dynamodb', 'elasticsearch'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
                'terraform', 'jenkins', 'gitlab', 'github actions'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'statistics',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras'
            ],
            'tools': [
                'git', 'linux', 'unix', 'bash', 'powershell', 'vim', 'vscode',
                'intellij', 'eclipse', 'jira', 'confluence', 'slack'
            ]
        }
        
        # Soft skills patterns
        self.soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'analytical thinking', 'creativity', 'adaptability', 'time management',
            'project management', 'critical thinking', 'collaboration'
        ]
        
        # Combine all skills for easier searching
        self.all_skills = []
        for category_skills in self.technical_skills.values():
            self.all_skills.extend(category_skills)
        self.all_skills.extend(self.soft_skills)
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using pattern matching and NLP.
        
        Args:
            text: Input text to extract skills from
            
        Returns:
            List of extracted skills
        """
        if not text:
            return []
        
        extracted_skills = set()
        
        # Load NLP model if not already loaded
        if not self.nlp:
            self.nlp = self._load_nlp_model()
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Extract skills using pattern matching
        pattern_skills = self._extract_skills_by_patterns(text_lower)
        extracted_skills.update(pattern_skills)
        
        # Extract skills using NLP if model is available
        if self.nlp:
            nlp_skills = self._extract_skills_by_nlp(text)
            extracted_skills.update(nlp_skills)
        
        # Extract additional skills using keyword context
        context_skills = self._extract_skills_by_context(text_lower)
        extracted_skills.update(context_skills)
        
        return list(extracted_skills)
    
    def _extract_skills_by_patterns(self, text: str) -> List[str]:
        """Extract skills using predefined patterns."""
        found_skills = []
        
        for skill in self.all_skills:
            # Create pattern for skill matching
            skill_pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            
            if re.search(skill_pattern, text):
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_skills_by_nlp(self, text: str) -> List[str]:
        """Extract skills using NLP techniques."""
        found_skills = []
        
        try:
            doc = self.nlp(text)
            
            # Extract entities that might be skills
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                    skill_candidate = ent.text.lower().strip()
                    if self._is_likely_skill(skill_candidate):
                        found_skills.append(skill_candidate)
            
            # Extract noun phrases that might be skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower().strip()
                if self._is_likely_skill(chunk_text):
                    found_skills.append(chunk_text)
        
        except Exception as e:
            # If NLP processing fails, continue with other methods
            pass
        
        return found_skills
    
    def _extract_skills_by_context(self, text: str) -> List[str]:
        """Extract skills by looking for contextual patterns."""
        found_skills = []
        
        # Patterns that often precede or follow skills
        skill_contexts = [
            r'experience\s+(?:with|in)\s+([^,.;]+)',
            r'proficient\s+(?:with|in)\s+([^,.;]+)',
            r'skilled\s+(?:with|in)\s+([^,.;]+)',
            r'knowledge\s+(?:of|in)\s+([^,.;]+)',
            r'familiar\s+(?:with|in)\s+([^,.;]+)',
            r'expertise\s+(?:with|in)\s+([^,.;]+)',
            r'technologies:\s*([^.;]+)',
            r'skills:\s*([^.;]+)',
            r'tools:\s*([^.;]+)'
        ]
        
        for pattern in skill_contexts:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                skill_text = match.group(1).strip()
                # Split by common separators
                potential_skills = re.split(r'[,;|&\n]+', skill_text)
                
                for potential_skill in potential_skills:
                    clean_skill = potential_skill.strip().lower()
                    if self._is_likely_skill(clean_skill):
                        found_skills.append(clean_skill)
        
        return found_skills
    
    def _is_likely_skill(self, text: str) -> bool:
        """
        Determine if a text snippet is likely to be a skill.
        
        Args:
            text: Text to evaluate
            
        Returns:
            True if likely a skill, False otherwise
        """
        if not text or len(text) < 2:
            return False
        
        # Remove extra whitespace
        text = text.strip()
        
        # Skip if too long (likely not a skill)
        if len(text.split()) > 4:
            return False
        
        # Skip common words that are not skills
        common_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
        }
        
        if text.lower() in common_words:
            return False
        
        # Check if it's in our predefined skills list
        if text.lower() in self.all_skills:
            return True
        
        # Additional heuristics for technical terms
        technical_indicators = [
            r'\b\w+\.(js|py|java|cpp|cs|rb|php)\b',  # File extensions
            r'\b\w+\.js\b',  # JavaScript libraries
            r'\b\w+SQL\b',  # Database variants
            r'\b\w+DB\b',   # Database variants
        ]
        
        for indicator in technical_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                return True
        
        return False
    
    def compare_skills(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[List[str], List[str]]:
        """
        Compare skills from resume and job description.
        
        Args:
            resume_skills: Skills extracted from resume
            job_skills: Skills extracted from job description
            
        Returns:
            Tuple of (matched_skills, missing_skills)
        """
        # Convert to lowercase sets for comparison
        resume_skills_lower = {skill.lower() for skill in resume_skills}
        job_skills_lower = {skill.lower() for skill in job_skills}
        
        # Find exact matches
        exact_matches = resume_skills_lower.intersection(job_skills_lower)
        
        # Find fuzzy matches (partial matches)
        fuzzy_matches = set()
        for job_skill in job_skills_lower:
            for resume_skill in resume_skills_lower:
                if self._are_skills_similar(job_skill, resume_skill):
                    fuzzy_matches.add(job_skill)
                    break
        
        # Combine exact and fuzzy matches
        all_matches = exact_matches.union(fuzzy_matches)
        
        # Find missing skills
        missing_skills = job_skills_lower - all_matches
        
        # Convert back to original case (use job description case as reference)
        matched_skills = []
        for skill in job_skills:
            if skill.lower() in all_matches:
                matched_skills.append(skill)
        
        missing_skills_list = []
        for skill in job_skills:
            if skill.lower() in missing_skills:
                missing_skills_list.append(skill)
        
        return matched_skills, missing_skills_list
    
    def _are_skills_similar(self, skill1: str, skill2: str) -> bool:
        """
        Check if two skills are similar (fuzzy matching).
        
        Args:
            skill1: First skill
            skill2: Second skill
            
        Returns:
            True if skills are similar, False otherwise
        """
        # Check if one skill contains the other
        if skill1 in skill2 or skill2 in skill1:
            return True
        
        # Check for common abbreviations and variations
        skill_variations = {
            'javascript': ['js', 'ecmascript'],
            'python': ['py'],
            'machine learning': ['ml'],
            'artificial intelligence': ['ai'],
            'database': ['db'],
            'sql server': ['mssql', 'microsoft sql'],
            'postgresql': ['postgres'],
            'amazon web services': ['aws'],
            'google cloud platform': ['gcp'],
            'microsoft azure': ['azure'],
        }
        
        for base_skill, variations in skill_variations.items():
            if (skill1 == base_skill and skill2 in variations) or \
               (skill2 == base_skill and skill1 in variations) or \
               (skill1 in variations and skill2 in variations):
                return True
        
        return False
    
    def categorize_skills(self, skills: List[str]) -> dict:
        """
        Categorize skills into different groups.
        
        Args:
            skills: List of skills to categorize
            
        Returns:
            Dictionary with categorized skills
        """
        categorized = {
            'programming_languages': [],
            'web_technologies': [],
            'databases': [],
            'cloud_platforms': [],
            'data_science': [],
            'tools': [],
            'soft_skills': [],
            'other': []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            categorized_skill = False
            
            # Check technical skills categories
            for category, category_skills in self.technical_skills.items():
                if skill_lower in category_skills:
                    categorized[category].append(skill)
                    categorized_skill = True
                    break
            
            # Check soft skills
            if not categorized_skill and skill_lower in self.soft_skills:
                categorized['soft_skills'].append(skill)
                categorized_skill = True
            
            # If not categorized, put in 'other'
            if not categorized_skill:
                categorized['other'].append(skill)
        
        return categorized
    
    def get_skill_recommendations(self, missing_skills: List[str], category: str = None) -> List[str]:
        """
        Get skill recommendations based on missing skills and category.
        
        Args:
            missing_skills: List of missing skills
            category: Optional category to focus recommendations
            
        Returns:
            List of recommended skills to learn
        """
        recommendations = []
        
        # If specific category skills are missing, recommend related skills
        categorized_missing = self.categorize_skills(missing_skills)
        
        for category, skills in categorized_missing.items():
            if skills and category in self.technical_skills:
                # Get all skills from the same category
                category_skills = self.technical_skills[category]
                
                # Recommend foundational skills from the same category
                for skill in category_skills:
                    if skill not in [s.lower() for s in missing_skills]:
                        recommendations.append(f"Consider learning {skill} (related to {category.replace('_', ' ')})")
        
        return recommendations[:5]  # Limit to top 5 recommendations
