import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
from mistralai import Mistral, UserMessage
import os
from time import sleep

# -----------------  Loading API Key -----------------
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]

# ----------------- Defining URLs -----------------
policies = {
    "Academic Annual Leave Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-annual-leave-policy",
    "Academic Appraisal Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-appraisal-policy",
    "Academic Appraisal Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-appraisal-procedure",
    "Academic Credentials Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-credentials-policy",
    "Academic Freedom Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-freedom-policy",
    "Academic Members' Retention Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-members%E2%80%99-retention-policy",
    "Academic Professional Development Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-professional-development",
    "Academic Qualifications Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-qualifications-policy",
    "Credit Hour Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/credit-hour-policy",
    "Intellectual Property Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/intellectual-property-policy",
    "Joint Appointment Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/joint-appointment-policy",
    "Program Accreditation Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/program-accreditation-policy",
    "Examination Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/examination-policy",
    "Student Conduct Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/student-conduct-policy",
    "Student Conduct Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/student-conduct-procedure",
    "Academic Schedule Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/academic-schedule-policy",
    "Academic Scheduling Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-scheduling-procedure",
    "Student Attendance Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/student-attendance-policy",
    "Student Attendance Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/student-attendance-procedure",
    "Student Appeals Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/student-appeals-policy",
    "Academic Standing Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-standing-policy",
    "Academic Standing Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/academic-standing-procedure",
    "Transfer Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/transfer-policy",
    "Admissions Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/admissions-policy",
    "Admissions Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/admissions-procedure",
    "Final Grade Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/final-grade-policy",
    "Final Grade Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/final-grade-procedure",
    "Registration Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/registration-policy",
    "Registration Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/registration-procedure",
    "Sport and Wellness Facilities and Services Usage Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/sport-and-wellness-facilities-and",
    "Student Engagement Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/student-engagement-policy",
    "Student Council Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/student-council-procedure",
    "International Student Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/international-student-policy",
    "International Student Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/international-student-procedure",
    "Graduation Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/graduation-policy",
    "Student Counselling Services Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/student-counselling-services-policy",
    "Graduate Admissions Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/graduate-admissions-policy",
    "Graduate Academic Standing Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/graduate-academic-standing-policy",
    "Graduate Academic Standing Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/udst-policies-and-procedures/graduate-academic-standing-procedure",
    "Graduate Final Grade Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/graduate-final-grade-policy",
    "Graduate Final Grade Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/graduate-final-grade-procedure",
    "Use of Library Space Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/use-library-space-policy",
    "Digital Media Centre Booking Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/digital-media-centre-booking",
    "Library Study Room Booking Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/library-study-room-booking-procedure",
    "Right to Refuse Service Procedure": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/right-refuse-service-procedure",
    "Scholarship and Financial Assistance Policy": "https://www.udst.edu.qa/about-udst/institutional-excellence-ie/policies-and-procedures/scholarship-and-financial-assistance"
}

def stream_response(text, placeholder, delay=0.005):
    """
    Displays text as if it's being typed in real-time.
    Args:
        text (str): The full text to display.
        placeholder (st.empty()): Streamlit placeholder for live updates.
        delay (float): Time delay between each chunk of text (default: 50ms).
    """
    displayed_text = ""  # Start with an empty text
    for char in text:
        displayed_text += char  # Append one character at a time
        placeholder.markdown(displayed_text)  # Update the placeholder
        sleep(delay)  # Simulate typing delay

def scrape_and_chunk_policies(relevant_policies):
    """Fetch relevant policies, combine them, and split into chunks."""
    chunks = []
    for name in relevant_policies:
        url = policies.get(name)
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator="\n").strip()  # entire page text
                policy_chunks = text.split("\n\n")  # split by paragraphs
                for chunk in policy_chunks:
                    if chunk.strip():
                        chunks.append((name, chunk))
    return chunks

def mistral(user_message, model="mistral-small-latest"):
    # In your real code, pick the model you need
    model = "mistral-large-latest"
    from mistralai import Mistral, UserMessage
    client = Mistral(api_key=MISTRAL_API_KEY)
    messages = [UserMessage(content=user_message)]
    chat_response = client.chat.complete(model=model, messages=messages)
    return chat_response.choices[0].message.content

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="UDST Policy Query System", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("UDST Policy Query System")
st.sidebar.header("Policies")
for name, url in policies.items():
    st.sidebar.markdown(f"- [{name}]({url})")

st.title("UDST Policy Query System")

user_query = st.text_input("Enter your question:")

if user_query:
    with st.spinner("Processing..."):
        # Mistral prompt to find relevant policies
        policy_list = "\n".join(policies.keys())
        prompt_policies = f"""
        Here is a list of policies:
        ---------------------
        {policy_list}
        ---------------------
        Based on the user query, which of these policies are most relevant? 
        you must choose minumum 2 relevant policies, in a comma-separated list.
        Query: {user_query}

        Relevant Policies (in a comma-separated list):
        """
        raw_response = mistral(prompt_policies)

        # Split the raw response by commas
        response_items = [item.strip() for item in raw_response.split(",")]

        # Filter so we only keep actual keys from our 'policies' dictionary
        relevant_policies = [rp for rp in response_items if rp in policies]

        # Display the relevant policies in a clean numbered list
        st.subheader("Relevant Policies")
        for i, policy_name in enumerate(relevant_policies, 1):
            st.markdown(f"{i}. {policy_name}")

        # If none matched, let the user know
        if not relevant_policies:
            st.write("No recognized policies returned by the model. Please try again.")
            st.stop()

        # Scrape the relevant policies’ text
        all_chunks = scrape_and_chunk_policies(relevant_policies)
        chunk_texts = [chunk[1] for chunk in all_chunks]

        # Build a structured context that associates each chunk with its policy
        structured_context = ""
        for policy_name, chunk_text in all_chunks:
            structured_context += (
            f"Policy Name: {policy_name}\n"
            f"-----------------\n"
            f"{chunk_text}\n\n"
            )

        answer_prompt = f"""
    We have collected text from the following policies. 
    For each piece of information you use in your final answer, 
    please specify the policy you are drawing from.

    Context:
    {structured_context}

    Now, using ONLY this context (and not prior knowledge), answer the query:
    \"{user_query}\"

    You must provide a well-structured answer based on the policies provided.
    and use all of the provided policies in your answer.
        """

        consolidated_response = mistral(answer_prompt)
    st.subheader("Consolidated Answer")
    # Create a placeholder for live writing effect
    response_placeholder = st.empty()

    # Stream response with typing effect
    stream_response(consolidated_response, response_placeholder)
    
    # Show link to each relevant policy
    st.subheader("Policies Links")
    for policy_name in relevant_policies:
        policy_link = policies[policy_name]
        st.markdown(f"- **{policy_name}** — [View Policy]({policy_link})")
