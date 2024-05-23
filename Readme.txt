####### Create S3 buckets for deepracer reporting
deepracer-data-collection.py writes to dallas-deepracer-reporting bucket (created in sandbox-5)
athena queries 

####### Create ECR repository named deepracer-reporting

####### Build docker image for deepracer-data-collection
C:/Users/maitr/chase/pcl/pcl aws --sandbox-user --sid o715815 --role-arn arn:aws:iam::941821586685:role/l1-developers

cd C:\Users\maitr\chase\deepracer-reporting\code
aws ecr get-login-password --region us-east-1 --profile adfs | docker login --username AWS --password-stdin 941821586685.dkr.ecr.us-east-1.amazonaws.com
docker build --progress=plain --no-cache -t deepracer-reporting .
docker tag deepracer-reporting:latest 941821586685.dkr.ecr.us-east-1.amazonaws.com/deepracer-reporting:latest
docker push 941821586685.dkr.ecr.us-east-1.amazonaws.com/deepracer-reporting:latest
####################Starting Ec2
Launch an Ec2 with Amazon Linux 2 AMI with appropriate IAM role. Refer to deepracer-reporting-server-role (IAM role) in sandbox-1

IAM policy - deepracer-reporting-server-policy

####################Deploy docker & other softwares in Ec2 -- Login to Ec2 using Session Manager and run following commands
sudo su
sudo yum install python37
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

sudo yum install docker
sudo yum install awscli
sudo systemctl enable docker.service
sudo systemctl start docker.service

####################Run deepracer-reporting in Ec2

rm -rf pwd.txt
aws ecr get-login-password --region us-east-1 >> pwd.txt
cat pwd.txt

