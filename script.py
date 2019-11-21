#! /usr/bin/python3

'''
Use requests lib to pull data from URL
Use beautiful soups to parse the data.
Filter the data using an external csv file of keywords
Export the filtered data to a new csv file in column format
'''

from bs4 import BeautifulSoup
import requests # find_all() get_text()
import datetime # needed for timestamp in output.csv

print("script running...")
result_count = 0
date_not_written = True

#import keywords from external csv file in a list, replace spaces with + for easy url insertion
file_of_keywords = open("keywords.csv", 'r')
keywords = []
for item in file_of_keywords:
    keywords.append(item.strip().lower().replace(" ","+"))
file_of_keywords.closed

# empty output file to ready it for new data.
with open("output.csv", "w"):
    pass

def get_content(search_term):
    global result_count
    global date_not_written

    # Use request lib to get homepage content, do your url research
    url = "https://www.bing.com/news/search?q=" +\
        search_term +\
        "&qft=interval%3d\"8\"&form=PTFTNR"
    first_request = requests.get(url)
    first_results = first_request.content

    # Use BeautifulSoup to parse the content
    soup1 = BeautifulSoup(first_results, "html5lib")

    # store the useful data in a list, remove the commas for easy csv export
    # Do your html/css research for appropriate tags
    bing_list = []
    for a_tag in soup1(class_='title', href=True):
        current_headline = a_tag.text.strip().lower().replace(',',"") + ','
        current_url = a_tag['href']

        bing_list.append(current_headline)
        bing_list.append(current_url + "\n")
        result_count += 1

    # export data to .csv as well as website name as a header
    #open local file in append mode
    with open("output.csv", "a") as local_file:
        if date_not_written:
            # add stamp to new export data
            todays_date = str(datetime.datetime.now().date())
            local_file.write(str(todays_date) + "," + '\n') 
            local_file.write("TITLE,URL\n")
            date_not_written = False

        # append data to file in column format
        for data in bing_list:
            local_file.write(data)

for each_keyword in keywords:
    get_content(each_keyword)

print("script completed. " + str(result_count) + " results returned.")
exit(0)
