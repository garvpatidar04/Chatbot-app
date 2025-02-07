Here's a well-structured `README.md` file for your project:

---

### 📌 TalentScout - AI Hiring Assistant

#### 🚀 An AI-powered chatbot to streamline the hiring process by conducting technical interviews, validating candidate responses, and scoring their performance.

---

## 📖 Project Overview

TalentScout is an AI-driven hiring assistant built using  **Streamlit** . It automates initial technical screenings by:

✅ **Collecting candidate information** (name, email, phone, experience, position, etc.)

✅ **Verifying email via OTP** before proceeding

✅ **Asking tailored technical interview questions** based on the candidate’s tech stack

✅ **Evaluating answers & scoring performance**

✅ **Sending interview results via email**

This tool helps companies **save time and effort** in screening candidates before a live interview.

---

## 🛠️ Installation Instructions

### 1️⃣ Prerequisites

Ensure you have the following installed:

* **Python 3.10+**
* **pip**
* **Streamlit** (`pip install streamlit`)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/garvpatidar04/Chatbot-app.git
cd <name of the folder you created to clone app>
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

🎉 Your TalentScout Hiring Assistant is now running locally!

---

## 📌 Usage Guide

1️⃣ Open the app in your browser (default: `http://localhost:8501/`).

2️⃣ The chatbot will **guide the candidate** through a structured hiring process.

3️⃣ Once the candidate's email is verified via OTP, the interview starts.

4️⃣ The chatbot **asks technical questions** based on the candidate’s tech stack.

5️⃣ Answers are **evaluated & scored** automatically.

6️⃣ The final result is  **emailed**.

---

## 🎯 Prompt Design

### 🔹 Candidate Input Validation

* Ensures correct format for **name, email, OTP, phone, experience, etc.**
* Uses predefined rules to **give meaningful feedback** if input is incorrect.

### 🔹 Technical Interview Questions

* Dynamically **generates 3 interview questions** per candidate:

  ✅ **Basic Concept**

  ✅ **Intermediate Problem-Solving**

  ✅ **Advanced Topic**

### 🔹 Answer Evaluation

* Answers are **scored from 0-10** based on:

  🎯 **Accuracy (40%)**

  🎯 **Completeness (30%)**

  🎯 **Clarity (20%)**

  🎯 **Best Practices (10%)**

---

## 🛠️ Challenges & Solutions

### ❌ Challenge: Handling State in Streamlit

> **Issue:** Initially struggled with maintaining user input across different steps.
>
> **Solution:** Learned about `st.session_state`, which  **persists values between interactions** .

### ❌ Challenge: Redirecting Conversation Flow

> **Issue:** When users provided unexpected input, redirecting them back was tricky.
>
> **Solution:** Implemented **step-based tracking** to ensure smooth navigation.

### ❌ Challenge: Debugging & Bug Fixes 😅

> **Issue:** Small bugs kept appearing throughout development.
>
> **Solution:** Continuous debugging, proper logging(Although removed in final phase, I add it latter with some improvement), and  **structured validation checks** .

---

## 📧 Future Improvements

✅ **More AI-driven responses** (e.g., GPT-based feedback)

✅ **Better UI/UX enhancements** using advanced CSS

✅ **Multiple interview formats** (HR, technical, behavioral)

✅ **Database storage for interview history (PostgreSQL or MongoDB)**

✅ Later I will implement the app using FastAPI (backend), React (frontend) and either PostgreSQl or MongoDB.

---

### 💡 Contributing

Feel free to open an issue or submit a PR if you have ideas to enhance the app!
