
# S3 Upload

    Created for an assessment. Upload a directory to an AWS bucket without losing the directory structure.

## Set Up

  
At the top of uploadDirectory.py fill in the values below. (DIR_PATH is the path of the directory you wish to upload (ex: DIR_PATH = r"C:\Users\Jensen\Desktop\dmAssesment\data").

	S3_BUCKET = ""
	DIR_PATH = r""
	ACCESS_ID = ""
	ACCESS_KEY=""

I used Python 3.7 in Spyder, but the the script uploadDirectory.py should be good to run outside of Spyder and in different Python versions (the async version is 3.4+).

 You'll need to install boto3 to run uploadDirectory.py.

# Tools

Python: I'm not an expert in Python, but I know it's a popular language to use with AWS and is supposed to be fairly fast with it.

Boto3: AWS SDK for Python.


# Train of Thought

Signed up for AWS, started up Spyder, got a list of files within a directory, and iteratively called boto3's upload_file. This took about two hours with setting up and looking up information/docs.

Wow. That was incredible slow. Six and a half minutes for 20 MBs of data…..

What's the problem?

Seems too extreme to be the case but upload_file, while it uses multiple threads to upload, is a blocking method and the files are uploading one by one.

## How to make it faster?

Asynchronous concurrency or multiple/parallel threads or processes. I originally thought I using async concurrency might be an appraoch but came to the conclusion that it shouldn't matter since I didn't realize that the calls I was making would be blocking.

I'm not sure if async concurrency will actually do anything, but let's go for it. It's less machine reliant (as opposed to threads - how many threads to use varies by machine) and simpler to me (managing threads, especially since boto's upload_file defaults to 10 threads so 10 calls = 100 threads unless it works different under the hood or I change the config).

On the flip side, I think dynamically assigning upload's a # of threads based on the file's size and threads available from that machine (would have to be a config set by the user of the code) would be superior but also more difficult to implement. (potential resource: [http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/](http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/))

## Async:

Python async docs: [https://docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

Had to use nest_asyncio to use asyncio (specifically asyncio.run) in spyder because it can't run when a even loop is already running. Other than that the coding went smoothly.

Except…. It was even slower (likely the same speed and slower by chance) at almost 7 minutes. I'm not surprised as I was doubtful going in. It obviously isn't functioning as intended: upload_file is clearly still blocking. My best guess is that it's thread use/management doesn't allow for async concurrency to run the methods concurrently.

## Multiprocessing:

Used: http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/
39 seconds: almost 9 times faster.

I'll try to throw something together to make it at least somewhat faster.

## Threads:

Used a semaphore to manage thread count and a max of 100 threads to start out. I was worried about upload_file's default 10 threads so I changed it's config to only use the main thread.

This had good results: 2.572920322418213 seconds and 1.8509435653686523 seconds (2 trials)

Time to play with the max thread count and the upload_file config to see if I can get better performance. I wonder if each upload_file being limited to one thread might affect performance if the files being uploaded are larger. That said, it automatically uses MultiPart at a certain filesize and I don't know how that interacts with threads.

50 max methods / max_concurrency=4 -> 1.1969361305236816 seconds and 0.871973991394043 seconds (2 trials)

25 max methods /max-concurrency=6-> 0.6859667301177979 seconds and 0.6299800872802734 seconds (2 trials)

15 max methods /max-concurrency=8->0.5949549674987793 seconds and 0.5879819393157959 seconds (2 trails)

Further investigation revealed these numbers aren't accurate, the print goes off before all the threads finish. Regardless, I'm out of time and this is my submission. I'm not going to change the 100 maxThreads (or maxMethods) and setting the config up to only use one thread as those numbers should be accurate (I think).

Setting up the basic version took about 2 hours and the other versions took a combined 3 hours.



