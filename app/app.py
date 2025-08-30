
# import shutil
# import os
# import asyncio
# import logging
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import assemblyai as aai
# from dotenv import load_dotenv
# load_dotenv()
# aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


# from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse

# from app.schemas import ChatRequestResponse, ChatMessage, LLMQueryResponse
# from app.services import stt, llm, tts

# logger = logging.getLogger("uvicorn.error")

# app = FastAPI(title="AI Voice Agent API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # In-memory chat session store
# chat_sessions = {}

# FALLBACK_TEXT = "I'm having trouble connecting right now, please try again."


# @app.post("/agent/chat/{session_id}", response_model=ChatRequestResponse)
# async def agent_chat(session_id: str, file: UploadFile = File(...)):
#     if session_id not in chat_sessions:
#         chat_sessions[session_id] = []

#     # Save audio temporarily
#     temp_file_path = f"temp_{file.filename}"
#     audio_bytes = await file.read()
#     with open(temp_file_path, "wb") as f:
#         f.write(audio_bytes)

#     try:
#         # STT
#         user_text = stt.STTService.transcribe_audio(temp_file_path)
#     except Exception as e:
#         logger.error(f"STT failure: {e}")
#         return await generate_fallback(session_id, "[STT failed]")

#     chat_sessions[session_id].append(ChatMessage(role="user", content=user_text))

#     # Build conversation prompt
#     conversation_prompt = "\n".join([f"{m.role.capitalize()}: {m.content}" for m in chat_sessions[session_id]])

#     try:
#         # LLM
#         assistant_text = llm.LLMService.generate_response(conversation_prompt)
#     except Exception as e:
#         logger.error(f"LLM failure: {e}")
#         return await generate_fallback(session_id, user_text)

#     chat_sessions[session_id].append(ChatMessage(role="assistant", content=assistant_text))

#     try:
#         # TTS
#         audio_url = tts.TTSService.generate_speech(assistant_text)
#     except Exception as e:
#         logger.error(f"TTS failure: {e}")
#         return await generate_fallback(session_id, user_text)

#     # Clean up temp file
#     os.remove(temp_file_path)

#     return ChatRequestResponse(
#         audio_url=audio_url,
#         transcript=user_text,
#         llm_response=assistant_text,
#         history=chat_sessions[session_id]
#     )


# @app.post("/llm/query", response_model=LLMQueryResponse)
# async def llm_query(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     audio_bytes = await file.read()
#     with open(temp_file_path, "wb") as f:
#         f.write(audio_bytes)

#     try:
#         prompt = stt.STTService.transcribe_audio(temp_file_path)
#     except Exception as e:
#         logger.error(f"STT failure: {e}")
#         audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
#         return LLMQueryResponse(audio_url=audio_url, transcript="[STT failed]", llm_response=FALLBACK_TEXT)

#     try:
#         reply = llm.LLMService.generate_response(prompt)
#     except Exception as e:
#         logger.error(f"LLM failure: {e}")
#         audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
#         return LLMQueryResponse(audio_url=audio_url, transcript=prompt, llm_response=FALLBACK_TEXT)

#     try:
#         audio_url = tts.TTSService.generate_speech(reply)
#     except Exception as e:
#         logger.error(f"TTS failure: {e}")
#         audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
#         reply = FALLBACK_TEXT

#     os.remove(temp_file_path)

#     return LLMQueryResponse(audio_url=audio_url, transcript=prompt, llm_response=reply)


# async def generate_fallback(session_id: str, user_text: str):
#     logger.warning(f"Generating fallback for session {session_id}")
#     try:
#         audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
#     except Exception as e:
#         logger.error(f"Fallback TTS failure: {e}")
#         audio_url = ""

#     return JSONResponse(content={
#         "audio_url": audio_url,
#         "transcript": user_text,
#         "llm_response": FALLBACK_TEXT,
#         "history": chat_sessions.get(session_id, [])
#     })



# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"Received message: {data}")
#             await websocket.send_text(f"Echo: {data}")
#     except WebSocketDisconnect:
#         print("Client disconnected")

