from flask import Flask, request, jsonify
from query import ask

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CSUSM Dining Guide</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #003366; }
        .subtitle { color: #666; margin-bottom: 30px; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #003366; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #0055a5; }
        #result { margin-top: 30px; background: white; padding: 20px; border-radius: 10px; display: none; }
        .answer { font-size: 16px; line-height: 1.6; }
        .sources { margin-top: 15px; font-size: 14px; color: #666; }
        .source-tag { background: #e8f0fe; padding: 3px 8px; border-radius: 3px; margin-right: 5px; }
        .loading { color: #666; font-style: italic; }
        .examples { margin-top: 20px; }
        .example-btn { background: #e8f0fe; color: #003366; border: 1px solid #003366; padding: 6px 12px; margin: 4px; border-radius: 15px; cursor: pointer; font-size: 13px; }
    </style>
</head>
<body>
    <h1>🍽️ CSUSM Unofficial Dining Guide</h1>
    <p class="subtitle">Ask anything about food and dining at Cal State San Marcos!</p>

    <input type="text" id="question" placeholder="e.g. What vegan options are available?" />
    <button onclick="askQuestion()">Ask</button>

    <div class="examples">
        <strong>Try these:</strong><br>
        <button class="example-btn" onclick="setQ('What vegan options are available on campus?')">Vegan options?</button>
        <button class="example-btn" onclick="setQ('Is the meal plan worth it?')">Is meal plan worth it?</button>
        <button class="example-btn" onclick="setQ('What food stations are in Campus Way Cafe?')">Campus Way Cafe menu?</button>
        <button class="example-btn" onclick="setQ('Tell me about Campus Coffee Cart')">Campus Coffee Cart?</button>
        <button class="example-btn" onclick="setQ('What are nearby restaurants?')">Nearby restaurants?</button>
    </div>

    <div id="result">
        <div class="answer" id="answer"></div>
        <div class="sources" id="sources"></div>
    </div>

    <script>
        function setQ(q) {
            document.getElementById('question').value = q;
            askQuestion();
        }

        async function askQuestion() {
            const question = document.getElementById('question').value;
            if (!question) return;

            const resultDiv = document.getElementById('result');
            const answerDiv = document.getElementById('answer');
            const sourcesDiv = document.getElementById('sources');

            resultDiv.style.display = 'block';
            answerDiv.innerHTML = '<span class="loading">Searching documents...</span>';
            sourcesDiv.innerHTML = '';

            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            const data = await response.json();
            answerDiv.innerHTML = data.answer.replace(/\n/g, '<br>');

            const uniqueSources = [...new Set(data.sources)];
            sourcesDiv.innerHTML = '<strong>Sources:</strong> ' +
                uniqueSources.map(s => `<span class="source-tag">${s}</span>`).join('');
        }

        document.getElementById('question').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') askQuestion();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/ask", methods=["POST"])
def ask_route():
    question = request.json.get("question")
    answer, chunks = ask(question)
    sources = [c["source"] for c in chunks]
    return jsonify({"answer": answer, "sources": sources})

if __name__ == "__main__":
    app.run(debug=True)