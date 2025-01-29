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
        - setup(device): Initializes the pipeline with the specified device.
        - decode_request(request): Convert the request payload to model input.
        - predict(inputs): Uses the model to generate audio from the input text.
        - encode_response(output): Convert the model output to a response payload.
    """

    def setup(self, device):
        """
        Sets up the pipeline for the text-to-speech task.
        """
        # Initialize the Kokoro pipeline
        self.device = device
        self.pipeline = KPipeline(lang_code="a", device=device)

    def decode_request(self, request):
        """
        Convert the request payload to model input.
        """
        # Get the inputs from request payload
        language_code = request.get("language_code", "a")
        text = request.get("text", "")
        voice = request.get("voice", "af_bella")

        # Return the inputs
        return language_code, text, voice

    def predict(self, inputs):
        """
        Run inference and generate audio file using the Kokoro model.
        """
        # Get the inputs
        language_code, text, voice = inputs

        # Initialize the pipeline if the language code has changed
        if self.pipeline.lang_code != language_code:
            self.pipeline = KPipeline(lang_code=language_code, device=self.device)

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
        final_audio, samplerate = combine_audio_files(output_dir)

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
