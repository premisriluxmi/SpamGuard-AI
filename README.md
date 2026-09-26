# SpamGuard-AI
AI-powered spam and scam message detection using machine learning.

## AI-Powered Spam & Scam Message Detection

SpamGuard AI is a machine learning based web application that checks whether an SMS message is **Spam or Not Spam**.

I built this project to learn how machine learning can be used for a real-world problem. I wanted to understand how text messages can be processed, converted into data, and classified using a machine learning model.

I also added some extra checks for common scam patterns, especially messages related to banking, urgent actions, rewards, verification, and suspicious keywords.

---

## 🚀 What SpamGuard AI Can Do

- Detect whether a message is Spam or Not Spam
- Show Spam and Not Spam probability
- Show a confidence score
- Find suspicious keywords in the message
- Give a Smart Analysis explanation
- Detect common banking and scam patterns
- Show recent message analysis
- Display a protection dashboard
- Provide basic security tips
- Work through a simple web interface

---

## 🧠 Machine Learning Used

For the machine learning part, I used **Multinomial Naive Bayes**.

The model classifies messages into two categories:

- **Ham** → Not Spam
- **Spam** → Suspicious or unwanted message

### Text Processing

Before giving the messages to the model, I used **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert the text into numerical features.

I also used **N-grams** so that the model can consider combinations of words instead of looking at only individual words.

The main text processing and machine learning libraries used are **Pandas and Scikit-learn**.

---

## 📊 Dataset

For this project, I combined two datasets:

- `SMSSpamCollection.csv`
- `banking_spam.csv`

After cleaning the data and removing duplicate messages, the final dataset contains:

- **5,198 unique messages**
- **4,531 Ham messages**
- **667 Spam messages**

The dataset contains both normal SMS messages and spam/scam-related messages.

I used this combined dataset so that the project could include some banking and scam-related examples along with the regular SMS spam data.

---

## 🛠️ Technologies I Used

### Programming

- Python

### Machine Learning

- Pandas
- Scikit-learn
- TF-IDF Vectorization
- Multinomial Naive Bayes

### Web Development

- Flask
- HTML
- CSS
- JavaScript

---

## 🔍 How the Project Works

The basic working of SpamGuard AI is:

1. The user enters an SMS message.
2. The message is processed by the application.
3. TF-IDF converts the message into numerical features.
4. The Multinomial Naive Bayes model analyzes the message.
5. The model predicts whether the message is Spam or Not Spam.
6. Spam and Not Spam probabilities are calculated.
7. The application checks for suspicious keywords and common scam patterns.
8. A Smart Analysis explanation is generated.
9. The final result is shown on the website.

For some banking-related messages, the application also checks combinations of banking terms, urgency, sensitive information requests, and actions such as clicking or verifying.

---

## 📁 Project Structure

```text
Spam-Message-Detector/
│
├── app.py
├── SMSSpamCollection.csv
├── banking_spam.csv
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/premisriluxmi/SpamGuard-AI.git
```

### 2. Open the Project Folder

```bash
cd SpamGuard-AI
```

### 3. Install the Required Libraries

```bash
pip install flask pandas scikit-learn
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open the Website

After running the application, open this address in your browser:

```text
http://127.0.0.1:5000
```

The SpamGuard AI website will open and you can start testing messages.

---

## 🧪 Some Example Messages

### Normal Message

```text
Hey bro, are you coming to college tomorrow?
```

**Result:** NOT SPAM

### Suspicious Message

```text
Congratulations! You won a cash prize. Click now to claim your reward!
```

**Result:** SPAM

The application can also identify suspicious words such as:

- cash
- won
- prize
- reward
- click
- claim
- now

---

## 🔐 Security Tips

💡 Never share passwords, OTPs or other sensitive personal information through messages.

🚨 Be careful with messages that create urgency or ask you to take immediate action.

---

## 📚 What I Learned From This Project

While working on SpamGuard AI, I learned how a machine learning project works from the dataset stage to the final web application.

Some of the things I practiced were:

- Cleaning and preparing datasets
- Working with text data
- Text preprocessing
- TF-IDF
- N-grams
- Machine learning classification
- Multinomial Naive Bayes
- Working with Pandas
- Using Scikit-learn
- Building a Flask application
- Connecting the ML model with a website
- Working with HTML, CSS and JavaScript
- Creating API-based communication between the frontend and backend
- Testing the model with different messages

One thing I understood from this project is that building a machine learning application is not just about training a model. We also need to prepare the data properly, test the predictions, connect the model to an application, and make the result easy for the user to understand.

---

## 🎯 Why I Built This Project

I chose spam and scam message detection because suspicious messages are something people commonly receive.

Through this project, I wanted to understand how machine learning and basic text analysis can be used to identify these types of messages.

The main idea of SpamGuard AI is to give users a simple way to check a message and understand why it may be suspicious.

---

## 🔮 Future Improvements

There are several things I would like to improve in the future:

- Add multilingual spam detection
- Use a larger and more diverse dataset
- Add URL and link analysis
- Try advanced NLP models
- Add real-time threat intelligence
- Improve scam detection for different types of messages
- Deploy the application online

---

## 👩‍💻 About Me

**Premi Sri Luxmi G**

MCA Student

I am interested in **Artificial Intelligence, Data Analytics and Machine Learning**, and I enjoy learning by building practical projects.

---

## ⭐ About This Project

SpamGuard AI is one of my practical machine learning projects where I worked on **text classification, spam detection, scam pattern analysis, and Flask web development**.

This project helped me understand how machine learning can be connected with a real application instead of using the model only through a Python script.
