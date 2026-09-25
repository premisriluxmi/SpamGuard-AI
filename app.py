from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# ============================================================
# DATASET PATHS
# ============================================================

SMS_DATASET = "SMSSpamCollection.csv"
BANKING_DATASET = "banking_spam.csv"


# ============================================================
# LOAD ORIGINAL SMS DATASET
# ============================================================

try:
    sms_df = pd.read_csv(
        SMS_DATASET,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="latin-1"
    )

    print("SMS dataset loaded successfully.")
    print("SMS dataset shape:", sms_df.shape)

except Exception as e:
    print("Error loading SMS dataset:", e)
    raise


# ============================================================
# LOAD BANKING SPAM DATASET
# ============================================================

try:
    banking_df = pd.read_csv(
        BANKING_DATASET,
        encoding="utf-8"
    )

    print("Banking dataset loaded successfully.")
    print("Banking dataset shape:", banking_df.shape)

except Exception as e:
    print("Error loading banking dataset:", e)
    raise


# ============================================================
# CLEAN ORIGINAL DATASET
# ============================================================

sms_df = sms_df[["label", "message"]].copy()

sms_df["label"] = sms_df["label"].astype(str).str.strip().str.lower()
sms_df["message"] = sms_df["message"].astype(str).str.strip()

sms_df = sms_df[
    sms_df["label"].isin(["ham", "spam"])
]

sms_df = sms_df[
    sms_df["message"].str.len() > 0
]


# ============================================================
# CLEAN BANKING DATASET
# ============================================================

banking_df = banking_df[["label", "message"]].copy()

banking_df["label"] = banking_df["label"].astype(str).str.strip().str.lower()
banking_df["message"] = banking_df["message"].astype(str).str.strip()

banking_df = banking_df[
    banking_df["label"].isin(["ham", "spam"])
]

banking_df = banking_df[
    banking_df["message"].str.len() > 0
]


# ============================================================
# COMBINE DATASETS
# ============================================================

df = pd.concat(
    [sms_df, banking_df],
    ignore_index=True
)

# Remove duplicate messages
df = df.drop_duplicates(
    subset=["message"]
).reset_index(drop=True)


# ============================================================
# CONVERT LABELS
# ============================================================

df["label_num"] = df["label"].map({
    "ham": 0,
    "spam": 1
})


print("\n====================================")
print("COMBINED DATASET")
print("====================================")

print("Total messages:", len(df))
print("\nClass distribution:")
print(df["label"].value_counts())


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X = df["message"]
y = df["label_num"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining messages:", len(X_train))
print("Testing messages:", len(X_test))


# ============================================================
# TF-IDF VECTORIZER
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=10000
)


# Convert training messages into numerical features
X_train_vectors = vectorizer.fit_transform(X_train)

# Convert testing messages
X_test_vectors = vectorizer.transform(X_test)


# ============================================================
# TRAIN NAIVE BAYES MODEL
# ============================================================

model = MultinomialNB()

model.fit(
    X_train_vectors,
    y_train
)


# ============================================================
# MODEL ACCURACY
# ============================================================

accuracy = model.score(
    X_test_vectors,
    y_test
)

