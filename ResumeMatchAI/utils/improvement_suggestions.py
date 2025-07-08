import re
from typing import List, Dict, Tuple
import random

def generate_improvement_suggestions(resume_text: str, job_description: str, 
                                   missing_skills: List[str]) -> Dict[str, List[str]]:
    """
    Generate comprehensive improvement suggestions for the resume.
    
    Args:
        resume_text: The resume text
        job_description: The job description text
        missing_skills: List of skills missing from the resume
        
    Returns:
        Dictionary categorizing different types of suggestions
    """
    suggestions = {
        "Missing Skills": [],
        "Content Enhancement": [],
        "Keyword Optimization": [],
        "Structure Improvements": [],
        "Action Items": []
    }
    
    # Generate missing skills suggestions
    suggestions["Missing Skills"] = generate_missing_skills_suggestions(missing_skills)
    
    # Generate content enhancement suggestions
    suggestions["Content Enhancement"] = generate_content_suggestions(resume_text, job_description)
    
    # Generate keyword optimization suggestions
    suggestions["Keyword Optimization"] = generate_keyword_suggestions(resume_text, job_description)
    
    # Generate structure improvement suggestions
    suggestions["Structure Improvements"] = generate_structure_suggestions(resume_text)
    
    # Generate actionable items
    suggestions["Action Items"] = generate_action_items(missing_skills, resume_text)
    
    return suggestions

def generate_missing_skills_suggestions(missing_skills: List[str]) -> List[str]:
    """Generate suggestions for missing skills."""
    suggestions = []
    
    if not missing_skills:
        suggestions.append("Great! All required skills are present in your resume.")
        return suggestions
    
    # Categorize missing skills
    technical_skills = []
    soft_skills = []
    tools_platforms = []
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        if any(tech in skill_lower for tech in ['python', 'java', 'sql', 'javascript', 'programming']):
            technical_skills.append(skill)
        elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'aws', 'azure']):
            tools_platforms.append(skill)
        elif any(soft in skill_lower for soft in ['communication', 'leadership', 'teamwork', 'management']):
            soft_skills.append(skill)
        else:
            technical_skills.append(skill)  # Default to technical
    
    # Generate specific suggestions for each category
    if technical_skills:
        suggestions.append(f"Consider adding these technical skills to your resume: {', '.join(technical_skills[:5])}")
        suggestions.append("Highlight any projects or experience where you've used similar technologies")
        
    if tools_platforms:
        suggestions.append(f"Include experience with these tools/platforms: {', '.join(tools_platforms[:3])}")
        suggestions.append("Mention any certifications or training in these technologies")
        
    if soft_skills:
        suggestions.append(f"Emphasize these soft skills with specific examples: {', '.join(soft_skills[:3])}")
        suggestions.append("Use quantifiable achievements to demonstrate these capabilities")
    
    # Priority recommendations
    high_priority = ['python', 'sql', 'machine learning', 'aws', 'react', 'java']
    priority_missing = [skill for skill in missing_skills if any(hp in skill.lower() for hp in high_priority)]
    
    if priority_missing:
        suggestions.append(f"High priority skills to develop: {', '.join(priority_missing[:3])}")
    
    return suggestions

def generate_content_suggestions(resume_text: str, job_description: str) -> List[str]:
    """Generate content enhancement suggestions."""
    suggestions = []
    
    # Analyze resume length
    word_count = len(resume_text.split())
    if word_count < 200:
        suggestions.append("Your resume appears brief. Consider adding more details about your experience and achievements.")
    elif word_count > 800:
        suggestions.append("Your resume is quite lengthy. Consider condensing to focus on most relevant experience.")
    
    # Check for quantifiable achievements
    numbers_pattern = r'\d+\.?\d*%?|\b\d+\b'
    numbers_found = len(re.findall(numbers_pattern, resume_text))
    
    if numbers_found < 3:
        suggestions.append("Add quantifiable achievements (e.g., 'Increased efficiency by 25%', 'Managed team of 5')")
    
    # Check for action verbs
    action_verbs = ['developed', 'implemented', 'managed', 'led', 'created', 'designed', 
                   'optimized', 'achieved', 'delivered', 'improved', 'built', 'analyzed']
    
    action_verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    
    if action_verb_count < 5:
        suggestions.append("Use more strong action verbs to describe your accomplishments")
        suggestions.append("Start bullet points with impactful verbs like 'Developed', 'Implemented', 'Led'")
    
    # Analyze job description for key requirements
    job_keywords = extract_key_requirements(job_description)
    resume_lower = resume_text.lower()
    
    missing_context = []
    for keyword in job_keywords[:5]:  # Check top 5 keywords
        if keyword.lower() not in resume_lower:
            missing_context.append(keyword)
    
    if missing_context:
        suggestions.append(f"Consider mentioning experience related to: {', '.join(missing_context)}")
    
    # Check for industry-specific terms
    industry_terms = extract_industry_terms(job_description)
    resume_industry_score = sum(1 for term in industry_terms if term.lower() in resume_lower)
    
    if resume_industry_score < len(industry_terms) * 0.3:
        suggestions.append("Include more industry-specific terminology to show domain knowledge")
    
    return suggestions

