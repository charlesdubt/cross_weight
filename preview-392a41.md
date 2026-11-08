# Kart Cross Weight Calculator

A mobile-optimized Streamlit app for calculating race kart cross weight,
front/rear weight bias, and left/right weight bias from four-corner scale readings.

## Features

- Four corner weight inputs (FL / FR / RL / RR) with lb/kg toggle
- Cross weight calculation (LF+RR for right-hand tracks, RF+LR for left-hand tracks)
- Front/Rear and Left/Right bias breakdown
- Target cross weight with ballast adjustment hints
- Phone-friendly layout with large touch targets

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **Create app** → select this repo → main file path: `app.py` → **Deploy**
