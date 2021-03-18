import boto3

from boto3.session import Session
ACCESS_KEY='AKIARPBX3JP2ZAFSNAVK'
SECRET_KEY='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'
session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')

#listing the contents of the file.
your_bucket = s3.Bucket('gk-aws-workshop1')
for s3_file in your_bucket.objects.all():
    print(s3_file.key)

#uploading a file
s3 = boto3.resource('s3')
s3.Object('gs-assesement3-cognizant', 'temp1.txt').upload_file(Filename = 'C:\\Users\\Administrator\\Desktop\\temp.txt')

#downloadin the file
s3 = boto3.resource('s3')
s3.Object('gs-assesement3-cognizant', 'temp1.txt').download_file(Filename = 'C:\\Users\\Administrator\\Desktop\\temp1.txt')
#deleting the file
obj = s3.Object("gs-assesement3-cognizant", "temp1.txt")
obj.delete()

