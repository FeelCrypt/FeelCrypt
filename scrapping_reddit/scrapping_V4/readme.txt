#### Version V4 ####
Goal is to make a script executable daily so it scraps only new comments, even on already
scrapped posts


## Plan ##

>| save every comments ID, grouped per post
	>| create a folder commment manager
	>| create a file named as the post ID
	>| save every comment ID in the file
> check if a post has new comments
	>| Function to count the already scrapped comments for 1 post ID
		>| get length of file
	> ?? or save the count somewhere (more files, but less calculation)
	> |function ask reddit api the nb of comments (or in code)
		>| recursive function to count all comments for a post
	> ?? Maybe if a post is older than, then do not even count (because old posts
	  usualy do not have new comments
		> Check the max time gap between a post creation and its latest comment
> if nb of comments is different : scrap new comments
	> |if condition for the loop
	> check if a comment has been scrapped
		> compare each id returned by api with the already scrapped comment id list
	> if not scrapped
		> scrapp comment
		> add ID to the list
		> update total comment counter
			> create function to add a to the comment counter

