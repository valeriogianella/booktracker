#!/usr/bin/env python3
"""
Setup and test script for Booktrack application
"""

import subprocess
import sys
import os
import platform


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True


def setup_environment():
    """Set up the development environment."""
    print("🚀 Setting up Booktrack development environment")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    if not check_python_version():
        return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Install app in development mode
    if not run_command("pip install -e .", "Installing Booktrack in development mode"):
        return False
    
    return True


def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests")
    
    # Run unit tests
    if not run_command("python -m pytest tests/ -v", "Running unit tests"):
        return False
    
    return True


def test_basic_functionality():
    """Test basic app functionality."""
    print("\n🔍 Testing basic functionality")
    
    # Test database creation
    test_script = """
import tempfile
import os
from booktrack.database import DatabaseManager

# Test database operations
with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
    db = DatabaseManager(tmp.name)
    
    # Add a test book
    book_id = db.add_book("Test Book", "Test Author", 200)
    print(f"✅ Added book with ID: {book_id}")
    
    # Add a reading session
    session_id = db.add_reading_session(book_id, 1800, 25, "Test session")
    print(f"✅ Added session with ID: {session_id}")
    
    # Get statistics
    stats = db.get_statistics()
    print(f"✅ Statistics: {stats['total_reading_time_seconds']} seconds read")
    
    # Export data
    export_data = db.export_data()
    print(f"✅ Export contains {len(export_data['books'])} books")
    
    # Clean up
    os.unlink(tmp.name)

print("✅ All database operations completed successfully")
"""
    
    if not run_command(f'python -c "{test_script}"', "Testing database operations"):
        return False
    
    return True


def build_android():
    """Build Android version."""
    print("\n📱 Building Android version")
    
    if not run_command("briefcase create android", "Creating Android project"):
        print("⚠️  Android build failed - this is normal if you don't have Android SDK")
        return False
    
    if not run_command("briefcase build android", "Building Android APK"):
        print("⚠️  Android build failed - this is normal if you don't have Android SDK")
        return False
    
    print("✅ Android build completed successfully")
    return True


def main():
    """Main setup and test script."""
    print("🎯 Booktrack Setup and Test Script")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed")
        sys.exit(1)
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup and tests completed successfully!")
    print("=" * 50)
    
    print("\n📋 Next steps:")
    print("1. Run the app: python -m booktrack")
    print("2. For Android build: python setup.py --android")
    print("3. Read TESTING.md for comprehensive testing instructions")
    
    # Optional Android build
    if "--android" in sys.argv:
        build_android()


if __name__ == "__main__":
    main()
