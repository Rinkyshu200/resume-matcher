import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import time
from typing import List, Dict, Tuple, Optional

# Import utility modules
from utils.text_extractor import extract_text_from_file
from utils.similarity_analyzer import SimilarityAnalyzer
from utils.skill_extractor import SkillExtractor
from utils.visualizations import create_match_chart, create_skills_radar_chart, create_comparison_chart
from utils.improvement_suggestions import generate_improvement_suggestions

# Page configuration
st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SimilarityAnalyzer()
    
if 'skill_extractor' not in st.session_state:
    st.session_state.skill_extractor = SkillExtractor()

if 'uploaded_resumes' not in st.session_state:
    st.session_state.uploaded_resumes = []

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

def main():
    st.title("🎯 Resume Matcher")
    st.markdown("**Analyze semantic similarity between resumes and job descriptions using advanced NLP**")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio(
        "Select Mode:",
        ["Single Resume Analysis", "Multi-Resume Comparison", "About"]
    )
    
    if mode == "Single Resume Analysis":
        single_resume_analysis()
    elif mode == "Multi-Resume Comparison":
        multi_resume_comparison()
    else:
        show_about()

def single_resume_analysis():
    """Handle single resume analysis workflow"""
    st.header("📋 Single Resume Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=['pdf', 'txt'],
            help="Upload a PDF or text file containing the resume"
        )
        
        resume_text = ""
        if uploaded_file is not None:
            with st.spinner("Extracting text from resume..."):
                try:
                    resume_text = extract_text_from_file(uploaded_file)
                    if resume_text:
                        st.success("✅ Resume text extracted successfully!")
                        with st.expander("Preview Resume Text"):
                            st.text_area("Extracted Text:", resume_text[:500] + "...", height=150, disabled=True)
                    else:
                        st.error("❌ Failed to extract text from the file. Please check the file format.")
                        return
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    return
    
    with col2:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=200,
            placeholder="Paste the job description here..."
        )
    
    # Analysis button
    if st.button("🔍 Analyze Match", type="primary", use_container_width=True):
        if not resume_text or not job_description:
            st.warning("⚠️ Please provide both a resume and job description.")
            return
        
        analyze_single_resume(resume_text, job_description, uploaded_file.name if uploaded_file else "Resume")

