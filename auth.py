import os
import PyPDF4
from google.oauth2.service_account import Credentials
from google.cloud import texttospeech
def upCloud(file):
    # Set the path to the JSON file containing your service account key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'E:\AudioPDF\TTS\mineral-order-380511-2b75ea0456cb.json'
    # Create a Credentials object from the environment variable
    creds = Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    print(" CONVERSION ")
    # Create a Text-to-Speech client using the credentials
    client = texttospeech.TextToSpeechClient(credentials=creds)
    with open(file, 'rb') as pdf_file:
        reader =PyPDF4.PdfFileReader(pdf_file)
        text = ''
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            text += page.extractText()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    output_file_path = r'E:/AudioPDF/TTS/output.mp3'

    # Write the response to the specified output file path
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file_path}"')
        
