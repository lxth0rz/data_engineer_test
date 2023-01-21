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

- There is a chance just data can be extracted directly from an endpoint.
![image](https://user-images.githubusercontent.com/7511696/213869937-6d676c94-190b-499f-9e15-50916f6e9406.png)

- Regular expressions required further improvments.

- Refactoring the `_extracting_data` function.
