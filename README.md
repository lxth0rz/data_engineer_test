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

### Solution Breakdown

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

- Write Tests

# Task 2: Regex
====================

#### Requirements: 
write a regex to process the string in rawDim to extract the height, width and the depth (as float64 integers).
#### Bonus: Is there a single regex for all 5 examples ?

The task is focused on using regular expressions (regex) to extract specific information from a string. The goal is to extract the height, width, and depth of an object as float64 integers from a string in the "rawDim" column of a DataFrame.

The DataFrame is read from a CSV file located in the "candidateEvalData" directory within the parent directory of the current working directory. The script starts by importing the os and pandas module, then it uses the os module to get current working directory, then it uses the os.path module to get the parent directory, then it appends the file path to the dim_df_correct.csv file using os.path.join(). Then it reads the file using pandas and prints the dataframe.

The task includes a bonus challenge to see if a single regex can be used to extract the information from all 5 examples. This will test your regex skills and ability to handle different variations of the input string.

### Solution Breakdown:

Added a regex function to extract height, width, and depth from the 'rawDim' column of a DataFrame. 
The function uses different regex patterns to match different formats of the rawDim string. The function 
also converts the extracted values from inches to centimeters if necessary. The script starts by importing 
the os, re and pandas module, then it uses the os module to get current working directory, then it uses the 
os.path module to get the parent directory, then it appends the file path to the dim_df_correct.csv file using 
os.path.join(). Then it reads the file using pandas and prints the dataframe.

Tne next `patterns_dict` is a dictionary that contains different regular expressions (regex) for extracting information from a 
string. The goal is to use these regex patterns to extract the height, width, and depth of an object as numbers from 
a string in a DataFrame.

```
patterns_dict = {'19×52cm': r"(\d+)×(\d+)×*(\d*)\s*(\w{2})",
                 "50 x 66,4 cm": r"([\d,]+)\sx\s([\d,]+)\s*([\d,]*)\s*(\w{2})",
                 "168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)": "([\d\.]+)\sx\s([\d\.]+)\sx\s([\d\.]+)\s*(\w{2})",
                 "Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)": "(\d+\.\d+)\s×\s(\d+\.\d+)\s×*\s*(\d*\.*\d*)\s*(\w{2})\)$",
                 "5 by 5in": "(\d+)\sby\s(\d+)\s*(\d*)(\w{2})",}
```
                 
Each key in the dictionary is a string that represents a different format of the information, and the corresponding 
value is the regex pattern used to extract the information from that format.

The code then uses the function extract_dim() which takes in a string from the DataFrame column rawDim and uses the 
patterns_dict to select the appropriate regex pattern to use for that string. The function then uses the re.compile() 
and search() methods to find a match for the regex pattern in the input string and extracts the height, width, and 
depth as floats using the match.group() method. The extracted values are then passed to the function format_dim() 
which converts the values to centimeters if the unit of measurement is inches.

### Possible Improvements

- Bonus: Is there a single regex for all 5 examples ?
  -- My very first trail leads to the next regex
  ~~`([\d\.,]+)\s*(?:×|x)\s*([\d\.,]+)\s*(?:×*|x*)\s*([\d\.,]*)(\w{2})|(\d+)\sby\s(\d+)\s*(\d*)(\w{2})`~~
  --- Only two tweaks remaining is to fix it for the 2nd capturing group for the third string then to capture the last group only for the forth string.
  --- Then, finally re-write it and try to find more ways to improve it.
  The next regex works much better for all of them
 `([\d\.,]+)\s*(?:×|x)\s*([\d\.,]+)\s*(?:×|x)*\s*([\d\.,]*)\s*(\w{2})\s*|(\d+)\s*by\s*(\d+)\s*([a-z]{2})`
  - In order for the above regex to work for them all, you need to extract the last group for the forth string `Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)`
    also despite that the above regex is working on them all in a regex editor, however, in Python if fail to capture the last string
     
- Code refactor
- Moving regex to a config file.
- Write Tests
- 
# Task 3: Web crawler
====================

### Requirements : 
This task involves creating a Scrapy spider to scrape information about artworks available for sale on 
the website https://www.bearspace.co.uk/purchase. The spider will navigate to the individual detail pages of each artwork, 
where information such as the title, media, dimensions, and price will be scraped. The collected information will be 
returned in a dataframe with the following columns: "url", "title", "media", "height_cm", "width_cm", and "price_gbp". 
The dataframe will have a shape of (n,6), where n is the total number of works available for purchase on the website. 
The spider will use Scrapy, a Python framework for web scraping, to extract the data and return it in a structured format.



### Solution Breakdown

        # Scrapy ItemLoader is a powerful tool that makes it easy to extract and process data from web pages, and it is widely used in web scraping projects.
        # Some benefits of using ItemLoader include:
        # Simplified item population: ItemLoader allows you to specify field-specific loaders, which can handle different types of data, such as text, numbers, and URLs. This makes it easy to extract and clean data without having to write custom code.
        # Reusability: ItemLoader can be reused across multiple spiders, allowing you to define your item processing logic in one place and reuse it throughout your project.
        # Modularity: ItemLoader allows you to define custom input and output processors for each field, which can be used to clean, validate or modify the data as it is loaded into the item.
        # Extensibility: ItemLoader is extensible, you can define custom loaders and processors for your specific needs.
        # Auto-populating fields: ItemLoader automatically populates fields that are defined in the item.
        # Flexible input: ItemLoader can handle data from multiple sources, such as response objects, lists, or dictionaries, making it easy to extract data from different types of web pages.

what is this regex capture
`height\s*(\d+)cm\s*x\s*width\s*(\d+)cm|([WHwhcmCMs\d\.]{1,6})\s*(?:x|X)\s*([WHwhcmCMs\d\.]{1,6})|(\d{2,3})\s*cm.*?diam`
            # Complex regex expression used to match dimensions and media, for ex: -but not limited to-
            # '99x99 cm'
            # '100cm x 80cm'
            # '38x32cm'
            # 'height 70cm x width 100cm'
            # '92X45 CM'
            # '58W x 85.5Hcm'
            # '30cm  diam '

### Possible Improvements

@@@ list all different cases of width and height
- Improve how the spider extracts width, height and media, may be using  the Jaccard similarity using NLTK similarity check
- Move Xpath to a config file or Settings.py
- Adding a config/mode to test only one artwork details URL.
- Adding a config/mode to test only one overview page URL.
- Adding more advanced data cleaning in the post processing.
- Adding a ref-url of the overviwepage URL that we extracted the current deatils url from *helps in further debugging in the future*
- Write Tests
- https://www.bearspace.co.uk/product-page/portal-8-by-jane-ward DIAM check