# # import datetime
# # @app.websocket("/ws-audio")
# # async def websocket_audio_endpoint(websocket: WebSocket):
# #     await websocket.accept()
# #     # Generate a filename using timestamp
# #     filename = f"audio_stream_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
# #     with open(filename, "wb") as audio_file:
# #         print(f"Saving audio to: {filename}")
# #         try:
# #             while True:
# #                 data = await websocket.receive_bytes()
# #                 audio_file.write(data)
# #         except Exception as e:
# #             print(f"WebSocket error: {e}")
# #         finally:
# #             print(f"Audio stream saved to: {filename}")
            

# # def on_data(transcript: aai.RealtimeTranscript):
# #     if not transcript.text:
# #         return
# #     if isinstance(transcript, aai.RealtimeFinalTranscript):
# #         print("Final:", transcript.text)
# #     else:
# #         print("Partial:", transcript.text)

# # def on_error(err):
# #     print("Error:", err)

# # @app.websocket("/ws-audio")
# # async def websocket_audio_endpoint(websocket: WebSocket):
# #     await websocket.accept()

# #     # AssemblyAI realtime client start
# #     rt = aai.RealtimeTranscriber(
# #         sample_rate=16000,   # audio format
# #         on_data=on_data,
# #         on_error=on_error,
# #     )
# #     rt.connect()

# #     try:
# #         while True:
# #             # Client se audio bytes aayenge
# #             data = await websocket.receive_bytes()
# #             rt.stream(data)   # AssemblyAI ko bhej do

# #     except Exception as e:
# #         print(f"WebSocket error: {e}")
# #     finally:
# #         rt.close()
# #         print("Audio stream ended")
# @app.websocket("/ws-audio")
# async def websocket_audio_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     # Callback jab transcript aaye
#     def on_data(transcript: aai.RealtimeTranscript):
#         if isinstance(transcript, aai.RealtimeFinalTranscript):
#             print("✅ Final:", transcript.text)
#             # Agar UI ko bhejna ho toh:
#             asyncio.create_task(websocket.send_text(f"Final: {transcript.text}"))
#         else:
#             print("📝 Partial:", transcript.text)

#     def on_error(err: Exception):
#         print("❌ Error:", err)

#     # AssemblyAI realtime transcriber start
#     rt = aai.RealtimeTranscriber(
#         sample_rate=16000,  # PCM 16kHz mono
#         on_data=on_data,
#         on_error=on_error,
#     )
#     rt.connect()

#     try:
#         while True:
#             # Client se audio bytes receive karo
#             data = await websocket.receive_bytes()
#             rt.stream(data)  # AssemblyAI ko bhejo
#     except WebSocketDisconnect:
#         print("🔌 Client disconnected")
#     finally:
#         rt.close()
#         print("🛑 Audio stream ended")
import os
import asyncio
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import assemblyai as aai

# ---- your existing imports for non-stream paths ----
from app.schemas import ChatRequestResponse, ChatMessage, LLMQueryResponse
from app.services import stt, llm, tts

# ---------- Setup ----------
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="AI Voice Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory chat session store
chat_sessions = {}
FALLBACK_TEXT = "I'm having trouble connecting right now, please try again."

# ---------- Non-streaming endpoints (as-is) ----------
@app.post("/agent/chat/{session_id}", response_model=ChatRequestResponse)
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    temp_file_path = f"temp_{file.filename}"
    audio_bytes = await file.read()
    with open(temp_file_path, "wb") as f:
        f.write(audio_bytes)

    try:
        user_text = stt.STTService.transcribe_audio(temp_file_path)
    except Exception as e:
        logger.error(f"STT failure: {e}")
        return await generate_fallback(session_id, "[STT failed]")

    chat_sessions[session_id].append(ChatMessage(role="user", content=user_text))
    conversation_prompt = "\n".join([f"{m.role.capitalize()}: {m.content}" for m in chat_sessions[session_id]])

    try:
        assistant_text = llm.LLMService.generate_response(conversation_prompt)
    except Exception as e:
        logger.error(f"LLM failure: {e}")
        return await generate_fallback(session_id, user_text)

    chat_sessions[session_id].append(ChatMessage(role="assistant", content=assistant_text))

    try:
        audio_url = tts.TTSService.generate_speech(assistant_text)
    except Exception as e:
        logger.error(f"TTS failure: {e}")
        return await generate_fallback(session_id, user_text)

    os.remove(temp_file_path)
    return ChatRequestResponse(
        audio_url=audio_url,
        transcript=user_text,
        llm_response=assistant_text,
        history=chat_sessions[session_id]
    )


