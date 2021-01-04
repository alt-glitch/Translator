import requests
import sys
from bs4 import BeautifulSoup
import argparse


def display(translation_list, examples_list, to_lang, word):
    print("Context examples:")
    file_out = sys.stdout
    f = open("{}.txt".format(word), "a")
    sys.stdout = f

    print("{} Translations:\n".format(to_lang.capitalize()))
    for i in translation_list:
        print(i)

    print("\n{} Examples:".format(to_lang.capitalize()))
    for j in range(10):
        if j % 2 == 0:
            print("\n")
            f.write("\n")
        print(examples_list[j])
    sys.stdout = file_out
    f.close()

    rf = open("{}.txt".format(word), "r")
    print(rf.read())
    rf.close()


def parse(r, to_lang, word):
    translation_list = []
    example_list = []

    soup = BeautifulSoup(r.text, 'html.parser')
    translations = soup.find(id="translations-content")
    examples = soup.find(id="examples-content")

    for translation in translations.find_all("a"):
        translation_list.append(translation.text.split()[0])

    for example in examples.find_all("div", class_="ltr"):
        example_list.append(" ".join(example.text.split()))

    display(translation_list, example_list, to_lang, word)


def send_request(to_lang, from_lang, word):
    base_url = "https://context.reverso.net/translation/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    url = "{}{}-{}/{}".format(base_url, from_lang, to_lang, word)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print(r.status_code, "OK")
            parse(r, to_lang, word)
        else:
            print(r.status_code, "Error")
            print("Sorry, unable to find", word)
            sys.exit()
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        sys.exit()


def translate_all(languages_available, from_lang, word):
    languages_available.remove(from_lang.capitalize())
    for to_lang in languages_available:
        send_request(to_lang.lower(), from_lang, word)


def check(from_lang, to_lang, languages_available):
    if from_lang.capitalize() not in languages_available:
        print("Sorry, the program doesn't support {}".format(from_lang))
        return -1

    elif to_lang.capitalize() not in languages_available and to_lang != "all":
        print("Sorry, this program doesn't support {}".format(to_lang))
        return -1
    else:
        return 0


def main():
    languages_available = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
                           "Portuguese", "Romanian", "Russian", "Turkish"]

    parser = argparse.ArgumentParser()
    parser.add_argument("from_lang")
    parser.add_argument("to_lang")
    parser.add_argument("word")
    args = parser.parse_args()

    from_lang = args.from_lang
    to_lang = args.to_lang
    word = args.word

    if check(from_lang, to_lang, languages_available) == -1:
        sys.exit()

    if to_lang == "all":
        translate_all(languages_available, from_lang, word)

    else:
        send_request(to_lang, from_lang, word)


if __name__ == '__main__':
    main()
