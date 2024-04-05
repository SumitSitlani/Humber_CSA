document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    const urlFragment1 = window.location.hash.substring(1);
    const urlFragment2 = window.location.hash.substring(2);
    const urlParams1 = new URLSearchParams(urlFragment1);
    const urlParams2 = new URLSearchParams(urlFragment2);

    const bookId = urlParams2.get('id');
    const id_token = urlParams1.get('id_token');
    console.log('ID Token:', id_token);
    console.log('Book ID:', bookId);

    if (bookId) {
        loadBookDetails(bookId); // Call with dynamic ID   
    }

  
    
    loadBooks(id_token);
    // Add book form submission handler
    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            addBook(id_token);
        });
    }



    const editBookForm = document.getElementById('editBookForm');
    if (editBookForm && bookId) {
        editBookForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            editBook(id_token);
        });
    }
});
 

// Load the books from the API
function loadBooks(id_token) {
    fetch('https://v9rf0t0gn8.execute-api.us-east-1.amazonaws.com/dev/book', {
             method: 'GET',
             headers: {
                'Authorization': id_token 
            }
        })
        .then(response => response.json()) // response.json() already parses the JSON string
        .then(data => {
            // No need to parse it again, just access the 'body' property
            displayBooks(data.body, id_token);
        })
        .catch(error => console.error('Fetching books failed:', error));
}


// Display the books in the DOM
function displayBooks(books, id_token) {
    const booksList = document.getElementById('booksList');
    //booksList.innerHTML = ''; // Clear the list before adding books
    booksList.classList.add('books-container'); // Add a class to the list

    
    books.forEach(book => {
        const bookContainer = document.createElement('div');
        bookContainer.classList.add('book');

        bookContainer.innerHTML = `
            <h2>${book.Title}</h2>
            <p><strong>Author:</strong> ${book.Authors}</p>
            <p><strong>Publisher:</strong> ${book.Publisher}</p>
            <p><strong>Year:</strong> ${book.Year}</p>
            <a href="edit-book.html#id_token=${id_token}&id=${book.id}" class="edit-button">Edit Book</a>
            <button class="delete-button" onclick="deleteBook(${book.id})"  >Delete Book</button>
        `;

        booksList.appendChild(bookContainer); // Add the book to the list
    });
}


function addBook(id_token) {
    const newBookData = {
        Title: document.getElementById('Title').value,
        Authors: document.getElementById('Authors').value,
        Publisher: document.getElementById('Publisher').value,
        Year: Number(document.getElementById('Year').value),
        id: Number(document.getElementById('id').value)
    };
    console.log('New Book Data:', newBookData);
    fetch('https://v9rf0t0gn8.execute-api.us-east-1.amazonaws.com/dev/book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': id_token
        },
        body: JSON.stringify(newBookData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Book added successfully!');
        
        addBookForm.reset();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error adding book: ' + error.message);
    });
}

function loadBookDetails(bookId) {
    
    console.log('Loading book details:', bookId);
    fetch(`https://v9rf0t0gn8.execute-api.us-east-1.amazonaws.com/dev/book/show/${bookId}`)
    .then(response => response.json())
    .then(data => {
        // Assuming the API returns the book details directly
        document.getElementById('Title').value = data.Title;
        document.getElementById('Authors').value = data.Authors;
        document.getElementById('Publisher').value = data.Publisher;
        document.getElementById('Year').value = data.Year;
    })
    .catch(error => console.error('Error loading book details:', error));
}



function editBook(id_token) {
    const urlFragment2 = window.location.hash.substring(2);
    const urlParams2 = new URLSearchParams(urlFragment2);

    const bookId = urlParams2.get('id');
    console.log('Book ID:', bookId);
    const newBookData = {
        Title: document.getElementById('Title').value,
        Authors: document.getElementById('Authors').value,
        Publisher: document.getElementById('Publisher').value,
        Year: Number(document.getElementById('Year').value)
    };
    console.log('New Book Data:', newBookData);
    fetch(`https://v9rf0t0gn8.execute-api.us-east-1.amazonaws.com/dev/book/edit/${bookId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': id_token
        },
        body: JSON.stringify(newBookData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Book edited successfully!');
        
        addBookForm.reset();
    })
    .catch((error) => {
        console.error('Error:', error);
        //alert('Error adding book: ' + error.message);
    });

}


// Add event listener to the books list
function deleteBook(bookId, id_token) {
    fetch(`https://v9rf0t0gn8.execute-api.us-east-1.amazonaws.com/dev/book/delete/${bookId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Book deleted successfully!');
        loadBooks();
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error deleting book: ' + error.message);
    });
 

}

function logoutUser() {
    // Remove the user's session from localStorage or any other session management approach you are using
    localStorage.removeItem('userSession');
    
    // Redirect the user to the login page or home page
    window.location.href = 'https://tp-withbooks.auth.us-east-1.amazoncognito.com/login?client_id=27rrbm1i5sjkkfggmai299o8gp&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2Ftinyurl.com%2Ftp-withbooks';
}
