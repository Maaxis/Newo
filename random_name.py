import random
def gen_name():
    adjectives = []
    nouns = []
    with open("adjectives.txt", "r") as f:
        adjectives = f.read().splitlines()
    with open("nouns.txt", "r") as f:
        nouns = f.read().splitlines()
    return (random.choice(adjectives) + "-" + random.choice(nouns)).lower()

if __name__ == "__main__":
    for i in range(100):
        print(gen_name())