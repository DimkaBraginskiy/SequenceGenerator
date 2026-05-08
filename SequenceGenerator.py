import random
import os

sequences = {}
stats = {}


def generate_sequence(length: int, distribution: dict = None) -> str:
    """Returns a random DNA sequence with optional weighted distribution."""
    letters = ["A", "C", "T", "G"]
    if distribution:
        weights = [distribution.get(base, 25.0) for base in letters]
        return "".join(random.choices(letters, weights=weights, k=length))
    return "".join(random.choice("ACTG") for _ in range(length))


def calculate_stats(sequence: str) -> dict:
    """Returns statistics using key 'gc_ratio_A' as per formal requirements."""
    dna_only = "".join([c for c in sequence if c.isupper()])
    seq_len = len(dna_only)
    if seq_len == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "gc_ratio_A": 0.0}

    results = {
        "A": round(dna_only.count("A") / seq_len * 100, 2),
        "T": round(dna_only.count("T") / seq_len * 100, 2),
        "C": round(dna_only.count("C") / seq_len * 100, 2),
        "G": round(dna_only.count("G") / seq_len * 100, 2)
    }
    results["gc_ratio_A"] = round(results["G"] + results["C"], 2)
    return results

def print_stats (stats: dict,
                 seq: str,
                 len: int):
    print(f"Sequence statistics:")

    for stat in stats:
        print(f"{stat}: {stats[stat]}%")


