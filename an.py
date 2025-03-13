from flask import Flask, request
import requests
import time
import random

app = Flask(__name__)

# 🔥 Random Emojis List
EMOJIS = ["🔥", "❤️", "😍", "💯", "👍", "🤩", "😎", "✨", "🎉", "😜"]

# 🔒 Random User-Agents (Facebook Detection से बचने के लिए)
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
]

# ✅ Function to Send Comments
def post_comment(post_id, token, comment):
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # 🎉 Add Random Emoji to Comment
    comment_with_emoji = comment + " " + random.choice(EMOJIS)

    data = {
        "message": comment_with_emoji,
        "access_token": token
    }
    
    url = f"https://graph.facebook.com/{post_id}/comments"

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            status = f"✅ Comment Sent: {comment_with_emoji}"
            print(status)  # 🔴 Live Console Output
            return status
        else:
            error_msg = f"❌ Error: {response.json()}"
            print(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"❌ Exception: {str(e)}"
        print(error_msg)
        return error_msg

@app.route("/", methods=["GET", "POST"])
def index():
    console_output = []
    
    if request.method == "POST":
        post_id = request.form.get("post_id")
        time_interval = int(request.form.get("time_interval", 30))

        # 📂 Read Comments File
        comments_file = request.files["comments_file"]
        comments = comments_file.read().decode("utf-8").splitlines()

        # 📂 Read Tokens File
        tokens_file = request.files["tokens_file"]
        tokens = tokens_file.read().decode("utf-8").splitlines()

        for token in tokens:
            for comment in comments:
                status = post_comment(post_id, token, comment)
                console_output.append(status)
                time.sleep(time_interval + random.randint(5, 20))  # ⏳ Random Delay

        return page_html(console_output)
    
    return page_html([])

def page_html(console_output):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 Rocky Roy Auto Commenter 🔥</title>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            input, button {{
                padding: 10px;
                margin: 5px;
            }}
            #console {{
                background-color: #222;
                padding: 10px;
                text-align: left;
                height: 300px;
                overflow-y: scroll;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>🚀 Rocky Roy Auto Commenter 🚀</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="post_id" placeholder="Enter Post ID" required><br>
            <input type="number" name="time_interval" placeholder="Time Interval (sec)" required><br>
            <label>📂 Upload Comments File:</label>
            <input type="file" name="comments_file" accept=".txt" required><br>
            <label>📂 Upload Tokens File:</label>
            <input type="file" name="tokens_file" accept=".txt" required><br>
            <button type="submit">🚀 Start Commenting</button>
        </form>

        <h2>🔥 Live Console 🔥</h2>
        <div id="console">
            {"".join(f"<p>{log}</p>" for log in console_output)}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("\n🔥 Rocky Roy Server Running on Port 10000 🔥\n")
    app.run(host="0.0.0.0", port=10000, debug=True)
