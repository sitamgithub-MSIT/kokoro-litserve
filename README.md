# Kokoro LitServe

[![Open In Studio](https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg)](https://lightning.ai/sitammeur/studios/kokoro-litserve)

[Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) is a high-performing, compact (82 million parameters) text-to-speech model released under the Apache 2.0 license. It supports American and British English, boasts multiple voice packs, and achieves top rankings despite limited training data. Its efficiency makes it ideal for various applications. This project shows how to create a self-hosted, private API that deploys the Kokoro [text-to-speech model](https://huggingface.co/hexgrad/Kokoro-82M) with LitServe, an easy-to-use, flexible serving engine for AI models built on FastAPI.

## Project Structure

The project is structured as follows:

- `server.py`: The file containing the main code for the web server.
- `client.py`: The file containing the code for client-side requests.
- `audio_utils.py`: The file containing utility functions for audio processing.
- `LICENSE`: The license file for the project.
- `README.md`: The README file that contains information about the project.
- `assets`: The folder containing screenshots for working on the application.
- `.gitignore`: The file containing the list of files and directories to be ignored by Git.

## Tech Stack

- Python (for the programming language)
- PyTorch (for the deep learning framework)
- Hugging Face Transformers Library (for the model)
- LitServe (for the serving engine)

## Getting Started

To get started with this project, follow the steps below:

1. Run the server: `python server.py`
2. Upon running the server successfully, you will see uvicorn running on port 8000.
3. Open a new terminal window.
4. Run the client: `python client.py`

Now, you can see the model's output based on the input request. The model will generate an audio file based on the input text and other parameters.

## Usage

The project can be used to serve the Kokoro text-to-speech model using LitServe. The model showcases how small-scale models can excel in specific areas. Its permissive licensing, user-friendliness, and versatile voice packs make it an invaluable resource for TTS applications, spanning from audiobooks to real-time assistants.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please raise an issue to discuss the changes you want to make. Once the changes are approved, you can create a pull request.

## License

This project is licensed under the [Apache-2.0 License](LICENSE).

## Contact

If you have any questions or suggestions about the project, please contact me on my GitHub profile.

Happy coding! 🚀
