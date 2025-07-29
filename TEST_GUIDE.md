# BookTrack Automated Testing Guide

> **Note**: This guide covers automated unit tests. For manual testing scenarios and setup instructions, see [TESTING.md](TESTING.md).

## Unified Test Structure

All automated tests have been consolidated into `tests/test_booktrack.py`, replacing the previous separate `test_core.py` file.

## Test Classes

### 1. TestDatabaseManager
- `test_add_book()` - Test adding books to the database
- `test_get_books()` - Test retrieving books with optional filtering
- `test_update_book()` - Test updating book information
- `test_delete_book()` - Test deleting books and cascade deletion of sessions
- `test_add_reading_session()` - Test adding reading sessions
- `test_get_reading_sessions()` - Test retrieving reading sessions
- `test_get_statistics()` - Test statistics calculation
- `test_export_data()` - Test data export functionality

### 2. TestTimer
- `test_timer_start_stop()` - Test basic timer operations
- `test_timer_pause_resume()` - Test pause/resume functionality
- `test_timer_reset()` - Test timer reset
- `test_format_time()` - Test time formatting utilities

### 3. TestDecimalHandling
- `test_decimal_book_pages()` - Test Decimal to int conversion for book pages
- `test_decimal_session_pages()` - Test Decimal to int conversion for session pages
- `test_decimal_book_update()` - Test Decimal handling in book updates
- `test_none_and_empty_values()` - Test handling of None/empty values

### 4. TestIntegration
- `test_complete_reading_workflow()` - End-to-end reading session workflow
- `test_data_export_integration()` - Complete data export test

## Running Tests

### Option 1: Standalone Tests (Recommended)
```bash
# Run user-friendly standalone tests (like the old test_core.py)
cd booktrack
python tests/test_booktrack.py --standalone
```

### Option 2: Full Unittest Suite
```bash
# Run all unittest tests with detailed output
cd booktrack
python -m unittest tests.test_booktrack -v

# Run specific test class
python -m unittest tests.test_booktrack.TestTimer -v

# Run all tests
python -m unittest discover tests -v
```

### Option 3: Test Runner Script
```bash
# Run standalone tests (default)
python run_tests.py

# Run unittest suite
python run_tests.py --unittest
```

## Test Features

- **Temporary Databases**: Each test uses isolated temporary SQLite databases
- **Windows Compatibility**: Proper file cleanup handling for Windows file locking
- **Decimal Handling**: Comprehensive testing of Decimal type conversion
- **Integration Testing**: Combined database and timer functionality tests
- **Export Validation**: JSON serialization testing for data export

## Files Involved

- `tests/test_booktrack.py` - Main unified test file
- `run_tests.py` - Test runner script
- `test_core.py` - Legacy file (now redirects to unified tests)

## Key Benefits

1. **Unified Structure**: All tests in one location
2. **Multiple Run Modes**: Standalone and unittest modes
3. **Comprehensive Coverage**: Database, timer, integration, and edge cases
4. **Windows Compatible**: Proper cleanup for Windows file system
5. **Easy to Extend**: Clear structure for adding new tests

## Example Output

```
🎯 Running Standalone Booktrack Tests
==================================================
🗄️  Testing Database Operations...
✅ Added book with ID: 1
✅ Retrieved 1 book(s)
✅ Added reading session with ID: 1
✅ Statistics: 1800 seconds total
✅ Updated book status
✅ Data export successful
✅ All database tests passed!

⏱️  Testing Timer Operations...
✅ Timer initial state correct
✅ Timer start/stop works: 00:00:00
✅ Timer pause/resume works
✅ Time formatting works
✅ All timer tests passed!

🎉 ALL STANDALONE TESTS PASSED!
==================================================
✅ The Booktrack application is working correctly!
🚀 You can now run the GUI with: python -m booktrack
```
