# Movie Rating and Review App

This Flask web application allows users to rate, review, and manage their favorite movies. Users can also add new movies, which are automatically fetched from The Movie Database (TMDb) using their API.

## Prerequisites

- Python 3.x
- Flask
- Flask Bootstrap5
- Flask SQLAlchemy
- Flask WTF
- Selenium
- BeautifulSoup
- ChromeDriver
- TMDb API Key (Get one [here](https://www.themoviedb.org/documentation/api))

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/isotronic/top-10-movies-website.git
   ```

2. Navigate to the project directory:
   ```bash
   cd top-10-movies-website
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Set the following environment variables:
   - `API_KEY`: Your TMDb API Key.
   - `API_READ_ACCESS_TOKEN`: TMDb API Read Access Token.

2. Adjust other parameters in the script as needed.

## Usage

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000` to access the application.

3. Rate, review, edit, and delete movies. You can also add new movies by searching and selecting from TMDb.

## Notes

- The application uses SQLite as the database, and a new database file (`top-10-movies.db`) will be created in the project directory.

- ChromeDriver is used for browser automation during movie data retrieval.

- The application runs in debug mode by default. Update the script (`app.py`) to change this behavior for production use.

## Acknowledgments

- This project utilizes Flask for web development, Flask SQLAlchemy for database management, Flask WTF for forms, and Flask Bootstrap5 for styling.

- Selenium and BeautifulSoup are used for web scraping during the movie data retrieval process.
