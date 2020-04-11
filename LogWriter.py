class LogWriter:
    @staticmethod
    def write_to_log_file_index(line_index, mark, playlist_download_log):
        log_file = open(playlist_download_log, "r")

        count = 0
        new_file_content = ""

        for line in log_file:
            stripped_line = line.strip()
            if count == line_index:
                stripped_line = stripped_line.replace(stripped_line, mark)
            new_file_content += stripped_line + "\n"
            count += 1

        new_file_content = new_file_content.rstrip()

        log_file.close()

        new_log_file = open(playlist_download_log, "w")
        new_log_file.write(new_file_content)
        new_log_file.close()

    @staticmethod
    def read_from_log_file_index(line_index, playlist_download_log):
        log_file = open(playlist_download_log, "r")

        count = 0
        line_read = ""

        for line in log_file:
            stripped_line = line.strip()
            if count == line_index:
                line_read = stripped_line
            count += 1

        log_file.close()
        return line_read
