# text-steganography

[Try the Web](https://edthedev254.github.io/text-steganography/) 

Above is the web version of the text stego tool. It has a simple UI, and I have been trying to make it work with GitHub Pages. I have tweaked it a little bit so that even the text hidden by the Tkinter version will work with it. 

I will also tweak the Tkinter version to work with the web version because the web will use a different marker for an invisible character.

##Requirements
  1. Python Version - Python 3.6 or higher is required (for UTF-8 handling and modern string formatting).
  2. Dependencies - This project uses the Tkinter library for the graphical interface.

## 💻 How to Run

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/EdTheDev254/text-steganography
    cd text-steganography
    ```
2.  **Run the application:**
    ```bash
    python main.py
    ```

## 📖 Usage
1.  **Hide Message:** Enter your secret (e.g., a password or emoji) and a cover sentence. Click "Hide Message" and copy the result.
2.  **Reveal Message:** Paste the "container" text into the Reveal tab and click "Reveal Hidden Message" to extract the secret.
