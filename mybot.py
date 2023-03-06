import gradio as gr
import os, openai, subprocess
import ffmpeg
from gtts import gTTS #Import Google Text to Speech
import sys
#sys.path.append('/path/to/ffmpeg')


# Define OpenAI API key 
openai.api_key = "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"

# Set up the model and prompt
model_engine = "gpt-3.5-turbo"

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

role = sys.argv[1]
system_content = "You are a " + role + ". Respond to all input in 30 words or less"
messages = [{"role":"system","content": system_content}]

def therapy(audio):
  print("Came here")
  global messages
  print("Calling Transcribe")

  audio_file = open(audio, "rb")
  transcript = openai.Audio.transcribe("whisper-1",audio_file)
  messages.append({"role":"user","content": transcript["text"]})

  response = openai.ChatCompletion.create(
  model='gpt-3.5-turbo',
  messages=messages
  )

  print("About to get into Audio")
  system_message = response['choices'][0]['message']
  messages.append(system_message)

  subprocess.call(["say",system_message['content']])
  chat_transcript = ""

  for message in messages:
    if message['role'] != 'system':
      chat_transcript += message['role'] + ":" + message['content'] + "\n\n"
    
  return chat_transcript


print("Launching Gradio")
gr.Interface(fn=therapy, inputs=gr.Audio(source="microphone",type="filepath"), outputs="text").launch()
print("Gradio Done")

