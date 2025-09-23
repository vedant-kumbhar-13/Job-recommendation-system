import streamlit as st
import pandas as pd
from job_recommendation import get_recommendations

# Initialize session state for toggling hidden recommendations
if 'show_hidden' not in st.session_state:
    st.session_state.show_hidden = False

# Load dataset
df = pd.read_csv("job_recommendation_dataset_with_salary.csv")

# Custom CSS Styling
st.markdown("""
    <style>
        .recommendation-card {
            background: #ffffff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            margin-bottom: 10px;
            width: 100%;
            max-width: 320px;
            display: inline-block;
            margin-right: 20px;
            vertical-align: top;
            color: black;
        }
        .recommendation-card h3 {
            color: black;
        }
        .linkedin-link {
            color: #0077b5;
            text-decoration: none;
        }
        .linkedin-link:hover {
            text-decoration: none;
        }
        .company-logo {
            width: 50px;
            height: 50px;
            object-fit: contain;
            border-radius: 4px;
            margin-bottom: 8px;
        }
        .top-heading {
            background-color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            color: #0077b5;
            margin-bottom: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-heading">🔍 Personalized Job Recommendation System</div>', unsafe_allow_html=True)

# User Inputs
qualification = st.selectbox("🎓 Select Qualification:", df["Required Qualifications"].unique())
skills = st.multiselect("💡 Select Skills:", df["Required Skills"].str.split(",").explode().unique())
languages = st.multiselect("💻 Select Programming Languages:",
                           df["Programming Languages"].str.split(",").explode().unique())
expected_salary = st.number_input("💰 Expected Salary (LPA):", min_value=1.0, max_value=50.0, step=0.5)

# Main button
if st.button("🚀 Get Recommendations"):
    recommendations = get_recommendations(qualification, skills, languages, df)
    st.session_state['recommendations'] = recommendations
    # Reset show_hidden when new recommendations are generated
    st.session_state.show_hidden = False

    # Filter based on expected salary
    salary_filtered = recommendations[recommendations["Min Salary (LPA)"] <= expected_salary]
    hidden_recommendations = recommendations[recommendations["Min Salary (LPA)"] > expected_salary]

    # Store for display
    st.session_state['salary_filtered'] = salary_filtered
    st.session_state['hidden_recommendations'] = hidden_recommendations

    # Case 1: No recommendations
    if recommendations.empty:
        st.warning("⚠️ No job matches your criteria.")
    # Case 2: No jobs within salary
    elif salary_filtered.empty:
        st.warning("⚠️ No job has a minimum salary within your expected salary.")
        if not hidden_recommendations.empty:
            st.button("👀 See All Recommendations", key="see_all", on_click=lambda: st.session_state.update(show_hidden=True))
    # Case 3: Partial matches
    elif len(salary_filtered) < len(recommendations):
        st.info(f"Only {len(salary_filtered)} of {len(recommendations)} jobs have a salary within your expectation.")
        if not hidden_recommendations.empty:
            st.button("👀 See All Recommendations", key="see_all", on_click=lambda: st.session_state.update(show_hidden=True))
    # Case 4: All match salary
    else:
        st.info(f"All {len(salary_filtered)} jobs meet your salary expectation.")

# Display recommendations
if 'recommendations' in st.session_state:
    recommendations = st.session_state['recommendations']
    salary_filtered = st.session_state.get('salary_filtered', pd.DataFrame())
    final_display = recommendations if st.session_state.show_hidden else salary_filtered

    if not final_display.empty:
        st.subheader("📌 Recommended Jobs:")
        for _, row in final_display.iterrows():
            st.markdown(
                f"""
                <div class='recommendation-card'>
                    <img src='{row['Company Logo']}' class='company-logo'>
                    <h3>{str(row['Job Title'])}</h3>
                    <p><strong>Company:</strong> {str(row['Company Name'])}</p>
                    <p><strong>🔹 Required Skills:</strong> {str(row['Required Skills'])}</p>
                    <p><strong>💻 Programming Languages:</strong> {str(row['Programming Languages'])}</p>
                    <p><strong>💰 Salary:</strong> {row['Min Salary (LPA)']} - {row['Max Salary (LPA)']} LPA</p>
                    <a class='linkedin-link' href='{row['LinkedIn Profile']}' target='_blank'>
                        <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='16' style='margin-bottom:-2px;'> View on LinkedIn
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )