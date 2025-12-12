from flask import Flask, request, jsonify, Response

from flask_cors import CORS
import asyncio

from assistant.pipeline import AssistantPipeline
# from assistant.tts import speak

app = Flask(__name__)
CORS(app)

pipeline = AssistantPipeline()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@app.route("/")
def home():
    return "ZIRA Backend Running"


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "online")

    async def run():
        user_text, ans_future = pipeline.process_text(text, mode)
        answer = await ans_future
        return answer

    answer = loop.run_until_complete(run())
    pass  # disable TTS in server mode


    return jsonify({"response": answer})


@app.route("/voice", methods=["POST"])
def voice():
    mode = request.headers.get("X-Mode", "online")
    audio_bytes = request.data

    async def run():
        user_text, ans_future = pipeline.process_audio(audio_bytes, mode)
        answer = await ans_future
        return user_text, answer

    user_text, answer = loop.run_until_complete(run())
    pass  # disable TTS in server mode


    return jsonify({
        "text": user_text,
        "response": answer
    })


# SSE streaming route (your UI expects this)
@app.route("/stream-query")
def stream_query():
    text = request.args.get("text", "")
    mode = request.args.get("mode", "online")

    async_gen = pipeline.ask_online_stream(text, mode)

    async def run_async_gen():
        async for token in async_gen:
            yield token

    def sync_wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_iter = run_async_gen()
        while True:
            try:
                token = loop.run_until_complete(async_iter.__anext__())
                yield f"data: {token}\n\n"
            except StopAsyncIteration:
                break
        loop.close()

    return Response(sync_wrapper(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
