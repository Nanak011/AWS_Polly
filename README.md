Workflow

```text
[ User ] 
   │
   ▼ (1. Upload Script)
┌───────────────────────┐
│  Source S3 Bucket     │ 
│  (Data Input Layer)   │
└──────────┬────────────┘
           │
           ▼ (2. ObjectCreated Event Trigger)
┌───────────────────────┐
│     AWS Lambda        │ ◄─── Reads [ IAM Execution Role ]
│ (Orchestration Engine)│      
└──────────┬────────────┘
           │
           ├──► (3. SynthesizeSpeech Request) ──► ┌───────────────────┐
           │                                      │   Amazon Polly    │
           │ ◄── (4. Returns AudioStream) ◄────── └───────────────────┘
           │
           ▼ (5. Writes Stream Payload)
┌───────────────────────┐
│ Destination S3 Bucket │ ──► [ User Downloads .mp3 Output ]
│ (Audio Output Layer)  │
└───────────────────────┘
```

* **Step one. Explore Amazon Polly.**
  * **1.1.** Open your AWS management console and type Polly into the top search bar.
  * **1.2.** Click on Amazon Polly and explore the various languages, voices and engines available. I am using Stephen's voice from the generative engine.

* **Step two. Create an I A M role.**
  * **2.1.** Search for I A M, and open the identity and access management dashboard.
  * **2.2.** On the left, click on Roles. Then, click the Create Role button.
  * **2.3.** Under Trusted Entity Type, leave AWS Service selected.
  * **2.4.** In the service dropdown menu, select Lambda from the list, and click Next.
  * **2.5.** On the permissions page, search for and check the box next to AWS Lambda Basic Execution Role, then Amazon S3 full access and Amazon Polly full access.
  * **2.6.** After that, click Next, name this role Poly Translation Role and click Create Role at the bottom.

* **Step three. Configure S3 buckets.**
  * **3.1.** Search for S 3 and create a bucket.
  * **3.2.** In the bucket name field, type a globally unique name for your source storage, such as, source bucket 0.
  * **3.3.** Scroll down to and click Create Bucket.
  * **3.4.** Repeat the process to build destination storage. Type a unique name, such as, destination bucket 0.
  * *(Note that while you can technically use a single bucket for both input and output, it is highly discouraged. Doing so creates a dangerous recursive loop where the output audio file accidentally re triggers the Lambda function over and over, rapidly inflating your AWS bill.)*

* **Step four. Develop the Lambda function.**
  * **4.1.** Search for lambda and Create a Function.
  * **4.2.** Leave Author From Scratch selected.
  * **4.3.** In the function name field, type, Polly Translator.
  * **4.4.** Under Runtime, select the latest version of Python.
  * **4.5.** Scroll down to the custom setting and in custom execution role, select your Poly Translation Role.
  * **4.6.** Save it and scroll to the bottom right and click the Create Function button. 
  Once the page loads, scroll down past the visual diagram to the runtime settings tabs.
  * **4.7.** Click on the Configuration tab, then select Environment Variables, then Click the Edit button and Add Environment Variable.
  * **4.8.** In the first Key box, type, SOURCE BUCKET, in all capital letters with an underscore. In its Value box, paste your exact source S3 bucket name.
  * **4.9.** Click Add Environment Variable again. In the second Key box, type, DESTINATION BUCKET, in all capital letters with an underscore. In its Value box, paste your exact destination S3 bucket name and save.
  * **4.10.** Now, scroll back up and click on the Code tab next to configuration.
  * **4.11.** Select all the default placeholder code and delete it. Paste the entire code from lambda.py.
  * **4.12.** Click the Deploy button on the text editor to save and activate these code changes. 

* **Step five. Add a trigger and destination.**
  * **5.1.** Scroll up to the top visual function overview diagram.
  * **5.2.** Click the Add Trigger button. In the trigger configuration select S3.
  * **5.3.** In the Bucket, select your source S3 bucket.
  * **5.4.** Under Event Types, ensure Put is selected and unselect others.
  * **5.5.** Scroll down to the Suffix text box and type, dot t x t, so that non text files are automatically ignored.
  * **5.6.** Check the recursive invocation acknowledgment box and add.
  * **5.7.** Then click on the destination button, select s3 from destination type, choose your destination bucket and save.

* **Step six. Testing and validation.**
  * **6.1.** Navigate back to the S3 console page.
  * **6.2.** Click into your source bucket name. Upload your text file and wait for the green success bar.
  * **6.3.** Now, navigate back to your S3 bucket list, click into your destination bucket, and click the refresh icon.
  * You will see a new dot m p three file appear with an identical filename. Select the file and download.

* **Finally, cloud cleanup. To maintain excellent cloud hygiene and avoid unexpected charges, we must stop unused serices and clear the workspace.**
  * **7.1.** Go to your S3 console, click into each bucket, select all files, click Delete, type permanently delete in the text confirmation box, and empty the storage.
  * **7.2.** Once empty, select the buckets from the main list and click Delete.
  * **7.3.** Next, go back to the Lambda console, click Actions at the top right of your function page, and click Delete.
  * **7.4.** Open the I A M console, click Roles, search for poly translation role, check the box, and click Delete.

* **Lastly, do not forget to clean up your cloud watch logs.**
  * **7.5.** Type CloudWatch into the top search bar, click on Log in the left sidebar, locate the row for your polly translator function, select it, and click Delete. 
  * This is a critical best practice. AWS charges an ongoing monthly storage fee for old logs left sitting in CloudWatch, and leaving them behind exposes information about your old infrastructure patterns. Deleting them ensures your account footprint returns to absolute zero, completely eliminating ongoing security risks and residual bills.
 

Link to video: https://www.linkedin.com/posts/gurunanakadhikari_i-built-an-automated-serverless-text-to-speech-ugcPost-7459301524905594880-EgSC?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEtEqhwBtd9Rjbr84IsWwWRE8ExCL1UNzXU
