import boto3
from botocore.config import Config
from typing import Optional

from utils import vprint

"""
This module gets imported by the preprocessor when filestorage is configured as 'aws_s3'
"""

class FileStorage:
	"""
	This class contains methods for storing and retrieving files from AWS S3
	"""

	def __init__(self, config: dict, secrets: dict) -> None:
		self.config = config
		self.secrets = secrets
		try:
			self.bucket_name = config['documents']['filestorage']['bucket']
			self.s3_client = boto3.client(
				's3',
				endpoint_url=secrets['documents']['aws']['s3_endpoint'],
				aws_access_key_id=secrets['documents']['aws']['access_key'],
				aws_secret_access_key=secrets['documents']['aws']['secret_key'],
				config=Config(signature_version='s3v4')
			)
		except KeyError:
			raise Exception("A bucket configuration is required with configuration 'documents;filestorage;bucket' and secrets 'aws;access_key' and 'aws;secret_key'")


	def read_from_storage(self, filename: str) -> str:
		"""
		Retrieve a file's content from AWS S3
		"""
		try:
			response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
			vprint(f"Retrieved {filename} from S3 bucket {self.bucket_name}", self.config)
			doc = response['Body'].read()
			
			if filename.endswith('.pdf'):
				return doc
			elif filename.endswith(('.md', '.txt')):
				return doc.decode('utf-8')
			else:
				raise ValueError(f"Unsupported file type for {filename}")
		except Exception as e:
			vprint(f"Error reading from S3: {e}", self.config)
			return None
		

	def put_on_storage(self, filename: str, content: str, content_type="binary") -> bool:
		"""
		Store a file's contentat filename in AWS S3
		"""
		try:
			if content_type == "binary":
				self.s3_client.put_object(
					Bucket=self.bucket_name, 
					Key=filename, 
					Body=content,
					ContentType='application/pdf'
				)
			elif content_type == "text":
				self.s3_client.put_object(
					Bucket=self.bucket_name, 
					Key=filename, 
					Body=content.encode('utf-8'),
					ContentType='text/markdown'
				)
			vprint(f"Uploaded {filename} to S3 bucket {self.bucket_name}", self.config)
			return True
		except Exception as e:
			vprint(f"Error uploading to S3: {e}", self.config)
			return False


	def get_documents(self, 
				    start_idx: Optional[int] = None, 
				    end_idx: Optional[int] = None, 
				    filelist: Optional[list] = None,
                    exclude_filenames: Optional[list] = None) -> list:
		"""
		Get documents from S3 bucket.
		If start_idx and end_idx are provided, fetches documents in that range.
		If filelist is provided, fetches only those files.
		"""
		documents = []
		if start_idx is not None:
			if end_idx is None:
				end_idx = start_idx
			for idx in range(start_idx, end_idx + 1):
				filename = f"{idx}.md"
				doc = self.read_from_storage(filename)
				if doc:
					documents.append({'text': doc, 'filename': filename})
		else:
			if not filelist:
				filelist = self.get_txt_files()
			for filename in filelist:
				if exclude_filenames and filename in exclude_filenames:
					continue
				doc = self.read_from_storage(filename)
				if doc:
					documents.append({'text': doc, 'filename': filename})
		
		return documents
	

	def get_txt_files(self) -> list:
		"""
		List all text files in the S3 bucket.
		Returns a list of filenames.
		"""
		response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
		files = []
		if 'Contents' in response:
			for obj in response['Contents']:
				if obj['Key'].endswith('.md'):
					files.append(obj['Key'])
		return files