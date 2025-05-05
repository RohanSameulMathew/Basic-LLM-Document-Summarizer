# LLM document analyser

**Description:** 

docsum.py is a command-line tool that uses meta's llama to generate concise summaries of various file types, including .txt, .pdf, .html, images, and URLs. It extracts readable text from the input, splits it into manageable chunks if the text is too long, and returns a short summary based on the prompt. For images, it uses base64 encoding to analyze content directly or from a URL.

## How to use:
Download the python file and install all the libraries provided in requirements.txt

You will also need to go to groq.com and create an account and API key

After that, run the python code in the terminal by typing 

```bash
$ python3 llm.py filename/website_url

```


## Examples

```bash
$ python3 llm.py news-mx.html
There is no text to summarize, but based on one of the URLs, it appears that a US court ruling related to Trump's use of a wartime law from 1798 for deportations was made by a divided Supreme Court. The decision allowed Trump to continue using the law.
```

```bash
$ python3 docsum.py docs/constitution-mx.txt
The Mexican government published decrees in 1999 reforming various articles of its constitution, including those related to the judiciary and federal powers. The decrees outlined transitional provisions for implementing the changes, including establishing a new entity for fiscal oversight.
```

```bash
$ python3 docsum.py docs/research_paper.pdf
The paper evaluates the performance of various text embedding models, including DOCSPLIT, on five datasets for few-shot text classification, achieving state-of-the-art results. DOCSPLIT outperforms other models with significant improvements in macro-F1 scores, particularly in few-shot learning settings.
```

```bash
$ python3 docsum.py https://elpais.com/us/
The given URLs from El País cover various topics including fashion, entertainment, and food. The articles discuss upcycling, LGBTQ+ experiences, Andy Kaufman's life, and food-related content such as menus and fermented foods.
```

```bash
$ python3 docsum.py https://www.cmc.edu/sites/default/files/about/images/20170213-cube.jpg
The image depicts a modern building with a glass-walled structure in the center, surrounded by a pool of water and a walkway. The building is situated in a courtyard setting, with other buildings visible in the background.
```
