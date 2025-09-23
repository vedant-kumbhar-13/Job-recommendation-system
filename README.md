

# 🚀 Job Recommendation System (Streamlit)

A lightweight and interactive job recommendation web app built with Streamlit. This project matches user profiles to relevant job roles using TF-IDF vectorization and cosine similarity over a curated dataset of job metadata.

## ✨ Key Features

  * **Content-Based Recommendations:** Utilizes TF-IDF with bigrams and cosine similarity to find the best job matches.
  * **Weighted Field Importance:** Prioritizes qualifications by applying weights: **Qualifications (×3)**, **Skills (×2)**, and **Languages (×1)**.
  * **Clean & Interactive UI:** Built with Streamlit to provide a simple user experience, displaying company info, required skills, LinkedIn links, and more.
  * **Salary Insights:** Includes salary bands (Min/Max, LPA) for each job, allowing users to compare opportunities at a glance.

-----

## ⚙️ How It Works

The recommendation logic follows a simple yet effective pipeline:

1.  **Text Preprocessing:** Job metadata is cleaned by converting text to lowercase, stripping punctuation, and collapsing excess whitespace.
2.  **Feature Engineering:** A single text feature is created for each job by combining its qualifications, skills, and programming languages with the specified weights.
3.  **TF-IDF Vectorization:** The combined text features are converted into a numerical matrix using `TfidfVectorizer`, configured with `ngram_range=(1,2)` and a maximum of 500 features.
4.  **Similarity Ranking:** Cosine similarity is calculated between the user's input and all jobs in the dataset. The system then returns a ranked list of the most similar and distinct job titles.

-----

## 🛠️ Technology Stack

  * **Backend & Core Logic:** Python
  * **Web Framework:** Streamlit
  * **Data Manipulation & ML:** Pandas, Scikit-learn

-----

## 🚀 Getting Started

Follow these steps to get the application running on your local machine.

### **Prerequisites**

  * Python 3.9 or higher
  * pip package manager

### **Installation & Setup**

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    # For Windows
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

3.  **Install the required dependencies:**

    ```sh
    pip install streamlit scikit-learn pandas
    ```

### **Running the Application**

Launch the Streamlit app with the following command:

```sh
streamlit run app.py
```

-----

## 📁 Project Structure

```
.
├── 📄 app.py                  # Streamlit UI and rendering logic
├── 📄 job_recommendation.py   # Preprocessing and recommendation logic
└── 📄 job_recommendation_dataset_with_salary.csv  # Dataset with job metadata
```

-----

## 📊 Dataset Schema

The dataset includes the following fields for each job entry:

  * `Job Title`
  * `Company Name`
  * `Required Qualifications`
  * `Required Skills`
  * `Programming Languages`
  * `LinkedIn Profile`
  * `Company Logo`
  * `Min Salary (LPA)`
  * `Max Salary (LPA)`
