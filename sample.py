import os
import sys
import json
import boto
from boto.s3.key import Key


def upload(s3urlargs):
    """
    Uploads the json results file to the S3 URL.
    S3 URL format: s3://dwollatechnicalexercise/problem1
    """
    aws_access_keyid = 'AKIAIUUNGK3IXE3UZO5Q'
    aws_secret_key = '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'
    try:
        conn = boto.connect_s3(aws_access_keyid, aws_secret_key)
        bucket = conn.get_bucket(s3urlargs[2])
        k = Key(bucket)
        k.key = s3urlargs[3]
        k.set_contents_from_filename('results.json')
        return
    except Exception, args:
        print args


def readrejects(flcn, s3urlargs):
    """
    Calculates the REJECTS per Source IP from the logfile
    and saves the result in json format file.
    """
    with open(flcn, 'r') as fileobj:
        iplist = []
        for line in fileobj:
            line_values = line.split(' ')
            if "REJECT" in line_values:
                iplist.append(line_values[4])
    fileobj.close()
    result_dict = {k:iplist.count(k) for k in iplist}
    with open('results.json', 'w') as outfile:
        json.dump(result_dict, outfile)
    outfile.close()
    upload(s3urlargs)
    return

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            s3urlargs = sys.argv[2].split('/')
            if os.path.isfile(sys.argv[1]) and len(s3urlargs) >= 4 and s3urlargs[3] != "":
                readrejects(sys.argv[1], s3urlargs)
            else:
                print "Check inputfile exists / s3url parameters "
        except Exception, args:
            print Exception, args
    else:
        print "Enter scriptname , inputfile and s3url"

