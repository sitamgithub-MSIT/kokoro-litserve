import os
import io
import soundfile as sf
import litserve as ls
from fastapi.responses import Response
from kokoro import KPipeline
from audio_utils import combine_audio_files


class KokoroAPI(ls.LitAPI):
    """
    KokoroAPI is a subclass of ls.LitAPI that provides an interface to the Kokoro model for text-to-speech task.

    Methods:
        - setup(device): Called once at startup for the task-specific setup.
        - decode_request(request): Convert the request payload to model input.
        - predict(inputs): Uses the model to generate audio from the input text.
        - encode_response(output): Convert the model output to a response payload.
    """

    def __init__(self):
        super().__init__()
        self.pipeline = None
        self.current_lang = None

    def setup(self, device):
        self.device = device

    def decode_request(self, request):
        """
        Convert the request payload to model input.
        """
        # Extract the inputs from request payload
        language_code = request.get("language_code", "a")
        text = request.get("text", "")
        voice = request.get("voice", "af_heart")

        # Initialize or update pipeline if language changes
        if self.current_lang != language_code:
            self.current_lang = language_code
            self.pipeline = KPipeline(lang_code=language_code, device=self.device)

        # Return the inputs
        return text, voice

    def predict(self, inputs):
        """
        Run inference and generate audio file using the Kokoro model.
        """
        # Get the inputs
        text, voice = inputs

        # Generate audio files
        generator = self.pipeline(text, voice=voice, speed=1, split_pattern=r"\n+")

        # Create the output directory if it does not exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save each audio file
        for i, (gs, ps, audio) in enumerate(generator):
            file_path = f"{output_dir}/{i}.wav"
            sf.write(file_path, audio, 24000)

        # Combine all audio files
        final_audio, samplerate = combine_audio_files(output_dir, i)

        # Save the final audio to a buffer
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, final_audio, samplerate, format="WAV")
        audio_buffer.seek(0)
        audio_data = audio_buffer.getvalue()
        audio_buffer.close()

        # Return the audio data
        return audio_data

    def encode_response(self, output):
        """
        Convert the model output to a response payload.
        """
        # Package the generated audio data into a response
        return Response(content=output, headers={"Content-Type": "audio/wav"})


if __name__ == "__main__":
    # Create an instance of the KokoroAPI class and run the server
    api = KokoroAPI()
    server = ls.LitServer(api, track_requests=True)
    server.run(port=8000)