def generate_keyword_suggestions(resume_text: str, job_description: str) -> List[str]:
    """Generate keyword optimization suggestions."""
    suggestions = []
    
    # Extract important keywords from job description
    job_keywords = extract_keywords_from_job(job_description)
    resume_lower = resume_text.lower()
    
    # Find missing important keywords
    missing_keywords = [kw for kw in job_keywords if kw.lower() not in resume_lower]
    
    if missing_keywords:
        suggestions.append(f"Consider incorporating these keywords: {', '.join(missing_keywords[:8])}")
        suggestions.append("Naturally integrate keywords into your experience descriptions")
    
    # Check keyword density
    total_words = len(resume_text.split())
    keyword_density = len([kw for kw in job_keywords if kw.lower() in resume_lower]) / total_words * 100
    
    if keyword_density < 2:
        suggestions.append("Increase relevant keyword density while maintaining natural flow")
    elif keyword_density > 10:
        suggestions.append("Reduce keyword stuffing - focus on natural integration")
    
    # Synonym suggestions
    synonym_suggestions = generate_synonym_suggestions(resume_text, job_description)
    if synonym_suggestions:
        suggestions.extend(synonym_suggestions)
    
    return suggestions

def generate_structure_suggestions(resume_text: str) -> List[str]:
    """Generate resume structure improvement suggestions."""
    suggestions = []
    
    # Check for common sections
    sections = {
        'summary': ['summary', 'objective', 'profile'],
        'experience': ['experience', 'work', 'employment'],
        'skills': ['skills', 'technical', 'competencies'],
        'education': ['education', 'degree', 'university']
    }
    
    missing_sections = []
    text_lower = resume_text.lower()
    
    for section, keywords in sections.items():
        if not any(keyword in text_lower for keyword in keywords):
            missing_sections.append(section)
    
    if 'summary' in missing_sections:
        suggestions.append("Add a professional summary at the top highlighting your key qualifications")
    
    if 'skills' in missing_sections:
        suggestions.append("Include a dedicated skills section to showcase your technical abilities")
    
    # Check for bullet points
    bullet_indicators = ['•', '*', '-', '▪']
    has_bullets = any(indicator in resume_text for indicator in bullet_indicators)
    
    if not has_bullets:
        suggestions.append("Use bullet points to improve readability and highlight achievements")
    
    # Check for consistent formatting
    if len(set(re.findall(r'^[\s\t]*[-*•]', resume_text, re.MULTILINE))) > 1:
        suggestions.append("Maintain consistent bullet point formatting throughout")
    
    # Length recommendations
    lines = resume_text.split('\n')
    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
    
    if avg_line_length > 100:
        suggestions.append("Consider breaking long paragraphs into shorter, more digestible points")
    
    return suggestions

def generate_action_items(missing_skills: List[str], resume_text: str) -> List[str]:
    """Generate specific actionable items."""
    action_items = []
    
    # Skill development actions
    if missing_skills:
        priority_skills = missing_skills[:3]  # Top 3 missing skills
        action_items.append(f"Priority: Start learning {priority_skills[0]} through online courses or projects")
        
        if len(priority_skills) > 1:
            action_items.append(f"Consider obtaining certification in {priority_skills[1]}")
        
        if len(priority_skills) > 2:
            action_items.append(f"Look for volunteer or side projects to gain experience in {priority_skills[2]}")
    
    # Content improvement actions
    if 'experience' not in resume_text.lower():
        action_items.append("Add a detailed work experience section with specific achievements")
    
    if not re.search(r'\d+', resume_text):
        action_items.append("Quantify your achievements with specific numbers and percentages")
    
    # Networking and research actions
    action_items.append("Research the company's tech stack and highlight relevant experience")
    action_items.append("Connect with current employees to understand role requirements better")
    
    # Portfolio and demonstration actions
    if any(skill in ' '.join(missing_skills).lower() for skill in ['programming', 'development', 'coding']):
        action_items.append("Create GitHub portfolio showcasing projects with the required technologies")
    
    action_items.append("Prepare specific examples demonstrating your problem-solving abilities")
    
    return action_items

