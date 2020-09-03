output_file = open("machine_learning_data_preprocessed_text.txt", 'a')
with open("machine_learning_data_raw_text.txt", 'rU') as fIn:
    for line in fIn:
        output_file.write(line.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").replace("'", " ").replace("\"", " ").replace("  ", " ").replace("  ", " "))