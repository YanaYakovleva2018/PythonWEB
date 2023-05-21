import json

from models import Author, Quote


def seed_authors_data(path):
    with open(path, "r", encoding="utf-8") as fd:
        authors = json.load(fd)

        for author in authors:
            record = Author(fullname=author.get("fullname"),
                            born_date=author.get("born_date"),
                            born_location=author.get("born_location"),
                            description=author.get("description"))
        record.save()


def seed_quotes_data(path):
    with open(path, "r", encoding="utf-8") as fd:
        quotes = json.load(fd)

        for q in quotes:
            author = Author.objects(fullname=q.get("author", None))
            record = Quote(tags=q.get("tags"),
                            quote=q.get("quote", None),
                            author=author[0])
        record.save()


if __name__ == "__main__":
    seed_authors_data("authors.json")
    seed_quotes_data("quotes.json")

