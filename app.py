import csv
import os

if __name__ == "__main__":
    csv_directory = "data/csv/"
    save_directory = "data/processed/"

    for file_name in os.listdir(csv_directory):
        save_file_name = file_name.split('.')[0] + '_processed.csv'
        file_path = csv_directory + file_name
        save_path = save_directory + save_file_name

        total_sections = 0
        starting_pages = 0
        removed_pages = 0
        ending_pages = 0
        section_starting_pages = 0
        section_removed_pages = 0
        section_ending_pages = 0
        section_name = ""
        section_header = ""
        processed_data = []
        empty = []

        with open(file_path, encoding='utf8', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            # Headers
            headers = next(reader)
            data = [row for row in reader]
            processed_data.append(headers)
            section = []
            for row in data:
                url = row[0]
                # Sections
                if not url.startswith('http') and not url == '':
                    if not section:
                        # If there is no info stored it is the first section
                        section_header = row
                        continue
                    else:
                        # Not the first section, count, save and start a new section
                        total_sections += 1
                        section_name = section_header[0]
                        section_ending_pages = section_starting_pages - section_removed_pages
                        section_info = "{}: {} URLs ({} initially, {} removed)".format(section_name,
                                                                                       section_ending_pages,
                                                                                       section_starting_pages,
                                                                                       section_removed_pages)

                        section_header[0] = section_info

                        # add the section header
                        processed_data.append(section_header)
                        # add the section to data
                        for item in section:
                            processed_data.append(item)
                        # and reset section vars
                        section_starting_pages = 0
                        section_removed_pages = 0
                        section_ending_pages = 0
                        section_header = row
                        section = []
                elif url == "":
                    processed_data.append(row)
                    empty = row
                    continue
                # URLs
                elif url.startswith("http"):
                    # this is a URL
                    starting_pages += 1
                    section_starting_pages += 1
                    if not url.endswith("index.html"):
                        # this is a keeper
                        section.append(row)
                    else:
                        section_removed_pages += 1
                        removed_pages += 1
                        continue

        row = empty
        # add final info
        ending_pages = starting_pages - removed_pages
        file_info = "{}: {} URLs total across {} sections ({} processed, {} removed)".format(file_path,
                                                                                             ending_pages,
                                                                                             total_sections,
                                                                                             starting_pages,
                                                                                             removed_pages)

        # write file
        processed_file = open(save_path, 'w', encoding='utf8')
        with processed_file:
            writer = csv.writer(processed_file)
            writer.writerows(processed_data)

        # log file info
        log_path = "data/processed/log.txt"
        log_file = open(log_path, 'a')
        log_file.write(file_info + "\n\n")
