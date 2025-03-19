import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style



ascii_art = f"""{Fore.RED} █████  ██     ██     ██ ███████ ██████      ███████  ██████ ██████   █████  ██████  ███████ ██████  
██   ██ ██     ██     ██ ██      ██   ██     ██      ██      ██   ██ ██   ██ ██   ██ ██      ██   ██ 
███████ ██     ██  █  ██ █████   ██████      ███████ ██      ██████  ███████ ██████  █████   ██████  
██   ██ ██     ██ ███ ██ ██      ██   ██          ██ ██      ██   ██ ██   ██ ██      ██      ██   ██ 
██   ██ ██      ███ ███  ███████ ██████      ███████  ██████ ██   ██ ██   ██ ██      ███████ ██   ██ 
                                                                                                     {Fore.CYAN}Created by {Fore.GREEN}3L173 H4CK3R 1337{Style.RESET_ALL}
"""

print(ascii_art)


# Set page config
st.set_page_config(page_title="AI Web Scraper", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    .big-title {
        font-size: 40px !important;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .sidebar-title {
        font-size: 22px !important;
        font-weight: bold;
        color: #ffffff;
    }
    .data-box {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# UI Header
st.markdown('<p class="big-title">🔍 AI Web Scraper - Contact Extractor</p>', unsafe_allow_html=True)
st.write("Extract **Emails, Phone Numbers, Names, and Links** from any website.")

# Sidebar for URL input
st.sidebar.markdown('<p class="sidebar-title">🌐 Enter Website URL</p>', unsafe_allow_html=True)
url = st.sidebar.text_input("", placeholder="https://example.com")

# Function to scrape website content
def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"❌ Error fetching website: {e}")
        return None

# Function to extract emails
def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(email_pattern, text)))

# Function to extract phone numbers
def extract_phone_numbers(text):
    phone_pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
    return list(set(re.findall(phone_pattern, text)))

# Function to extract names (basic heuristic)
def extract_names(text):
    name_pattern = r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"  # Matches capitalized first & last names
    return list(set(re.findall(name_pattern, text)))

# Function to extract links
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        links.append(full_url)
    return list(set(links))

# Scraping process
if st.sidebar.button("🚀 Start Scraping"):
    if url.strip():
        st.info("🔍 Scraping the website... Please wait.")
        html_content = scrape_website(url)

        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            text_content = soup.get_text(separator=" ")

            # Extracting information
            emails = extract_emails(text_content)
            phone_numbers = extract_phone_numbers(text_content)
            names = extract_names(text_content)
            links = extract_links(html_content, url)

            # Display Results using tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📧 Emails", "📞 Phone Numbers", "🆔 Names", "🔗 Links"])

            with tab1:
                st.subheader("📧 Extracted Emails")
                if emails:
                    for email in emails:
                        st.code(email, language="text")
                else:
                    st.warning("No emails found.")

            with tab2:
                st.subheader("📞 Extracted Phone Numbers")
                if phone_numbers:
                    for phone in phone_numbers:
                        st.code(phone, language="text")
                else:
                    st.warning("No phone numbers found.")

            with tab3:
                st.subheader("🆔 Extracted Names")
                if names:
                    for name in names:
                        st.code(name, language="text")
                else:
                    st.warning("No names found.")

            with tab4:
                st.subheader("🔗 Extracted Links")
                if links:
                    for link in links:
                        st.markdown(f"🔗 [{link}]({link})", unsafe_allow_html=True)
                else:
                    st.warning("No links found.")
    else:
        st.sidebar.warning("⚠️ Please enter a valid website URL.")
