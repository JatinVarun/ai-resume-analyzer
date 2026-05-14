# 🤖 AI-Powered Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Overview

An intelligent resume screening system that uses **Natural Language Processing (NLP)** and **Machine Learning** to analyze resumes and match them with job descriptions based on skill similarity. This tool automates the hiring workflow and improves candidate ranking efficiency.

### ✨ Key Features

- **🎯 TF-IDF Vectorization**: Advanced text analysis using term frequency-inverse document frequency
- **📊 Cosine Similarity**: Accurate similarity matching algorithm
- **🔍 Keyword Extraction**: Identifies important skills and requirements
- **📱 Interactive Dashboard**: User-friendly Streamlit interface
- **📈 Single & Batch Analysis**: Analyze one or multiple resumes
- **💾 CSV Export**: Download analysis results
- **🎓 Comprehensive Scoring**: Detailed similarity metrics and recommendations

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|----------|
| **Python** | Core language |
| **Streamlit** | Web interface & dashboard |
| **Scikit-learn** | ML algorithms & TF-IDF |
| **NLTK** | Natural Language Processing |
| **Pandas** | Data manipulation & analysis |
| **NumPy** | Numerical computations |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/JatinVarun/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to that URL

## 🚀 Usage

### Single Resume Analysis

1. Select "Single Resume" mode from the sidebar
2. Enter or upload a resume
3. Enter or upload a job description
4. Click "Analyze Resume"
5. View detailed results including:
   - Similarity score (0-100%)
   - Matched keywords
   - Missing keywords
   - Top resume and job keywords
   - Recommendation status

### Batch Analysis

1. Select "Batch Analysis" mode from the sidebar
2. Enter the job description
3. Add multiple resumes (up to 10)
4. Click "Analyze All Resumes"
5. View ranked results with summary statistics
6. Export results as CSV if needed

### Example Inputs

**Sample Resume Snippet:**
```
John Doe
Software Engineer

Skills: Python, JavaScript, Machine Learning, NLP, TensorFlow, Django
Experience: 5 years in AI/ML development
Projects: Built recommendation systems, chatbots, and data analysis tools
```

**Sample Job Description:**
```
We are looking for a Machine Learning Engineer with:
- 3+ years of experience
- Strong Python skills
- Experience with NLP
- TensorFlow or PyTorch knowledge
- Experience with data analysis
```

## 🔧 How It Works

### 1. Text Preprocessing
- Converts text to lowercase
- Removes URLs, emails, and special characters
- Tokenizes text into words
- Removes stopwords (common words like 'the', 'a')
- Lemmatizes words (reduces to base form)

### 2. TF-IDF Vectorization
- **TF (Term Frequency)**: How often a word appears in a document
- **IDF (Inverse Document Frequency)**: How unique a word is across documents
- Creates numerical vectors representing documents
- Captures semantic importance of terms

### 3. Cosine Similarity
- Compares vectors using cosine distance
- Returns similarity score between 0 and 1
- Score × 100 = percentage match
- Formula: `cos(θ) = (A · B) / (||A|| × ||B||)`

### 4. Keyword Matching
- Extracts top keywords from both documents
- Identifies overlapping keywords
- Calculates match percentage
- Highlights missing skills

## 📊 Understanding the Results

### Similarity Score
- **75-100%**: Excellent Match ⭐⭐⭐⭐⭐
- **60-74%**: Good Match ⭐⭐⭐⭐
- **45-59%**: Moderate Match ⭐⭐⭐
- **30-44%**: Weak Match ⭐⭐
- **0-29%**: Poor Match ⭐

### Metrics Explained
- **Similarity %**: Overall match percentage between resume and job
- **Keywords Matched**: Number of keywords found in both documents
- **Match %**: Percentage of job keywords found in resume
- **Missing Keywords**: Skills required for the job not found in resume

## 🎯 Use Cases

1. **HR & Recruitment**
   - Automate resume screening
   - Rank candidates automatically
   - Reduce time-to-hire

2. **Career Development**
   - Identify skill gaps
   - Tailor resumes for specific jobs
   - Improve job applications

3. **Job Matching**
   - Find suitable job postings
   - Match candidates with positions
   - Improve hiring workflow

## 📈 Performance Metrics

- **Accuracy**: High semantic matching using TF-IDF
- **Speed**: Processes resumes in milliseconds
- **Scalability**: Can analyze up to 10 resumes in batch mode
- **Reliability**: Handles various resume formats

## 🔐 Privacy & Security

- All processing happens locally on your machine
- No data is stored or transmitted
- No API calls to external services
- Complete user privacy

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Reinstall requirements
```bash
pip install -r requirements.txt
```

### Issue: PDF upload not working
**Solution:** Install PyPDF2
```bash
pip install PyPDF2
```

### Issue: NLTK data not found
**Solution:** The app automatically downloads required NLTK data on first run

### Issue: Application won't start
**Solution:** Ensure you're in the correct directory and virtual environment is activated

## 🚀 Future Enhancements

- [ ] Support for more document formats (DOCX, PDF)
- [ ] Custom skill database
- [ ] Machine learning model training on company data
- [ ] Resume parsing for structured data extraction
- [ ] Email integration for automated screening
- [ ] Advanced analytics dashboard
- [ ] API endpoint for integration
- [ ] Multi-language support
- [ ] Real-time collaboration features

## 📝 Project Structure

```
ai-resume-analyzer/
├── app.py                 # Streamlit application
├── resume_analyzer.py    # Core NLP analysis engine
├── requirements.txt      # Project dependencies
├── README.md            # Documentation
└── .gitignore          # Git ignore file
```

## 💡 Code Examples

### Using ResumeAnalyzer Programmatically

```python
from resume_analyzer import ResumeAnalyzer

# Initialize analyzer
analyzer = ResumeAnalyzer()

# Analyze single resume
report = analyzer.generate_report(resume_text, job_description)
print(f"Similarity: {report['similarity_score']}%")
print(f"Recommendation: {report['recommendation']}")

# Extract keywords
keywords = analyzer.extract_keywords(resume_text, top_n=15)
print(f"Top keywords: {keywords}")

# Batch analysis
results = analyzer.batch_analyze([resume1, resume2, resume3], job_description)
for result in results:
    print(f"Resume: {result['similarity_score']}%")
```

## 📚 References

- [TF-IDF Explanation](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [NLTK Documentation](https://www.nltk.org/)
- [Scikit-learn ML](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Jatin Varun**
- GitHub: [@JatinVarun](https://github.com/JatinVarun)
- LinkedIn: [Jatin Varun](https://linkedin.com/in/jatinvarun)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to Contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show Your Support

Give a ⭐ if you found this project helpful!

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Made with ❤️ using Python, NLP, and Machine Learning**
