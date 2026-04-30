import random


def generate_sequence (length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    letters = "ACTG"
    seq = ""

    for i in range(length):
        seq += random.choice(letters)

    return seq



def calculate_stats (sequence: str) -> dict :
    """Returns a dictionary of sequence statistics.
    Keys: "A", "C", "G", "T" ( float values , %),
    "GC" ( float value , %)."""

    stats = {
        "A" : 0,
        "C" : 0,
        "T" : 0,
        "G" : 0
    }

    for char in sequence:
        if char == 'A':
            stats["A"] += 1
        if char == 'C':
            stats["C"] += 1
        if char == 'T':
            stats["T"] += 1
        if char == 'G':
            stats["G"] += 1

    return stats

def print_stats (stats: dict,
                 seq: str,
                 len: int):
    print(f"Sequence statistics n={seq.__len__()}")






def insert_name (sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
    Name written in lowercase letters."""
    name = name.lower()

    randpos = random.randrange(0, sequence.__len__())

    sequence = sequence[:randpos] + name + sequence[randpos:]

    return sequence



def format_fasta ( seq_id : str , description : str ,
                 sequence: str, line_width : int = 80) -> str:
    """Returns a formatted FASTA record as a string."""

def validate_positive_int (prompt: str,
                          min_val : int = 1,
                          max_val : int = 100_000) -> int:
    while True:
        len = (int)(input("Enter sequence length: "))
        if min_val > len > max_val:
            print("Error: value must be an integer in the range [1, 100000].")
            continue
        break
    return len

    """Gets an integer from the user in a range.
    In case of an error, repeats the question."""

def perform_inputs ():
    while True:
        seq_id = input("Enter sequence ID: ")
        if seq_id.__len__() <= 0:
            print("Error: At least one character is needed for the Sequence ID")
            continue
        if  seq_id.__contains__(' '):
            print("Error: Sequence ID can not have a white space")
            continue

        desc = input("Enter a description of the sequence: ")
        name = input("Enter your name: ")
        if name.__len__() <= 0:
            print("Error: At least one character is needed for the Name")
            continue
        break

    return seq_id, desc, name



def main ():
    len = validate_positive_int(1, 10000)
    seq_id, desc, name = perform_inputs()

    seq = generate_sequence(len)
    print(seq)

    seq_with_name = insert_name(seq, name)
    print(seq_with_name)

    stats = calculate_stats(seq_with_name)
    print_stats(stats, seq_with_name, len)


if __name__ == "__main__":
    main ()
 
