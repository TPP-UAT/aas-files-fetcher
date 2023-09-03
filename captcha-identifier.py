from bs4 import BeautifulSoup

try:
    with open('captcha.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("The specified file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

# Parse the raw html into a BeautifulSoup object
soup = BeautifulSoup(content, "html.parser")

# Extrae todo el texto del objeto BeautifulSoup
text = soup.get_text()
print(text)

# Busca el texto deseado en el texto extraído
text_to_find = "We apologize for the inconvenience..."
if text_to_find in text:
    print(f"Encontrado: {text_to_find}")
else:
    print(f"No se encontró: {text_to_find}")
