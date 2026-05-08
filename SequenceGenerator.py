import random

sequences = {}
stats = {}

def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    letters = "ACTG"
    return "".join(random.choice(letters) for _ in range(length))


def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics including gc_ratio_A."""
    # Filter out name characters (lowercase) for accurate stats
    dna_only = "".join([c for c in sequence if c.isupper()])
    seq_len = len(dna_only)

    if seq_len == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "gc_ratio_A": 0.0}

    # Internal key "gc_ratio_A" used as per formal requirements
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


def insert_name (sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
    Name written in lowercase letters."""
    name = name.lower()
    randpos = random.randrange(0, sequence.__len__())
    sequence = sequence[:randpos] + name + sequence[randpos:]
    return sequence


def format_fasta ( seq_id : str , description : str ,
                 sequence: str, line_width : int = 80) -> str:
    header = ">" + seq_id + " " + description + "\n"
    lines = [
        sequence[i : i + line_width]
        for i in range(0, len(sequence), line_width)
    ]
    body = "".join(lines)
    return header + body

def save_fasta (fasta: str,
                seq_id: str):
    filename = seq_id + ".fasta"
    with open(filename, "w") as f:
        f.write(fasta)

    """Returns a formatted FASTA record as a string."""

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


def run_analysis_pipeline(length, seq_id, desc, name, multi_file=None):
    """Executes the generation, analysis, and saving for a single sequence."""
    # 1. Generate
    raw_seq = generate_sequence(length)
    seq_with_name = insert_name(raw_seq, name)

    # 2. Stats
    current_stats = calculate_stats(seq_with_name)
    stats[seq_id] = current_stats
    sequences[seq_id] = seq_with_name

    # 3. Display
    print(f"\nSequence statistics (n={length}):")
    for key, val in current_stats.items():
        label = "GC-content" if key == "gc_ratio_A" else key
        print(f"{label}: {val:.2f}%")

    # 4. Features
    # find_motifs(seq_with_name)
    # rna = transcribe_to_rna(seq_with_name)
    # prot = translate_to_protein(seq_with_name)

    # 5. Format and Save
    fasta_main = format_fasta(seq_id, desc, seq_with_name)
    # fasta_rna = format_fasta(f"{seq_id}_mRNA", f"RNA transcription of {seq_id}", rna)
    # fasta_prot = format_fasta(f"{seq_id}_PROT", f"Translation of {seq_id}", prot)

    # final_output = fasta_main + fasta_rna + fasta_prot

    target_name = multi_file if multi_file else seq_id
    # save_fasta(final_output, target_name, mode="a" if multi_file else "w")
    print(f"Sequence saved to: {target_name}.fasta")

def main():
    """Main entry point: Handlings Batch Mode selection and program flow."""
    decision = input("Batch mode? (y/n): ").lower()

    if decision == "y":
        num_seqs = validate_positive_int("Enter number of sequences: ", 1, 100)
        batch_filename = "Batch_Results"
        for i in range(num_seqs):
            print(f"\n--- Sequence #{i + 1} ---")
            length = validate_positive_int("Enter sequence length: ", 1, 100000)
            seq_id, desc, name = perform_metadata_inputs()
            run_analysis_pipeline(length, f"{seq_id}_{i + 1}", desc, name, multi_file=batch_filename)
    else:
        length = validate_positive_int("Enter sequence length: ", 1, 100000)
        seq_id, desc, name = perform_metadata_inputs()
        run_analysis_pipeline(length, seq_id, desc, name)


if __name__ == "__main__":
    main ()
 
