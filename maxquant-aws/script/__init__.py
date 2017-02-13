def upload():
	bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

	bucket = conn.create_bucket(bucket_name,
	location=boto.s3.connection.Location.DEFAULT)

	testfile = "Users/Brenden/text1.txt"
	print 'Uploading %s to Amazon S3 bucket %s' % \(testfile, bucket_name)

	def percent_cb(complete, total):
    		sys.stdout.write('.')
    		sys.stdout.flush()


	k = Key(bucket)
	k.key = 'testfile'
	k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)
}
