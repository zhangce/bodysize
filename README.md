bodysize
========

This applicaiton assumes a database with the name `bodysize`.
You can first import the DB from the file bodysize.sql

##Tables

`words`: The text content of a document

     Column | Type | Modifiers 
    --------+------+-----------
     docid  | text | 
     wordid | text | 
     word   | text | 
     sentid | text | 

`captions`: Information parsed from the caption of a document

     Column | Type | Modifiers 
    --------+------+-----------
     docid  | text |      e.g., H.html/H.html
     figure | text |      e.g., 497
     label  | text |      e.g., 4c
     mag    | text |      e.g., 15
     phrase | text |      e.g., oxoplecia gouldi
     prov   | text |      e.g., Fig. 497,4c. O. gouldi Ulrich & Cooper, Caradoc, Oklahoma; detail of ornament on dorsal valve, XI5 (new).

`figures`: Figure measurements extracted from the vision component

       Column   | Type | Modifiers 
    ------------+------+-----------
     docid      | text |      e.g., H.html/H.html
     figurename | text |      e.g., 381
     label      | text |      e.g., 2a
     major      | text |      e.g., 65.362667
     minor      | text |      e.g., 43.349333
