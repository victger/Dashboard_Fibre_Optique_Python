# Fiber Access Dashboard in Metropolitan France

This project is a web application built using Python, Dash, and Selenium to visualize fiber access data across regions, departments, and municipalities in Metropolitan France. It scrapes and processes data, generates interactive maps and charts, and allows users to explore data via a dashboard.

Thanks to the automated download of the latest documents, users can access up-to-date information on fiber coverage across Metropolitan France. The data is sourced and regularly updated from the official government database site, data-gouv.fr.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Project Components](#project-components)
  - [Data Download and Processing](#data-download-and-processing)
  - [Dashboard Layout](#dashboard-layout)
  - [Selenium Setup](#selenium-setup)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Fiber Access Dashboard provides interactive data visualizations of fiber connectivity across France. Users can:
- View a map showing the proportion of households connected to fiber in different regions, departments, and municipalities.
- Use sliders to select specific time periods and analyze fiber deployment trends.
- Explore detailed graphs on fiber accessibility.

This project combines data scraping with Selenium, data processing with Pandas, and data visualization using Dash.

## Features

- **Interactive Dashboard**: Users can explore fiber access data through maps and line charts.
- **Period Selector**: Slider allows users to choose different time periods for analysis.
- **Automated Data Scraping**: The application uses Selenium to scrape data from online sources.
- **Dockerized Application**: Easy to run with Docker for consistent environments.

## Installation

### Prerequisites

- Python 3.12 or higher
- Docker (optional, for containerized setup)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/fiber-access-dashboard.git
   cd fiber-access-dashboard
   ```

2. **Install dependencies**:
   Create a virtual environment and install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

   The app will run locally at `http://127.0.0.1:8050` within minutes.

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t fiber-dashboard .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8050:8050 fiber-dashboard
   ```

   The app will be available at `http://localhost:8050`.

## Usage

Once the application is running, you can:

1. **View the interactive map**: It shows fiber access by region, department, or municipality.
2. **Use the slider**: Choose a period to explore changes in fiber connectivity.
3. **Analyze charts**: Explore trends with line charts based on processed data.

## File Structure

```bash
fiber-access-dashboard/
│
├── app/
│   ├── app.py           # Dash app setup and execution
│   ├── layout.py        # Layout and interface of the dashboard
│   ├── callbacks.py     # Contains Dash callbacks for interactivity
│   ├── graphs.py        # Helper functions to create graphs
│   ├── map.py           # Creates the map to be displayed in the application
│
├── driver/
│   ├── driver.py        # Instantiates the driver to download latest files
│
├── utils/
│   ├── download_files.py  # Script to download and scrape data
│   ├── utils.py           # Data processing utilities
│
├── Dockerfile           # Docker setup instructions
├── requirements.txt     # Python dependencies
├── main.py              # Main script to run the app
├── driver.py            # Selenium setup for Chrome WebDriver
└── README.md            # This README file
```

## Project Components

### Data Download and Processing

The project starts by downloading the necessary data via `download_files.py` and processing it using `process_data()` from `utils/utils.py`. The processed data is then passed into the Dash app for visualization.

### Dashboard Layout

The layout is built with Dash components in `layout.py`. The main components are:
- A **title** and **description**.
- A **slider** for selecting time periods.
- **Graphs** to visualize the proportion of fiber access.
- An **interactive map** embedded using an HTML iframe.

### Selenium Setup

Selenium is used to automate the scraping process for the latest data. In `driver.py`, a Chrome WebDriver is configured to run headlessly, with optimizations for Docker environments (e.g., `--no-sandbox`, `--disable-dev-shm-usage`).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
