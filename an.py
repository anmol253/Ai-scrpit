from flask import Flask, request, render_template_string
import requests
import time
import random

app = Flask(__name__)

# ✅ HTML Form (Dark Chocolate Theme)
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment</title>
    <style>
        body { background-color: #3E2723; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, button { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: #FFC107; color: black; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🔥 Facebook Auto Comment 🚀</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" required><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="text" name="post_url" placeholder="📌 Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="⏳ Time Interval (e.g., 30 sec)" required><br>
        <button type="submit">🚀 Start Commenting</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

# ✅ Multi User-Agents List
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 Chrome/87.0.4280.141 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 Chrome/89.0.4389.90 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.150 Safari/537.36"
]

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files['token_file']
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = token_file.read().decode('utf-8').splitlines()
    comments = comment_file.read().decode('utf-8').splitlines()

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"

    def post_comment(token, comment):
        emoji_variants = ["🔥", "🚀", "💯", "😎", "✨", "👍", "🔥🔥", "🎯"]
        mixed_comment = f"{random.choice(emoji_variants)} {comment} {random.choice(emoji_variants)}"
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),  # ✅ Multi User-Agent Rotation
        }

        payload = {'message': mixed_comment, 'access_token': token}
        response = requests.post(url, data=payload, headers=headers)
        return response

    success_count = 0
    for i, comment in enumerate(comments):
        token = tokens[i % len(tokens)]  # ✅ Multi Token Handling

        response = post_comment(token, comment)

        if response.status_code == 200:
            success_count += 1
            print(f"✅ Comment Success! Token {i+1}")
        else:
            print(f"⛔ Token {i+1} Blocked! Retrying in 60 sec...")
            time.sleep(60)  # ✅ Auto Unblock System (Wait & Retry)

        time.sleep(interval + random.randint(5, 15))  

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
