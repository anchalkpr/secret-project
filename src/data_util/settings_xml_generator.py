import sys, codecs


file_template = "<EVAL ID=\"EVAL_ID_TOKEN\">\n" + \
                "<MODEL-ROOT>models</MODEL-ROOT>\n" + \
                "<PEER-ROOT>systems</PEER-ROOT>\n" + \
                "<INPUT-FORMAT TYPE=\"SEE\">  </INPUT-FORMAT>\n" + \
                "<PEERS>\n" + \
                "<!--" + \
                "<P ID=\"1\">TOPIC_TOKEN_english_summary_1.html</P>\n" + \
                "<P ID=\"2\">TOPIC_TOKEN_english_summary_2.html</P>\n" + \
                "-->" + \
                "<p ID=\"3\">TOPIC_TOKEN_english_summary_3.html</p>\n" + \
                "</PEERS>" + \
                "<MODELS>" + \
                "<M ID=\"1\">TOPIC_TOKEN_english_summary_baseline.html</M>\n" + \
                "<!--" + \
                "<M ID=\"2\">TOPIC_TOKEN_english_summary_LDA.html</M>\n" + \
                "-->" + \
                "</MODELS>\n" + \
                "</EVAL>\n"

topics_list_file = "topics_list.txt"
with codecs.open(topics_list_file, 'r', encoding='utf-8') as topicsfile:
    topics_list = topicsfile.readlines()

setting_xml = "<ROUGE_EVAL version=\"1.55\">"

for topic in topics_list:
    eval_xml = file_template
    eval_xml = eval_xml.replace("EVAL_ID_TOKEN", topic)
    eval_xml = eval_xml.replace("TOPIC_TOKEN", topic)
    setting_xml += eval_xml


setting_xml += "</ROUGE_EVAL>"
print(setting_xml)
