import boto3
from flask import Flask, render_template, request
from aws_xray_sdk.core import xray_recorder

app=application=Flask(__name__)
LAMBDA_TRACE_HEADER_KEY = 'set'
LAMBDA_TASK_ROOT_KEY = 'set'
TOUCH_FILE_DIR = '/tmp/.aws-xray/'
TOUCH_FILE_PATH = '/tmp/.aws-xray/initialized'


@app.route('/upload')
def start():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def s3_upload_file():
    segment = xray_recorder.begin_segment('1')
    subsegment = xray_recorder.begin_subsegment('requesting form data/upload')
    bucket = request.form.get('bucket')
    filename = request.form.get('filename')
    s3_upload_svc = boto3.resource('s3')
    bucket_selected = s3_upload_svc.Bucket(bucket)
    with open(filename, 'rb') as f:
        bucket_selected.upload_fileobj(f,Key=filename)
        #confirm if tag argument is needed.
    xray_recorder.end_subsegment()
    xray_recorder.end_segment()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)

#￿Early AM practice with bootstrap, boto3, xray traces and boto3 - poc (quick and dirty)
#Elliott Arnold 6-11-19

#https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/basic.html#manually-create-segment-subsegment
#https://github.com/aws/aws-xray-daemon
#https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon-local.html
#https://stackoverflow.com/questions/25034123/flask-value-error-view-function-did-not-return-a-response
#https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/basic.html
#https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html