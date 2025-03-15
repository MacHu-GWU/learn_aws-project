Amazon Q Business Lite
----------------------

### $3 per user/mo.

#### The Amazon Q Business Lite subscription provides users access to basic functionality such as asking questions and receiving permission-aware responses.

Securely connect Amazon Q Business to your business knowledge and data

Receive permission-aware responses in a conversational interface (responses up to approximately one page)

Use secure and seamless sign-on with enterprise login

Amazon Q Business Pro
---------------------

### $20 per user/mo.

#### The Amazon Q Business Pro subscription provides users access to the full suite of Amazon Q Business capabilities, including access to Amazon Q Apps, and Amazon Q in QuickSight (Reader Pro).

Securely connect Amazon Q Business to your business knowledge and data

Receive permission-aware responses in a conversational interface (responses up to approximately seven pages)

Use secure and seamless sign-on with enterprise login

Create new content quickly

Gain fast insights on your uploaded files

Gain data insights with Amazon Q in QuickSight (Reader Pro)

Custom and fully managed plugins for popular third-party applications

Get images as responses if you choose to select image processing

#### Amazon Q Apps:

Easily create, publish, and share apps

Choose the data sources for each app card

Create and consume Amazon Q Apps outputs with APIs

Index pricing
-------------

Amazon Q Business offers two index types for production and proof of concept (PoC) workloads.You are charged for index units per hour depending on the type of index and the number of units. You can increase or decrease the number of units based on the number of documents you want to index.Note that once an index is created you will incur charges for it regardless of whether you have utilized any document capacity within that index. You can delete the index to stop the charges.

The**Starter Index**is deployed in a single Availability Zone, making it ideal for PoCs and developer workloads.

*   Priced at $0.140 per hour for one unit (limit five units per application)
*   $0.003 per image ($3/1000 images)
*   Audio $0.006/minute
*   Video $0.050/minute
*   One unit includes:
    *   100 hours of connector usageper month
    *   20,000 documents or 200 MB of extracted text, whichever comes first

The **Enterprise Index** is deployed across three Availability Zones, making it best for production workloads.

*   Priced at $0.264 per hour for one unit
*   $0.003 per image ($3/1000 images)
*   Audio $0.006/minute
*   Video $0.050/minute
*   One unit includes:
    *   100 hours of connector usageper month
    *   20,000 documents or 200 MB of extracted text, whichever comes first

Free trial
----------

The free trial terms for Amazon Q Business and Amazon Q in QuickSight are as follows.  

**Free Trial terms**

Amazon Q Business user subscriptions (Amazon Q Business Pro and Lite)

Amazon Q Business offers a 60-day free trial for up to 50 Amazon Q Business Pro or Lite users per application

Amazon Q Business Index (Enterprise and Starter)

Free trial of 1,500 index hours per application to be used in 60 days

Amazon Q in QuickSight user subscription (Amazon Q Business Pro)

30-day free trial for up to 4 users per Amazon QuickSight account

  
Note the following about free trials:

*   For customers subscribing the same user to both products with an Amazon Q Business Pro subscription, the free trial for that user will end whenever the first free trial expires. For example, if a user is added to an Amazon Q Business application and a QuickSight account at the same time through an Amazon Q Business Pro subscription, their free trial will end after 30 days. As another example, if a user is added to an Amazon Q Business application on day 1 with an Amazon Q Business Pro subscription and later added to a QuickSight account on day 15, then their free trial will end on day 45.
*   A free trial applies per user. If a user has used their free trial in one Amazon Q Business application or QuickSight account, they will not get a second free trial in another application.  
    
*   Amazon Q Business has a limit of 1 free-trial application per AWS Payer account. Each free-trial application includes 50 users and 1500 index hours to be used in 60 days as explained above.
*   The free-trial clock for 60 days starts when you create an Amazon Q Business application

Pricing examples
----------------

### Example 1:

You are an enterprise company with 5,000 employees looking to deploy Amazon Q Business. You decide to purchase Amazon Q Business Lite for 4,500 users and Amazon Q Business Pro for 500 users. You have 1 million enterprise documents across sources like SharePoint, Confluence, and ServiceNow that need indexing with an Enterprise Index. Your monthly charges will be as follows:

Enterprise Index for 1M documents will need 50 index units of 20K capacity each (assuming that the extracted text size of 1M documents is less than 200 MB \* 50 units = 10 GB) :  

