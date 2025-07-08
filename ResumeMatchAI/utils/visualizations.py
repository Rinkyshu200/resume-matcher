import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict

def create_match_chart(similarity_score: float) -> go.Figure:
    """
    Create a gauge chart showing the match score.
    
    Args:
        similarity_score: Similarity score (0-100)
        
    Returns:
        Plotly figure object
    """
    # Determine color based on score
    if similarity_score >= 80:
        color = "green"
    elif similarity_score >= 60:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = similarity_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Match Score"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "gray"},
                {'range': [70, 90], 'color': "lightgreen"},
                {'range': [90, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "darkblue", 'family': "Arial"},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_skills_radar_chart(resume_skills: List[str], job_skills: List[str], 
                            matched_skills: List[str]) -> go.Figure:
    """
    Create a radar chart showing skills coverage.
    
    Args:
        resume_skills: Skills from resume
        job_skills: Skills from job description
        matched_skills: Matched skills between resume and job
        
    Returns:
        Plotly figure object
    """
    # Categorize skills for radar chart
    skill_categories = {
        'Programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby'],
        'Web Technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js'],
        'Databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
        'Data Science': ['machine learning', 'data analysis', 'pandas', 'numpy'],
        'Tools': ['git', 'linux', 'jira', 'jenkins']
    }
    
    # Calculate scores for each category
    categories = []
    resume_scores = []
    job_scores = []
    match_scores = []
    
    for category, category_skills in skill_categories.items():
        categories.append(category)
        
        # Count skills in each category
        resume_count = sum(1 for skill in resume_skills 
                          if any(cat_skill in skill.lower() for cat_skill in category_skills))
        job_count = sum(1 for skill in job_skills 
                       if any(cat_skill in skill.lower() for cat_skill in category_skills))
        match_count = sum(1 for skill in matched_skills 
                         if any(cat_skill in skill.lower() for cat_skill in category_skills))
        
        # Convert to scores (normalize by maximum possible)
        max_possible = max(len(category_skills), max(resume_count, job_count, 1))
        
        resume_scores.append((resume_count / max_possible) * 100)
        job_scores.append((job_count / max_possible) * 100)
        match_scores.append((match_count / max_possible) * 100)
    
    # Create radar chart
    fig = go.Figure()
    
    # Add resume skills trace
    fig.add_trace(go.Scatterpolar(
        r=resume_scores,
        theta=categories,
        fill='toself',
        name='Resume Skills',
        line_color='blue',
        fillcolor='rgba(0, 100, 255, 0.1)'
    ))
    
    # Add job requirements trace
    fig.add_trace(go.Scatterpolar(
        r=job_scores,
        theta=categories,
        fill='toself',
        name='Job Requirements',
        line_color='red',
        fillcolor='rgba(255, 0, 0, 0.1)'
    ))
    
    # Add matched skills trace
    fig.add_trace(go.Scatterpolar(
        r=match_scores,
        theta=categories,
        fill='toself',
        name='Matched Skills',
        line_color='green',
        fillcolor='rgba(0, 255, 0, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Skills Coverage by Category",
        height=500
    )
    
    return fig

def create_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a horizontal bar chart comparing multiple resumes.
    
    Args:
        df: DataFrame with resume comparison data
        
    Returns:
        Plotly figure object
    """
    # Sort by similarity score
    df_sorted = df.sort_values('similarity_score', ascending=True)
    
    # Create color scale based on scores
    colors = []
    for score in df_sorted['similarity_score']:
        if score >= 80:
            colors.append('green')
        elif score >= 60:
            colors.append('orange')
        else:
            colors.append('red')
    
    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        x=df_sorted['similarity_score'],
        y=df_sorted['filename'],
        orientation='h',
        marker_color=colors,
        text=[f"{score:.1f}%" for score in df_sorted['similarity_score']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>' +
                      'Match Score: %{x:.1f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Resume Match Comparison",
        xaxis_title="Match Score (%)",
        yaxis_title="Resume Files",
        height=max(400, len(df) * 50),
        showlegend=False,
        margin=dict(l=200, r=50, t=50, b=50)
    )
    
    # Add vertical lines for score ranges
    fig.add_vline(x=50, line_dash="dash", line_color="gray", 
                  annotation_text="Minimum", annotation_position="top")
    fig.add_vline(x=70, line_dash="dash", line_color="orange", 
                  annotation_text="Good", annotation_position="top")
    fig.add_vline(x=90, line_dash="dash", line_color="green", 
                  annotation_text="Excellent", annotation_position="top")
    
    return fig

def create_skills_distribution_chart(categorized_skills: Dict[str, List[str]]) -> go.Figure:
    """
    Create a pie chart showing distribution of skills by category.
    
    Args:
        categorized_skills: Dictionary with categorized skills
        
    Returns:
        Plotly figure object
    """
    # Filter out empty categories
    categories = []
    counts = []
    
    for category, skills in categorized_skills.items():
        if skills:
            categories.append(category.replace('_', ' ').title())
            counts.append(len(skills))
    
    if not categories:
        # Create empty chart if no skills
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No skills categorized",
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title="Skills Distribution",
            height=400,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=0.3,
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Skills Distribution by Category",
        height=400,
        showlegend=True
    )
    
    return fig

def create_skills_match_breakdown(matched_skills: List[str], missing_skills: List[str]) -> go.Figure:
    """
    Create a stacked bar chart showing matched vs missing skills breakdown.
    
    Args:
        matched_skills: List of matched skills
        missing_skills: List of missing skills
        
    Returns:
        Plotly figure object
    """
    categories = ['Skills Analysis']
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    
    fig = go.Figure(data=[
        go.Bar(name='Matched Skills', x=categories, y=[matched_count], 
               marker_color='green', text=[f"{matched_count}"], textposition='auto'),
        go.Bar(name='Missing Skills', x=categories, y=[missing_count], 
               marker_color='red', text=[f"{missing_count}"], textposition='auto')
    ])
    
    fig.update_layout(
        barmode='stack',
        title='Skills Match Breakdown',
        yaxis_title='Number of Skills',
        height=300,
        showlegend=True
    )
    
    return fig

def create_improvement_priority_chart(missing_skills: List[str], skill_importance: Dict[str, int] = None) -> go.Figure:
    """
    Create a chart showing improvement priorities for missing skills.
    
    Args:
        missing_skills: List of missing skills
        skill_importance: Optional dictionary mapping skills to importance scores
        
    Returns:
        Plotly figure object
    """
    if not missing_skills:
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No missing skills identified",
            showarrow=False,
            font=dict(size=16, color="green")
        )
        fig.update_layout(
            title="Improvement Priorities",
            height=300,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig
    
    # Assign importance scores if not provided
    if not skill_importance:
        skill_importance = {}
        high_priority_keywords = ['python', 'java', 'sql', 'machine learning', 'aws', 'react']
        
        for skill in missing_skills:
            if any(keyword in skill.lower() for keyword in high_priority_keywords):
                skill_importance[skill] = 3  # High priority
            else:
                skill_importance[skill] = 2  # Medium priority
    
    # Sort skills by importance
    sorted_skills = sorted(missing_skills, 
                          key=lambda x: skill_importance.get(x, 1), 
                          reverse=True)
    
    # Limit to top 10 for readability
    top_skills = sorted_skills[:10]
    priorities = [skill_importance.get(skill, 1) for skill in top_skills]
    
    # Create horizontal bar chart
    colors = ['red' if p == 3 else 'orange' if p == 2 else 'yellow' for p in priorities]
    
    fig = go.Figure(go.Bar(
        y=top_skills,
        x=priorities,
        orientation='h',
        marker_color=colors,
        text=['High' if p == 3 else 'Medium' if p == 2 else 'Low' for p in priorities],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Missing Skills - Learning Priority",
        xaxis_title="Priority Level",
        yaxis_title="Skills",
        height=max(300, len(top_skills) * 30),
        showlegend=False,
        margin=dict(l=150, r=50, t=50, b=50)
    )
    
    return fig
