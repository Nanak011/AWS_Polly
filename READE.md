# ⚡ Secure Serverless Text-to-Speech Translation Pipeline

An automated, event-driven AWS architecture that instantly converts uploaded `.txt` files into high-quality, natural audio `.mp3` tracks using serverless infrastructure and generative AI.

---

## 🗺️ System Architecture

To prevent your text diagram from breaking on smaller screens or mobile layouts, it is locked inside a responsive code box below. Scroll horizontally if viewing on a narrow screen:

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

---

## 🛠️ Step-by-Step Implementation Guide

### 🎙️ Step 1. Explore Amazon Polly
* **1.1.** Open your AWS management console and type **Polly** into the top search bar.
* **1.2.** Click on **Amazon Polly** and explore the various languages, voices, and engines available. *(Note: This project utilizes Stephen's voice from the advanced Generative engine).*

### 🔑 Step 2. Create an IAM Role
* **2.1.** Search for **IAM**, and open the Identity and Access Management dashboard.
* **2.2.** On the left-hand sidebar menu, click on **Roles**. Then, click the orange **Create Role** button.
* **2.3.** Under *Trusted Entity Type*, leave **AWS Service** selected.
* **2.4.** In the service dropdown menu, select **Lambda** from the list, and click **Next**.
* **2.5.** On the permissions page, search for and check the boxes next to the following standard policies:
  * `AWSLambdaBasicExecutionRole`
  * `AmazonS3FullAccess`
  * `AmazonPollyFullAccess`
* **2.6.** Click **Next**, name this execution role `Poly-Translation-Role`, and click **Create Role** at the bottom.

### 📦 Step 3. Configure S3 Buckets
* **3.1.** Search for **S3** in the top search bar and click **Create Bucket**.
* **3.2.** In the bucket name field, type a globally unique name for your source storage (e.g., `source-bucket-0-yourname`).
* **3.3.** Scroll to the bottom of the page and click **Create Bucket**.
* **3.4.** Repeat the process to build your destination storage layer. Type a unique name (e.g., `destination-bucket-0-yourname`).

> ⚠️ **DevOps Best Practice Warning:** While you can technically use a single bucket for both input and output files, it is highly discouraged. Doing so creates a dangerous recursive invocation loop where the output audio file accidentally re-triggers the Lambda function over and over, rapidly inflating your AWS bill.

### ⚡ Step 4. Develop the Lambda Function
* **4.1.** Search for **Lambda** and click **Create Function**.
* **4.2.** Leave **Author From Scratch** selected.
* **4.3.** In the *Function name* field, type `Polly-Translator`.
* **4.4.** Under *Runtime*, select the latest version of **Python**.
* **4.5.** Scroll down to the permissions section, expand the default execution role settings, select **Use an existing role**, and choose your `Poly-Translation-Role`.
* **4.6.** Click the orange **Create Function** button. 
* **4.7.** Once the page loads, click on the **Configuration** tab under the function diagram, select **Environment Variables** from the left list, and click **Edit** $\rightarrow$ **Add Environment Variable**.
* **4.8.** Create the first variable:
  * **Key:** `SOURCE_BUCKET`
  * **Value:** *(Your exact source S3 bucket name)*
* **4.9.** Click **Add Environment Variable** again to create the second variable:
  * **Key:** `DESTINATION_BUCKET`
  * **Value:** *(Your exact destination S3 bucket name)*
  * Click **Save**.
* **4.10.** Scroll back up, click on the **Code** tab next to configuration, and open the `lambda_function.py` file.
* **4.11.** Select all the default placeholder code, delete it, and paste your complete `lambda.py` project script.
* **4.12.** Click the **Deploy** button above the text editor to save and activate these changes.

### 🎯 Step 5. Add a Trigger and Destination
* **5.1.** Scroll up to the top visual function overview diagram.
* **5.2.** Click the **Add Trigger** button. In the trigger configuration search bar, select **S3**.
* **5.3.** In the *Bucket* dropdown, select your source S3 bucket.
* **5.4.** Under *Event Types*, ensure **Put** is selected and uncheck all other options.
* **5.5.** Scroll down to the *Suffix* text box and type `.txt` so that non-text files are automatically ignored by your engine.
* **5.6.** Check the recursive invocation acknowledgment box and click **Add**.
* **5.7.** Next, click on the **Add Destination** button on your diagram layout, select **S3** from the destination type dropdown, choose your destination bucket, and click **Save**.

### 🧪 Step 6. Testing and Validation
* **6.1.** Navigate back to your S3 console page.
* **6.2.** Click into your source bucket name, click **Upload**, drop a plain `.txt` file into the pane, and wait for the green success bar.
* **6.3.** Navigate back to your S3 bucket list, click into your destination bucket, and click the circular **Refresh** icon.
* **6.4.** You will see a brand new `.mp3` file appear with an identical filename. Select the file checkbox and click **Download** to enjoy your completed high-quality narration track.

---

## 🧹 Cloud Hygiene & Post-Project Cleanup

To maintain excellent cloud hygiene and avoid unexpected charges, you must completely clear your cloud workspace after testing:

* **7.1.** Go to your S3 console, click into each bucket, select all files, click **Delete**, type `permanently delete` in the text confirmation box, and empty the storage.
* **7.2.** Once completely empty, select the buckets from the main S3 list page and click **Delete**.
* **7.3.** Go back to the Lambda console, click the **Actions** dropdown at the top right of your function page, and click **Delete**.
* **7.4.** Open the IAM console, click **Roles**, search for `Poly-Translation-Role`, check the selection box, and click **Delete**.
* **7.5.** **Crucial Step:** Search for **CloudWatch** in the top search bar, click on **Log Groups** in the left sidebar, locate the row matching your `/aws/lambda/Polly-Translator` function, select it, and click **Delete**.

> 💡 **Why delete CloudWatch Logs?** This is a critical infrastructure best practice. AWS charges an ongoing monthly storage fee for old logs left sitting in CloudWatch. Furthermore, leaving them behind exposes historic information about your old architecture infrastructure patterns. Deleting them ensures your account footprint returns to absolute zero, completely eliminating ongoing security risks and residual billing leaks.
