# TODO


- [x] update fetch_data() to also search using a period delimited string
- [x] write clean_data() function that cleans the data
- [x] create an input_params() function to search for the movie, with given parameters such as resolution
- [x] update fetch_data() to use the input parameters
- [x] display to the user the options they have in table format, and allow them to enter the id they want
- [x] write magnetiser() to generate the magnet link
- [x] santise user's input
- [ ] document functions

## Notes

clean_data() - takes data as a list of tuples. Returns a dictionary with the id as the key.

magnetiser should return magnet string in the format "magnet:?xt=urn:btih:{HASH}&dn={NAME}"