*   $0.264 per hour \* 50 units \* 24 hours \* 30 days = $9,504

User subscriptions:

*   4,500 users \* $3 per user/month = $13,500
*   500 users \* $20 per user/month = $10,000
*   Total user subscriptions: $23,500

In summary, your monthly charges are as follows::  

*   Enterprise Index: $9,504
*   User subscriptions: $23,500
*   Total per month: $33,004

### Example 2:

In the preceding scenario, you decided to upgrade 300 of the Lite users to Amazon Q Business Pro, considering that those employees could benefit from the advanced features. Additionally, you decided to cancel Amazon Q Lite subscriptions for 10 users who left the company. You made these changes on the 10th day of the month. Upgrades are prorated, and downgrades/cancellations apply starting next month. Therefore, for the remainder of that month, you will be charged the full monthly rate for the 4,200 Lite users. The 500 Pro users will also be billed for the full month. The 300 upgraded users will be prorated, with 10 days billed at the Lite rate and 20 days at the upgraded Pro rate.  

Therefore, for the current month, your user subscription charges are as follows:

*   $3 \* 4,200 + $20 \* 500 + \[$3 \* (10/30) + $20 \* (20/30)\] \* 300 = $26,900

Starting next month, you will have (4,500 - 300 - 10 = 4,190) users with Lite and (500 + 300 = 800) users with Pro. Therefore, your charges from the next month are as follows:

*   $3 \* 4,190 + $20 \* 800 = $28,570 per month  
    

Since you didn’t change anything on index capacity, your index charges remain the same at $9,360 per month.  

In summary, your monthly charges starting next month are as follows:  

*   Enterprise Index: $9,360
*   User subscriptions: $28,570
*   Total per month: $37,930  
    

### Example 3:

You have 1,000 employees at your company. Your IT team uses Amazon Q Business to answer employee questions. They assigned Amazon Q Business Lite subscriptions to all 1,000 employees. The IT help desk chatbot contains 10,000 documents.

Separately, your sales team uses Amazon Q Business for 100 sales reps to help them answer customer questions, create presentations, and implement actions using plugins. You assigned these 100 sellers the Amazon Q Business Pro plan. Their sales chatbot contains 200,000 documents. You granted the sales team access to QuickSight so that they can create documents and presentations using sales data, access dashboards with natural language data summaries, and ask questions about the data.

With Amazon Q Business, subscriptions are deduplicated, and users are charged once for the highest tier. So, the 100 sales reps are charged at the Pro rate, while the 900 other employees are charged at the Lite rate. Amazon Q Business users are charged separately across each AWS IAM Identity Center instance, so all applications must use the same IAM Identity Center instance to be charged only once per user.

Your monthly user charges are as follows:

*   100 users at $20 Pro rate: 100 \* $20 = $2,000
*   900 users at $3 Lite rate: 900 \* $3 = $2,700
*   Total user subscriptions: $2,000 + $2,700 = $4,700

For indexing, you have two separate apps: the 10K document IT chatbot and the 200K document sales chatbot.

The IT chatbot requires 1 index unit at $0.264 \* 24 hours \* 30 days \* 1 unit = $190.08 per month.

The larger sales chatbot needs 10 index units at $0.264 \* 24 hours \* 30 days \* 10 units = $1,900.80 per month.

In total, your estimated monthly charges are as follows:

*   User subscriptions: $4,700
*   IT chatbot index: $190.08
*   Sales chatbot index: $1,900.80
*   Amazon Q in QuickSight enablement fee: $250/month/account
*   Total per month: $4,700 + $190.08 + $1,900.8 +$250 = $7040.88  
    

### Example 4:

You are an enterprise company or independent software vendor (ISV) looking to embed Amazon Q Business into your own application. You end users would be enabled to get answers to questions related to your product features while staying within your user interface. You decide to purchase Amazon Q Business Lite for your 5,000 users. To begin, you first create an Enterprise Index using your product documentation. This amounts to 200,000 documents. Your monthly charges are as follows:

**Enterprise Index** for 200,000 documents will need 10 index units of 20K capacity each (assuming that the extracted text size of 1M documents is less than 200 MB \* 50 units = 10 GB):

*   $0.264 per hour \* 10 units \* 24 hours \* 30 days = $1,900.80

**User subscriptions:**

*   Amazon Q Business Lite subscription for 5,000 users \* $3 per user/month = $15,000 In summary, your monthly charges are as follows:
*   Enterprise index: $1,900.80
*   User subscriptions: $15,000
*   Total per month: $16,900.80

