import openai
import os
from dotenv import load_dotenv


# Klucz API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funkcja odczytująca artykuł z pliku tekstowego
def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def clean_html_code(html_code):
    # Usuwamy znaczniki ```html z początku oraz ``` z końca
    if html_code.startswith("```"):
        html_code = html_code[7:]  # Usuwa "```html\n"
    if html_code.endswith("```"):
        html_code = html_code[:-3]  # Usuwa końcowe "```"
    return html_code.strip()  # Usuwamy ewentualne białe znaki na końcach

# Funkcja generująca kod HTML na podstawie treści artykułu i promptu
def generate_html(article_text):
    prompt = (
        # f"Stwórz HTML dla następującego artykułu. Kod ma być zgodny HMTL5. Zawżyj i podziel treść artykułu na <section>, <h> i <p>."
        # f"Zaproponuj mi gdzie można wstawić znaczniki <img>."
        # f"Dodaj placeholdery < img src='image_placeholder.jpg' alt='' >"
        # f"w miejscach, gdzie można by wstawić grafiki. Treść artykułu: {article_text}. Treść ma być cała."
        # f"W atrybucie alt generuj prompt generujący image. Każdy alt musi być wypełniony."
        # #f"Zamieść wynik w znacznikach <body></body>. Nie generuj <html> i <head>, nie dodawaj ```html i ```"
        # f"Zwrócony kod powinien zawierać wyłącznie zawartość do wstawienia pomiędzy tagami <body> i </body>. Nie dołączaj znaczników <html>, <head>, <body> ani html"
        f"Generate HTML code based on the provided text file content {article_text}.Follow these guidelines:"
        f"1. Identify distinct sections based on text structure or paragraph breaks."
        f"2. For each identified section:"
        f"- Create a < section > tag."
        f"- Use the first line of each section as an < h2 > heading."
        f"- Wrap each remaining paragraph in < p > tags."
        f"3. Insert an < img > tag at the end of each section with src='image_placeholder.jpg' and an appropriate alt text based on the heading add on the begaing text image."
        f"Ensure the structure resembles this format:"
        f"< section >"
        f"< h2 > Title from First Line of Section < / h2 >"
        f"< p > First paragraph of content for this section.< / p >"
        f"< p > Second paragraph, and so on.< / p >"
        f"< img src='image_placeholder.jpg' alt='Description for this section' >"
        f"< / section >"
        f"Apply this structure to all sections in the text file, creating a clean HTML layout for each section with headings and paragraphs."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000
        )
        # Odbierz wygenerowany tekst z API
        generated_html = response['choices'][0]['message']['content'].strip()

        # Oczyść kod HTML z bloków ```html i ```
        cleaned_html = clean_html_code(generated_html)

        return cleaned_html
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Funkcja zapisująca wygenerowany HTML do pliku
def save_html(content, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Główna funkcja aplikacji
def main():
    # Ścieżka do pliku z artykułem
    article_path = 'tresc_artykulu.txt'
    # Ścieżka do zapisu wygenerowanego pliku HTML
    output_path = 'artykul.html'

    # Wczytaj pliki
    article_text = read_article(article_path)
    # Wygeneruj HTML
    generated_html = generate_html(article_text)
    # Zapisz wygenerowany HTML do pliku
    save_html(generated_html, output_path)

    print(f"Wygenerowany kod HTML zapisano w pliku {output_path}")

if __name__ == "__main__":
    main()
