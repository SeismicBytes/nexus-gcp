# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl
from PIL import Image
import os
import base64 # Needed for logo embedding
from pathlib import Path # Better path handling

# --- 1. Phronesis Apex Theme Configuration Constants ---
# (Constants remain the same)
PRIMARY_ACCENT_COLOR = "#cd669b"
PRIMARY_ACCENT_COLOR_RGB = "205, 102, 155"
CARD_TEXT_COLOR = "#a9b4d2"
CARD_TITLE_TEXT_COLOR = PRIMARY_ACCENT_COLOR # Use Primary Accent for Card Title
MAIN_TITLE_COLOR = "#f0f8ff" # Adjusted to match Apex reference title color
BODY_TEXT_COLOR = "#ffff"
SUBTITLE_COLOR = "#8b98b8"
MAIN_BACKGROUND_COLOR = "#0b132b"
CARD_BACKGROUND_COLOR = "#1c2541"
SIDEBAR_BACKGROUND_COLOR = "#121a35"
HOVER_GLOW_COLOR = f"rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.4)"
CONTAINER_BG_COLOR = "rgba(11, 19, 43, 0.0)"
CONTAINER_BORDER_RADIUS = "15px"
INPUT_BG_COLOR = "#1c2541"
INPUT_BORDER_COLOR = "#3a506b"
INPUT_TEXT_COLOR = BODY_TEXT_COLOR
BUTTON_PRIMARY_BG = PRIMARY_ACCENT_COLOR
BUTTON_PRIMARY_TEXT = "#FFFFFF"
BUTTON_SECONDARY_BG = "transparent"
BUTTON_SECONDARY_TEXT = PRIMARY_ACCENT_COLOR
BUTTON_SECONDARY_BORDER = PRIMARY_ACCENT_COLOR
DATAFRAME_HEADER_BG = "#1c2541"
DATAFRAME_HEADER_TEXT = MAIN_TITLE_COLOR
DATAFRAME_CELL_BG = MAIN_BACKGROUND_COLOR
DATAFRAME_CELL_TEXT = BODY_TEXT_COLOR
CHART_SUCCESS_COLOR = "#2ecc71" # Green
CHART_WARNING_COLOR = "#f39c12" # Orange
CHART_ERROR_COLOR = "#e74c3c" # Red

# --- Font Families ---
TITLE_FONT = "'Montserrat', sans-serif"
BODY_FONT = "'Roboto', sans-serif"
CARD_TITLE_FONT = "'Montserrat', sans-serif"

# --- Logo Configuration (Adopted from Phronesis Apex reference) ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
LOGO_PATH = current_dir / "ppl_logo.png" # Use pathlib for robustness

# Function to load and encode image to base64 (from Apex reference)
def get_base64_of_bin_file(bin_file):
    try:
        # Ensure the path is treated as a string for open() if needed, Path objects work directly too
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Warning: Logo file not found at {bin_file}")
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

logo_base64 = get_base64_of_bin_file(LOGO_PATH)
# Use a placeholder div if logo fails to load (from Apex reference)
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Phronesis Partners Logo" class="logo">' if logo_base64 else '<div class="logo-placeholder">Logo</div>'


