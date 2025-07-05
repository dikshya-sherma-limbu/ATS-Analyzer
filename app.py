import base64
import io
from dotenv import load_dotenv  # To load environment variables from a .env file
load_dotenv() # Load environment variables
import streamlit as st  # Streamlit for the web app
import os # To interact with the operating system
from PIL import Image # Python Imaging Library for image processing
import pdf2image # To convert PDF files to images
import google.generativeai as genai # Google Generative AI for text generation

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Configure Google Generative AI with the API key

# Function to get the response from the Gemini model
# Takes input text, PDF content, and a prompt as arguments
def get_gemini_response(input,pdf_content,prompt):
  model = genai.GenerativeModel("models/gemini-1.5-flash-latest")  # Initialize the Gemini model

  response=model.generate_content([input,pdf_content[0],prompt])  # Generate content using the model
  return response.text  # Return the generated text

# Function to set up the input PDF
# Takes an uploaded file as an argument and returns the PDF base64 encoded content
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_content = pdf2image.convert_from_bytes(uploaded_file.read())  # Convert PDF to images
            
        first_page=pdf_content[0]
        
        #convert into bytes
        
        img_byte_arr=io.BytesIO() # Convert the first page to bytes
        first_page.save(img_byte_arr, format='JPEG')  # Save the image in JPEG format
        img_byte_arr = img_byte_arr.getvalue()  # Get the byte value of the image

        pdf_parts = [{
            "mime_type": "image/jpeg",  # Specify the MIME type as JPEG
            "data": base64.b64encode(img_byte_arr).decode('utf-8'),  # Encode the image bytes to base64 - meaning it can be sent as a string
        }]
        return pdf_parts
    # If no file is uploaded, raise an error
    else:
        raise FileNotFoundError("No file uploaded")  # Raise an error if no file is uploaded



#Steamlit app setup
st.set_page_config(page_title="ATS Analyzer", page_icon=":book:", layout="wide")  # Set the page configuration for Streamlit
st.title("Let me analyze your resume")  # Set the title of the app

input_text = st.text_area("Job Description",key="job_description")  # Input field for the user's question
uploaded_file = st.file_uploader("Upload resume(PDF)", type=["pdf"])  # File uploader for PDF files

if uploaded_file is not None:
    st.markdown("File uploaded successfully!")  # Confirmation message when a file is uploaded

submit_button1 = st.button("Tell Me About the Resume")  # Submit button for the user's question

submit_button2= st.button("ATS Percentage Match")  # Submit button for both the question and PDF file


input_prompt1 ="""
You are an expert HR with extensive experience in resume evaluation and candidate assessment in Technical roles sucha as Full stack developer, web developer, software developer. Your task is to analyze the resume provided in the PDF file against the provided Job Description. The resume is in the PDF format, and you should extract relevant information from it to provide a comprehensive answer. Please ensure that your response is concise and share your professional evaluation on whether the candidate's profile aligns with provided job desctiption , also highlight the strength and weakness of the candidate's profile.
Please provide your evaluation in a clear and structured format with bullet points and major missing skills.

"""

input_prompt2="""You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of how ATS systems evaluate resumes against job descriptions and core ATS functionality. Your task is to analyze the resume provided in the PDF file against the provided Job Description. Give me the percentage match of the resume with the job description, and also provide what is missing in candidate profile and a detailed analysis of what the candidate should do to improve their resume and skills to increase their chances of getting selected by ATS systems.
"""

if submit_button1:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)  # Get the response from the Gemini model
        st.subheader("Response: ")
        st.write(response)  # Display the response in the Streamlit app
    else:
        st.error("Please upload a PDF file and enter a job description.")
        
elif submit_button2:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)  # Get the response from the Gemini model
        st.subheader("Response: ")
        st.write(response)  # Display the response in the Streamlit app
    else:
        st.error("Please upload a PDF file and enter a job description.")