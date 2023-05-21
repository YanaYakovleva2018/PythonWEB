import redis
from redis_lru import RedisLRU
from mongoengine import DoesNotExist
from models import Quote, Author

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_name(value):
    try:
        author = Author.objects(fullname__startswith=value.title())[0]
        quotes = Quote.objects(author=author)
        if quotes:
            result = []
            for quote in quotes:
                r = f"{quote.quote}\n{quote.author.fullname}     tags:{', '.join(quote.tags)}"
                result.append(r)
            return result
    except DoesNotExist:
        print(f'Author {value} was not found')

@cache
def find_by_tag(value):
    try:
        result = []
        for quote in Quote.objects(tags__startswith=value):
            r = f"{quote.quote}\n{quote.author.fullname}     tags: {', '.join(quote.tags)}"
            result.append(r)
        return result
    except DoesNotExist:
        print(f'Tag:{value} was not found')

@cache
def find_by_tags(value):
    try: 
        result = []
        for quote in Quote.objects():
            for tag in quote.tags:
                if tag in value.split(","):
                    r = f"{quote.quote}\n{quote.author.fullname}      tags: {', '.join(quote.tags)}"
                    if r not in result:
                        result.append(r)
        return result
    except DoesNotExist:
        print(f'Tags:{value} do not exists')

if __name__ == "__main__":
    while True:
        user_input = input("Command: ").strip().lower()
        if user_input == "exit":
            print('Good bye!')
            break
        else:
            try:
                command, value = user_input.split(":")
                command, value = command.strip(), value.strip()

                if command == "name":
                    print(find_by_name(value))
                elif command == "tag":
                    print(find_by_tag(value))
                elif command == "tags":
                    print(find_by_tags(value))                   
            except Exception as err:
                print(err)
    