# 🕰️ Hodiny

**Hodiny** is an interactive clock website with five distinctive visual styles and support for time zones around the world.

## ✨ Features

- Five clock styles: Orloj, Modern, Cuckoo, Digital, and Neon
- Live time updates every second
- Worldwide time-zone selection
- Responsive design for desktop and mobile
- Built with the original Flask application in mind

## 🌐 Website

Open the GitHub Pages site:

**https://it2407.github.io/hodiny/**

## 🚀 Run locally

```bash
pip install -r requirements.txt
python main.py
```

Then visit `http://localhost:5000`.

## 🐳 Docker

```bash
docker build -t hodiny .
docker run --rm -p 5000:5000 hodiny
```

Open `http://localhost:5000`.

## 🛠️ Technologies

- Python
- Flask
- HTML, CSS, and JavaScript
- Docker
- Time Zone Database

## 📁 Project structure

```text
hodiny/
├── main.py
├── requirements.txt
├── Dockerfile
├── index.html
└── README.md
```

## 🎨 Clock styles

- **Orloj** — classic astronomical clock
- **Modern** — clean glassmorphism design
- **Cuckoo** — wooden cuckoo clock
- **Digital** — green terminal-style display
- **Neon** — colorful cyberpunk theme

## 👤 Author

Created by [it2407](https://github.com/it2407).

## 📄 License

This project currently has no license. If you want others to reuse or contribute to the code, consider adding an open-source license.
