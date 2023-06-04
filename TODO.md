# TODO


- [ ] update fetch_data() to also search using a period delimited string
- [ ] write clean_data() function that cleans the data
- [ ] update fetch_data() so that it can search for a resolution
- [ ] create an input_params() function to search for the movie, with given parameters such as resolution
- [ ] write magnetiser() to generate the magnet link

## Notes

clean_data() - takes data as a list of tuples. Returns a dictionary with the id as the key.

magnetiser should return magnet string in the format "magnet:?xt=urn:btih:{HASH}&dn={NAME}"