### Example 5:

You are an enterprise company with 500 employees looking to deploy Amazon Q Business. You decide to purchase Amazon Q Business Lite for 450 users and Amazon Q Business Pro for 50 users. You have 1000 enterprise documents across sources like SharePoint, Confluence, and ServiceNow that need indexing with an Enterprise Index. On an average, your documents have two images or visuals you want to extract information from them and make them searchable. You decide to weekly sync all the data to keep it refreshed leading to 4 syncs on an average per month.

Your monthly charges will be as follows:

**Enterprise Index** for 1000 documents will need 1 index units of 20K capacity (assuming that the extracted text size of 1000 documents and images is less than 200 MB):

*   $0.264 per hour \* 1 unit \* 24 hours \* 30 days = $190
*   $0.003 per image \* 2 \* 1000 images \* 4 sync of all documents = $24

**User subscriptions**:

*   450 users \* $3 per user/month = $1350
*   50 users \* $20 per user/month = $1000
*   Total user subscriptions: $2350

**In summary**, your monthly charges are as follows:

*   Enterprise Index: $190
*   Image processing: $24
*   User subscriptions: $2350
*   Total per month: $2564

### Example 6:

You are an enterprise company with 50 employees looking to deploy Amazon Q Business. You decide to purchase Amazon Q Business Lite for 450 users and Amazon Q Business Pro for 50 users. You have 1000 enterprise documents across sources like SharePoint, Confluence, and ServiceNow that need indexing with an Enterprise Index. Of these 1000 documents, let us say there are 20 audio files that are 60 minutes long on an average, and 10 video files that are 30 minutes long on an average. You want to extract information from these multimedia files and make them searchable. You decide to weekly sync all the data to keep it refreshed leading to 4 syncs on an average per month. Additionally, your audio and video files don’t change across these syncs, so Q Business is only processing them once for ingestion.

Your monthly charges will be as follows:

**Enterprise Index** for 1000 documents will need 1 index units of 20K capacity (assuming that the extracted text size of 1000 documents inclusive of the transcriptions for audio and video is less than 200 MB):  

*   $0.264 per hour \* 1 unit \* 24 hours \* 30 days = $190
*   $0.006 per minute \* 60 minutes per audio file \* 20 audio files \* 1 sync of all documents = $7.2 (Note that there are no extra charges for the remaining 3 syncs as long as the files haven’t changed)  
    
*   $0.050 per minute \* 30 minutes per video file \* 10 video files \* 1 sync of all documents = $15 (Note that there are no extra charges for the remaining 3 syncs as long as the files haven’t changed)

**User subscriptions**:

*   450 users \* $3 per user/month = $1350
*   50 users \* $20 per user/month = $1000  
    
*   Total user subscriptions: $2350

**In summary**, your monthly charges are as follows:

*   Enterprise Index: $190
*   Audio processing: $7.2  
    
*   Video processing: $15  
    
*   User subscriptions: $2350
*   Total per month: $2562.2  
    

  
**Note**: User subscriptions are created per Amazon Q Business application or QuickSight account. Each admin can independently create, update, or delete subscriptions for users for their specific Amazon Q Business application or QuickSight account. For applications using IAM Identity Center, AWS will deduplicate subscriptions across all Amazon Q Business applications and QuickSight accounts, and charge each user only once for their highest subscription level. Note that deduplication will apply only if the Amazon Q Business applications and QuickSight accounts share the same IAM Identity Center instance. Users subscribed to Q Business applications using IAM federation, will be charged once per IAM identity provider for OIDC-based as well as SAML-based applications. For example, if a user is subscribed to five different Q Business applications all associated with the same IAM identity provider, that user will be charged once. However, if the Q Business applications are associated with five IAM identity providers, the user will be charged five times. In scenarios where a user is subscribed to a mix of applications, the charging structure is as follows: 1. For applications using IAM Identity Center, users will be charged once across all these applications that share the same IAM Identity Center Instance. 2. For applications using IAM federation, users will be charged once per IAM identity provider. The User subscriptions are prorated when created or upgraded based on the number of days left in the calendar month. Any cancellations or downgrades are not prorated and apply starting in the next calendar month. The charges for user subscription starts only after first use by the user. After a user's first use, subscription charges will continue each month until the user's subscriptions have been removed.
