import boto3,os,pathlib
 
def make_bucket(s3Service,bucket_name):
    resp = s3Service.create_bucket(Bucket=bucket_name)
    print("\nS3 bucket {} has been created sucessfully. ".format(bucket_name))

def delete_bucket(service,bucket_name):
    service.delete_bucket(Bucket=bucket_name)
    print("\nS3 bucket {} has been deleted sucessfully. \n".format(bucket_name))
    
def s3_upload_file(bucket_name,filename,tag):
    s3_upload_svc = boto3.resource('s3')
    bucket_selected = s3_upload_svc.Bucket(bucket_name)
    with open(filename, 'rb') as file:
        bucket_selected.upload_fileobj(file,tag)
    print("\nFile {} has been uploaded sucessfully to bucket {}. \n".format(filename,bucket_name))    

def s3_download_file(bucket_name,save_file,tag):
    s3_upload_svc = boto3.resource('s3')
    bucket_selected = s3_upload_svc.Bucket(bucket_name)
    with open(save_file, 'wb') as ink:
        bucket_selected.download_fileobj(tag, ink)    
    print("\nFile {} has been downloaded sucessfully from bucket {}. \n".format(tag,bucket_name))    

def list_s3_buckets(s3Service):
    result = s3Service.list_buckets()
    bucket_names = [bucket['Name'] for bucket in result['Buckets']]
    print("\nCurrently you have the following S3 buckets:\n")
    print(bucket_names)
    return bucket_names

def get_matching_files(path,extension):    
    full_file_path = [str(pathlib.Path(file)) for file in os.scandir(path)]
    filtered = [file for file in full_file_path if file.endswith(extension)]  
    return filtered

def scan_for_files():    
    path = input('Please enter a path to scan for files. ')
    extension = input('Please enter a file extension to filter your search. ')
    dir_contents = get_matching_files(path,extension)
    print('There are {} files with extension type {} '.format(dir_contents.__len__(),extension))   #special method __len__ to sum the matching files
    for file in dir_contents:
        print(file)       
    return dir_contents

def main():    
    s3_service = boto3.client('s3')
    print("\nThis script allows the user to work with the AWS S3 service --\nit can be used to upload files, download files, list bucket contents, create and delete buckets\nin addition to listing files that match a specified criteria on the local machine.\n")
    print()
    while True:       
        response = input("\nType:\n\n'sf' to scan OS for files,\n'lb' to list your s3 buckets,\n'mb' to make a new storage bucket,\n'db' to delete an existing storage bucket,\n'uf' to upload a file to a storage bucket, \n'df' to download file from your storage bucket,\n'q' to quit.\n\n")
        
        if response.lower() == "sf":
           matching_files = scan_for_files()
        elif response.lower() == "lb":           
            buckets = list_s3_buckets(s3_service)
        elif response.lower() == "mb":            
            bucket_name = input('Please enter a name for your new bucket: ')
            make_bucket(s3_service,bucket_name)
        elif response.lower() == "db":           
            buckets = list_s3_buckets(s3_service)
            selected_bucket = input('Please select a bucket that appears in the list: ')
            delete_bucket(s3_service,selected_bucket)
        elif response.lower() == "uf":            
            buckets = list_s3_buckets(s3_service)
            selected_bucket = input('Please select a bucket that appears in the list: ')
            matching_files = scan_for_files()
            file_name = input('Please enter the full path to the file you wish to upload to S3: ')
            tag = input('Please enter a file name tag for this file: ')
            s3_upload_file(selected_bucket,file_name,tag)
        elif response.lower() == "df":            
            buckets = list_s3_buckets(s3_service)
            selected_bucket = input('Please select the S3 bucket containing the file you wish to download. ')            
            tag = input('Please enter the tag/key of the file you wish to download from. ')
            save_file_as = input('Save file as: ')
            s3_download_file(selected_bucket,save_file_as,tag)
        elif response.lower() == "q":
            print('Goodbye')
            break
        else:
            continue
                
                
if __name__ == "__main__":
    main()


#file_info script enhanced to include S3 functionality - Elliott Arnold = Si3mshady learning aws using  python3 - a series 2-18-19


