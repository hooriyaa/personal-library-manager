
import streamlit as st
import json

# File to store the library data
LIBRARY_FILE = "library.json"

# Load Library Data
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save Library Data
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Add a New Book
def add_book(library, title, author, year, genre, read_status, rating, summary):
    library.append({
        "Title": title,
        "Author": author,
        "Publication Year": year,
        "Genre": genre,
        "Read Status": read_status,
        "Rating": rating,
        "Summary": summary
    })
    save_library(library)

# Remove a Book
def remove_book(library, title):
    library = [book for book in library if book["Title"].lower() != title.lower()]
    save_library(library)
    return library

# Search Books
def search_books(library, query, search_by):
    return [book for book in library if query.lower() in book[search_by].lower()]

# Display Statistics
def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read Status"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Recommend Books by Genre
def recommend_books(library, genre):
    return [book for book in library if book["Genre"].lower() == genre.lower()]

# UI Enhancements
st.set_page_config(page_title="📚 Personal Library Manager",page_icon="📖", layout="wide")
st.title("📖 My Digital Library")
st.markdown("Welcome to your personal library manager! Organize and track your books effortlessly. 📚")

library = load_library()

# Sidebar Menu
menu = ["🏠 Home", "➕ Add a Book", "🗑 Remove a Book", "🔍 Search for a Book", 
        "📖 Display All Books", "📊 Display Statistics", "📢 Get Book Recommendations"]
choice = st.sidebar.radio("📌 Choose an option", menu)

# Home
if choice == "🏠 Home":
    st.image("bookshelf.jpg", width=600)
    st.markdown("**Explore and manage your book collection with ease!**")
    st.info("Navigate through the sidebar to add, remove, search, or view your library.")

# Add a Book
elif choice == "➕ Add a Book":
    st.subheader("📌 Add a New Book to Your Collection")
    title = st.text_input("📖 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("📚 Genre")
    read_status = st.checkbox("✅ Mark as Read")
    rating = st.slider("⭐ Rating", min_value=0, max_value=5, step=1)
    summary = st.text_area("📝 Short Summary")

    if st.button("➕ Add Book"):
        add_book(library, title, author, year, genre, read_status, rating, summary)
        st.success(f'✔️ "{title}" has been added to your library!')

# Remove a Book
elif choice == "🗑 Remove a Book":
    st.subheader("❌ Remove a Book")
    book_titles = [book["Title"] for book in library]
    
    if book_titles:
        selected_book = st.selectbox("🗂 Select a book to remove", book_titles)
        if st.button("🗑 Remove Book"):
            library = remove_book(library, selected_book)
            st.success(f'❌ "{selected_book}" has been removed!')
    else:
        st.warning("No books in the library yet.")

# Search for a Book
elif choice == "🔍 Search for a Book":
    st.subheader("🔎 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input("🔍 Enter search query")

    if st.button("🔎 Search"):
        results = search_books(library, query, search_by)
        
        if results:
            for book in results:
                rating = book.get("Rating", "N/A")
                summary = book.get("Summary", "No summary available")
                st.success(f'📖 **{book["Title"]}** by *{book["Author"]}* ({book["Publication Year"]}) - {book["Genre"]} - ⭐ {rating}/5')
                st.markdown(f'📜 **Summary:** {summary}')
        else:
            st.warning("No matching books found.")

# Display All Books
elif choice == "📖 Display All Books":
    st.subheader("📚 Your Library Collection")
    
    if library:
        for book in library:
            rating = book.get("Rating", "N/A")
            summary = book.get("Summary", "No summary available")
            st.info(f'📖 **{book["Title"]}** by *{book["Author"]}* ({book["Publication Year"]}) - {book["Genre"]} - ⭐ {rating}/5')
            st.markdown(f'📜 **Summary:** {summary}')
    else:
        st.warning("Your library is empty. Start adding books!")

# Display Statistics
elif choice == "📊 Display Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = display_statistics(library)
    
    st.metric(label="📚 Total Books", value=total_books)
    st.metric(label="✅ Percentage Read", value=f"{percentage_read:.2f}%")

# Book Recommendations
elif choice == "📢 Get Book Recommendations":
    st.subheader("📢 Get Book Recommendations")
    genre = st.text_input("📚 Enter Genre for Recommendations")
    
    if st.button("📢 Recommend Books"):
        recommendations = recommend_books(library, genre)
        
        if recommendations:
            for book in recommendations:
                rating = book.get("Rating", "N/A")
                summary = book.get("Summary", "No summary available")
                st.success(f'📖 **{book["Title"]}** by *{book["Author"]}* ({book["Publication Year"]}) - {book["Genre"]} - ⭐ {rating}/5')
                st.markdown(f'📜 **Summary:** {summary}')
        else:
            st.warning(f"No recommendations found for the genre '{genre}'. Try adding books in this category!")

st.sidebar.markdown("📌 **Library data is saved automatically. Happy Reading!**")
