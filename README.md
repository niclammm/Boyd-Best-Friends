# Boyd Best Friends
 The bestest of Boyds students

For police officers, they just need to open the website and select the corresponding police station and click "Go To Map". this will display the patrol route. 

For backend, the user is required to input a txt file. The file is separated into 2 sections. The first section is the list of coordinates and requires 3 fields per data point: Coordinate Name, X coordinate, Y coordinate. The second part of the txt file is the list of edges. It is of the form First Coordinate, Second Coordinate, Edge Weight. Upon running the python code, it will prompt the user for the input file. After users enter the input file name, it will generate the google sheet with coordinates. Then, googlesheetstofolial.py is ran to generate the html map from the google sheets, which can be viewed from the webpage.

**GOOGLE SERVICE ACCOUNT DETAILS OMITTED**