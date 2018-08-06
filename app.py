import csv

if __name__ == "__main__":
    file_path = "data/csv/bio.csv"
    save_path = "data/processed/bio_processed.csv"
    headers = []
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
        i = 0
        section = []
        for row in reader:
            # process the row
            url = row[0]
            # Headers
            if i == 0:
                # add headers
                processed_data.append(row)
                column_count = len(row)
                print(column_count)
                i += 1
                continue

            # Sections
            if not url.startswith('http') and not url == '':
                if not section:
                    # If there is no info stored it is the first section
                    section_header = row
                    continue
                else:
                    # Tally the data, save and start a new section
                    total_sections += 1
                    section_name = section_header[0]
                    section_ending_pages = section_starting_pages - section_removed_pages
                    section_info = "{}: {} URLs ({} initially, {} removed)".format(section_name, section_ending_pages,
                                                                                   section_starting_pages,
                                                                                   section_removed_pages)

                    section_header[0] = section_info

                    # add the section header
                    processed_data.append(section_header)
                    i += 1
                    # add the section to data
                    for item in section:
                        processed_data.append(item)
                    # and reset section vars
                    section_starting_pages = 0
                    section_removed_pages = 0
                    section_ending_pages = 0
                    section_header = row
                    section = []
                    # append the new row to start a new section
            elif url == "":
                processed_data.append(row)
                empty = row
                i += 1
                continue
            # URLs
            elif url.startswith("http"):
                # this is a URL
                starting_pages += 1
                section_starting_pages += 1
                if not url.endswith("index.html"):
                    # keeper
                    section.append(row)
                    i += 1
                else:
                    section_removed_pages += 1
                    removed_pages += 1
                    i += 1
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
