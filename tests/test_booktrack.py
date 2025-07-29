"""
Tests for the Booktrack application
"""

from decimal import Decimal
import unittest
import tempfile
import os
import json
import sys
from datetime import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from booktrack.database import DatabaseManager
from booktrack.timer import Timer


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        # Ensure database connection is closed
        self.db_manager = None
        # Give Windows time to release the file handle
        import time
        time.sleep(0.1)
        try:
            os.unlink(self.temp_db.name)
        except (OSError, PermissionError):
            # On Windows, sometimes the file is still locked
            import gc
            gc.collect()
            time.sleep(0.2)
            try:
                os.unlink(self.temp_db.name)
            except (OSError, PermissionError):
                pass  # Ignore if we can't delete (Windows file locking)
    
    def test_add_book(self):
        """Test adding a book."""
        book_id = self.db_manager.add_book(
            title="Test Book",
            author="Test Author",
            total_pages=300
        )
        self.assertIsInstance(book_id, int)
        self.assertGreater(book_id, 0)
    
    def test_get_books(self):
        """Test retrieving books."""
        # Add test books
        book_id1 = self.db_manager.add_book("Book 1", "Author 1")
        book_id2 = self.db_manager.add_book("Book 2", "Author 2")
        
        # Get all books
        books = self.db_manager.get_books()
        self.assertEqual(len(books), 2)
        
        # Get active books
        active_books = self.db_manager.get_books(status='Active')
        self.assertEqual(len(active_books), 2)
    
    def test_update_book(self):
        """Test updating a book."""
        book_id = self.db_manager.add_book("Original Title", "Original Author")
        
        # Update book
        success = self.db_manager.update_book(
            book_id,
            title="Updated Title",
            status="Read"
        )
        self.assertTrue(success)
        
        # Verify update
        book = self.db_manager.get_book(book_id)
        self.assertEqual(book['title'], "Updated Title")
        self.assertEqual(book['status'], "Read")
    
    def test_delete_book(self):
        """Test deleting a book."""
        book_id = self.db_manager.add_book("To Delete", "Author")
        
        # Add a reading session
        session_id = self.db_manager.add_reading_session(book_id, 1800)
        
        # Delete book
        success = self.db_manager.delete_book(book_id)
        self.assertTrue(success)
        
        # Verify book is deleted
        book = self.db_manager.get_book(book_id)
        self.assertIsNone(book)
        
        # Verify sessions are deleted
        sessions = self.db_manager.get_reading_sessions(book_id)
        self.assertEqual(len(sessions), 0)
    
    def test_add_reading_session(self):
        """Test adding a reading session."""
        book_id = self.db_manager.add_book("Test Book", "Test Author")
        
        session_id = self.db_manager.add_reading_session(
            book_id=book_id,
            duration_seconds=1800,
            pages_read=25,
            notes="Good reading session"
        )
        
        self.assertIsInstance(session_id, int)
        self.assertGreater(session_id, 0)
    
    def test_get_reading_sessions(self):
        """Test retrieving reading sessions."""
        book_id = self.db_manager.add_book("Test Book", "Test Author")
        
        # Add sessions
        session_id1 = self.db_manager.add_reading_session(book_id, 1800)
        session_id2 = self.db_manager.add_reading_session(book_id, 2400)
        
        # Get sessions for book
        sessions = self.db_manager.get_reading_sessions(book_id)
        self.assertEqual(len(sessions), 2)
        
        # Get all sessions
        all_sessions = self.db_manager.get_reading_sessions()
        self.assertEqual(len(all_sessions), 2)
    
    def test_get_statistics(self):
        """Test getting statistics."""
        book_id = self.db_manager.add_book("Test Book", "Test Author")
        self.db_manager.add_reading_session(book_id, 1800)
        self.db_manager.add_reading_session(book_id, 2400)
        
        stats = self.db_manager.get_statistics()
        
        self.assertEqual(stats['total_reading_time_seconds'], 4200)
        self.assertEqual(stats['total_sessions'], 2)
        self.assertEqual(stats['total_books'], 1)
        self.assertIn('Active', stats['books_by_status'])
        self.assertEqual(stats['books_by_status']['Active'], 1)
    
    def test_export_data(self):
        """Test data export."""
        book_id = self.db_manager.add_book("Test Book", "Test Author")
        self.db_manager.add_reading_session(book_id, 1800)
        
        export_data = self.db_manager.export_data()
        
        self.assertIn('books', export_data)
        self.assertIn('reading_sessions', export_data)
        self.assertIn('statistics', export_data)
        self.assertIn('export_date', export_data)
        
        self.assertEqual(len(export_data['books']), 1)
        self.assertEqual(len(export_data['reading_sessions']), 1)


