# Text Analysis Flask Application

This is a web application built with Flask that allows users to upload image files, extract the text from these files, generate a word cloud from the extracted text, and then serve the word cloud image for download.

### Features

Text extraction from different file types:

- Images (.png): The pytesseract library, an OCR (Optical Character Recognition) 

- Word cloud generation: The word cloud library generates a word cloud from the combined text extracted from all uploaded files. The word cloud is saved as a PNG image with a unique filename, generated using the uuid library.

- File download: The Flask send_from_directory function serves the generated word cloud image for download when the user navigates to the appropriate download URL.
  

### How It Works

When a user navigates to the root URL, the index() function is called to handle the request. If the request method is POST, which means the user has submitted the form with files, the application checks if the user consented to process the files.

If consent is given, the application gets a list of uploaded images from the form data and processes each image. The text extracted from each file is added to a combined text string.

After all files have been processed, the application generates a word cloud from the combined text and saves it as a PNG image in a static directory. The user is then redirected to a download URL to download the word cloud image.


### Running the Application

To run the application, use the command python/ python3 app.py in the terminal, where app.py is the file name containing this application. This will start the Flask web server, and the application will be accessible in a web browser at the URL localhost:5000 or 127.0.0.1:5000 unless otherwise specified.

Remember to install the necessary libraries (Flask, pytesseract, wordcloud) using pip/pip3 before running the application.

