This desktop app will be used to convert easely timetables to gtfs

Things to do in order:
The program should only take care of UTF-8 files. In input and in output. -DONE
There should be a function to verify if stops names look alike and ask the user if they're the same. -DONE
Every time the user is asked, the user's feedback should be put in files so that the program won't ask again. -DONE
There should be an option to fuse stops by performing a check on the files mentioned above. -DONE
Trips's id should be "line-service-tripNumber" two trips can be like "3-W-12" et "3-S-12" without conflict.
There should be an option to delete lines or trips.
After the print in the files, there should be something to show the structure of the agency object, like:
Agency_id:
----->Route 1
	----> W : 32 trips
	----> S : 13 trips
----->Route 2
	----> WSD: 33 trips
and so on. It'll be easier to check that the program is not doing anything crazy.
Add an option to remove trips which have the same start and end (and service).
Check if there is a way to facilitate adding regular trips.

Add a graphical interface

Machine learning stuff