# Selenium Airlines

## Overview
Selenium Airlines is a Python-based web scraping project designed to collect information from airliners.net. The project uses Selenium to automate the browsing and data extraction process, integrating proxy support and anti-detection measures to avoid being blocked.

## *Problem  :
chat client from fiverr.com
https://drive.google.com/file/d/16X1KPmPwuoJiNMJIxYpb3l3DlZsZkFRL/view?usp=sharing

## *Solution  :
Airliners.net have a good antibot feature and  I cannot scrape with beautiful soap and scrapy framework, so I try to scrap it with selenium with Proxy Support and Anti-Detection Measures.
## Features
- **Proxy Support**: Configure and use proxies to avoid IP bans.
- **Anti-Detection Measures**: Randomize user agents, simulate human-like interactions, and use headless browsing.
- **Data Extraction**: Scrape airline information, aircraft details, and image URLs from airliners.net.
- **CSV Export**: Save the scraped data into a CSV file for further analysis.

## Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/rjrizani/selenium_airlanes.git
    cd selenium_airlanes
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory with the following content:
      ```plaintext
      PROXY_HOST_=your_proxy_host
      PROXY_PORT_=your_proxy_port
      PROXY_USER_=your_proxy_user
      PROXY_PASS_=your_proxy_password
      ```

## Usage
1. **Run the scraper**:
    ```bash
    python main.py
    ```

2. **Check the output**:
    - The scraped data will be saved in a CSV file with a name like `scraped_data_YYYYMMDD.csv`.

## Functions
- **create_proxy_auth_extension**: Creates a Chrome extension for proxy authentication.
- **get_driver**: Configures and returns a Chrome WebDriver with anti-detection measures.
- **human_like_interaction**: Simulates human-like behavior by randomizing mouse movements and scrolling.
- **scrape_page**: Navigates to a given URL, interacts with the page, and extracts information.
- **save_to_csv**: Saves scraped data to a CSV file.

## Contributing
Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

## Acknowledgments
- Special thanks to the maintainers of Selenium and airliners.net for providing the tools and data used in this project.