@app.post("/llm/query", response_model=LLMQueryResponse)
async def llm_query(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    audio_bytes = await file.read()
    with open(temp_file_path, "wb") as f:
        f.write(audio_bytes)

    try:
        prompt = stt.STTService.transcribe_audio(temp_file_path)
    except Exception as e:
        logger.error(f"STT failure: {e}")
        audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
        return LLMQueryResponse(audio_url=audio_url, transcript="[STT failed]", llm_response=FALLBACK_TEXT)

    try:
        reply = llm.LLMService.generate_response(prompt)
    except Exception as e:
        logger.error(f"LLM failure: {e}")
        audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
        return LLMQueryResponse(audio_url=audio_url, transcript=prompt, llm_response=FALLBACK_TEXT)

    try:
        audio_url = tts.TTSService.generate_speech(reply)
    except Exception as e:
        logger.error(f"TTS failure: {e}")
        audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
        reply = FALLBACK_TEXT

    os.remove(temp_file_path)
    return LLMQueryResponse(audio_url=audio_url, transcript=prompt, llm_response=reply)


async def generate_fallback(session_id: str, user_text: str):
    logger.warning(f"Generating fallback for session {session_id}")
    try:
        audio_url = tts.TTSService.generate_speech(FALLBACK_TEXT)
    except Exception as e:
        logger.error(f"Fallback TTS failure: {e}")
        audio_url = ""

    return JSONResponse(content={
        "audio_url": audio_url,
        "transcript": user_text,
        "llm_response": FALLBACK_TEXT,
        "history": chat_sessions.get(session_id, [])
    })


@app.websocket("/ws")
async def websocket_plain_echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# ---------- 🔴 Realtime Streaming with AssemblyAI ----------
@app.websocket("/ws-audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    """
    Expect: raw PCM Int16 mono 16 kHz chunks from the browser.
    Sends back Partial/Final transcripts as text frames.
    Also logs transcripts to server console for the Day-17 screenshot.
    """
    await websocket.accept()
    loop = asyncio.get_running_loop()
    transcript_queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()

    # Callback from AssemblyAI SDK (may be called from another thread)
    def on_data(transcript: aai.RealtimeTranscript):
        if not getattr(transcript, "text", None):
            return
        kind = "Final" if isinstance(transcript, aai.RealtimeFinalTranscript) else "Partial"
        # push to async queue thread-safely
        asyncio.run_coroutine_threadsafe(transcript_queue.put((kind, transcript.text)), loop)
        # also log on server for screenshot
        if kind == "Final":
            print("✅ Final:", transcript.text)
        else:
            print("📝 Partial:", transcript.text)

    def on_error(err: Exception):
        print("❌ AssemblyAI Error:", err)

    # Use the new Universal streaming model to avoid deprecation warnings
    rt = aai.RealtimeTranscriber(
    sample_rate=16000,
    on_data=on_data,
    on_error=on_error,
    model="universal",   # ✅ ab yeh chalega
)
    try:
        rt.connect()

        async def pump_transcripts():
            # forward transcripts to the browser
            while True:
                kind, text = await transcript_queue.get()
                try:
                    await websocket.send_text(f"{kind}: {text}")
                except Exception:
                    break

        pump_task = asyncio.create_task(pump_transcripts())

        while True:
            audio_bytes = await websocket.receive_bytes()  # raw PCM Int16LE bytes
            rt.stream(audio_bytes)

    except WebSocketDisconnect:
        print("🔌 Client disconnected from /ws-audio")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            rt.close()
        except Exception:
            pass
        # cancel pump task if running
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
        print("🛑 Audio stream ended")

