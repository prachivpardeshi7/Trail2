import os
from dotenv import load_dotenv
from gtts import gTTS
import gradio as gr
from brain_of_doc import encode_image, analyze_image_with_query
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts  

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Prompt for image + audio combo
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

def process_inputs(audio_filepath, image_filepath):
    # ✅ 1. Transcribe
    speech_to_text_output = transcribe_with_groq(
        stt_model="whisper-large-v3",
        audio_filepath=audio_filepath
    )

    # ✅ 2. Analyze Image
    if image_filepath:
        encoded = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=system_prompt + "\n" + speech_to_text_output,
            encoded_image=encoded,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided to analyze."

    # ✅ 3. Convert response to speech
    output_audio_path = "doctor_response.mp3"
    text_to_speech_with_gtts(doctor_response, output_audio_path)

    return speech_to_text_output, doctor_response, output_audio_path

# ✅ Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms"),
        gr.Image(type="filepath", label="Upload a medical image")
    ],
    outputs=[
        gr.Textbox(label="Transcribed Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(type="filepath", label="Doctor's Voice Response")
    ],
    title="🧠 AI Doctor with Vision and Voice",
    description="Speak your symptoms and upload a medical image. The AI doctor will listen, analyze, and reply with a voice."
)

iface.launch(debug=True, share=True)