class TestTimer(unittest.TestCase):
    """Test cases for Timer."""
    
    def setUp(self):
        """Set up timer for testing."""
        self.timer = Timer()
    
    def test_timer_start_stop(self):
        """Test basic timer start and stop."""
        self.assertFalse(self.timer.is_running)
        self.assertEqual(self.timer.get_elapsed_time(), 0.0)
        
        self.timer.start()
        self.assertTrue(self.timer.is_running)
        
        # Wait a bit
        import time
        time.sleep(0.1)
        
        elapsed = self.timer.stop()
        self.assertFalse(self.timer.is_running)
        self.assertGreater(elapsed, 0.0)
        self.assertLess(elapsed, 1.0)  # Should be less than a second
    
    def test_timer_pause_resume(self):
        """Test timer pause and resume."""
        self.timer.start()
        
        import time
        time.sleep(0.1)
        
        self.timer.pause()
        paused_time = self.timer.get_elapsed_time()
        self.assertFalse(self.timer.is_running)
        
        # Wait while paused
        time.sleep(0.1)
        
        # Time should not have increased
        self.assertEqual(self.timer.get_elapsed_time(), paused_time)
        
        # Resume
        self.timer.resume()
        self.assertTrue(self.timer.is_running)
        
        time.sleep(0.1)
        
        final_time = self.timer.stop()
        self.assertGreater(final_time, paused_time)
    
    def test_timer_reset(self):
        """Test timer reset."""
        self.timer.start()
        
        import time
        time.sleep(0.1)
        
        self.timer.reset()
        self.assertFalse(self.timer.is_running)
        self.assertEqual(self.timer.get_elapsed_time(), 0.0)
    
    def test_format_time(self):
        """Test time formatting."""
        # Test various time formats
        self.assertEqual(self.timer.format_time(0), "00:00:00")
        self.assertEqual(self.timer.format_time(61), "00:01:01")
        self.assertEqual(self.timer.format_time(3661), "01:01:01")
        self.assertEqual(self.timer.format_time(7323), "02:02:03")


