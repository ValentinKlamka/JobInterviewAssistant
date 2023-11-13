from openai import OpenAI
client = OpenAI()

audio_file= open("output0.wav", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  response_format="text"
)
print (transcript)