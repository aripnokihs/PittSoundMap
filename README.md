# 🗺️ Pitt Sound Map
### For SteelHacks XII

![Project Banner Placeholder](/assets/banner.png)
*(Insert a banner image of the Pitt campus or your project logo here)*

## 🌟 Overview

Pitt Sound Map is an interactive platform that enhances **accessibility on campus** while also helping **alumni reconnect with familiar places** through sound.

* For **current students and visitors**, the map provides auditory cues about traffic signals, daily campus activity, and special events — supporting users with visual impairments or those seeking greater spatial awareness.
* For **alumni**, the map serves as an immersive memory portal, allowing them to hear iconic campus sounds (Cathedral bells, Schenley Plaza chatter, Forbes traffic lights) and relive their Pitt experience.

## ✨ Features

* 📍 **Interactive Map (Leaflet.js)**: Explore Pitt landmarks, tap pins, and hear authentic recordings.
* 🎧 **Sound Uploads**: Students and visitors can submit their own audio clips with metadata (date, time of day, tags, description).
* 🏷️ **Categorization**: Filter sounds by **Daily**, **Events**, and **Incidents** for focused exploration.
* 🔍 **Accessibility First**: Sounds like crosswalk beeps and traffic signals aid navigation for visually impaired students.
* 🎓 **Alumni Recall**: Alumni can relive the atmosphere of Pitt through ambient campus recordings.

![Screenshot Placeholder - Map View](/assets/map-screenshot.png)
*(Insert a screenshot of the map interface with pins)*

## 🏗️ Tech Stack

* **Frontend**: HTML + JavaScript (Leaflet.js for maps, custom modals for upload/login)
* **Backend**: Python + FastAPI (REST API for uploads and retrieval)
* **Database**: PostgreSQL (sound metadata and user info)
* **Storage**: Local/Cloud for audio files

## 🚀 Installation

### Prerequisites

* Python 3.10+
* PostgreSQL 14+
* Node.js (for serving static frontend if needed)

### Backend Setup

```bash
git clone https://github.com/<your-repo>/pitt-sound-map.git
cd pitt-sound-map/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
```

### Database Setup

```sql
CREATE DATABASE pitt_soundmap;

-- Example table
CREATE TABLE sounds (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  file_url TEXT NOT NULL,
  date DATE,
  time_of_day TEXT,
  tag TEXT,
  description TEXT,
  latitude FLOAT,
  longitude FLOAT
);
```

### Frontend Setup

```bash
cd pitt-sound-map/frontend
# Serve locally (example with Python)
python3 -m http.server 8080
```

Visit: [http://localhost:8080/index.html](http://localhost:8080/index.html)

## 📊 Accessibility Use Cases

* **Visually Impaired Students**: Crosswalk signals and environmental cues assist safe navigation.
* **Neurodiverse Users**: Predictable and tagged sound environments reduce sensory surprises.
* **Alumni Memory Recall**: Sounds tied to campus locations trigger vivid recollections and emotional connections.

![Screenshot Placeholder - Upload Form](/assets/upload-form.png)
*(Insert screenshot of your upload form)*

## 🔮 Future Improvements

* ✅ GPS metadata auto-detection during uploads
* ✅ Community moderation (upvotes/flags) for verifying sounds
* ✅ Scalable cloud storage for thousands of recordings
* ✅ “Memory Mode” for alumni, curating iconic Pitt sounds

## 👥 Team

* \[Your Names Here]
* Hackathon project, \[Hackathon Name] 2025

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---


