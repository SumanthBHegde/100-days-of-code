# Weather CLI Application

This is a Python-based command-line application to fetch weather data using the OpenWeatherMap API and store the results in a local SQLite database. The app also provides the ability to view, update, and delete weather information from the database.

## Requirements

1. Python 3.x
2. Virtual Environment (`venv`)
3. API Key from OpenWeatherMap

## Setup

1. Clone the repository or download the project files.

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Obtain an API Key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).

6. Set your OpenWeatherMap API key as an environment variable:

   - On Windows:
     ```bash
     set OPENWEATHER_API_KEY=your_api_key_here
     ```
   - On Mac/Linux:
     ```bash
     export OPENWEATHER_API_KEY=your_api_key_here
     ```

## Usage

The application allows you to fetch weather data and store it in a local SQLite database, as well as view, update, and delete stored data.

### Fetch Weather Data

You can fetch weather data for a specific city using the following command:

```bash
python weather_cli.py fetch --city <city_name>
```

For example:

```bash
python weather_cli.py fetch --city Sirsi
```

### View Weather Data

To view weather data stored in the database, use the following command:

```bash
python weather_cli.py view --city <city_name>
```

For example:

```bash
python weather_cli.py view --city Sirsi
```

### Update Weather Data

To update the weather data for a specific city, use the following command:

```bash
python weather_cli.py update --city <city_name>
```

This will fetch the latest weather data for the specified city and update the record in the database.

### Delete Weather Data

To delete weather data for a specific city from the database, use the following command:

```bash
python weather_cli.py delete --city <city_name>
```

For example:

```bash
python weather_cli.py delete --city Sirsi
```

### Display Available Commands

To see the available commands and options, run:

```bash
python weather_cli.py --help
```

## File Structure

- `weather_cli.py`: Main file containing the weather CLI application logic.
- `requirements.txt`: File listing the dependencies for the project.
- `README.md`: Documentation for the project.
- `weather.db`: SQLite database file where the weather data is stored (automatically created on the first run).

## Features

- Fetch weather data using OpenWeatherMap API.
- Store weather data in a local SQLite database.
- View, update, and delete stored weather data.

## License

This project is licensed under the MIT License.
