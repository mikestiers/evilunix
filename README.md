# evilunix
Detect and repair files on OS X with extended attribute issues (aka "Unix Executable file")

Some files that were pulled from archives were missing their fork data / extended attributes.  Most of them were fonts, but it was certainly not exclusive.  The symptoms are as follows:

File is listed as "Unix Executable File" under file type in OS X Finder when it should have an association
Font file is 0k in size, but still works (font data is in the metadata of the file)

Unix is not evil, but the problem was and it put the validity of a very large archive into question.  This was able to bring some confidence back to the data.
