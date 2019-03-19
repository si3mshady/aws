import boto3
from s3_boto3_practice import list_s3_buckets


def aws_transcribe(boto_svc,job_name,src_s3):  #init boto3 transcribeService     
    result = boto_svc.start_transcription_job(TranscriptionJobName=job_name,
    LanguageCode='en-US',
    MediaSampleRateHertz=44100,
    MediaFormat='mp3',
    Media={'MediaFileUri':src_s3},
    OutputBucketName='speech-to-text-subtitles',
    Settings={'ChannelIdentification': True })
    

def send_sms(boto_svc,msg): #boto3 sns service 
        with open('cell.txt') as cell:
                 hello_moto = cell.read().strip()
        boto_svc.publish(PhoneNumber=hello_moto,Message=msg) 

def main():
        sms = boto3.client('sns')
        s3_service = boto3.client('s3')
        transcribe_svc = boto3.client('transcribe')
        list_s3_buckets(s3_service)        
        job_name = input('Please enter a job name to begin transcribing the audio file: ')
        audio_uri = "https://s3.amazonaws.com/s3-filerepo-si3mshady/Prototype.mp3"
        aws_transcribe(transcribe_svc,job_name,audio_uri)              
        msg=transcribe_svc.list_transcription_jobs()
        send_sms(sms,str(msg))

if __name__ == "__main__":
        main()

#diy AWS practice with python & boto3 - transcribeService and SNS - Elliott Arnold - 2-20-19








