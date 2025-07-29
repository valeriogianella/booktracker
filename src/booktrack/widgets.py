import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import List, Dict, Optional
from .database import DatabaseManager


class BookForm:
    """Form widget for adding/editing books."""
    
    def __init__(self, on_save_callback, book_data: Optional[Dict] = None):
        self.on_save_callback = on_save_callback
        self.book_data = book_data
        self.is_edit_mode = book_data is not None
        
        # Create form inputs
        self.title_input = toga.TextInput(
            value=book_data.get('title', '') if book_data else '',
            style=Pack(flex=1, margin=5)
        )
        
        self.author_input = toga.TextInput(
            value=book_data.get('author', '') if book_data else '',
            style=Pack(flex=1, margin=5)
        )
        
        self.pages_input = toga.NumberInput(
            value=book_data.get('total_pages') if book_data and book_data.get('total_pages') else None,
            style=Pack(flex=1, margin=5)
        )
        
        self.cover_url_input = toga.TextInput(
            value=book_data.get('cover_image_url', '') if book_data else '',
            style=Pack(flex=1, margin=5)
        )
        
        if self.is_edit_mode:
            self.status_selection = toga.Selection(
                items=['Active', 'Read', 'Paused', 'Abandoned'],
                value=book_data.get('status', 'Active'),
                style=Pack(flex=1, margin=5)
            )
    
    def create_form_box(self) -> toga.Box:
        """Create the form layout."""
        form_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        # Title
        form_box.add(toga.Label('Title *', style=Pack(margin=(0, 0, 5, 0))))
        form_box.add(self.title_input)
        
        # Author
        form_box.add(toga.Label('Author *', style=Pack(margin=(10, 0, 5, 0))))
        form_box.add(self.author_input)
        
        # Total Pages
        form_box.add(toga.Label('Total Pages', style=Pack(margin=(10, 0, 5, 0))))
        form_box.add(self.pages_input)
        
        # Cover URL
        form_box.add(toga.Label('Cover Image URL', style=Pack(margin=(10, 0, 5, 0))))
        form_box.add(self.cover_url_input)
        
        # Status (only for edit mode)
        if self.is_edit_mode:
            form_box.add(toga.Label('Status', style=Pack(margin=(10, 0, 5, 0))))
            form_box.add(self.status_selection)
        
        # Buttons
        button_box = toga.Box(style=Pack(direction=ROW, margin=10))
        
        save_button = toga.Button(
            'Update' if self.is_edit_mode else 'Add Book',
            on_press=self.save_book,
            style=Pack(flex=1, margin=5)
        )
        
        cancel_button = toga.Button(
            'Cancel',
            on_press=self.cancel,
            style=Pack(flex=1, margin=5)
        )
        
        button_box.add(save_button)
        button_box.add(cancel_button)
        
        form_box.add(button_box)
        
        return form_box
    
    def save_book(self, widget):
        """Save the book data."""
        # Validate required fields
        if not self.title_input.value or not self.author_input.value:
            # TODO: Show error message
            return
        
        # Convert pages to int, handling None and empty string cases
        total_pages = self.pages_input.value
        if total_pages is not None and total_pages != '':
            try:
                total_pages = int(total_pages)
            except (ValueError, TypeError):
                total_pages = None
        else:
            total_pages = None
        
        book_data = {
            'title': self.title_input.value,
            'author': self.author_input.value,
            'total_pages': total_pages,
            'cover_image_url': self.cover_url_input.value if self.cover_url_input.value else None
        }
        
        if self.is_edit_mode:
            book_data['status'] = self.status_selection.value
            book_data['id'] = self.book_data['id']
        
        self.on_save_callback(book_data)
    
    def cancel(self, widget):
        """Cancel form operation."""
        self.on_save_callback(None)


