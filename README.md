# 🎬 Videoflix

**Videoflix** is a modern video streaming platform that allows users to register, authenticate, and stream videos in multiple resolutions.

Authentication is securely handled using **JWT (JSON Web Tokens)**, and video delivery is based on **HLS (HTTP Live Streaming)** using `.m3u8` playlists and segmented media files.

---

## 🚀 Features

* User registration and email-based account activation
* Secure JWT authentication (login, logout, token refresh)
* Password reset functionality
* Protected API endpoints
* Video streaming in multiple resolutions (360p, 480p, 720p, 1080p)
* HLS streaming with segmented video delivery
* Adaptive bitrate streaming for smooth playback

---

## 🛠️ Tech Stack

* **Backend:** Django 6 & Django REST Framework, Python 3.12
* **Authentication:** JWT (HttpOnly Cookies)
* **Streaming Protocol:** HLS
* **Database:** PostgreSQL / SQLite
* **Web Server:** Gunicorn, Whitenoise

---

## 🎥 FFmpeg Requirement

FFmpeg is required for video transcoding and HLS segment generation.

### Install FFmpeg (Linux/Ubuntu)

```bash
sudo apt update
sudo apt install ffmpeg
```

### Usage Example

```bash
ffmpeg -i input.mp4 -hls_time 10 -hls_playlist_type vod output.m3u8
```

### Docker

Ensure FFmpeg is installed in your backend container:

```Dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

> In this project FFmpeg is already installed via Alpine (`apk add ffmpeg`).

### Environment Variable

If needed, define the FFmpeg path in `.env`:

```
FFMPEG_PATH=/usr/bin/ffmpeg
```

---

## 📦 Required Libraries (Overview)

### Core

* **Django** – Main backend framework
* **djangorestframework** – REST API framework
* pymediainfo==7.0.1 – Video metadata parsing

### Authentication

* **djangorestframework_simplejwt** – JWT authentication
* **PyJWT** – Token handling

### Background & Caching

* **redis** – In-memory datastore
* **django-redis** – Redis integration
* **rq / django-rq** – Background jobs

### Database

* **psycopg2-binary** – PostgreSQL driver

### Utilities

* **python-dotenv** – Environment variables
* **python-dateutil, pytz, tzdata** – Date & timezone handling
* **sqlparse** – SQL formatting
* **packaging** – Version handling

### Server

* **gunicorn** – WSGI server
* **whitenoise** – Static file serving

### Misc

* **asgiref** – ASGI support
* **click, colorama** – CLI tools
* **croniter** – Cron scheduling
* **six** – Compatibility layer

---

## 🔐 Authentication

Videoflix uses **cookie-based JWT authentication**:

* **Access Token** → HttpOnly cookie for authorized API requests
* **Refresh Token** → HttpOnly cookie for renewing expired access tokens

Example request:

```http
GET /api/protected-endpoint HTTP/1.1
Host: api.videoflix.com
Cookie: access_token=<access_token>; refresh_token=<refresh_token>
```

Renew access token via `/api/token/refresh/`.

---

## 🎥 Video Streaming

* Videos delivered via **HLS**
* Client requests `.m3u8` playlist
* Playlist references multiple segments
* Adaptive bitrate ensures smooth playback

### Supported Resolutions

* 360p, 480p, 720p, 1080p

---

## ⚙️ Installation & Setup (Docker)

Create a `.env` file (copy values from `.env.template` and adjust them):

```


# Email Configuration (⚠️ replace with real credentials)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_user_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your_email@example.com
```

> ⚠️ Important: Replace all email values with real SMTP credentials (e.g. Gmail, Outlook, or your provider). Otherwise features like account activation and password reset will not work.

Start containers:

```bash
docker-compose up --build
```

---

## ▶️ Running the Project

### Prerequisites

* Docker Desktop installed
* Docker running

### Access

```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

---

## 🧪 Testing

```bash
docker-compose exec web python manage.py test
```

---

## 📄 API Endpoints

All endpoints are under `/api/`. Authentication is handled via JWT cookies or headers.

### 🔐 Authentication

| Method | Endpoint                                | Description         |
| ------ | --------------------------------------- | ------------------- |
| POST   | /api/register/                          | Register user       |
| GET    | /api/activate/<uidb64>/<token>/         | Activate account    |
| POST   | /api/login/                             | Login (JWT cookies) |
| POST   | /api/logout/                            | Logout              |
| POST   | /api/token/refresh/                     | Refresh token       |
| POST   | /api/password_reset/                    | Send reset email    |
| POST   | /api/password_confirm/<uidb64>/<token>/ | Confirm reset       |

### 🎥 Videos

| Method | Endpoint                                | Description  | Auth     |
| ------ | --------------------------------------- | ------------ | -------- |
| GET    | /api/video/                             | List videos  | Optional |
| GET    | /api/video/<id>/<resolution>/index.m3u8 | HLS manifest | Optional |
| GET    | /api/video/<id>/<resolution>/<segment>  | HLS segment  | Optional |

### ⚙️ Other

| Endpoint    | Description        |
| ----------- | ------------------ |
| /admin/     | Django admin panel |
| /django-rq/ | RQ dashboard       |

---

## 📁 Project Structure

```
videoflix/
├── auth_app/        # Authentication logic
├── video_app/   # Video handling & HLS streaming
├── core/            # Settings & core config
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## 🤝 Contributing

Contributions are welcome!

---

## 📄 License

MIT License © philiptesch