def analyze_single_resume(resume_text: str, job_description: str, filename: str):
    """Analyze a single resume against a job description"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Compute similarity
        status_text.text("Computing semantic similarity...")
        progress_bar.progress(25)
        
        similarity_score = st.session_state.analyzer.compute_similarity(resume_text, job_description)
        
        # Step 2: Extract skills
        status_text.text("Extracting and matching skills...")
        progress_bar.progress(50)
        
        resume_skills = st.session_state.skill_extractor.extract_skills(resume_text)
        job_skills = st.session_state.skill_extractor.extract_skills(job_description)
        matched_skills, missing_skills = st.session_state.skill_extractor.compare_skills(resume_skills, job_skills)
        
        # Step 3: Generate suggestions
        status_text.text("Generating improvement suggestions...")
        progress_bar.progress(75)
        
        suggestions = generate_improvement_suggestions(resume_text, job_description, missing_skills)
        
        # Step 4: Complete
        status_text.text("Analysis complete!")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        display_analysis_results(
            filename, similarity_score, matched_skills, missing_skills, 
            resume_skills, job_skills, suggestions
        )
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def display_analysis_results(filename: str, similarity_score: float, matched_skills: List[str], 
                           missing_skills: List[str], resume_skills: List[str], 
                           job_skills: List[str], suggestions: Dict[str, List[str]]):
    """Display comprehensive analysis results"""
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Overall match score
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.metric("Overall Match Score", f"{similarity_score:.1f}%")
        st.plotly_chart(create_match_chart(similarity_score), use_container_width=True)
    
    with col2:
        st.metric("Matched Skills", len(matched_skills))
        st.metric("Missing Skills", len(missing_skills))
    
    with col3:
        st.metric("Resume Skills", len(resume_skills))
        st.metric("Required Skills", len(job_skills))
    
    # Skills analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.success(f"• {skill}")
        else:
            st.info("No directly matched skills found.")
    
    with col2:
        st.subheader("❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.error(f"• {skill}")
        else:
            st.success("All required skills are present!")
    
    # Skills radar chart
    if resume_skills and job_skills:
        st.subheader("📈 Skills Coverage Analysis")
        skills_chart = create_skills_radar_chart(resume_skills, job_skills, matched_skills)
        st.plotly_chart(skills_chart, use_container_width=True)
    
    # Improvement suggestions
    if suggestions:
        st.subheader("💡 Improvement Suggestions")
        
        for category, items in suggestions.items():
            with st.expander(f"{category} ({len(items)} suggestions)"):
                for item in items:
                    st.write(f"• {item}")

def multi_resume_comparison():
    """Handle multiple resume comparison workflow"""
    st.header("👥 Multi-Resume Comparison")
    
    # Job description input
    st.subheader("Job Description")
    job_description = st.text_area(
        "Enter the job description for comparison:",
        height=150,
        placeholder="Paste the job description here..."
    )
    
    # Resume upload section
    st.subheader("Upload Multiple Resumes")
    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        help="Upload multiple PDF or text files containing resumes"
    )
    
    if uploaded_files and job_description:
        if st.button("🔍 Compare All Resumes", type="primary"):
            compare_multiple_resumes(uploaded_files, job_description)
    
    # Display previous results if available
    if st.session_state.analysis_results:
        display_comparison_results()

def compare_multiple_resumes(uploaded_files, job_description: str):
    """Compare multiple resumes against a job description"""
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(uploaded_files)
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        progress_bar.progress((i + 1) / total_files)
        
        try:
            # Extract text
            resume_text = extract_text_from_file(uploaded_file)
            if not resume_text:
                st.warning(f"⚠️ Could not extract text from {uploaded_file.name}")
                continue
            
            # Analyze
            similarity_score = st.session_state.analyzer.compute_similarity(resume_text, job_description)
            resume_skills = st.session_state.skill_extractor.extract_skills(resume_text)
            job_skills = st.session_state.skill_extractor.extract_skills(job_description)
            matched_skills, missing_skills = st.session_state.skill_extractor.compare_skills(resume_skills, job_skills)
            
            results.append({
                'filename': uploaded_file.name,
                'similarity_score': similarity_score,
                'matched_skills': len(matched_skills),
                'missing_skills': len(missing_skills),
                'total_skills': len(resume_skills),
                'matched_skills_list': matched_skills,
                'missing_skills_list': missing_skills
            })
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    
    if results:
        st.session_state.analysis_results = results
        st.success(f"✅ Successfully analyzed {len(results)} resumes!")
        st.rerun()

def display_comparison_results():
    """Display comparison results for multiple resumes"""
    results = st.session_state.analysis_results
    
    st.markdown("---")
    st.header("📊 Comparison Results")
    
    # Create dataframe for display
    df = pd.DataFrame(results)
    df = df.sort_values('similarity_score', ascending=False)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resumes", len(df))
    with col2:
        st.metric("Best Match", f"{df['similarity_score'].max():.1f}%")
    with col3:
        st.metric("Average Match", f"{df['similarity_score'].mean():.1f}%")
    with col4:
        st.metric("Lowest Match", f"{df['similarity_score'].min():.1f}%")
    
    # Comparison chart
    st.subheader("📈 Resume Comparison Chart")
    comparison_chart = create_comparison_chart(df)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Detailed results table
    st.subheader("📋 Detailed Results")
    
    # Format the dataframe for display
    display_df = df[['filename', 'similarity_score', 'matched_skills', 'missing_skills', 'total_skills']].copy()
    display_df.columns = ['Resume File', 'Match Score (%)', 'Matched Skills', 'Missing Skills', 'Total Skills']
    display_df['Match Score (%)'] = display_df['Match Score (%)'].round(1)
    
    st.dataframe(display_df, use_container_width=True)
    
    # Individual resume details
    st.subheader("🔍 Individual Resume Analysis")
    
    selected_resume = st.selectbox(
        "Select a resume for detailed analysis:",
        options=df['filename'].tolist(),
        index=0
    )
    
    if selected_resume:
        resume_data = df[df['filename'] == selected_resume].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**✅ Matched Skills:**")
            for skill in resume_data['matched_skills_list']:
                st.success(f"• {skill}")
        
        with col2:
            st.write("**❌ Missing Skills:**")
            for skill in resume_data['missing_skills_list']:
                st.error(f"• {skill}")
    
    # Clear results button
    if st.button("🗑️ Clear Results"):
        st.session_state.analysis_results = []
        st.rerun()

def show_about():
    """Display information about the application"""
    st.header("ℹ️ About Resume Matcher")
    
    st.markdown("""
    ### 🎯 Purpose
    Resume Matcher is an intelligent application that helps both job seekers and recruiters by analyzing 
    the semantic similarity between resumes and job descriptions using advanced Natural Language Processing (NLP).
    
    ### 🔧 Features
    - **Text Extraction**: Supports PDF and plain text resume uploads
    - **Semantic Analysis**: Uses sentence-transformers for advanced similarity computation
    - **Skill Matching**: Identifies matched and missing skills automatically
    - **Visual Analytics**: Interactive charts and progress indicators
    - **Multi-Resume Comparison**: Compare multiple candidates against one job description
    - **Improvement Suggestions**: Get actionable feedback for resume enhancement
    
    ### 🚀 How It Works
    1. **Upload**: Upload your resume (PDF or text) or multiple resumes for comparison
    2. **Input**: Paste the job description you want to match against
    3. **Analysis**: Our NLP models compute semantic similarity and extract key skills
    4. **Results**: View match scores, skill analysis, and improvement suggestions
    
    ### 💡 Technology Stack
    - **Streamlit**: Web application framework
    - **Sentence Transformers**: Semantic similarity computation
    - **spaCy**: Natural language processing and skill extraction
    - **PyMuPDF**: PDF text extraction
    - **Plotly**: Interactive visualizations
    
    ### 👥 Target Users
    - **Job Seekers**: Optimize resumes for specific job applications
    - **Recruiters**: Quickly screen and compare multiple candidates
    - **HR Professionals**: Streamline the initial candidate evaluation process
    
    ### 📊 Match Score Interpretation
    - **90-100%**: Excellent match - strong candidate
    - **70-89%**: Good match - consider for interview
    - **50-69%**: Moderate match - review skills gap
    - **Below 50%**: Poor match - significant skills gap
    """)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit and advanced NLP techniques**")

if __name__ == "__main__":
    main()
