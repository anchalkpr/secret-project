import sys, os, ntpath, codecs


html_template = "<html>" + \
                "\n<head>\n<title>TITLE_TOKEN</title>\n</head>\n<body bgcolor=\"white\">\nPARAGRAPHS_TOKEN</body>\n" + \
                "</html>"
paragraph_template = "<a name=\"NUM_TOKEN\">[NUM_TOKEN]</a> <a href=\"#NUM_TOKEN\" id=NUM_TOKEN>SENTENCE_TOKEN</a>\n"
html_files_path_system = "/Users/anshulip/GitHub/secret-project/systems/"
html_files_path_model = "/Users/anshulip/GitHub/secret-project/models/"


def format_html(filename, dir_path, html_files_path):
    title = filename
    with codecs.open(dir_path + filename, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    paragraph = ""
    linecount = 1

    paragraph_template_copy = paragraph_template
    for line in lines:
        paragraph_template_copy = paragraph_template
        paragraph_template_copy = paragraph_template_copy.replace("NUM_TOKEN", str(linecount))
        paragraph_template_copy = paragraph_template_copy.replace("SENTENCE_TOKEN", line[:-1])
        paragraph += paragraph_template_copy
        linecount += 1

    title = filename[0: len(filename) - 4]

    html_template_copy = html_template
    html_template_copy = html_template_copy.replace("TITLE_TOKEN", title)
    html_template_copy = html_template_copy.replace("PARAGRAPHS_TOKEN", paragraph)
    print(html_template_copy)

    html_filename = title + ".html"
    writer = codecs.open(html_files_path + html_filename, 'w', encoding='utf-8')
    print(html_files_path + html_filename)
    writer.write(html_template_copy)
    writer.close()


def batch_format(dir_path, html_files_path):
    file_set = set()
    for file_path in os.listdir(dir_path):
        file_name = ntpath.basename(file_path)
        if file_name.endswith(".txt"):
            file_set.add(file_name)

    while len(file_set) > 0:
        filename = file_set.pop()
        format_html(filename, dir_path, html_files_path)
    pass


#format_html("anti-human-trafficking_english.txt")
batch_format("/Users/anshulip/GitHub/secret-project/Data/human_summaries/", html_files_path_model)
batch_format("/Users/anshulip/GitHub/secret-project/Data/generated_summaries/", html_files_path_system)