def insert_name(sequence: str, name: str) -> str:
    """Inserts a lowercase name at a random position."""
    name = name.lower()
    randpos = random.randint(0, len(sequence))
    return sequence[:randpos] + name + sequence[randpos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record."""
    header = f">{seq_id} {description}\n"
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    return header + "\n".join(lines) + "\n"


def save_fasta(fasta: str, seq_id: str, folder: str = None):
    """Saves the FASTA record into a specific folder if provided."""
    filename = f"{seq_id}.fasta"

    if folder:
        # Create the directory if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
        # Join the folder path and filename
        filepath = os.path.join(folder, filename)
    else:
        filepath = filename

    with open(filepath, "w") as f:
        f.write(fasta)

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        try:
            val = int(input(prompt))
            if not (min_val <= val <= max_val):
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
                continue
            return val
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")

"""Gets an integer from the user in a range.
In case of an error, repeats the question."""

def perform_metadata_inputs ():
    while True:
        seq_id = input("Enter sequence ID: ").strip()
        if not seq_id or ' ' in seq_id:
            print("Error: Sequence ID cannot be empty or contain spaces.")
            continue
        desc = input("Enter a description of the sequence: ")
        name = input("Enter your name: ").strip()
        if not name:
            print("Error: Name is required.")
            continue
        return seq_id, desc, name

def perform_single_input():
    len = validate_positive_int("Enter sequence length: ", 1, 10000)
    seq_id, desc, name = perform_metadata_inputs()

    seq = generate_sequence(len)
    print(seq)

    seq_with_name = insert_name(seq, name)
    print(seq_with_name)

    stats[seq_id] = calculate_stats(seq_with_name)
    print_stats(stats, seq_with_name, len)

    fasta = format_fasta(seq_id, desc, seq_with_name)
    save_fasta(fasta, seq_id)

def perform_batch_input():
    while True:
        seq_num = (int)(input("Enter a number of sequences: ")) - 1
        if(type(seq_num) != int or seq_num <= 0):
            print("Error: At least one character is needed for the Sequence number")
            continue
        break


    for i in range(seq_num):
        print(f"Sequence #{i+1}")
        perform_single_input()
        len = validate_positive_int("Enter sequence length: ", 1, 10000)
        seq_id, desc, name = perform_metadata_inputs()
        seq = generate_sequence(len)

        seq_with_name = insert_name(seq, name)

        sequences[seq_id] = seq_with_name
        stats[seq_id] = calculate_stats(seq_with_name)

        fasta = format_fasta(seq_id, desc, seq_with_name)
        save_fasta(fasta, seq_id)

    print("SEQUENCES:\n" + sequences.__str__())
    print("STATISTICS:\n" + stats.__str__())

def prompt_batch_mode():
    while True:
        decision = input("Batch mode? (y/n): ")
        if decision == "y":
            perform_batch_input()
            return
        if decision == "n":
            print("Continuing")
            perform_single_input()
            return
        else:
            print("Error: Invalid input")
            continue


def prompt_distribution() -> dict:
    """Prompts user for nucleotide percentages and validates the sum."""
    while True:
        print("\nEnter percentage distribution (must sum to 100):")
        try:
            a = float(input("Percentage of A: "))
            c = float(input("Percentage of C: "))
            g = float(input("Percentage of G: "))
            t = float(input("Percentage of T: "))

            if round(a + c + g + t, 2) == 100.0:
                return {"A": a, "C": c, "G": g, "T": t}
            else:
                print(f"Error: Sum is {a + c + g + t}%. It must be exactly 100%.")
        except ValueError:
            print("Error: Please enter numeric values.")


def find_motifs(sequence: str):
    """Searches for a motif and prints 1-based biological positions."""
    dna_only = "".join([c for c in sequence if c.isupper()])
    motif = input("Enter DNA motif to search for: ").strip().upper()
    if not motif: return

    positions = []
    start = 0
    while True:
        idx = dna_only.find(motif, start)
        if idx == -1: break
        positions.append(idx + 1)
        start = idx + 1
    print(f"Motif '{motif}' found at positions: {positions}" if positions else "Motif not found.")

    if positions:
        print(f"Motif '{motif}' found at positions: {positions}")
    else:
        print(f"Motif '{motif}' not found in the sequence.")
    return positions

def get_complement(sequence: str) -> str:
    """Returns the complementary DNA strand (A-T, C-G)."""
    dna_only = "".join([c for c in sequence if c.isupper()])
    pairs = str.maketrans("ACTG", "TGAC")
    return dna_only.translate(pairs)

def get_reverse_complement(sequence: str) -> str:
    """Returns the reverse complement of the DNA strand."""
    return get_complement(sequence)[::-1]


def run_analysis_pipeline(length, seq_id, desc, name, output_folder=None, distribution_decision="n"):
    # 1. Setup & Generate
    dist = prompt_distribution() if distribution_decision == "y" else None
    raw_seq = generate_sequence(length, dist)

    # 2. Statistics (on pure DNA)
    current_stats = calculate_stats(raw_seq)
    stats[seq_id] = current_stats
    print(f"\nSequence statistics (n={length}):")
    for key, val in current_stats.items():
        label = "GC-content" if key == "gc_ratio_A" else key
        print(f"{label}: {val:.2f}%")

    # 3. Features
    find_motifs(raw_seq)
    comp = get_complement(raw_seq)
    rev_comp = get_reverse_complement(raw_seq)

    # 4. Prepare FASTA Content
    seq_with_name = insert_name(raw_seq, name)
    main_record = format_fasta(seq_id, desc, seq_with_name)
    comp_record = format_fasta(f"{seq_id}_COMP", "Complementary strand", comp)
    rev_record = format_fasta(f"{seq_id}_REV_COMP", "Reverse complement", rev_comp)

    # Combine and add mandatory footer
    full_content = main_record + comp_record + rev_record

    # 5. Save
    filepath = f"{seq_id}.fasta"
    if output_folder:
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        filepath = os.path.join(output_folder, filepath)

    with open(filepath, "w") as f:
        f.write(full_content)
    print(f"File saved: {filepath}")


def main():
    batch_decision = input("Batch mode? (y/n): ").lower()
    dist_decision = input("Custom nucleotide distribution? (y/n): ").lower()

    if batch_decision == "y":
        num = validate_positive_int("Enter number of sequences: ", 1, 100)
        folder = "Batch_Results"
        for i in range(num):
            print(f"\n--- Sequence #{i + 1} ---")
            length = validate_positive_int("Length: ", 1, 100000)
            seq_id, desc, name = perform_metadata_inputs()
            run_analysis_pipeline(length, f"{seq_id}_{i + 1}", desc, name, folder, dist_decision)
    else:
        length = validate_positive_int("Length: ", 1, 100000)
        seq_id, desc, name = perform_metadata_inputs()
        run_analysis_pipeline(length, seq_id, desc, name, None, dist_decision)


if __name__ == "__main__":
    main()