def extract_key_requirements(job_description: str) -> List[str]:
    """Extract key requirements from job description."""
    # Common requirement indicators
    requirement_patterns = [
        r'required?\s*:?\s*([^.;]+)',
        r'must\s+have\s*:?\s*([^.;]+)',
        r'essential\s*:?\s*([^.;]+)',
        r'qualifications?\s*:?\s*([^.;]+)',
        r'responsibilities?\s*:?\s*([^.;]+)'
    ]
    
    requirements = []
    text_lower = job_description.lower()
    
    for pattern in requirement_patterns:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            req_text = match.group(1).strip()
            # Split by common separators and clean
            req_items = re.split(r'[,;|&\n]+', req_text)
            for item in req_items:
                clean_item = item.strip()
                if len(clean_item) > 3 and len(clean_item.split()) <= 4:
                    requirements.append(clean_item)
    
    return requirements[:10]  # Return top 10

def extract_keywords_from_job(job_description: str) -> List[str]:
    """Extract important keywords from job description."""
    # Technical terms and skills
    tech_patterns = [
        r'\b[A-Z]{2,}\b',  # Acronyms
        r'\b\w+\.js\b',    # JavaScript frameworks
        r'\b\w+SQL\b',     # Database variants
        r'\b\w+-\w+\b'     # Hyphenated terms
    ]
    
    keywords = []
    
    # Extract using patterns
    for pattern in tech_patterns:
        matches = re.findall(pattern, job_description)
        keywords.extend(matches)
    
    # Extract common technical terms
    common_tech_terms = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes',
        'git', 'linux', 'agile', 'scrum', 'ci/cd'
    ]
    
    job_lower = job_description.lower()
    for term in common_tech_terms:
        if term in job_lower:
            keywords.append(term)
    
    # Remove duplicates and return
    return list(set(keywords))

def extract_industry_terms(job_description: str) -> List[str]:
    """Extract industry-specific terms."""
    industry_indicators = {
        'finance': ['financial', 'banking', 'trading', 'investment', 'fintech'],
        'healthcare': ['healthcare', 'medical', 'patient', 'clinical', 'pharma'],
        'ecommerce': ['ecommerce', 'retail', 'marketplace', 'customer', 'sales'],
        'saas': ['saas', 'subscription', 'platform', 'cloud', 'enterprise'],
        'gaming': ['gaming', 'game', 'unity', 'unreal', 'mobile games'],
        'ai_ml': ['ai', 'machine learning', 'deep learning', 'neural', 'nlp']
    }
    
    job_lower = job_description.lower()
    industry_terms = []
    
    for industry, terms in industry_indicators.items():
        for term in terms:
            if term in job_lower:
                industry_terms.append(term)
    
    return list(set(industry_terms))

def generate_synonym_suggestions(resume_text: str, job_description: str) -> List[str]:
    """Generate suggestions for using synonyms to match job description language."""
    suggestions = []
    
    synonym_map = {
        'developed': ['built', 'created', 'designed', 'implemented'],
        'managed': ['led', 'supervised', 'oversaw', 'directed'],
        'improved': ['enhanced', 'optimized', 'upgraded', 'refined'],
        'worked': ['collaborated', 'partnered', 'contributed', 'participated'],
        'used': ['utilized', 'employed', 'leveraged', 'applied']
    }
    
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    for base_word, synonyms in synonym_map.items():
        if base_word in resume_lower:
            # Check if job description uses any synonyms
            job_synonyms = [syn for syn in synonyms if syn in job_lower]
            if job_synonyms:
                suggestions.append(f"Consider using '{job_synonyms[0]}' instead of '{base_word}' to match job language")
    
    return suggestions
