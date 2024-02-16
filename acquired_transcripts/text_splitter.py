import os

def split_into_chunks(file_path, approx_chunk_size=900):
    """
    Splits the file at file_path into chunks at newline characters, 
    with each chunk being approximately 900 characters long but may be longer to complete the line.
    Each chunk is saved as a separate file in the 'chunks' directory and begins with the original file's name.
    """
    # Create 'chunks' directory if it does not exist
    if not os.path.exists('chunks'):
        os.makedirs('chunks')

    # Extract filename without the .txt extension
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.readlines()

    current_chunk = [f"Title: {base_filename}\nBody:\n"]
    current_count = 0
    chunk_index = 0

    for line in file_content:
        current_count += len(line)
        if current_count >= approx_chunk_size:
            # Write the current chunk to a file
            chunk_file_name = f"chunks/{base_filename}-{chunk_index}.txt"
            with open(chunk_file_name, 'w', encoding='utf-8') as chunk_file:
                chunk_file.write(''.join(current_chunk))
            print(f"Chunk {chunk_index} written to {chunk_file_name}")

            # Reset for the next chunk
            current_chunk = [f"Title: {base_filename}\nBody:\n"]
            current_count = len(line)
            chunk_index += 1
        current_chunk.append(line)

    # Write any remaining content as a final chunk
    if len(current_chunk) > 1:  # There is more than just the header
        chunk_file_name = f"chunks/{base_filename}-{chunk_index}.txt"
        with open(chunk_file_name, 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(''.join(current_chunk))
        print(f"Final chunk {chunk_index} written to {chunk_file_name}")

def process_all_txt_files():
    """
    Processes all .txt files in the current directory.
    """
    for file in os.listdir('.'):
        if file.endswith('.txt'):
            split_into_chunks(file)

# Run the function to process all .txt files
process_all_txt_files()
