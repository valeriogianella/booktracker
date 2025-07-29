"""
Test script to verify Decimal handling is fixed
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from booktrack.database import DatabaseManager
import tempfile
from decimal import Decimal

def test_decimal_handling():
    """Test that Decimal values are properly converted."""
    print("🧪 Testing Decimal Handling Fix...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_path = tmp.name
    
    try:
        db = DatabaseManager(tmp_path)
        
        # Test adding a book with Decimal total_pages
        book_id = db.add_book(
            title="Test Book", 
            author="Test Author", 
            total_pages=Decimal('200')  # This was causing the error
        )
        print(f"✅ Added book with Decimal pages: {book_id}")
        
        # Test getting the book back
        book = db.get_book(book_id)
        print(f"✅ Retrieved book: {book['title']} - {book['total_pages']} pages")
        assert book['total_pages'] == 200  # Should be converted to int
        
        # Test adding reading session with Decimal pages_read
        session_id = db.add_reading_session(
            book_id=book_id,
            duration_seconds=1800,
            pages_read=Decimal('25'),  # This was also causing issues
            notes="Test session"
        )
        print(f"✅ Added session with Decimal pages read: {session_id}")
        
        # Test updating book with Decimal
        success = db.update_book(
            book_id, 
            total_pages=Decimal('250')  # Update with Decimal
        )
        print(f"✅ Updated book with Decimal pages: {success}")
        
        # Verify the update
        updated_book = db.get_book(book_id)
        assert updated_book['total_pages'] == 250
        print(f"✅ Verified update: {updated_book['total_pages']} pages")
        
        # Test with None and empty values
        db.add_book("Book 2", "Author 2", None)  # None pages
        db.add_book("Book 3", "Author 3", "")    # Empty string pages
        print("✅ Handled None and empty values correctly")
        
        print("✅ All Decimal handling tests passed!")
        
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

if __name__ == "__main__":
    test_decimal_handling()
    print("\n🎉 Decimal handling fix verified!")
    print("The application should now work without Decimal errors.")
