class FileHandler:
    @staticmethod
    def write_to_file_index(line_index, mark, file_name):
        file = open(file_name, "r")

        count = 0
        new_file_content = ""

        for line in file:
            stripped_line = line.strip()
            if count == line_index:
                stripped_line = stripped_line.replace(stripped_line, mark)
            new_file_content += stripped_line + "\n"
            count += 1

        new_file_content = new_file_content.rstrip()

        file.close()

        new_log_file = open(file_name, "w")
        new_log_file.write(new_file_content)
        new_log_file.close()

    @staticmethod
    def read_from_file_index(line_index, file_name):
        file = open(file_name, "r")

        count = 0
        line_read = ""

        for line in file:
            stripped_line = line.strip()
            if count == line_index:
                line_read = stripped_line
            count += 1

        file.close()
        return line_read

    @staticmethod
    def append_to_a_file(mark, file_name):
        log_file = open(file_name, "a")
        log_file.write("\n" + mark)
        log_file.close()
