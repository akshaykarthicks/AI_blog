# AI Blog Generator

This Django project allows users to generate high-quality blog articles from YouTube videos using artificial intelligence. It downloads audio from YouTube using `yt-dlp`, transcribes it with AssemblyAI, and generates a blog post using the Gemini API.

## Features
- User authentication (signup, login, logout)
- Download audio from YouTube videos
- Transcribe audio to text using AssemblyAI
- Generate blog articles from transcripts using Gemini API
- Responsive frontend with Tailwind CSS

## Requirements
- Python 3.10+
- Django 5.1+
- yt-dlp
- ffmpeg (must be installed and available in PATH)
- AssemblyAI API key
- Gemini API key
- (Optional) Supabase/PostgreSQL for database

## Setup

1. **Clone the repository**

```bash
# Clone your project
cd your_project_folder
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
pip install yt-dlp ffmpeg-python
```

4. **Install ffmpeg**
- Download and install ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
- Make sure `ffmpeg` is available in your system PATH

5. **Set up environment variables**

Create a `.env` file in your project root:

```
GEMINI_API_KEY=your_gemini_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

6. **Configure your database**
- By default, the project uses Supabase/PostgreSQL. Update `DATABASES` in `Ai_app/settings.py` as needed.

7. **Run migrations**

```bash
python manage.py migrate
```

8. **Run the development server**

```bash
python manage.py runserver
```

## Usage
- Open your browser and go to `http://127.0.0.1:8000/`
- Sign up or log in
- Paste a YouTube video link and click "Generate"
- Wait for the AI to generate a blog article from the video

## Troubleshooting
- If YouTube audio download fails, make sure yt-dlp and ffmpeg are installed and up to date.
- If transcription fails, check your AssemblyAI API key and account limits.
- If blog generation fails, check your Gemini API key and usage limits.
- For database connection issues, verify your Supabase/PostgreSQL credentials and network access.

## References
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [AssemblyAI Docs](https://www.assemblyai.com/docs/)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs/)
- [Django Docs](https://docs.djangoproject.com/)

## License
MIT 