class TestDecimalHandling(unittest.TestCase):
    """Test cases for Decimal value handling."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        # Ensure database connection is closed
        self.db_manager = None
        # Give Windows time to release the file handle
        import time
        time.sleep(0.1)
        try:
            os.unlink(self.temp_db.name)
        except (OSError, PermissionError):
            # On Windows, sometimes the file is still locked
            import gc
            gc.collect()
            time.sleep(0.2)
            try:
                os.unlink(self.temp_db.name)
            except (OSError, PermissionError):
                pass  # Ignore if we can't delete (Windows file locking)
    
    def test_decimal_book_pages(self):
        """Test that Decimal total_pages values are properly converted."""
        # Test adding a book with Decimal total_pages
        book_id = self.db_manager.add_book(
            title="Test Book", 
            author="Test Author", 
            total_pages=Decimal('200')  # This was causing the error
        )
        self.assertIsInstance(book_id, int)
        
        # Test getting the book back
        book = self.db_manager.get_book(book_id)
        self.assertEqual(book['total_pages'], 200)  # Should be converted to int
        self.assertIsInstance(book['total_pages'], int)
    
    def test_decimal_session_pages(self):
        """Test that Decimal pages_read values are properly converted."""
        book_id = self.db_manager.add_book("Test Book", "Test Author", 300)
        
        # Test adding reading session with Decimal pages_read
        session_id = self.db_manager.add_reading_session(
            book_id=book_id,
            duration_seconds=1800,
            pages_read=Decimal('25'),  # This was also causing issues
            notes="Test session"
        )
        self.assertIsInstance(session_id, int)
        
        # Verify the session
        sessions = self.db_manager.get_reading_sessions(book_id)
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]['pages_read'], 25)
        self.assertIsInstance(sessions[0]['pages_read'], int)
    
    def test_decimal_book_update(self):
        """Test updating book with Decimal values."""
        book_id = self.db_manager.add_book("Test Book", "Test Author", 200)
        
        # Test updating book with Decimal
        success = self.db_manager.update_book(
            book_id, 
            total_pages=Decimal('250')  # Update with Decimal
        )
        self.assertTrue(success)
        
        # Verify the update
        updated_book = self.db_manager.get_book(book_id)
        self.assertEqual(updated_book['total_pages'], 250)
        self.assertIsInstance(updated_book['total_pages'], int)
    
    def test_none_and_empty_values(self):
        """Test handling of None and empty string values."""
        # Test with None pages
        book_id1 = self.db_manager.add_book("Book 1", "Author 1", None)
        book1 = self.db_manager.get_book(book_id1)
        self.assertIsNone(book1['total_pages'])
        
        # Test with empty string pages
        book_id2 = self.db_manager.add_book("Book 2", "Author 2", "")
        book2 = self.db_manager.get_book(book_id2)
        self.assertIsNone(book2['total_pages'])


class TestIntegration(unittest.TestCase):
    """Integration tests combining database and timer functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.timer = Timer()
    
    def tearDown(self):
        """Clean up test environment."""
        # Ensure database connection is closed
        self.db_manager = None
        self.timer = None
        # Give Windows time to release the file handle
        import time
        time.sleep(0.1)
        try:
            os.unlink(self.temp_db.name)
        except (OSError, PermissionError):
            # On Windows, sometimes the file is still locked
            import gc
            gc.collect()
            time.sleep(0.2)
            try:
                os.unlink(self.temp_db.name)
            except (OSError, PermissionError):
                pass  # Ignore if we can't delete (Windows file locking)
    
    def test_complete_reading_workflow(self):
        """Test a complete reading session workflow."""
        # Add a book
        book_id = self.db_manager.add_book(
            title="Integration Test Book", 
            author="Test Author", 
            total_pages=200
        )
        
        # Start timer
        self.timer.start()
        self.assertTrue(self.timer.is_running)
        
        # Simulate reading time
        import time
        time.sleep(0.1)
        
        # Stop timer and get duration
        duration = self.timer.stop()
        self.assertGreater(duration, 0)
        
        # Record reading session
        session_id = self.db_manager.add_reading_session(
            book_id=book_id,
            duration_seconds=int(duration * 60),  # Convert to minutes for realistic value
            pages_read=25,
            notes="Integration test session"
        )
        
        # Verify session was recorded
        sessions = self.db_manager.get_reading_sessions(book_id)
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]['book_title'], "Integration Test Book")
        self.assertEqual(sessions[0]['pages_read'], 25)
        
        # Check statistics
        stats = self.db_manager.get_statistics()
        self.assertEqual(stats['total_sessions'], 1)
        self.assertEqual(stats['total_books'], 1)
        self.assertGreater(stats['total_reading_time_seconds'], 0)
    
    def test_data_export_integration(self):
        """Test complete data export functionality."""
        # Add books and sessions
        book_id1 = self.db_manager.add_book("Book 1", "Author 1", 200)
        book_id2 = self.db_manager.add_book("Book 2", "Author 2", 300)
        
        self.db_manager.add_reading_session(book_id1, 1800, 25, "Session 1")
        self.db_manager.add_reading_session(book_id2, 2400, 30, "Session 2")
        
        # Export data
        export_data = self.db_manager.export_data()
        
        # Verify export structure
        self.assertIn('export_date', export_data)
        self.assertIn('books', export_data)
        self.assertIn('reading_sessions', export_data)
        self.assertIn('statistics', export_data)
        
        # Verify export content
        self.assertEqual(len(export_data['books']), 2)
        self.assertEqual(len(export_data['reading_sessions']), 2)
        self.assertEqual(export_data['statistics']['total_books'], 2)
        self.assertEqual(export_data['statistics']['total_sessions'], 2)
        self.assertEqual(export_data['statistics']['total_reading_time_seconds'], 4200)
        
        # Verify export can be serialized to JSON
        try:
            json.dumps(export_data)
        except (TypeError, ValueError):
            self.fail("Export data is not JSON serializable")


