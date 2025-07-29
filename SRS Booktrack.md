# **Software Requirements Specification (SRS)**

## **for**

## **Booktrack**

**Version 1.0**

**Prepared by:** Valerio Gianella

**Date:** 29.07.2025

### **Table of Contents**

1. Introduction  
   1.1. Purpose  
   1.2. Document Conventions  
   1.3. Intended Audience and Reading Suggestions  
   1.4. Project Scope  
   1.5. References  
2. Overall Description  
   2.1. Product Perspective  
   2.2. Product Functions  
   2.3. User Classes and Characteristics  
   2.4. Operating Environment  
   2.5. Design and Implementation Constraints  
   2.6. Assumptions and Dependencies  
3. System Features  
   3.1. System Feature 1 (e.g., User Account Management)  
   3.2. System Feature 2 (e.g., Data Dashboard)  
   3.3. ... (add as many features as needed)  
4. External Interface Requirements  
   4.1. User Interfaces  
   4.2. Hardware Interfaces  
   4.3. Software Interfaces  
   4.4. Communications Interfaces  
5. Non-Functional Requirements  
   5.1. Performance Requirements  
   5.2. Safety Requirements  
   5.3. Security Requirements  
   5.4. Software Quality Attributes  
   5.5. Business Rules  
6. Appendices  
   A. Glossary  
   B. Analysis Models (Optional)  
   C. To-be-determined List (Optional)

### **1. Introduction**

#### **1.1. Purpose**

Booktrack is an application that helps the user to keep track of his reading time, by logging the time that was spent reading.

#### **1.2. Document Conventions**

We refer to Booktrack as the application, the app, the software, the program, interchangeably.

#### **1.3. Intended Audience and Reading Suggestions**

These requirements are intended to specify what the app should do and how it should be implemented. If some specifications are contradictory or impossible to implement, the agent implementing the software should ask for clarification and not act on its own accord, unless specified in this way.

#### **1.4. Project Scope**

We want to allow the user to register and manage books.  
We want to allow the user to perform some action wrt a book: log reading time, log page read and take notes.

#### **1.5. References**

N/A for this application.

### **2. Overall Description**

#### **2.1. Product Perspective**

This product is a new, standalone mobile application.

#### **2.2. Product Functions**

* Registration of a new book.  
* Management of the registered books (modify, delete, change status of an existing book).  
* Ability to start and stop a timer connected to a specific book that has been previously registered by the user. The recorded time is saved, together with the information of the book to which it was connected.  
* Visualization of Historical Data (reading history)  
* User Profile Settings Management

#### **2.3. User Classes and Characteristics**

* **General User:** This is the only profile using the app. The user doesn't need to login.

#### **2.4. Operating Environment**

The app is an Android app, able to run on the latest Android version.

#### **2.5. Design and Implementation Constraints**

The application shall be implemented in Python using the BeeWare framework. All application data (books, logs, etc.) shall be persisted locally on the device in a single-file SQLite database.

#### **2.6. Assumptions and Dependencies**

The app has no dependencies.

### **3. System Features**

#### **3.1 Feature: Book Management**

* **Description:** Users must be able to add, view, modify, and delete books in their personal library. This library is the central repository for all their reading material.  
* **Functional Requirements:**  
  * REQ-1: The system shall provide a form for the user to manually add a new book. The form must capture:  
    * Title (Text, Mandatory)  
    * Author (Text, Mandatory)  
    * Total Pages (Integer, Optional)  
    * Cover Image URL (Text, Optional)  
  * REQ-2: Upon creation, a book's status shall default to "Active".  
  * REQ-3: The user shall be able to change a book's status to one of the following: "Active", "Read", "Paused", "Abandoned".  
  * REQ-4: The system shall allow the user to edit all fields of an existing book.  
  * REQ-5: The system shall allow the user to delete a book. Deleting a book must also delete all associated reading logs and notes. The system must ask for confirmation before deletion.

#### **3.2 Feature: Reading Session Timer**

* **Description:** Users can time their reading sessions for any "Active" book in their library.  
* **Functional Requirements:**  
  * REQ-6: The main library view must display a "Start Reading" button next to each "Active" book.  
  * REQ-7: Clicking "Start Reading" will navigate the user to a dedicated timer page for that book. This page will display the book's title and a running stopwatch.  
  * REQ-8: The timer page must have a "Stop & Save" button.  
  * REQ-9: Upon clicking "Stop & Save", the system shall present a form to log:  
    * The elapsed time (pre-filled from the stopwatch).  
    * The number of pages read in that session (Integer, Optional).  
    * A short note about the session (Text, Optional).  
  * REQ-10: Saving the session log shall store the record and associate it with the correct book.

#### **3.3 Feature: Export Data**

* **Description:** Users can export the data of the library and of the reading sessions.  
* **Functional Requirements:**  
  * REQ-11: The user can export all the data present in the library and of the reading sessions pressing a button.  
  * REQ-12: The exported data is saved in a single json file.

### **4. External Interface Requirements**

#### **4.1. User Interfaces**

The main screen shows a list of 'Active' books. A navigation bar allows the user to switch to an 'All Books' view and a 'Statistics' view. Tapping 'Add Book' opens a form modal.  
The ‘All Books’ displays all the books in the library.   
The 'Statistics' view displays the time spent reading, by day, by week, and by month.

#### **4.2. Hardware Interfaces**

The system does not have any direct hardware interfaces.

#### **4.3. Software Interfaces**

The system will interface with the Python sqlite3 library to manage the local database file stored within the application's private data directory on the device.

#### **4.4. Communications Interfaces**

The system does not have any direct communications interfaces.

### **5. Non-Functional Requirements**

#### **5.1. Performance Requirements**

PERF-1: PERF-1: The application's main screen shall be visible and interactive within 2 seconds of the user tapping the app icon.  
PERF-2: Database queries for fetching the user's library should complete in under 500 milliseconds.

#### **5.2. Safety Requirements**

N/A for this application.

#### **5.3. Security Requirements**

N/A for this application.

#### **5.4. Software Quality Attributes**

USABILITY-1: A user must be able to start a reading session for a book from the main library view in no more than two clicks.  
RELIABILITY-1: Reading session data must be saved transactionally. A failure during saving should not result in a partially saved or corrupt log entry.

#### **5.5. Business Rules**

BR-1: A timer cannot be started for a book whose status is "Read" or "Abandoned".

### **6. Appendices**

#### **A. Glossary**

*(Define any terms, acronyms, and abbreviations used in this document to ensure clear and consistent understanding.)*

#### **B. Analysis Models (Optional)**

*(This section can include relevant diagrams, such as data flow diagrams, class diagrams, or state-transition diagrams.)*

#### **C. To-be-determined List (Optional)**

*(A list of items that are not yet decided and need further clarification.)*