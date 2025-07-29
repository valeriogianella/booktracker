import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Manages SQLite database operations for the Booktrack application."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Store in app's private data directory
            app_dir = os.path.expanduser("~/.booktrack")
            os.makedirs(app_dir, exist_ok=True)
            db_path = os.path.join(app_dir, "booktrack.db")
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    total_pages INTEGER,
                    cover_image_url TEXT,
                    status TEXT DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create reading_sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reading_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    pages_read INTEGER,
                    notes TEXT,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
    
    def add_book(self, title: str, author: str, total_pages: Optional[int] = None, 
                 cover_image_url: Optional[str] = None) -> int:
        """Add a new book to the library."""
        # Convert total_pages to int if it's a Decimal or other numeric type
        if total_pages is not None:
            try:
                total_pages = int(total_pages) if total_pages != '' else None
            except (ValueError, TypeError):
                total_pages = None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, total_pages, cover_image_url)
                VALUES (?, ?, ?, ?)
            ''', (title, author, total_pages, cover_image_url))
            conn.commit()
            return cursor.lastrowid
    
    def get_books(self, status: Optional[str] = None) -> List[Dict]:
        """Get books from the library, optionally filtered by status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('''
                    SELECT id, title, author, total_pages, cover_image_url, status, created_at
                    FROM books WHERE status = ?
                    ORDER BY created_at DESC
                ''', (status,))
            else:
                cursor.execute('''
                    SELECT id, title, author, total_pages, cover_image_url, status, created_at
                    FROM books
                    ORDER BY created_at DESC
                ''')
            
            books = []
            for row in cursor.fetchall():
                books.append({
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'total_pages': row[3],
                    'cover_image_url': row[4],
                    'status': row[5],
                    'created_at': row[6]
                })
            return books
    
    def get_book(self, book_id: int) -> Optional[Dict]:
        """Get a specific book by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, author, total_pages, cover_image_url, status, created_at
                FROM books WHERE id = ?
            ''', (book_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'total_pages': row[3],
                    'cover_image_url': row[4],
                    'status': row[5],
                    'created_at': row[6]
                }
            return None
    
    def update_book(self, book_id: int, title: str = None, author: str = None,
                    total_pages: int = None, cover_image_url: str = None,
                    status: str = None) -> bool:
        """Update an existing book."""
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if author is not None:
            updates.append("author = ?")
            params.append(author)
        if total_pages is not None:
            updates.append("total_pages = ?")
            # Convert total_pages to int if it's a Decimal or other numeric type
            try:
                total_pages = int(total_pages) if total_pages != '' else None
            except (ValueError, TypeError):
                total_pages = None
            params.append(total_pages)
        if cover_image_url is not None:
            updates.append("cover_image_url = ?")
            params.append(cover_image_url)
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        
        if not updates:
            return False
        
        params.append(book_id)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE books SET {", ".join(updates)}
                WHERE id = ?
            ''', params)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_book(self, book_id: int) -> bool:
        """Delete a book and all associated reading sessions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Delete associated reading sessions first
            cursor.execute('DELETE FROM reading_sessions WHERE book_id = ?', (book_id,))
            # Delete the book
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def add_reading_session(self, book_id: int, duration_seconds: int,
                           pages_read: Optional[int] = None,
                           notes: Optional[str] = None) -> int:
        """Add a new reading session."""
        # Convert pages_read to int if it's a Decimal or other numeric type
        if pages_read is not None:
            try:
                pages_read = int(pages_read) if pages_read != '' else None
            except (ValueError, TypeError):
                pages_read = None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reading_sessions (book_id, duration_seconds, pages_read, notes)
                VALUES (?, ?, ?, ?)
            ''', (book_id, duration_seconds, pages_read, notes))
            conn.commit()
            return cursor.lastrowid
    
    def get_reading_sessions(self, book_id: Optional[int] = None) -> List[Dict]:
        """Get reading sessions, optionally filtered by book."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if book_id:
                cursor.execute('''
                    SELECT rs.id, rs.book_id, rs.duration_seconds, rs.pages_read,
                           rs.notes, rs.session_date, b.title, b.author
                    FROM reading_sessions rs
                    JOIN books b ON rs.book_id = b.id
                    WHERE rs.book_id = ?
                    ORDER BY rs.session_date DESC
                ''', (book_id,))
            else:
                cursor.execute('''
                    SELECT rs.id, rs.book_id, rs.duration_seconds, rs.pages_read,
                           rs.notes, rs.session_date, b.title, b.author
                    FROM reading_sessions rs
                    JOIN books b ON rs.book_id = b.id
                    ORDER BY rs.session_date DESC
                ''')
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'id': row[0],
                    'book_id': row[1],
                    'duration_seconds': row[2],
                    'pages_read': row[3],
                    'notes': row[4],
                    'session_date': row[5],
                    'book_title': row[6],
                    'book_author': row[7]
                })
            return sessions
    
    def get_statistics(self) -> Dict:
        """Get reading statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total reading time
            cursor.execute('SELECT SUM(duration_seconds) FROM reading_sessions')
            total_seconds = cursor.fetchone()[0] or 0
            
            # Total sessions
            cursor.execute('SELECT COUNT(*) FROM reading_sessions')
            total_sessions = cursor.fetchone()[0]
            
            # Total books
            cursor.execute('SELECT COUNT(*) FROM books')
            total_books = cursor.fetchone()[0]
            
            # Books by status
            cursor.execute('''
                SELECT status, COUNT(*) FROM books GROUP BY status
            ''')
            books_by_status = dict(cursor.fetchall())
            
            # Reading time by day (last 30 days)
            cursor.execute('''
                SELECT DATE(session_date) as date, SUM(duration_seconds) as total_seconds
                FROM reading_sessions
                WHERE session_date >= datetime('now', '-30 days')
                GROUP BY DATE(session_date)
                ORDER BY date DESC
            ''')
            daily_stats = cursor.fetchall()
            
            return {
                'total_reading_time_seconds': total_seconds,
                'total_sessions': total_sessions,
                'total_books': total_books,
                'books_by_status': books_by_status,
                'daily_stats': daily_stats
            }
    
    def export_data(self) -> Dict:
        """Export all data as JSON-serializable dictionary."""
        books = self.get_books()
        sessions = self.get_reading_sessions()
        stats = self.get_statistics()
        
        return {
            'export_date': datetime.now().isoformat(),
            'books': books,
            'reading_sessions': sessions,
            'statistics': stats
        }