def run_standalone_tests():
    """Run standalone tests similar to test_core.py functionality."""
    print("🎯 Running Standalone Booktrack Tests")
    print("=" * 50)
    
    # Test database operations
    print("🗄️  Testing Database Operations...")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_path = tmp.name
    
    try:
        db = DatabaseManager(tmp_path)
        
        # Test adding a book
        book_id = db.add_book(
            title="Test Book", 
            author="Test Author", 
            total_pages=200
        )
        print(f"✅ Added book with ID: {book_id}")
        
        # Test getting books
        books = db.get_books()
        assert len(books) == 1
        assert books[0]['title'] == "Test Book"
        print(f"✅ Retrieved {len(books)} book(s)")
        
        # Test adding reading session
        session_id = db.add_reading_session(
            book_id=book_id,
            duration_seconds=1800,
            pages_read=25,
            notes="Great reading session!"
        )
        print(f"✅ Added reading session with ID: {session_id}")
        
        # Test getting statistics
        stats = db.get_statistics()
        assert stats['total_reading_time_seconds'] == 1800
        assert stats['total_sessions'] == 1
        print(f"✅ Statistics: {stats['total_reading_time_seconds']} seconds total")
        
        # Test updating book
        success = db.update_book(book_id, status='Read')
        assert success
        print("✅ Updated book status")
        
        # Test data export
        export_data = db.export_data()
        assert len(export_data['books']) == 1
        assert len(export_data['reading_sessions']) == 1
        print("✅ Data export successful")
        
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass
    
    print("✅ All database tests passed!\n")
    
    # Test timer operations
    print("⏱️  Testing Timer Operations...")
    
    timer = Timer()
    
    # Test initial state
    assert timer.get_elapsed_time() == 0.0
    assert not timer.is_running
    print("✅ Timer initial state correct")
    
    # Test start/stop
    timer.start()
    assert timer.is_running
    import time
    time.sleep(0.1)
    elapsed = timer.stop()
    assert elapsed > 0
    assert not timer.is_running
    print(f"✅ Timer start/stop works: {timer.format_time(elapsed)}")
    
    # Test pause/resume
    timer.reset()
    timer.start()
    time.sleep(0.05)
    timer.pause()
    paused_time = timer.get_elapsed_time()
    time.sleep(0.05)
    assert timer.get_elapsed_time() == paused_time
    timer.resume()
    time.sleep(0.05)
    final_time = timer.stop()
    assert final_time > paused_time
    print("✅ Timer pause/resume works")
    
    # Test time formatting
    assert timer.format_time(0) == "00:00:00"
    assert timer.format_time(61) == "00:01:01"
    assert timer.format_time(3661) == "01:01:01"
    print("✅ Time formatting works")
    
    print("✅ All timer tests passed!\n")
    
    print("🎉 ALL STANDALONE TESTS PASSED!")
    print("=" * 50)
    print("✅ The Booktrack application is working correctly!")
    print("🚀 You can now run the GUI with: python -m booktrack")


def main():
    """Main function to run tests."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--standalone':
        # Run standalone tests like test_core.py
        try:
            run_standalone_tests()
            return 0
        except Exception as e:
            print(f"❌ Standalone test failed: {e}")
            return 1
    else:
        # Run unittest suite
        unittest.main()

if __name__ == '__main__':
    main()
