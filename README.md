# Task 1: Parsing HTML
## Scraping and Parsing HTML to Extract Painting Information and Create a Dataframe using Python

### Requirements
- Task: You will scrape and process simple html page located here `candidateEvalData/webpage.html`
- Output: A dataframe of 1 row and 8 columns where the columns are:
    1. The name of the artist (e.g. Peter Doig)
    2. The name of the painting (e.g. The Architect's Home in the Ravine)
    3. Price realised in GBP (e.g. 11 282 500)
    4. Price realised in USD (e.g. 6 370 908)
    5. Estimates in GBP (e.g. 10 000 000, 15 000 000)
    6. Estimate in USD (e.g. 14 509 999, 21 764 999)
    7. The url of the image of the painting
    8. Saledate of the painting (e.g. 2016-02-11)

### Task Breakdown

To parse the HTML, we will use the `requests` and `lxml` libraries. The `requests` library will be used to send
an HTTP request to the webpage and retrieve the HTML content. The `lxml` library will then be used to parse the HTML
content and extract the relevant information.

First, we will import the necessary modules and retrieve the HTML content from the webpage using the `requests.get()` method.
Then, we will use the `html.fromstring()` method from the `lxml` library to create an HTML tree that we can traverse
and extract the information from.

Next, we will use various xpath selectors to extract the information for each column. For example, to extract
the artist name, we can use the xpath selector `//span[@class='artist-name']/text()` to find the span element with
the class `artist-name` and retrieve its text content. We will repeat this process for each column
using appropriate xpath selectors.

Finally, we will use the `pandas` library to create a dataframe with the extracted information, and format the
information as necessary (e.g. converting prices to numeric values and converting the date string to a `datetime` object).

### Possible Improvements

- There is a chance that data can be extracted directly from an endpoint. I didn't digg much further.
![image](https://user-images.githubusercontent.com/7511696/213869937-6d676c94-190b-499f-9e15-50916f6e9406.png)

- Regular expressions require further improvements to handle more cases.

- ~~Refactoring the `_extracting_data` function.~~ Done Perfectly!

- Refactoring the `_post_processing` function.
   - Change the post-processing of the fields to be using their types rather than their names.

- ~~Move all the Xpaths to a config file.~~ Done Perfectly!

- Finding any remaining hardcoded strings in the script that could be moved in a config file.

Task Title: 2. Regex
====================

### Task Title: 2. Regex
### Requirement: write a regex to process the string in rawDim to extract the height, width and the depth (as float64 integers).
### Bonus: Is there a single regex for all 5 examples ?

The task is focused on using regular expressions (regex) to extract specific information from a string. The goal is to extract the height, width, and depth of an object as float64 integers from a string in the "rawDim" column of a DataFrame.

The DataFrame is read from a CSV file located in the "candidateEvalData" directory within the parent directory of the current working directory. The script starts by importing the os and pandas module, then it uses the os module to get current working directory, then it uses the os.path module to get the parent directory, then it appends the file path to the dim_df_correct.csv file using os.path.join(). Then it reads the file using pandas and prints the dataframe.

The task includes a bonus challenge to see if a single regex can be used to extract the information from all 5 examples. This will test your regex skills and ability to handle different variations of the input string.