### Manipulating the html

#### Defining the function(s)
#Here is the original code where the following functions are defined: https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
#We don't need to use the 'parse_url' function since we have to parse the URL differently. In future we should write our own version of the function though - essentially one function call to produce the desired table.
#Currently this function does not quite work as required, the number of columns does not work automatically and must be manually entered.

#def parse_url(self, url):
#    response = requests.get(url)
#    soup = BeautifulSoup(response.text, 'lxml')
#    return [(table['id'],self.parse_html_table(table))\
#            for table in soup.find_all('table')]  

def parse_html_table(self, table, def_cols = -1):
    n_columns = 0
    n_rows=0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):

        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                if (def_cols == -1):
                    n_columns = len(td_tags)
                else:
                    n_columns = def_cols

        # Handle column names if we find them
        th_tags = row.find_all('th') 
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text().strip())

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,
                      index= range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.get_text().strip()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    # Convert to float if possible
    for col in df:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass

    return df