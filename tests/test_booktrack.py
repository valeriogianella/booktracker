"""
Tests for the Booktrack application
"""

import unittest
import tempfile
import os
import json
from datetime import datetime

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
        os.unlink(self.temp_db.name)
    
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


if __name__ == '__main__':
    unittest.main()