# --- 2. Apex Theme CSS Styling (Modified Header CSS) ---
APP_STYLE = f"""
<style>
    /* --- Import Fonts --- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap');

    /* --- Global Body & Streamlit App Styling --- */
    body {{
        background-color: {MAIN_BACKGROUND_COLOR};
        color: {BODY_TEXT_COLOR}; /* Default text color */
        font-family: {BODY_FONT};
    }}
    .stApp {{
        background-color: {MAIN_BACKGROUND_COLOR};
        color: {BODY_TEXT_COLOR}; /* Ensure app text inherits */
    }}
    .stApp > header {{
        background-color: transparent;
        border-bottom: none;
    }}

    /* --- Main Content Area Container --- */
    .main .block-container {{
        max-width: 1100px; /* Consistent width */
        padding: 2rem 1rem 4rem 1rem; /* Top padding adjusted */
        background-color: {CONTAINER_BG_COLOR};
        border-radius: {CONTAINER_BORDER_RADIUS};
        color: {BODY_TEXT_COLOR};
        margin: auto;
        font-family: {BODY_FONT};
    }}

    /* --- START: Header Section CSS (Adopted from Phronesis Apex) --- */
    .header-container {{
        display: flex;
        flex-direction: row;
        align-items: center;
        width: fit-content; /* Make container only as wide as content */
        margin-left: auto;   /* Auto margin left */
        margin-right: auto;  /* Auto margin right */
        margin-bottom: 3rem; /* Keep space below header */
        text-align: left; /* Keep text aligned left relative to logo */
    }}

    .logo {{
        height: 80px;          /* ADJUST height as needed */
        width: auto;
        margin-right: 1.5rem;   /* Space between logo and title */
        margin-bottom: 0;
        /* filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)); /* Optional shadow */
        flex-shrink: 0;
        vertical-align: middle;
    }}

    /* Style for placeholder if logo fails */
    .logo-placeholder {{
        height: 80px;
        width: 80px;
        margin-right: 1.5rem;
        background-color: #333;
        border: 1px dashed #555;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #888;
        font-size: 0.9em;
        text-align: center;
        border-radius: 5px;
        flex-shrink: 0;
    }}

    .title {{ /* Styling for H1 title within header */
        font-family: {TITLE_FONT};
        font-size: 2.8rem;
        font-weight: 700;
        color: {MAIN_TITLE_COLOR}; /* Use Apex title color */
        letter-spacing: 1px;
        margin: 0;
        padding: 0;
        line-height: 1.2;
        text-shadow: 0 0 8px rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.2); /* Subtle glow */
    }}
    /* --- END: Header Section CSS --- */

    /* --- General Headings (H2, H3 etc.) --- */
    /* Keep H2/H3 styles for potential future use or other sections */
    h2, h3 {{
        font-family: {TITLE_FONT}; color: {PRIMARY_ACCENT_COLOR}; margin-top: 2.5rem;
        margin-bottom: 1.5rem; border-bottom: 1px solid rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.3);
        padding-bottom: 0.6rem; font-weight: 600; font-size: 1.7rem;
    }}
     /* Style specifically for the Jobs quote H3 */
     h3.jobs-quote {{
        font-family: {BODY_FONT}; /* Use body font for quote */
        border-bottom: none;
        padding-bottom: 0;
        text-align: center;
        color: white; /* White text */
        font-size: 1.3rem; /* Slightly larger */
        font-weight: 400; /* Regular weight */
        font-style: italic; /* Italicize */
        margin-top: 1rem; /* Space above quote */
        margin-bottom: 3rem; /* Space below quote before cards */
        line-height: 1.6;
    }}
    h4 {{
        font-family: {CARD_TITLE_FONT}; color: {MAIN_TITLE_COLOR}; font-weight: 600;
        margin-top: 2rem; margin-bottom: 1rem; font-size: 1.3rem;
    }}
    h6 {{
        color: {SUBTITLE_COLOR}; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;
        font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;
        border-bottom: 1px solid {INPUT_BORDER_COLOR}; padding-bottom: 0.2rem;
    }}

    /* --- Button Styling --- */
    /* (Button CSS remains the same) */
    div[data-testid="stButton"] > button {{
        border-radius: 20px; padding: 0.6rem 1.6rem; font-weight: 600; font-family: {BODY_FONT};
        transition: all 0.3s ease; border: 1px solid {BUTTON_SECONDARY_BORDER};
        background-color: {BUTTON_SECONDARY_BG}; color: {BUTTON_SECONDARY_TEXT};
    }}
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px); box-shadow: 0 4px 10px rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.2);
        border-color: {PRIMARY_ACCENT_COLOR}; color: {PRIMARY_ACCENT_COLOR};
        background-color: rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.05);
    }}
    div[data-testid="stButton"] > button:active {{ transform: translateY(0px); box-shadow: none; }}
    div[data-testid="stButton"] > button[kind="primary"] {{
         background-color: {BUTTON_PRIMARY_BG}; color: {BUTTON_PRIMARY_TEXT}; border-color: {BUTTON_PRIMARY_BG};
    }}
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
         background-color: {PRIMARY_ACCENT_COLOR}; color: {BUTTON_PRIMARY_TEXT}; border-color: {PRIMARY_ACCENT_COLOR};
         box-shadow: 0 6px 15px rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.3); opacity: 0.9;
    }}
     div[data-testid="stButton"] > button:disabled {{
        background-color: rgba(255, 255, 255, 0.1) !important; color: rgba(255, 255, 255, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.2) !important; cursor: not-allowed;
    }}
    div[data-testid="stButton"] > button:disabled:hover {{
         box-shadow: none; transform: none; background-color: rgba(255, 255, 255, 0.1) !important;
    }}

    /* --- Input Element Styling --- */
    /* (Input CSS remains the same) */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: {INPUT_BG_COLOR} !important; color: {INPUT_TEXT_COLOR} !important;
        border: 1px solid {INPUT_BORDER_COLOR} !important; border-radius: 8px !important;
        box-shadow: none !important;
    }}
    div[data-baseweb="popover"] ul[role="listbox"] {{
         background-color: {CARD_BACKGROUND_COLOR}; border: 1px solid {INPUT_BORDER_COLOR};
         color: {INPUT_TEXT_COLOR};
    }}
    div[data-baseweb="popover"] ul[role="listbox"] li {{
        color: {INPUT_TEXT_COLOR};
    }}
    div[data-baseweb="popover"] ul[role="listbox"] li:hover {{
        background-color: rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.2);
        color: {PRIMARY_ACCENT_COLOR};
    }}
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label {{
        color: {BODY_TEXT_COLOR} !important; font-weight: 600; font-family: {BODY_FONT}; margin-bottom: 0.5rem;
    }}

    /* --- Radio Button Styling --- */
    /* (Radio CSS remains the same) */
    div[data-testid="stRadio"] label p {{ color: {BODY_TEXT_COLOR} !important; }}
    div[data-testid="stRadio"] label span {{ border-color: {INPUT_BORDER_COLOR} !important; }}
     div[data-testid="stRadio"] label input:checked + div div {{ background-color: {PRIMARY_ACCENT_COLOR} !important; }}

    /* --- Data Editor / DataFrame Styling --- */
    /* (DataFrame CSS remains the same) */
    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {{
        border: 1px solid {INPUT_BORDER_COLOR}; border-radius: 8px; background-color: {DATAFRAME_CELL_BG};
    }}
    .stDataFrame th, .stDataEditor th {{
        background-color: {DATAFRAME_HEADER_BG} !important; color: {DATAFRAME_HEADER_TEXT} !important;
        font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px;
        border-radius: 0 !important; border-bottom: 2px solid {PRIMARY_ACCENT_COLOR} !important;
    }}
    .stDataFrame td, .stDataEditor td {{
        font-size: 0.9rem; vertical-align: middle; padding: 0.6rem 0.7rem; color: {DATAFRAME_CELL_TEXT};
        border-bottom: 1px solid {INPUT_BORDER_COLOR}; border-right: 1px solid {INPUT_BORDER_COLOR};
    }}
    div[data-testid="stDataEditor"] td input, div[data-testid="stDataEditor"] td div[data-baseweb="select"] > div {{
         background-color: {INPUT_BG_COLOR} !important; color: {INPUT_TEXT_COLOR} !important;
         border: 1px solid {PRIMARY_ACCENT_COLOR} !important;
    }}

    /* --- Markdown & Misc Elements --- */
    .stMarkdown p, .stMarkdown li {{ color: {BODY_TEXT_COLOR}; line-height: 1.6; }}
    .stMarkdown a {{ color: {PRIMARY_ACCENT_COLOR}; text-decoration: none; }}
    .stMarkdown a:hover {{ text-decoration: underline; }}
    /* Blockquote style removed as requested */
    /* .stMarkdown blockquote {{ ... }} */
    .stCaption {{ color: {SUBTITLE_COLOR}; font-size: 0.85rem; }}

    /* --- Alert Styling --- */
    /* (Alert CSS remains the same) */
    div[data-testid="stAlert"] {{
        border-radius: 8px !important; border: 1px solid {INPUT_BORDER_COLOR} !important;
        border-left-width: 5px !important; padding: 1rem 1.2rem !important;
    }}
    div[data-testid="stAlert"] div[role="alert"] {{ font-family: {BODY_FONT}; font-size: 0.95rem; }}
    div[data-testid="stAlert"][data-baseweb="notification-info"] {{
        border-left-color: {PRIMARY_ACCENT_COLOR} !important; background-color: rgba({PRIMARY_ACCENT_COLOR_RGB}, 0.1) !important;
    }}
    div[data-testid="stAlert"][data-baseweb="notification-info"] div[role="alert"] {{ color: {PRIMARY_ACCENT_COLOR} !important; font-weight: 500; }}
    div[data-testid="stAlert"][data-baseweb="notification-info"] svg {{ fill: {PRIMARY_ACCENT_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-warning"] {{
        border-left-color: {CHART_WARNING_COLOR} !important; background-color: rgba(243, 156, 18, 0.1) !important;
    }}
     div[data-testid="stAlert"][data-baseweb="notification-warning"] div[role="alert"] {{ color: {CHART_WARNING_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-warning"] svg {{ fill: {CHART_WARNING_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-error"] {{
        border-left-color: {CHART_ERROR_COLOR} !important; background-color: rgba(231, 76, 60, 0.1) !important;
    }}
     div[data-testid="stAlert"][data-baseweb="notification-error"] div[role="alert"] {{ color: {CHART_ERROR_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-error"] svg {{ fill: {CHART_ERROR_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-success"] {{
        border-left-color: {CHART_SUCCESS_COLOR} !important; background-color: rgba(46, 204, 113, 0.1) !important;
    }}
     div[data-testid="stAlert"][data-baseweb="notification-success"] div[role="alert"] {{ color: {CHART_SUCCESS_COLOR} !important; }}
    div[data-testid="stAlert"][data-baseweb="notification-success"] svg {{ fill: {CHART_SUCCESS_COLOR} !important; }}


    /* --- Theme-specific custom containers (Feedback form etc.) --- */
    .theme-container {{
        background-color: {CARD_BACKGROUND_COLOR};
        border: 1px solid {INPUT_BORDER_COLOR};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    .theme-container h3 {{ /* Style for H3 inside theme-container (e.g., Feedback Form title) */
        color: {MAIN_TITLE_COLOR} !important; /* Use white/light color */
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        border-bottom: none !important; /* No border */
        padding-bottom: 0 !important;
        font-size: 1.4rem !important;
        font-weight: 600; /* Make it bold */
        font-family: {TITLE_FONT}; /* Consistent title font */
    }}

    /* --- App Card Styling --- */
    /* (App Card CSS remains mostly the same, including status badge) */
    .app-card-link {{
        text-decoration: none !important;
        display: block;
        height: 100%;
        color: inherit;
    }}
    .app-card-link:hover {{
        text-decoration: none !important;
    }}

    .app-card {{
        background-color: {CARD_BACKGROUND_COLOR};
        border: 2px solid transparent;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0;
        margin-bottom: 20px;
        text-align: left;
        transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1),
                    box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1),
                    border-color 0.4s ease,
                    background-color 0.4s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
        cursor: pointer;
        height: 100%;
    }}
    .app-card:hover {{
        transform: translateY(-10px);
        border-color: {PRIMARY_ACCENT_COLOR};
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3), 0 0 20px {HOVER_GLOW_COLOR};
    }}
    .card-status {{
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.75rem;
        font-weight: bold;
        color: white;
        z-index: 2;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .card-status.active {{ background-color: {CHART_SUCCESS_COLOR}; }}
    .card-status.inactive {{ background-color: {CHART_ERROR_COLOR}; }}
    .app-card .card-title {{
        font-family: {CARD_TITLE_FONT};
        font-weight: 600;
        color: {CARD_TITLE_TEXT_COLOR};
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
        margin-top: 0;
        padding-right: 70px;
        text-shadow: none;
        z-index: 1;
        position: relative;
    }}
    .app-card .card-description {{
        font-family: {BODY_FONT};
        color: {CARD_TEXT_COLOR};
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
        margin-bottom: 1.5rem;
        text-shadow: none;
        z-index: 1;
        position: relative;
        flex-grow: 1;
    }}
    .card-arrow {{
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        font-size: 1.3rem;
        color: {PRIMARY_ACCENT_COLOR};
        opacity: 0;
        transform: translateX(-10px);
        transition: opacity 0.3s ease, transform 0.3s ease;
        z-index: 2;
    }}
    .app-card:hover .card-arrow {{
        opacity: 1;
        transform: translateX(0);
    }}

    /* --- Expander Styling --- */
    /* (Expander CSS remains the same) */
    div[data-testid="stExpander"] div[role="button"] p {{
        color: {PRIMARY_ACCENT_COLOR} !important;
        font-weight: 600;
        font-size: 1.2em;
        font-family: {TITLE_FONT};
        margin-bottom: 0;
    }}
     div[data-testid="stExpander"] {{
        border: 1px solid {INPUT_BORDER_COLOR};
        border-radius: 10px;
        background-color: {CARD_BACKGROUND_COLOR};
        margin-top: 2.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        overflow: hidden;
    }}
     div[data-testid="stExpander"] details {{
        padding: 0.8rem 1.2rem;
     }}
     div[data-testid="stExpander"] summary {{
        cursor: pointer;
        outline: none;
     }}
     div[data-testid="stExpander"] summary:hover {{
         color: {PRIMARY_ACCENT_COLOR};
     }}
     div[data-testid="stExpander"] > div > div {{
         padding: 0 1.2rem 1.2rem 1.2rem;
     }}


    /* --- Footer Styling --- */
    .footer {{
        text-align: center; color: {SUBTITLE_COLOR}; opacity: 0.7; margin: 4rem auto 1rem auto;
        font-size: 0.9rem; max-width: 1100px; padding-bottom: 1rem;
    }}

    /* --- Streamlit Cleanup --- */
    header[data-testid="stHeader"], footer {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}

    /* --- Responsive Adjustments --- */
    /* (Responsive CSS requires updates for the new header) */
    @media (max-width: 768px) {{
        .main .block-container {{ padding: 2rem 1rem 3rem 1rem; }}
        .header-container {{ margin-bottom: 2.5rem; }}
        .logo {{ height: 60px; margin-right: 1rem;}}
        .logo-placeholder {{ height: 60px; width: 60px; margin-right: 1rem; }}
        .title {{ font-size: 2.2rem; }}
        h2, h3 {{ font-size: 1.5rem; }}
        h3.jobs-quote {{ font-size: 1.1rem; margin-bottom: 2rem; }}
        h4 {{ font-size: 1.1rem; }}
        div[data-testid="stButton"] > button {{ padding: 0.5rem 1.2rem; }}
        .theme-container, div[data-testid="stExpander"] {{ padding: 15px; margin-top: 2rem; }}
        .app-card {{ padding: 1rem; min-height: 180px; margin-bottom: 15px; }}
        .app-card .card-title {{ font-size: 1.3rem; padding-right: 65px; }}
        .app-card .card-description {{ font-size: 0.85rem; margin-bottom: 1rem; }}
        .card-arrow {{ bottom: 0.8rem; right: 0.8rem; font-size: 1.2rem; }}
        .card-status {{ top: 8px; right: 8px; font-size: 0.7rem; }}
        .footer {{ margin-top: 2rem; font-size: 0.8rem; }}
        div[data-testid="stExpander"] div[role="button"] p {{ font-size: 1.1em; }}
         div[data-testid="stExpander"] > div > div {{ padding: 0 15px 15px 15px; }}
    }}
     @media (max-width: 480px) {{
         .header-container {{
             flex-direction: column; /* Stack logo/title */
             text-align: center;
             gap: 0.8rem;
             margin-bottom: 2rem;
         }}
         .logo {{ margin-right: 0; height: 50px; }}
         .logo-placeholder {{ margin-right: 0; height: 50px; width: 50px; }}
         .title {{ font-size: 2rem; }}
         h3.jobs-quote {{ font-size: 1rem; margin-bottom: 1.5rem; }}
         .app-card {{ padding: 0.8rem; min-height: 160px; margin-bottom: 10px; }}
         .app-card .card-title {{ font-size: 1.2rem; padding-right: 60px; }}
         .app-card .card-description {{ font-size: 0.8rem; margin-bottom: 0.8rem; }}
         .card-arrow {{ bottom: 0.6rem; right: 0.6rem; font-size: 1rem; }}
         .card-status {{ top: 6px; right: 6px; font-size: 0.65rem; padding: 2px 6px;}}
         div[data-testid="stExpander"] div[role="button"] p {{ font-size: 1em; }}
         div[data-testid="stExpander"] > div > div {{ padding: 0 10px 10px 10px; }}
     }}

</style>
"""

