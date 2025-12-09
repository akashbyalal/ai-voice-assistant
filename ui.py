from flask import Flask, request, jsonify
from assistant.pipeline import AssistantPipeline
from assistant.tts import speak

app = Flask(__name__)
pipeline = AssistantPipeline()


@app.route("/")
def home():
    return """
<html>
<head>
<title>ZIRA Voice Assistant</title>

<style>
body{
    background:#0f1115;
    color:#e4e6eb;
    font-family:Inter,Arial;
    display:flex;
    align-items:center;
    justify-content:center;
    height:100vh;
    margin:0;
}
.container{
    width:380px;
    background:#1b1f26;
    padding:30px;
    border-radius:12px;
    box-shadow:0 0 20px rgba(0,0,0,0.5);
}
input{
    width:100%;
    padding:10px;
    border:none;
    border-radius:6px;
    background:#242a34;
    color:white;
    font-size:15px;
    margin-bottom:10px;
}
button{
    width:100%;
    padding:10px;
    border:none;
    border-radius:6px;
    background:#5865f2;
    color:white;
    font-size:16px;
    cursor:pointer;
    margin-top:8px;
}
button:hover{
    background:#4752c4;
}
.response-box{
    margin-top:15px;
    padding:12px;
    background:#14171b;
    border-radius:6px;
    min-height:40px;
}
</style>

</head>
<body>

<div class="container">
    <h2>ZIRA Assistant</h2>

    <input id="msg" placeholder="Ask a question...">
    <button onclick="sendText()">Ask</button>
    <button onclick="recordVoice()">🎤 Speak</button>

    <div class="response-box" id="response"></div>
</div>


<script>
async function sendText(){
    const txt = document.getElementById("msg").value;
    const res = await fetch('/query', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({text:txt})
    });
    const data = await res.json();
    document.getElementById("response").innerText = data.response;
}


// --- AUDIO RECORDING ---
let mediaRecorder;
let audioChunks = [];

async function recordVoice(){
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, {type:'audio/wav'});
        audioChunks = [];

        const buffer = await blob.arrayBuffer();

        const res = await fetch('/voice', {
            method:'POST',
            headers:{'Content-Type':'audio/wav'},
            body: buffer
        });

        const data = await res.json();
        document.getElementById("response").innerText = data.response;
    };

    mediaRecorder.start();
    setTimeout(()=> mediaRecorder.stop(), 3000);
}
</script>

</body>
</html>
"""




@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    text = data.get("text", "")
    out = pipeline.process_text(text)
    speak(out)
    return jsonify({"response": out})

@app.route("/voice", methods=["POST"])
def voice():
    # audio bytes from browser
    audio_bytes = request.data  

    out = pipeline.process_audio(audio_bytes)
    speak(out)

    return jsonify({"response": out})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
