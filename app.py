from flask import Flask, render_template
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    # APIキーを取得
    api_key = os.getenv('GCP_API_KEY')
    return render_template('index.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