class BookListItem:
    """Widget for displaying a single book in the list."""
    
    def __init__(self, book_data: Dict, on_start_reading, on_edit_book, on_delete_book):
        self.book_data = book_data
        self.on_start_reading = on_start_reading
        self.on_edit_book = on_edit_book
        self.on_delete_book = on_delete_book
    
    def create_item_box(self) -> toga.Box:
        """Create the book item layout."""
        item_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        
        # Book info
        info_box = toga.Box(style=Pack(direction=ROW, margin=5))
        
        # Book details
        details_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        title_label = toga.Label(
            self.book_data['title'],
            style=Pack(font_weight='bold', margin=(0, 0, 2, 0))
        )
        
        author_label = toga.Label(
            f"by {self.book_data['author']}",
            style=Pack(font_size=12, margin=(0, 0, 2, 0))
        )
        
        status_label = toga.Label(
            f"Status: {self.book_data['status']}",
            style=Pack(font_size=10, margin=(0, 0, 2, 0))
        )
        
        details_box.add(title_label)
        details_box.add(author_label)
        details_box.add(status_label)
        
        if self.book_data.get('total_pages'):
            pages_label = toga.Label(
                f"Pages: {self.book_data['total_pages']}",
                style=Pack(font_size=10)
            )
            details_box.add(pages_label)
        
        info_box.add(details_box)
        
        # Action buttons
        button_box = toga.Box(style=Pack(direction=COLUMN, margin=5))
        
        if self.book_data['status'] == 'Active':
            start_button = toga.Button(
                'Start Reading',
                on_press=lambda x: self.on_start_reading(self.book_data),
                style=Pack(width=120, margin=2)
            )
            button_box.add(start_button)
        
        edit_button = toga.Button(
            'Edit',
            on_press=lambda x: self.on_edit_book(self.book_data),
            style=Pack(width=120, margin=2)
        )
        
        delete_button = toga.Button(
            'Delete',
            on_press=lambda x: self.on_delete_book(self.book_data),
            style=Pack(width=120, margin=2)
        )
        
        button_box.add(edit_button)
        button_box.add(delete_button)
        
        info_box.add(button_box)
        
        item_box.add(info_box)
        
        # Add separator
        separator = toga.Box(style=Pack(height=1, background_color='#CCCCCC', margin=(5, 0)))
        item_box.add(separator)
        
        return item_box


class SessionLogForm:
    """Form for logging reading session details."""
    
    def __init__(self, duration_seconds: int, on_save_callback):
        self.duration_seconds = duration_seconds
        self.on_save_callback = on_save_callback
        
        # Create form inputs
        self.duration_label = toga.Label(
            f"Reading Time: {self.format_duration(duration_seconds)}",
            style=Pack(font_weight='bold', margin=5)
        )
        
        self.pages_input = toga.NumberInput(
            style=Pack(flex=1, margin=5)
        )
        
        self.notes_input = toga.MultilineTextInput(
            style=Pack(flex=1, height=100, margin=5)
        )
    
    def format_duration(self, seconds: int) -> str:
        """Format duration as HH:MM:SS."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def create_form_box(self) -> toga.Box:
        """Create the session log form layout."""
        form_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        form_box.add(self.duration_label)
        
        # Pages read
        form_box.add(toga.Label('Pages Read', style=Pack(margin=(10, 0, 5, 0))))
        form_box.add(self.pages_input)
        
        # Notes
        form_box.add(toga.Label('Session Notes', style=Pack(margin=(10, 0, 5, 0))))
        form_box.add(self.notes_input)
        
        # Buttons
        button_box = toga.Box(style=Pack(direction=ROW, margin=10))
        
        save_button = toga.Button(
            'Save Session',
            on_press=self.save_session,
            style=Pack(flex=1, margin=5)
        )
        
        cancel_button = toga.Button(
            'Cancel',
            on_press=self.cancel,
            style=Pack(flex=1, margin=5)
        )
        
        button_box.add(save_button)
        button_box.add(cancel_button)
        
        form_box.add(button_box)
        
        return form_box
    
    def save_session(self, widget):
        """Save the session data."""
        # Convert pages to int, handling None and empty string cases
        pages_read = self.pages_input.value
        if pages_read is not None and pages_read != '':
            try:
                pages_read = int(pages_read)
            except (ValueError, TypeError):
                pages_read = None
        else:
            pages_read = None
        
        session_data = {
            'duration_seconds': self.duration_seconds,
            'pages_read': pages_read,
            'notes': self.notes_input.value if self.notes_input.value else None
        }
        self.on_save_callback(session_data)
    
    def cancel(self, widget):
        """Cancel the session logging."""
        self.on_save_callback(None)
