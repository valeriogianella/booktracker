"""
Simple test script to verify Booktrack core functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from booktrack.database import DatabaseManager
from booktrack.timer import Timer
import tempfile
import time

def test_database():
    """Test database functionality."""
    print("🗄️  Testing Database Operations...")
    
    # Create temporary database
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
        
        # Clear database reference
        db = None
        
    finally:
        # Clean up
        try:
            os.unlink(tmp_path)
        except:
            pass  # Ignore cleanup errors
    
    print("✅ All database tests passed!\n")

def test_timer():
    """Test timer functionality."""
    print("⏱️  Testing Timer Operations...")
    
    timer = Timer()
    
    # Test initial state
    assert timer.get_elapsed_time() == 0.0
    assert not timer.is_running
    print("✅ Timer initial state correct")
    
    # Test start/stop
    timer.start()
    assert timer.is_running
    time.sleep(0.1)  # Wait a bit
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
    time.sleep(0.05)  # Wait while paused
    assert timer.get_elapsed_time() == paused_time  # Should not change
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

def main():
    """Run all tests."""
    print("🎯 Testing Booktrack Core Functionality")
    print("=" * 50)
    
    try:
        test_database()
        test_timer()
        
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        print("✅ The Booktrack application is working correctly!")
        print("🚀 You can now run the GUI with: python -m booktrack")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
