#this script is a Flask web application that allows users to upload images, 
#processes the text in them, generates a word cloud from the extracted text, and serves the 
#generated image for download.
#6/24/23

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image #image processing library
import pytesseract #OCR tool
from wordcloud import WordCloud #generates wordclouds
import os
import uuid #for file operations

app = Flask(__name__) #creates a new flask web application

UPLOAD_FOLDER = 'static' #where uploaded files get stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #sets up a config value for the Flask app; variables the app may need will be stores in the upload_folder

@app.route('/', methods=['GET', 'POST']) #tells Flask what URL should trigger the index() function. This route can handle both GET and POST requests
def index(): #defines the index route -- when the user navigates to the root URL, this function will be called to handle the request
    if request.method == 'POST': #if request method is POST, it means the user has submitted the form with files
        #checks for user consent using Flask's request object (contains all the info about the clients request)
        consent = request.form.get('consent')
        if not consent:
            return "Consent not given.", 400 #user must give consent to move forward, else an error message will show
        
        #once consent is given, script get the list of uploaded images
        files = request.files.getlist('images')
        
        #processes images -- creates an empty list called combined_text
        combined_text = ''
        for file in files: #loops through each image uploaded, uses Image processing lib and OCR tool to extract text from image
            ocr_result = pytesseract.image_to_string(Image.open(file))
            combined_text += ' ' + ocr_result #adds the extracted text to the combined_text list with a space separating the content from the previous content
    
        if combined_text.strip() == '':
            return "No text extracted from the images.", 400 #if no text can be extracted, an error message will show

        #generates a word cloud from the combined text and saves it as a png file
        wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(combined_text) #generates a wordclou using the combinted text from processing the uploaded files
        file_name = str(uuid.uuid4()) + '.png' #creates a unique file name for the image -- uuid generates a random, unique identifier, which is then converted to a string and then concatenated w .png
        wordcloud.to_file(os.path.join(UPLOAD_FOLDER, file_name)) #saves the word cloud image to a file

        #redirects user where they can download the file
        return redirect(url_for('download', file_name=file_name)) 

    return render_template('index.html')

#defines the dynamic download route and sends wordcloud image to the static directory
@app.route('/download/<file_name>')
def download(file_name): #takes file_name as an argument
    return send_from_directory(UPLOAD_FOLDER, file_name) #sends the file from the directory to the client who made the request

#runs the Flask app and enables debugging to provide error pages if something goes wrong
if __name__ == '__main__':
    app.run(debug=True) #the command to start the Flask wb server to run the app
