# Introduction of Computational Biology

A public Python Streamlit website for learning computational biology through biological cell theory, realistic profile-specific 3D labelled cell diagrams, and quizzes.

## Student Details

- **Name:** Ummarvali muzakir
- **Registration number:** RA2511026050021
- **Department:** CSE Aiml
- **Section:** A

## Features

- Headline: **Introduction of Computational Biology**
- Realistic profile-specific 3D labelled diagrams built with Plotly
- Theory for representative biological cells:
  - Animal cell
  - Plant cell
  - Bacterial cell
  - Fungal cell
  - Protist cell
  - Neuron
  - Red blood cell
  - White blood cell
- Quiz questions and instant feedback for every cell type
- Sidebar student details card
- Ready for Streamlit Community Cloud and GitHub hosting as a repository

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Select **New app**.
4. Choose this GitHub repository and branch.
5. Set the main file path to `app.py`.
6. Click **Deploy**.

## Project structure

```text
app.py                  # Main Python Streamlit application
requirements.txt        # Python dependencies
.streamlit/config.toml  # Streamlit theme configuration
```
