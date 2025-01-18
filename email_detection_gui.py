import tkinter as tk
from tkinter import messagebox
import pickle
from bs4 import BeautifulSoup
import re

# Load the trained model and vectorizer
with open('phishing_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Function to clean email text
def clean_email(text):
    text = text.lower()
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    return text

# Function to predict email type
def detect_email():
    email_content = email_text.get("1.0", tk.END).strip()
    if not email_content:
        messagebox.showerror("Input Error", "Please enter email content.")
        return

    cleaned_email = clean_email(email_content)
    email_vec = vectorizer.transform([cleaned_email])
    prediction = model.predict(email_vec)

    # Get confidence level (if model provides this information)
    # If model provides probability, uncomment the next two lines.
    # prediction_proba = model.predict_proba(email_vec)[0]
    # confidence = max(prediction_proba)

    result_text = "Phishing Email" if prediction == 1 else "Non-Phishing Email"
    
    # Update result label with the prediction
    result_label.config(text=f"Result: {result_text}", fg="white")
    
    if prediction == 1:
        result_label.config(bg="red")
    else:
        result_label.config(bg="green")

# Create GUI
root = tk.Tk()
root.title("Email Phishing Detection")

# Email Text Input
tk.Label(root, text="Enter Email Content:", font=("Arial", 14)).pack(pady=10)
email_text = tk.Text(root, height=10, width=50, font=("Arial", 12))
email_text.pack(pady=10)

# Detect Button
detect_button = tk.Button(root, text="Detect Phishing", font=("Arial", 14), command=detect_email, bg="#4CAF50", fg="white")
detect_button.pack(pady=20)

# Result Label
result_label = tk.Label(root, text="Result: ", font=("Arial", 14), width=40, height=2)
result_label.pack(pady=10)

# Run the application
root.mainloop()
