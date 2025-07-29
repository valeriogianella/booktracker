# Booktrack Test Instructions

This document provides comprehensive instructions for testing the Booktrack application.

## Testing Environment Setup

### Prerequisites

1. **Python 3.8+** installed
2. **Git** for cloning the repository
3. **Virtual environment** (recommended)

### Installation Steps

1. **Set up virtual environment:**
```bash
python -m venv booktrack_env
```

2. **Activate virtual environment:**
   - Windows: `booktrack_env\Scripts\activate`
   - Linux/Mac: `source booktrack_env/bin/activate`

3. **Install dependencies:**
```bash
pip install briefcase toga pytest
```

4. **Navigate to project directory:**
```bash
cd booktrack
```

## Running Tests

### 1. Unit Tests

Run the automated test suite:

```bash
python -m pytest tests/ -v
```

Or run specific test modules:

```bash
python -m unittest tests.test_booktrack.TestDatabaseManager
python -m unittest tests.test_booktrack.TestTimer
```

### 2. Application Testing

#### Desktop Testing (Development Mode)

Run the application in development mode:

```bash
python -m booktrack
```

## Manual Testing Scenarios

### Scenario 1: Book Management

**Test Adding a Book:**
1. Launch the application
2. Click "Add Book"
3. Fill in:
   - Title: "The Great Gatsby"
   - Author: "F. Scott Fitzgerald"
   - Total Pages: 180
4. Click "Add Book"
5. Verify the book appears in the Active Books list

**Test Editing a Book:**
1. Find the book you just added
2. Click "Edit"
3. Change the status to "Read"
4. Add a cover image URL (optional)
5. Click "Update"
6. Verify changes are saved

**Test Deleting a Book:**
1. Click "Delete" on a book
2. Confirm the deletion
3. Verify the book is removed from the list

### Scenario 2: Reading Session Timer

**Test Starting a Reading Session:**
1. Ensure you have an "Active" book
2. Click "Start Reading" next to an active book
3. Verify the timer starts (00:00:00 and counting)
4. Let it run for a few seconds

**Test Pause/Resume:**
1. Click "Pause" while timer is running
2. Verify timer stops counting
3. Click "Resume"
4. Verify timer continues from where it left off

**Test Stopping and Saving Session:**
1. Click "Stop & Save"
2. In the session form:
   - Verify reading time is pre-filled
   - Add pages read: 15
   - Add notes: "Great chapter!"
3. Click "Save Session"
4. Verify you're returned to the book list

### Scenario 3: Navigation and Views

**Test Navigation:**
1. Click "Active Books" - should show only active books
2. Click "All Books" - should show all books regardless of status
3. Click "Statistics" - should show reading statistics
4. Verify navigation works smoothly

**Test Statistics View:**
1. Navigate to Statistics
2. Verify display of:
   - Total reading time
   - Total sessions
   - Books by status
   - Daily reading history

### Scenario 4: Data Export

**Test Data Export:**
1. Click "Export Data"
2. Verify export completes successfully
3. Check your home directory for the exported JSON file
4. Open the JSON file and verify it contains:
   - Books data
   - Reading sessions data
   - Statistics
   - Export timestamp

### Scenario 5: Error Handling

**Test Required Field Validation:**
1. Try to add a book without a title
2. Try to add a book without an author
3. Verify appropriate error handling

**Test Timer on Non-Active Books:**
1. Set a book status to "Read" or "Paused"
2. Verify "Start Reading" button is not available
3. Manually try to start a session (should show error)

## Android Testing (Advanced)

### Building for Android

1. **Create Android project:**
```bash
briefcase create android
```

2. **Build the app:**
```bash
briefcase build android
```

3. **Run on device/emulator:**
```bash
briefcase run android
```

### Android-Specific Tests

1. **Installation Test:**
   - Install APK on Android device
   - Verify app launches successfully

2. **Performance Test:**
   - Test app startup time (should be < 2 seconds per SRS)
   - Test database operations (should be < 500ms per SRS)

3. **Data Persistence Test:**
   - Add books and sessions
   - Close and reopen the app
   - Verify data persists

4. **Touch Interface Test:**
   - Test all buttons and navigation
   - Verify timer interface works on touch
   - Test form inputs on mobile keyboard

## Performance Testing

### Database Performance

Run this test script to verify database performance:

```python
import time
from booktrack.database import DatabaseManager

# Test database query performance
db = DatabaseManager(':memory:')

# Add test data
start_time = time.time()
for i in range(100):
    db.add_book(f"Book {i}", f"Author {i}")
end_time = time.time()

print(f"Adding 100 books took: {(end_time - start_time) * 1000:.2f}ms")

# Test query performance
start_time = time.time()
books = db.get_books()
end_time = time.time()

print(f"Querying 100 books took: {(end_time - start_time) * 1000:.2f}ms")
assert (end_time - start_time) < 0.5, "Database query too slow!"
```

## Expected Test Results

### Unit Tests
- All database operations should pass
- Timer functionality should work correctly
- Data export should produce valid JSON

### Manual Tests
- Book management should work smoothly
- Timer should be accurate and responsive
- Navigation should be intuitive
- Data should persist between sessions

### Performance Tests
- App startup: < 2 seconds
- Database queries: < 500ms
- Timer updates: Smooth 1-second intervals

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure all dependencies are installed
   - Check virtual environment is activated

2. **Database Issues:**
   - Check file permissions
   - Verify SQLite is available

3. **UI Issues:**
   - Ensure Toga is properly installed
   - Check for platform-specific requirements

### Debug Mode

Run with debug output:

```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from booktrack.app import main
app = main()
app.main_loop()
"
```

## Test Completion Checklist

- [ ] Unit tests pass
- [ ] Book CRUD operations work
- [ ] Timer functionality works
- [ ] Navigation between views works
- [ ] Statistics display correctly
- [ ] Data export works
- [ ] Performance requirements met
- [ ] Error handling works
- [ ] Android build succeeds (if testing mobile)
- [ ] Data persists between sessions

## Reporting Issues

When reporting issues, include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Error messages (if any)
4. Platform and Python version
5. Test environment details
