from pydoc import importfile

import openai
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# import ipdb


# API key passed from file .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function that reads an article from a text file
def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# A function that generates HTML code based on the content of the article and the prompt
def generate_html(article_text):
    article_text = article_text.replace("\n", " ")
    prompt = (
        f"Generate HTML code based on the provided text file content {article_text}. Follow these guidelines:"
        f"1. Identify distinct sections based on text structure or paragraph breaks."
        f"2. For each identified section:"
        f"- Create a <section> tag."
        f"- Use the first line of each section as an <h2> heading."
        f"- Wrap each remaining paragraph in <p> tags."
        f"3. Insert an <img> tag at the end of each section with src='image_placeholder.jpg' and an appropriate alt text based on the heading."
        f"4. Add a <figcaption> tag below each <img> tag with a brief description or note for the image. Use the section heading as a reference for the description."
        f"5. If the line starts with '*', wrap it in <p> and <em>."
        f"6. The alt attribute must always start with the word 'Image' followed by a short description based on the section heading. "
        f"Ensure the structure resembles this format:"
        f"<section>"
        f"  <h2>Title from First Line of Section</h2>"
        f"  <p>First paragraph of content for this section.</p>"
        f"  <p>Second paragraph, and so on.</p>"
        f"  <figure>"
        f"    <img src='image_placeholder.jpg' alt='Description for this section'>"
        f"    <figcaption>Description for this image, based on the section heading.</figcaption>"
        f"  </figure>"
        f"</section>"
        f"Apply this structure to all sections in the text file, creating a clean HTML layout for each section with headings, paragraphs, images, and captions."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10000
        )


        # Receiving generated text from the API
        generated_html = response['choices'][0]['message']['content'].strip()

        # Clean HTML code from html blocks
        beauty = BeautifulSoup(generated_html, 'html.parser')
        length_of_generated_html = len(beauty.contents)
        cleaned_html = ''.join([
            str(tag) for tag in beauty.contents[1:length_of_generated_html-1]
        ])

        return cleaned_html
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# A function that saves the generated HTML to a file
def save_html(content, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    # Path to the article file and szablon
    article_path = 'data/tresc_artykulu.txt'
    # Path to save the generated HTML file
    output_path = 'result/artykul.html'

    # Load files
    article_text = read_article(article_path)
    # Generate HTML
    generated_html = generate_html(article_text)
    # Save the generated HTML to a file
    save_html(generated_html, output_path)

    print(f"The generated HTML code is saved in a file {output_path}")

if __name__ == "__main__":
    main()