print("\n====================================")
print("MODEL INFORMATION")
print("====================================")

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Model: Multinomial Naive Bayes")
print("Vectorizer: TF-IDF")


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# ANALYZE MESSAGE
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # ----------------------------------------------------
        # GET MESSAGE
        # ----------------------------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Please enter a message."
            }), 400


        # ----------------------------------------------------
        # LOWERCASE MESSAGE
        # ----------------------------------------------------

        lower_message = message.lower()


        # ====================================================
        # ML PREDICTION
        # ====================================================

        message_vector = vectorizer.transform(
            [message]
        )

        ml_prediction = model.predict(
            message_vector
        )[0]

        probabilities = model.predict_proba(
            message_vector
        )[0]


        # Probability values
        ml_not_spam_probability = probabilities[0] * 100
        ml_spam_probability = probabilities[1] * 100


        # ====================================================
        # SMART ANALYSIS KEYWORDS
        # ====================================================

        banking_words = [
            "bank",
            "account",
            "upi",
            "kyc",
            "debit card",
            "credit card",
            "atm",
            "net banking",
            "transaction",
            "payment",
            "wallet",
            "beneficiary",
            "loan",
            "refund",
            "card",
            "cash"
        ]


        urgent_words = [
            "urgent",
            "immediately",
            "now",
            "suspended",
            "blocked",
            "expired",
            "warning",
            "limited",
            "disable",
            "disabled",
            "expires",
            "last chance"
        ]


        reward_words = [
            "won",
            "winner",
            "prize",
            "reward",
            "cash",
            "free",
            "lottery",
            "bonus",
            "gift",
            "offer"
        ]


        action_words = [
            "click",
            "verify",
            "update",
            "claim",
            "activate",
            "confirm",
            "login",
            "log in",
            "reactivate",
            "unlock",
            "validate",
            "open link",
            "tap"
        ]


        sensitive_words = [
            "otp",
            "pin",
            "password",
            "cvv",
            "passcode",
            "security code",
            "verification code"
        ]


        # ====================================================
        # FIND KEYWORDS
        # ====================================================

        banking_hits = [
            word for word in banking_words
            if word in lower_message
        ]

        urgent_hits = [
            word for word in urgent_words
            if word in lower_message
        ]

        reward_hits = [
            word for word in reward_words
            if word in lower_message
        ]

        action_hits = [
            word for word in action_words
            if word in lower_message
        ]

        sensitive_hits = [
            word for word in sensitive_words
            if word in lower_message
        ]


        # ====================================================
        # ALL DETECTED KEYWORDS
        # ====================================================

        keywords = []

        keywords.extend(banking_hits)
        keywords.extend(urgent_hits)
        keywords.extend(reward_hits)
        keywords.extend(action_hits)
        keywords.extend(sensitive_hits)

        # Remove duplicates while preserving order
        keywords = list(dict.fromkeys(keywords))


        # ====================================================
        # HYBRID BANKING SCAM DETECTION
        # ====================================================
        #
        # The ML model makes the normal prediction.
        #
        # This additional safety layer detects common banking
        # scam patterns such as:
        #
        # Bank + Urgency + Action
        # Bank + Urgency + Multiple banking terms
        # Bank + Sensitive information + Action
        #
        # This prevents legitimate payment messages from being
        # incorrectly marked as spam just because they contain
        # words like "UPI" or "payment".
        # ====================================================

        banking_scam = False

        # Rule 1:
        # Banking + urgency + action
        if (
            len(banking_hits) >= 1
            and len(urgent_hits) >= 1
            and len(action_hits) >= 1
        ):
            banking_scam = True


        # Rule 2:
        # Multiple banking terms + urgency
        elif (
            len(banking_hits) >= 2
            and len(urgent_hits) >= 1
        ):
            banking_scam = True


        # Rule 3:
        # Banking + sensitive information + action
        elif (
            len(banking_hits) >= 1
            and len(sensitive_hits) >= 1
            and len(action_hits) >= 1
        ):
            banking_scam = True


        # ====================================================
        # FINAL PREDICTION
        # ====================================================

        if banking_scam:

            # Override ML prediction for strong banking scam
            result = "SPAM"

            # Keep the original ML confidence but make sure
            # obvious scam messages have a strong final score.
            spam_probability = max(
                ml_spam_probability,
                90.0
            )

            not_spam_probability = (
                100.0 - spam_probability
            )

            confidence = spam_probability

            message_type = "Banking Scam / Suspicious"

            explanation = (
                "This message contains banking-related terms "
                "combined with urgency or a request to verify, "
                "activate, click, or provide sensitive information. "
                "These are common indicators of banking scams."
            )


        else:

            # Normal ML prediction
            if ml_prediction == 1:

                result = "SPAM"

                spam_probability = ml_spam_probability
                not_spam_probability = ml_not_spam_probability

                confidence = spam_probability


            else:

                result = "NOT SPAM"

                spam_probability = ml_spam_probability
                not_spam_probability = ml_not_spam_probability

                confidence = not_spam_probability


            # =================================================
            # MESSAGE TYPE
            # =================================================

            if banking_hits:
                message_type = "Banking / Financial"

            elif reward_hits:
                message_type = "Reward / Promotional"

            elif urgent_hits:
                message_type = "Urgent / Suspicious"

            elif action_hits:
                message_type = "Action Required"

            else:
                message_type = "General Message"


            # =================================================
            # EXPLANATION
            # =================================================

            if result == "SPAM":

                if reward_hits:

                    explanation = (
                        "The message contains promotional or "
                        "reward-related language that may indicate "
                        "a spam or scam message."
                    )

                elif urgent_hits:

                    explanation = (
                        "The message uses urgent or threatening "
                        "language that may be intended to pressure "
                        "the recipient into taking immediate action."
                    )

                elif action_hits:

                    explanation = (
                        "The message asks the recipient to perform "
                        "an action such as clicking, verifying, "
                        "updating, or activating something."
                    )

                else:

                    explanation = (
                        "The machine learning model detected "
                        "patterns similar to spam messages."
                    )

            else:

                explanation = (
                    "The message appears to be a normal message "
                    "based on the trained machine learning model."
                )


        # ====================================================
        # ROUND VALUES FOR UI
        # ====================================================

        confidence = round(
            float(confidence),
            2
        )

        spam_probability = round(
            float(spam_probability),
            2
        )

        not_spam_probability = round(
            float(not_spam_probability),
            2
        )


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "message": message,

            "prediction": result,

            "confidence": confidence,

            "spam_probability": spam_probability,

            "not_spam_probability": not_spam_probability,

            "message_type": message_type,

            "keywords": keywords,

            "explanation": explanation

        })


    except Exception as e:

        print("Analysis error:", e)

        return jsonify({
            "error": "Something went wrong while analyzing the message."
        }), 500


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n====================================")
    print("       SPAMGUARD AI")
    print("====================================")
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")
    print("====================================\n")

    app.run(
        debug=True
    )