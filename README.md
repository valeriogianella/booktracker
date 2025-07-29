# Booktrack

A reading time tracking application built with Python and the BeeWare framework.

## Features

- **Book Management**: Add, edit, and delete books in your personal library
- **Reading Session Timer**: Time your reading sessions with start/stop functionality
- **Reading Statistics**: View your reading progress and statistics
- **Data Export**: Export all your data to JSON format
- **Local Storage**: All data is stored locally in a SQLite database

## Requirements

- Python 3.8 or higher
- BeeWare/Toga framework
- SQLite (included with Python)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install briefcase toga
```

## Development Setup

1. Navigate to the project directory:
```bash
cd booktrack
```

2. Install in development mode:
```bash
pip install -e .
```

## Running the Application

### Development Mode

```bash
python -m booktrack
```

### Building for Android

1. Create the Android project:
```bash
briefcase create android
```

2. Build the APK:
```bash
briefcase build android
```

3. Package the APK:
```bash
briefcase package android
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python -m unittest tests.test_booktrack
```

## Project Structure

```
booktrack/
├── src/
│   └── booktrack/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py           # Main application
│       ├── database.py      # Database management
│       ├── timer.py         # Timer functionality
│       └── widgets.py       # UI widgets and forms
├── tests/
│   └── test_booktrack.py    # Test suite
├── pyproject.toml           # Project configuration
└── README.md
```

## Usage

### Adding Books

1. Click "Add Book" in the navigation bar
2. Fill in the book title and author (required)
3. Optionally add total pages and cover image URL
4. Click "Add Book" to save

### Starting a Reading Session

1. Find an "Active" book in your library
2. Click "Start Reading" next to the book
3. The timer will start automatically
4. Use "Pause" and "Resume" as needed
5. Click "Stop & Save" when finished
6. Log pages read and notes (optional)
7. Click "Save Session" to record the session

### Viewing Statistics

Click "Statistics" in the navigation bar to view:
- Total reading time
- Number of reading sessions
- Books by status
- Daily reading history

### Exporting Data

Click "Export Data" to save all your books, reading sessions, and statistics to a JSON file in your home directory.

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request
