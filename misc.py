import random, string

def gen_random_password(length: int) -> str:
    all = string.ascii_lowercase+string.ascii_uppercase + \
        string.digits+string.punctuation
    return "".join(random.sample(all, length))