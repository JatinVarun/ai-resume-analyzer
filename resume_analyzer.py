import re
import string
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class ResumeAnalyzer:
    """
    AI-Powered Resume Analyzer using NLP and Machine Learning.
    Analyzes resumes and matches them with job descriptions based on skill similarity.
    """

    def __init__(self):
        """Initialize the Resume Analyzer with NLP tools."""
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', lowercase=True)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_matrix = None
        self.feature_names = None

    def preprocess_text(self, text):
        """
        Preprocess resume/job description text.
        
        Args:
            text (str): Raw text to preprocess
            
        Returns:
            str: Cleaned and processed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                  if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)

    def extract_keywords(self, text, top_n=15):
        """
        Extract important keywords from text using TF-IDF.
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to return
            
        Returns:
            list: List of top keywords with their scores
        """
        preprocessed = self.preprocess_text(text)
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf = vectorizer.fit_transform([preprocessed])
        
        feature_names = np.array(vectorizer.get_feature_names_out())
        tfidf_scores = tfidf.toarray()[0]
        
        top_indices = tfidf_scores.argsort()[-top_n:][::-1]
        keywords = [(feature_names[i], round(tfidf_scores[i], 4)) for i in top_indices if tfidf_scores[i] > 0]
        
        return keywords

    def calculate_similarity(self, resume_text, job_description):
        """
        Calculate cosine similarity between resume and job description.
        
        Args:
            resume_text (str): Resume content
            job_description (str): Job description content
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Preprocess texts
        resume_processed = self.preprocess_text(resume_text)
        job_processed = self.preprocess_text(job_description)
        
        # Vectorize using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_processed, job_processed])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return round(similarity * 100, 2)  # Return as percentage

    def match_keywords(self, resume_text, job_description):
        """
        Find matching keywords between resume and job description.
        
        Args:
            resume_text (str): Resume content
            job_description (str): Job description content
            
        Returns:
            dict: Dictionary with matched and missing keywords
        """
        # Extract keywords from both texts
        resume_keywords = set([kw[0] for kw in self.extract_keywords(resume_text, top_n=20)])
        job_keywords = set([kw[0] for kw in self.extract_keywords(job_description, top_n=20)])
        
        # Find matches and differences
        matched = resume_keywords.intersection(job_keywords)
        missing = job_keywords - resume_keywords
        extra = resume_keywords - job_keywords
        
        return {
            'matched_keywords': sorted(list(matched)),
            'missing_keywords': sorted(list(missing)),
            'extra_keywords': sorted(list(extra)),
            'match_percentage': round((len(matched) / len(job_keywords) * 100), 2) if job_keywords else 0
        }

    def generate_report(self, resume_text, job_description):
        """
        Generate a comprehensive analysis report.
        
        Args:
            resume_text (str): Resume content
            job_description (str): Job description content
            
        Returns:
            dict: Comprehensive analysis report
        """
        similarity_score = self.calculate_similarity(resume_text, job_description)
        keyword_analysis = self.match_keywords(resume_text, job_description)
        resume_keywords = self.extract_keywords(resume_text, top_n=10)
        job_keywords = self.extract_keywords(job_description, top_n=10)
        
        # Generate recommendation
        if similarity_score >= 75:
            recommendation = "Excellent Match! Highly Recommended"
            rating = "⭐⭐⭐⭐⭐"
        elif similarity_score >= 60:
            recommendation = "Good Match! Recommended"
            rating = "⭐⭐⭐⭐"
        elif similarity_score >= 45:
            recommendation = "Moderate Match. Consider for interview"
            rating = "⭐⭐⭐"
        elif similarity_score >= 30:
            recommendation = "Weak Match. Not recommended"
            rating = "⭐⭐"
        else:
            recommendation = "Poor Match. Not suitable"
            rating = "⭐"
        
        return {
            'similarity_score': similarity_score,
            'recommendation': recommendation,
            'rating': rating,
            'keyword_analysis': keyword_analysis,
            'top_resume_keywords': resume_keywords,
            'top_job_keywords': job_keywords,
            'matched_count': len(keyword_analysis['matched_keywords']),
            'missing_count': len(keyword_analysis['missing_keywords']),
            'match_percentage': keyword_analysis['match_percentage']
        }

    def batch_analyze(self, resumes_list, job_description):
        """
        Analyze multiple resumes against a job description.
        
        Args:
            resumes_list (list): List of resume texts
            job_description (str): Job description content
            
        Returns:
            list: List of analysis reports ranked by similarity
        """
        results = []
        
        for idx, resume in enumerate(resumes_list):
            report = self.generate_report(resume, job_description)
            report['resume_id'] = idx + 1
            results.append(report)
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return results