docker login --username AWS --password eyJwYXlsb2FkIjoia3doaTJSaUt1VmpDNkNCaTlqbDM2UndnWHJYNUExK2tsL0dnVGxvRlZvcFd1OGdCZ2NrTHp0ajJCRmpBVDQxbGl0RHRaT2VNdzJMMWYyN3BraTBaeTBqeDRTMnQ1QVBFQ2FkUFhraUFSa0Y5SFhwZVZxVEUwWG84REVxbG9mYmMrVlNja2t2K1ZJRUc2bE12Q1dSZXMvcy8zUUc5THU1aWEzYk1ET0dKZ1Q0Ky9PdkZRdGZQS1R6WER3K281dFFPeXFNKzlRc3dEY2ZOYmg1elk4LytleEE1aGlQRWxmN3JUVzVNS1pTdHl5TWJwZ3FORjRuM3NGLzR1RHJ4a3FIbnhNOWdOdkgrRzJndEUzTE5RRDVOTnNIbzIzemFTbjZiaDUwdWxDSW16M0ZORVNoaDV0ZzJBN0FzK2FNRXVHWVNHTlpPRFlrL2MvRHg5bFBMWkc4YWpZbzZhLzNWclhuSUgyaStONDQralBUdGU0Y2NhQmFKYjhucVZlN2h4YktNN2lkaEZ6c0I1dFMzR2pFRjRteTVEZ21OZnE1RW1vQXMwVDhsc2NHRkpTS0IxQUlJZGZQanlxeUltWUpLY01pcUt3YmpmSkxLM21yZUJYWWRFRmpCRmlNKzZzT0RMN2xWSjNieUcyeTUyVkhsNW9iRURsTWNOc0llMU1IaTN1VlpFY1VqOTZxRHlua1A4TVcreWNTcjZSSU9pM2NIRUhDcDBlR0xjU0xxaW1iZWxwbk1peEsvSko4Z3VNUFFDR3BKZ0RhWlpFZmsyZHhWbTI1VzNSdXQyaEFvMHVMNmtxc05xdGNDVlJBZldyeENEbHdITFZteExRbWduZTZmSWxXSjY5YTh1YUVFWU96a0d0Y25WalNuNmdqQTZRTzFvS1hIR1Q2cHplYndWL2JJemQ0aFVYckk0SU1oZmM2K1QxOE9tcTBDS04xWDk1bjZVMS95TmIzNFF6UHZ3bm92bjFmZ2ZmM1BYL214YjgvallPMHVYVVk0ZmFaZkx3Y3dKYmI2dXpYTjA3RGhhUEdrU2dOMk5rK1hCbDFSYkNMRGVXVk55cjJEMHhIb0x3VGZ2NFpIYjkyRmNJVUxRbGdOeTl0dDVjcmczU0pacXZIbHdxU2pUOWlvOEpITzlxRDlnWnJRdEoxalhnMXlWYmtuNUtrbENZbDJCY0JSUzd0VGg4bXV3WUlCTGxrY1ZETUJ3VkQrbFFZeUhUT1ZRVDBQUVEwU29zdDBXdGtyRVJ1Z3A4WWMvU3A3ZS9IcVdoYzFoZFB5MjBRbFhJTWRXeTFISms2TDJlOFlsU3VtaUpWTTJhc0s0WmdhNk4zVmVOeEpQNlVXM21pKzdSZ2kwUEh0Y29hWDlUNHdJNHBoU3lZL25UMkU2aXJlYUtzaklZTWVucC9DeXN4UFVNV3Bqbkt1b3l6MWtuUmhnVkZmZUFvaFp4V29PbXl0bjF6ZFMzZnNTdXJSWVllRU1TaWxmVmpIWUUzZEVvQWxhdWlhUE4xNjdsK3NDbzloRGdqSk5QbzhuT1dYOHBQYXlGK0hHaEZLTFVLdmF1VHdZaUhyanh1TFRGRERNdE1FK2hEb1ErTk5ObjRtRkh2bzlWczI2YTFxL2xWR1U3a2hBUkNRN05TL1ZCcGt4YjYwa2hWb0Z0QnUyM3p2aDd6RHZxbTd5ZGpnRU8zOTY5NlNLN1U4c0tESUdpVjRJTUplRCszaFBMMUxIc3I2dDdaTWJaUjNMTlNscE5aRElWL1dudTN0ZVFKOGVaVk9UYW9wVjRHcmdpQ2g4TlhaWnhtTWJubStaVHMvWE1yL0NYVkE4MDdCaEhidEMxb0lYNlRJODlvMFZ6UzI2ZlVKWHRvMWF5dEx1UmJ1dFZ5Z0RUb082bVUzaHptT0Z1SmxuWE1NYnNxU0dLTVUyYVlTeUlTSy9ab0U1UlBxQ0VCb1pMaWRFdmU4N0tudVg5Z2paVk5xQ0pEL3JnWTE4MjJjVGlMMm9hWUlpU3lUalVQa0pPNDRnaVM5UFJWTHNqZ3JPL0NxbStCK2xZQzRiaXR3bTJCSnhaR21aSExicjNmSmV5ak55MWVsRGdtWkdMUWNsVWYySXJjSmprWGZndWZmaW1EVzdCNFRVeitHL2t2OWpCSVl4QVNyanIzT294eGhhMXo1cUpQZHhPUmswck1ZUUtkUnYwR2JxbWNVQ1JJVjZsa1pLQU41Q2lXTXVMOXVBSFljQXVRcm5sWXFBSHNXVU5wS0k3Z0FZdVJDZGFXY2ZwcURyY2FSRDhRZlYzSjZtcFFnYldSellWRnpUK2lJeXBjcnlZVk5HWjF6QmFMcEo1SGVIZ3VxRzN0dTA0YzF1bDluM082b3doL2YiLCJkYXRha2V5IjoiQVFFQkFIaHdtMFlhSVNKZVJ0Sm01bjFHNnVxZWVrWHVvWFhQZTVVRmNlOVJxOC8xNHdBQUFINHdmQVlKS29aSWh2Y05BUWNHb0c4d2JRSUJBREJvQmdrcWhraUc5dzBCQndFd0hnWUpZSVpJQVdVREJBRXVNQkVFRElxK1AwekMwa2x4b05zY2ZRSUJFSUE3aUVHTXp1Y0YzdXo1UmVnS3NCbFI5dmtnY2d2MmJnR0ZmZXdlTVRQdC9MZUNEa2FzWitTNzdDZ0hvMUVOclc5VFEyTEozOXJkaEhwU1BSST0iLCJ2ZXJzaW9uIjoiMiIsInR5cGUiOiJEQVRBX0tFWSIsImV4cGlyYXRpb24iOjE2NjM5MDMzOTV9 739731981269.dkr.ecr.us-east-1.amazonaws.com


docker image rm 739731981269.dkr.ecr.us-east-1.amazonaws.com/deepracer-reporting:latest --force
docker pull 739731981269.dkr.ecr.us-east-1.amazonaws.com/deepracer-reporting:latest
docker run 739731981269.dkr.ecr.us-east-1.amazonaws.com/deepracer-reporting:latest

docker image prune
docker system prune