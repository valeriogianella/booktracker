"""
Booktrack - Main application module
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .database import DatabaseManager
from .timer import Timer
from .widgets import BookForm, BookListItem, SessionLogForm


class Booktrack(toga.App):
    """Main Booktrack application class."""
    
    def startup(self):
        """Initialize the app."""
        self.db_manager = DatabaseManager()
        self.current_timer = None
        self.current_book = None
        self.timer_task = None
        
        # Create main interface
        self.create_main_interface()
        
        # Show main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_container
        self.main_window.show()
        
        # Load initial data
        self.refresh_book_list()
    
    def create_main_interface(self):
        """Create the main application interface."""
        # Create navigation
        self.create_navigation()
        
        # Create main content area
        self.main_content = toga.ScrollContainer(style=Pack(flex=1))
        
        # Create main container
        self.main_container = toga.Box(style=Pack(direction=COLUMN))
        self.main_container.add(self.nav_box)
        self.main_container.add(self.main_content)
        
        # Show active books by default
        self.show_active_books()
    
    def create_navigation(self):
        """Create navigation bar."""
        self.nav_box = toga.Box(style=Pack(direction=ROW, margin=10, background_color='#f0f0f0'))
        
        # Navigation buttons
        active_btn = toga.Button(
            'Active Books',
            on_press=self.show_active_books,
            style=Pack(flex=1, margin=5)
        )
        
        all_books_btn = toga.Button(
            'All Books',
            on_press=self.show_all_books,
            style=Pack(flex=1, margin=5)
        )
        
        stats_btn = toga.Button(
            'Statistics',
            on_press=self.show_statistics,
            style=Pack(flex=1, margin=5)
        )
        
        add_book_btn = toga.Button(
            'Add Book',
            on_press=self.show_add_book_form,
            style=Pack(flex=1, margin=5)
        )
        
        export_btn = toga.Button(
            'Export Data',
            on_press=self.export_data,
            style=Pack(flex=1, margin=5)
        )
        
        self.nav_box.add(active_btn)
        self.nav_box.add(all_books_btn)
        self.nav_box.add(stats_btn)
        self.nav_box.add(add_book_btn)
        self.nav_box.add(export_btn)
    
    def show_active_books(self, widget=None):
        """Show active books view."""
        self.current_view = 'active_books'
        self.refresh_book_list(status='Active')
    
    def show_all_books(self, widget=None):
        """Show all books view."""
        self.current_view = 'all_books'
        self.refresh_book_list()
    
    def show_statistics(self, widget=None):
        """Show statistics view."""
        self.current_view = 'statistics'
        self.display_statistics()
    
    def refresh_book_list(self, status: Optional[str] = None):
        """Refresh the book list display."""
        books = self.db_manager.get_books(status=status)
        
        # Create content box
        content_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        if not books:
            empty_label = toga.Label(
                'No books found. Add a book to get started!',
                style=Pack(text_align='center', margin=20)
            )
            content_box.add(empty_label)
        else:
            title = f"{'Active' if status == 'Active' else 'All'} Books ({len(books)})"
            title_label = toga.Label(
                title,
                style=Pack(font_size=18, font_weight='bold', margin=(0, 0, 10, 0))
            )
            content_box.add(title_label)
            
            for book in books:
                book_item = BookListItem(
                    book,
                    self.start_reading_session,
                    self.edit_book,
                    self.delete_book
                )
                content_box.add(book_item.create_item_box())
        
        self.main_content.content = content_box
    
    def display_statistics(self):
        """Display reading statistics."""
        stats = self.db_manager.get_statistics()
        
        content_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        # Title
        title_label = toga.Label(
            'Reading Statistics',
            style=Pack(font_size=18, font_weight='bold', margin=(0, 0, 10, 0))
        )
        content_box.add(title_label)
        
        # Total reading time
        total_hours = stats['total_reading_time_seconds'] / 3600
        time_label = toga.Label(
            f"Total Reading Time: {total_hours:.1f} hours",
            style=Pack(font_size=14, margin=5)
        )
        content_box.add(time_label)
        
        # Total sessions
        sessions_label = toga.Label(
            f"Total Reading Sessions: {stats['total_sessions']}",
            style=Pack(font_size=14, margin=5)
        )
        content_box.add(sessions_label)
        
        # Total books
        books_label = toga.Label(
            f"Total Books: {stats['total_books']}",
            style=Pack(font_size=14, margin=5)
        )
        content_box.add(books_label)
        
        # Books by status
        if stats['books_by_status']:
            status_label = toga.Label(
                'Books by Status:',
                style=Pack(font_size=14, font_weight='bold', margin=(10, 0, 5, 0))
            )
            content_box.add(status_label)
            
            for status, count in stats['books_by_status'].items():
                status_item = toga.Label(
                    f"  {status}: {count}",
                    style=Pack(font_size=12, margin=(0, 0, 2, 20))
                )
                content_box.add(status_item)
        
        # Recent daily stats
        if stats['daily_stats']:
            daily_label = toga.Label(
                'Daily Reading Time (Last 30 Days):',
                style=Pack(font_size=14, font_weight='bold', margin=(10, 0, 5, 0))
            )
            content_box.add(daily_label)
            
            for date, seconds in stats['daily_stats'][:7]:  # Show last 7 days
                hours = seconds / 3600
                daily_item = toga.Label(
                    f"  {date}: {hours:.1f} hours",
                    style=Pack(font_size=12, margin=(0, 0, 2, 20))
                )
                content_box.add(daily_item)
        
        self.main_content.content = content_box
    
    def show_add_book_form(self, widget=None):
        """Show add book form."""
        def on_save(book_data):
            if book_data:
                try:
                    self.db_manager.add_book(
                        title=book_data['title'],
                        author=book_data['author'],
                        total_pages=book_data['total_pages'],
                        cover_image_url=book_data['cover_image_url']
                    )
                    self.show_success_message('Book added successfully!')
                    self.refresh_current_view()
                except Exception as e:
                    self.show_error_message(f'Error adding book: {str(e)}')
            else:
                self.refresh_current_view()
        
        book_form = BookForm(on_save)
        self.main_content.content = book_form.create_form_box()
    
    def edit_book(self, book_data: Dict):
        """Show edit book form."""
        def on_save(updated_data):
            if updated_data:
                try:
                    self.db_manager.update_book(
                        book_id=updated_data['id'],
                        title=updated_data['title'],
                        author=updated_data['author'],
                        total_pages=updated_data['total_pages'],
                        cover_image_url=updated_data['cover_image_url'],
                        status=updated_data['status']
                    )
                    self.show_success_message('Book updated successfully!')
                    self.refresh_current_view()
                except Exception as e:
                    self.show_error_message(f'Error updating book: {str(e)}')
            else:
                self.refresh_current_view()
        
        book_form = BookForm(on_save, book_data)
        self.main_content.content = book_form.create_form_box()
    
    async def delete_book(self, book_data: Dict):
        """Delete a book after confirmation."""
        try:
            result = await self.main_window.confirm_dialog(
                'Confirm Deletion',
                f"Are you sure you want to delete '{book_data['title']}'? This will also delete all reading sessions for this book."
            )
            
            if result:
                self.db_manager.delete_book(book_data['id'])
                self.show_success_message('Book deleted successfully!')
                self.refresh_current_view()
        except Exception as e:
            self.show_error_message(f'Error deleting book: {str(e)}')
    
    def start_reading_session(self, book_data: Dict):
        """Start a reading session for a book."""
        if book_data['status'] not in ['Active']:
            self.show_error_message('Cannot start reading session for non-active books.')
            return
        
        self.current_book = book_data
        self.current_timer = Timer()
        self.current_timer.start()
        
        self.show_timer_interface()
        
        # Start timer update task
        self.timer_task = asyncio.create_task(self.update_timer_display())
    
    def show_timer_interface(self):
        """Show the timer interface."""
        content_box = toga.Box(style=Pack(direction=COLUMN, margin=20, text_align='center'))
        
        # Book title
        book_title = toga.Label(
            f"Reading: {self.current_book['title']}",
            style=Pack(font_size=18, font_weight='bold', margin=(0, 0, 10, 0), text_align='center')
        )
        content_box.add(book_title)
        
        # Author
        book_author = toga.Label(
            f"by {self.current_book['author']}",
            style=Pack(font_size=14, margin=(0, 0, 20, 0), text_align='center')
        )
        content_box.add(book_author)
        
        # Timer display
        self.timer_display = toga.Label(
            '00:00:00',
            style=Pack(font_size=32, font_weight='bold', margin=20, text_align='center')
        )
        content_box.add(self.timer_display)
        
        # Control buttons
        button_box = toga.Box(style=Pack(direction=ROW, margin=10))
        
        pause_button = toga.Button(
            'Pause',
            on_press=self.pause_timer,
            style=Pack(flex=1, margin=5)
        )
        
        resume_button = toga.Button(
            'Resume',
            on_press=self.resume_timer,
            style=Pack(flex=1, margin=5)
        )
        
        stop_button = toga.Button(
            'Stop & Save',
            on_press=self.stop_and_save_session,
            style=Pack(flex=1, margin=5)
        )
        
        cancel_button = toga.Button(
            'Cancel',
            on_press=self.cancel_session,
            style=Pack(flex=1, margin=5)
        )
        
        button_box.add(pause_button)
        button_box.add(resume_button)
        button_box.add(stop_button)
        button_box.add(cancel_button)
        
        content_box.add(button_box)
        
        self.main_content.content = content_box
    
    async def update_timer_display(self):
        """Update the timer display continuously."""
        while self.current_timer and self.timer_display:
            try:
                elapsed_time = self.current_timer.format_time()
                self.timer_display.text = elapsed_time
                await asyncio.sleep(1)
            except Exception:
                break
    
    def pause_timer(self, widget):
        """Pause the current timer."""
        if self.current_timer:
            self.current_timer.pause()
    
    def resume_timer(self, widget):
        """Resume the current timer."""
        if self.current_timer:
            self.current_timer.resume()
    
    def stop_and_save_session(self, widget):
        """Stop timer and show session log form."""
        if self.current_timer:
            elapsed_seconds = int(self.current_timer.stop())
            
            # Cancel timer update task
            if self.timer_task:
                self.timer_task.cancel()
                self.timer_task = None
            
            self.show_session_log_form(elapsed_seconds)
    
    def cancel_session(self, widget):
        """Cancel the current reading session."""
        if self.current_timer:
            self.current_timer.reset()
        
        if self.timer_task:
            self.timer_task.cancel()
            self.timer_task = None
        
        self.current_timer = None
        self.current_book = None
        
        self.refresh_current_view()
    
    def show_session_log_form(self, duration_seconds: int):
        """Show the session logging form."""
        def on_save(session_data):
            if session_data:
                try:
                    self.db_manager.add_reading_session(
                        book_id=self.current_book['id'],
                        duration_seconds=session_data['duration_seconds'],
                        pages_read=session_data['pages_read'],
                        notes=session_data['notes']
                    )
                    self.show_success_message('Reading session saved successfully!')
                except Exception as e:
                    self.show_error_message(f'Error saving session: {str(e)}')
            
            # Reset timer state
            self.current_timer = None
            self.current_book = None
            self.refresh_current_view()
        
        session_form = SessionLogForm(duration_seconds, on_save)
        self.main_content.content = session_form.create_form_box()
    
    def refresh_current_view(self):
        """Refresh the current view."""
        if hasattr(self, 'current_view'):
            if self.current_view == 'active_books':
                self.show_active_books()
            elif self.current_view == 'all_books':
                self.show_all_books()
            elif self.current_view == 'statistics':
                self.show_statistics()
        else:
            self.show_active_books()
    
    async def export_data(self, widget=None):
        """Export all data to JSON file."""
        try:
            data = self.db_manager.export_data()
            
            # Create export filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"booktrack_export_{timestamp}.json"
            
            # Get user's home directory for export
            export_path = os.path.join(os.path.expanduser("~"), filename)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            await self.main_window.info_dialog(
                'Export Successful',
                f'Data exported successfully to:\n{export_path}'
            )
            
        except Exception as e:
            await self.main_window.error_dialog(
                'Export Failed',
                f'Failed to export data: {str(e)}'
            )
    
    def show_success_message(self, message: str):
        """Show success message to user."""
        # In a real app, this could be a toast notification
        # For now, we'll use the console
        print(f"SUCCESS: {message}")
    
    def show_error_message(self, message: str):
        """Show error message to user."""
        # In a real app, this could be a toast notification
        # For now, we'll use the console
        print(f"ERROR: {message}")


def main():
    """Main entry point for the application."""
    return Booktrack(
        formal_name="Booktrack",
        app_id="com.valerio.booktrack",
        description="A reading time tracking application"
    )


if __name__ == '__main__':
    app = main()
    app.main_loop()
