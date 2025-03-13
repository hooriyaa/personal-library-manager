import streamlit as st
import sqlite3


st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it does not exist
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT,
            read_status BOOLEAN,
            rating INTEGER,
            summary TEXT
        )
    """)
    conn.commit()

create_table()

# Function to add a book
def add_book(title, author, year, genre, read_status, rating, summary):
    cursor.execute("""
        INSERT INTO books (title, author, year, genre, read_status, rating, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, author, year, genre, read_status, rating, summary))
    conn.commit()

# Function to remove a book
def remove_book(title):
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()

# Function to search for books
def search_books(query, search_by):
    cursor.execute(f"SELECT * FROM books WHERE LOWER({search_by}) LIKE LOWER(?)", ('%' + query + '%',))
    return cursor.fetchall()

# Function to fetch all books
def get_all_books():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

# Function to display statistics
def display_statistics():
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]

    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Function to recommend books by genre
def recommend_books(genre):
    cursor.execute("SELECT * FROM books WHERE LOWER(genre) = LOWER(?)", (genre,))
    return cursor.fetchall()

# Streamlit UI

st.title("📚 Personal Library Manager")

# Sidebar Menu
st.sidebar.markdown("📌 **Choose an option**")
choice = st.sidebar.radio("Select an option", 
                          list({
                              "🏠 Home": "Home",
                              "➕ Add a Book": "Add a Book",
                              "🗑 Remove a Book": "Remove a Book",
                              "🔍 Search for a Book": "Search for a Book",
                              "📖 Display All Books": "Display All Books",
                              "📊 Display Statistics": "Display Statistics",
                              "📢 Get Book Recommendations": "Get Book Recommendations",
                          }.keys()), 
                          label_visibility="collapsed")

st.sidebar.write("")  # Minimal spacing
st.sidebar.markdown("📌 **Library data is saved automatically.**")
st.sidebar.write("")  # Minimal spacing
st.sidebar.markdown("📚 Happy Reading! 😊")

# Home
if choice == "🏠 Home":
    st.image("bookshelf.jpg", width=600)
    st.markdown("**Explore and manage your book collection with ease!**")
    st.info("Navigate through the sidebar to add, remove, search, or view your library.")

# Add a Book
elif choice == "➕ Add a Book":
    st.subheader("📌 Add a New Book to Your Collection")
    title = st.text_input("📖 Title", key="title")
    author = st.text_input("✍️ Author", key="author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1, key="year")
    genre = st.text_input("📚 Genre", key="genre")
    read_status = st.checkbox("✅ Mark as Read", key="read_status")
    rating = st.slider("⭐ Rating", min_value=0, max_value=5, step=1, key="rating")
    summary = st.text_area("📝 Short Summary", key="summary")

    if st.button("➕ Add Book"):
        add_book(title, author, year, genre, read_status, rating, summary)
        st.success(f'✔️ "{title}" has been added to your library!')

# Remove a Book
elif choice == "🗑 Remove a Book":
    st.subheader("❌ Remove a Book")
    cursor.execute("SELECT title FROM books")
    book_titles = [row[0] for row in cursor.fetchall()]
    
    if book_titles:
        selected_book = st.selectbox("🗂 Select a book to remove", book_titles, key="remove_book")
        if st.button("🗑 Remove Book"):
            remove_book(selected_book)
            st.success(f'❌ "{selected_book}" has been removed!')
    else:
        st.warning("No books in the library yet.")

# Search for a Book
elif choice == "🔍 Search for a Book":
    st.subheader("🔎 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"], key="search_by")
    query = st.text_input("🔍 Enter search query", key="search_query")

    if st.button("🔎 Search"):
        results = search_books(query, search_by)
        
        if results:
            for book in results:
                st.success(f'📖 **{book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - ⭐ {book[6]}/5')
                st.markdown(f'📜 **Summary:** {book[7]}')
        else:
            st.warning("No matching books found.")

# Display All Books
elif choice == "📖 Display All Books":
    st.subheader("📚 Your Library Collection")
    
    books = get_all_books()
    if books:
        for book in books:
            st.info(f'📖 **{book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - ⭐ {book[6]}/5')
            st.markdown(f'📜 **Summary:** {book[7]}')
    else:
        st.warning("Your library is empty. Start adding books!")

# Display Statistics
elif choice == "📊 Display Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = display_statistics()
    
    st.metric(label="📚 Total Books", value=total_books)
    st.metric(label="✅ Percentage Read", value=f"{percentage_read:.2f}%")

# Book Recommendations
elif choice == "📢 Get Book Recommendations":
    st.subheader("📢 Get Book Recommendations")
    genre = st.text_input("📚 Enter Genre for Recommendations", key="recommend_genre")
    
    if st.button("📢 Recommend Books"):
        recommendations = recommend_books(genre)
        
        if recommendations:
            for book in recommendations:
                st.success(f'📖 **{book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - ⭐ {book[6]}/5')
                st.markdown(f'📜 **Summary:** {book[7]}')
        else:
            st.warning(f"No recommendations found for the genre '{genre}'. Try adding books in this category!")

# Close the database connection
conn.close()