# --- 3. Inject the custom CSS ---
st.markdown(APP_STYLE, unsafe_allow_html=True)

# --- Header (Logo and Title - Adopted from Apex) ---
# Use the markdown structure from the reference code
st.markdown(
    f"""
    <div class="header-container">
        {logo_html}
        <h1 class="title">Phronesis Nexus</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Placeholder for solutions data (remains the same) ---
solutions = [
  {
      "name": "Phronesis Pulse 2.0",
      "description": "Use unique Yahoo Finance Tickers to extract company profile and financial details",
      "status": "ACTIVE",
      "version": "2.0",
      "documentation": "[Documentation](http://example.com/doc1)",
      "feedback": "[Feedback](http://example.com/feedback1)",
      "link": "http://192.168.4.126:9001",
      "image": "icons/pulse_icon.png"
  },
  {
      "name": "Database Search Engine",
      "description": "Company database interactive front-end",
      "status": "ACTIVE",
      "version": "Beta",
      "documentation": "[Documentation](http://example.com/doc2)",
      "feedback": "[Feedback](http://example.com/feedback2)",
      "link": "http://192.168.4.126:9002",
      "image": "icons/explore_icon.png"
  },
  {
      "name": "UID Generator",
      "description": "Generate unique IDs for Companies",
      "status": "ACTIVE",
      "version": "Beta",
      "documentation": "[Documentation](http://example.com/doc4)",
      "feedback": "[Feedback](http://example.com/feedback4)",
      "link": "http://192.168.4.126:9003",
      "image": "icons/uid_icon.png"
  },
  {
      "name": "IP: Geospatial Data Extraction",
      "description": "Bulk Extraction and Dashboard of IP addresses",
      "status": "ACTIVE",
      "version": "Alpha",
      "documentation": "[Documentation](http://example.com/doc4)",
      "feedback": "[Feedback](http://example.com/feedback4)",
      "link": "http://192.168.4.126:9004",
      "image": "icons/ip_icon.png"
  },
  {
      "name": "Database Updater",
      "description": "Company database updates",
      "status": "COMING SOON!",
      "version": "Pre-Beta",
      "documentation": "[Documentation](http://example.com/doc3)",
      "feedback": "[Feedback](http://example.com/feedback3)",
      "link": "http://192.168.4.126:9005",
      "image": "icons/comingsoon.png"
  }
]

# --- Function to generate HTML for an App Card (Using 'Active' only as before) ---
def generate_app_card_html(solution):
    """Generates the HTML string for a single solution card with status indicator (ALWAYS ACTIVE)."""
    status_class = "active"
    status_text = "Active"
    status_indicator_html = f'<span class="card-status {status_class}">{status_text}</span>'

    card_html = f"""
    <a href="{solution.get('link', '#')}" target="_blank" class="app-card-link" title="{solution.get('description', 'No description')}">
        <div class="app-card">
            {status_indicator_html}
            <h2 class="card-title">{solution.get('name', 'Unnamed Solution')}</h2>
            <p class="card-description">
                {solution.get('description', 'No description provided.')}<br>
                <strong>Version:</strong> {solution.get('version', 'N/A')}
            </p>
            <span class="card-arrow">→</span>
        </div>
    </a>
    """
    return card_html

# --- feedback_form function (remains the same) ---
def feedback_form():
  """Renders the feedback form elements within a pre-styled container."""
  user_name = st.text_input("Your Name", key="user_name")
  solution_names = [solution['name'] for solution in solutions]
  selected_solution = st.selectbox("Select Solution", solution_names, key="selected_solution")
  feedback_category = st.selectbox("Feedback Category", ["Status Inactive", "Urgent Fix", "New features request", "General feedback"], key="feedback_category")
  feedback = st.text_area("Your Feedback", height=150, key="feedback")
  if st.button("Submit Feedback", type="primary"):
      if not user_name or not feedback:
          st.warning("Please fill in all fields.")
          return

      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      feedback_data = {
          "Name": user_name,
          "Time": current_time,
          "Category": feedback_category,
          "Feedback": feedback
      }
      df = pd.DataFrame([feedback_data])
      file_path = 'feedback.xlsx'
      try:
          try:
              # Try reading the specific sheet
              existing_data = pd.read_excel(file_path, sheet_name=selected_solution)
              new_data = pd.concat([existing_data, df], ignore_index=True)
          except FileNotFoundError:
              # If file doesn't exist, create a new DataFrame
              new_data = df
              # Ensure excel writer starts in write ('w') mode if file is new
              write_mode = 'w'
          except ValueError: # Handles case where sheet doesn't exist in an existing file
              new_data = df
              write_mode = 'a' # Append mode if file exists but sheet doesn't
          else:
              # If sheet was read successfully, use append mode
              write_mode = 'a'

          # Use ExcelWriter for more control over sheet writing/overwriting
          # if_sheet_exists='replace' will overwrite the sheet if it exists, 'overlay' might be safer but complex
          with pd.ExcelWriter(file_path, mode=write_mode, engine='openpyxl', if_sheet_exists='replace') as writer:
              new_data.to_excel(writer, sheet_name=selected_solution, index=False)
              # If opening in 'w' mode, ensure other sheets aren't lost (this requires reading all sheets first)
              # Simpler approach for now: 'replace' assumes you manage sheets individually

          st.success(f"Thank you for your feedback on {selected_solution}!")

      except PermissionError:
          st.error(f"Permission denied: Could not write to {file_path}. Ensure the file is not open elsewhere and the application has write permissions.")
      except Exception as e:
          st.error(f"An error occurred saving feedback: {e}")


# --- Main App Layout (Simplified Top Section) ---

# --- REMOVED Welcome Section ---
# st.markdown("<h2>Welcome to Phronesis Automation & AI Lab</h2>", unsafe_allow_html=True)
# st.markdown("This is the central hub...", unsafe_allow_html=True)
# st.markdown("<blockquote>Efficiency is doing things right...</blockquote>", unsafe_allow_html=True)


# --- REMOVED Available Solutions Header ---
# st.markdown("<h2>Available Solutions</h2>", unsafe_allow_html=True)

# --- Steve Jobs Quote (Kept) ---
# Using the specific class 'jobs-quote' for styling defined in CSS
st.markdown("<h3 class='jobs-quote'>\"You cannot mandate productivity, you must provide the tools to let people become their best.\" <br>— Steve Jobs</h3>", unsafe_allow_html=True)

# --- Display Solutions Cards ---
num_columns = 2
cols = st.columns(num_columns, gap="large") # Add gap like Apex example

for index, solution in enumerate(solutions):
    card_html = generate_app_card_html(solution)
    with cols[index % num_columns]:
        st.markdown(card_html, unsafe_allow_html=True)


# --- Feedback Section (remains the same) ---
with st.expander("Click to expand Feedback Form", expanded=False):
    st.markdown('<div class="theme-container">', unsafe_allow_html=True)
    st.markdown("<h3>Feedback Form</h3>", unsafe_allow_html=True) # Title inside container
    feedback_form()
    st.markdown('</div>', unsafe_allow_html=True)


# --- Footer (Adopted from Apex) ---
st.markdown(
    f"""
    <div class="footer">
        <p>© 2025 Phronesis Partners. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)

