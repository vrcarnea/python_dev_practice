
def scraper(page_url, target_url): 
    
    my_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    
    #grabbing the HTML and getting text 
    fantasy_page = get(page_url, headers = my_header)

    doc = lh.fromstring(fantasy_page.content)
    
    print(fantasy_page)
    
    #parsing table elements in the HTML inside the pattern "//tr" --> this is a table element 

    table_elements = doc.xpath('//tr')
    
    #creating an empty array to insert the table elements 
    cols = []
    i = 0 #setting the increment 

    for t in table_elements[1]:
        i+1
        name = t.text_content() #getting the column name from the HTML table 
        #print('%d:"%s"'% (i, name))
        cols.append((name, [])); 
        
        #Since out first row is the header, data is stored on the second row onwards

    for j in range(1,len(table_elements)):
        #T is our j'th row
        T=table_elements[j]

        #If row is not of size 24, the //tr data is not from our table 
        if len(T)!=len(table_elements[1]):
            break

        #i is the index of our column
        i=0

        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 

            #Append the data to the empty list of the i'th column
            cols[i][1].append(data)
            #Increment i for the next column
            i+=1
        
    #creating a dictionary for the columns in the parsed table 
    Dict={title:column for (title,column) in cols}

    df=pd.DataFrame(Dict)
    
    #data cleaning 
    df = df.drop(df.loc[df["Rk"] == 'Rk'].index)
    df = df.drop('', 1)
    
    #Grapping Parameters for looping 
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    
    #writing to google sheets 
    import time 

    #Now will can access our google sheets we call client.open on StartupName
    sheet = client.open_by_url(target_url) #2019-q4_fantasy-web-scraping/passing

    ws = sheet.get_worksheet(0)

    shaped_data = df.transpose()

    ws.insert_row(df.columns.tolist(), 1)

    for i in range(1, n_rows+1): 
        row = df.iloc[i-1].tolist()
        index = i+1
        if i%10 == 0: #printing the step in the loop
            print(i)  
            time.sleep(15)
            
        ws.insert_row(row, index) #writing the data 
    
    print('row ', i, ' end of file')
    time.sleep(45)