import streamlit as st
import pandas as pd
from resume_analyzer import ResumeAnalyzer
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .match-high {
        color: #28a745;
        font-weight: bold;
    }
    .match-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .match-low {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ResumeAnalyzer()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    mode = st.radio("Select Analysis Mode", ["Single Resume", "Batch Analysis"])
    st.markdown("---")
    st.info("💡 **How it works:**\n- Upload resume and job description\n- AI analyzes using NLP & TF-IDF\n- Get similarity score and recommendations")

# Main header
st.title("🤖 AI-Powered Resume Analyzer")
st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
    <h3>Intelligent Resume Screening System using NLP & Machine Learning</h3>
    <p>Analyze resumes and match them with job descriptions based on skill similarity</p>
    </div>
    """, unsafe_allow_html=True)

if mode == "Single Resume":
    st.markdown("---")
    st.header("📋 Single Resume Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Resume")
        resume_input = st.radio("Resume Input Method:", ["Paste Text", "Upload File"], key="resume_method")
        
        if resume_input == "Paste Text":
            resume_text = st.text_area(
                "Paste your resume here:",
                height=300,
                placeholder="Paste resume content here..."
            )
        else:
            resume_file = st.file_uploader("Upload Resume (TXT or PDF)", type=["txt", "pdf"])
            if resume_file:
                if resume_file.type == "text/plain":
                    resume_text = resume_file.read().decode('utf-8')
                else:
                    try:
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(resume_file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                    except:
                        st.error("Please install PyPDF2 for PDF support: pip install PyPDF2")
                        resume_text = ""
            else:
                resume_text = ""
    
    with col2:
        st.subheader("💼 Job Description")
        job_input = st.radio("Job Description Input Method:", ["Paste Text", "Upload File"], key="job_method")
        
        if job_input == "Paste Text":
            job_description = st.text_area(
                "Paste job description here:",
                height=300,
                placeholder="Paste job description here..."
            )
        else:
            job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])
            if job_file:
                job_description = job_file.read().decode('utf-8')
            else:
                job_description = ""
    
    st.markdown("---")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Resume", use_container_width=True)
    
    if analyze_button:
        if resume_text.strip() and job_description.strip():
            with st.spinner("🔄 Analyzing resume..."):
                report = st.session_state.analyzer.generate_report(resume_text, job_description)
                st.session_state.analysis_results = report
        else:
            st.error("❌ Please provide both resume and job description")
    
    # Display results
    if st.session_state.analysis_results:
        report = st.session_state.analysis_results
        
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Similarity Score
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Similarity Score", f"{report['similarity_score']}%")
        with col2:
            st.metric("Rating", report['rating'])
        with col3:
            st.metric("Keywords Matched", report['matched_count'])
        with col4:
            st.metric("Match %", f"{report['match_percentage']}%")
        
        # Recommendation
        st.markdown("---")
        if report['similarity_score'] >= 75:
            st.success(f"✅ {report['recommendation']}")
        elif report['similarity_score'] >= 60:
            st.info(f"ℹ️ {report['recommendation']}")
        elif report['similarity_score'] >= 45:
            st.warning(f"⚠️ {report['recommendation']}")
        else:
            st.error(f"❌ {report['recommendation']}")
        
        # Detailed Analysis
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Matched Keywords")
            if report['keyword_analysis']['matched_keywords']:
                for kw in report['keyword_analysis']['matched_keywords']:
                    st.write(f"🟢 {kw}")
            else:
                st.write("No matching keywords found")
        
        with col2:
            st.subheader("❌ Missing Keywords")
            if report['keyword_analysis']['missing_keywords']:
                for kw in report['keyword_analysis']['missing_keywords']:
                    st.write(f"🔴 {kw}")
            else:
                st.write("All required keywords found!")
        
        # Top Keywords
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📌 Top Resume Keywords")
            df_resume = pd.DataFrame(report['top_resume_keywords'], columns=['Keyword', 'Score'])
            st.dataframe(df_resume, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("📌 Top Job Keywords")
            df_job = pd.DataFrame(report['top_job_keywords'], columns=['Keyword', 'Score'])
            st.dataframe(df_job, use_container_width=True, hide_index=True)

else:  # Batch Analysis
    st.markdown("---")
    st.header("📋 Batch Resume Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Job Description")
        job_input = st.radio("Job Description Input Method:", ["Paste Text", "Upload File"], key="batch_job")
        
        if job_input == "Paste Text":
            job_description = st.text_area(
                "Paste job description:",
                height=200,
                placeholder="Paste job description here..."
            )
        else:
            job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"], key="batch_job_file")
            job_description = job_file.read().decode('utf-8') if job_file else ""
    
    with col2:
        st.subheader("📄 Resumes")
        num_resumes = st.number_input("Number of resumes to analyze:", min_value=1, max_value=10, value=3)
        
        resumes_list = []
        for i in range(num_resumes):
            resume_text = st.text_area(
                f"Resume {i+1}:",
                height=150,
                placeholder=f"Paste resume {i+1} here...",
                key=f"resume_{i}"
            )
            if resume_text.strip():
                resumes_list.append(resume_text)
    
    st.markdown("---")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        batch_button = st.button("🔍 Analyze All Resumes", use_container_width=True)
    
    if batch_button:
        if resumes_list and job_description.strip():
            with st.spinner("🔄 Analyzing resumes..."):
                results = st.session_state.analyzer.batch_analyze(resumes_list, job_description)
                st.session_state.analysis_results = results
        else:
            st.error("❌ Please provide job description and at least one resume")
    
    # Display results
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        st.markdown("---")
        st.header("📊 Batch Analysis Results")
        
        # Summary table
        summary_data = []
        for result in results:
            summary_data.append({
                'Rank': result['resume_id'],
                'Similarity %': result['similarity_score'],
                'Rating': result['rating'],
                'Keywords Matched': result['matched_count'],
                'Recommendation': result['recommendation'][:30] + "..."
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        # Detailed results
        st.markdown("---")
        st.subheader("📋 Detailed Analysis")
        
        for idx, result in enumerate(results):
            with st.expander(f"Resume {result['resume_id']} - Score: {result['similarity_score']}%"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Similarity", f"{result['similarity_score']}%")
                with col2:
                    st.metric("Rating", result['rating'])
                with col3:
                    st.metric("Keywords Matched", result['matched_count'])
                
                st.write(f"**Recommendation:** {result['recommendation']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Matched Keywords:**")
                    if result['keyword_analysis']['matched_keywords']:
                        st.write(", ".join(result['keyword_analysis']['matched_keywords'][:10]))
                    else:
                        st.write("None")
                
                with col2:
                    st.write("**Missing Keywords:**")
                    if result['keyword_analysis']['missing_keywords']:
                        st.write(", ".join(result['keyword_analysis']['missing_keywords'][:10]))
                    else:
                        st.write("None")
        
        # Export results
        st.markdown("---")
        if st.button("📥 Export Results as CSV"):
            export_data = []
            for result in results:
                export_data.append({
                    'Resume_ID': result['resume_id'],
                    'Similarity_Score': result['similarity_score'],
                    'Rating': result['rating'],
                    'Matched_Keywords': len(result['keyword_analysis']['matched_keywords']),
                    'Missing_Keywords': len(result['keyword_analysis']['missing_keywords']),
                    'Match_Percentage': result['match_percentage'],
                    'Recommendation': result['recommendation']
                })
            
            df_export = pd.DataFrame(export_data)
            csv = df_export.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; margin-top: 30px;'>
    <p>🚀 AI-Powered Resume Analyzer | Built with Streamlit, NLP & Machine Learning</p>
    <p>Version 1.0 | Created with ❤️</p>
    </div>
    """, unsafe_allow_html=True)
