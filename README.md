# From Podman AI Lab to OpenShift AI

**Overview**

The following article shows you how to go from a chatbot reciepe in the Podman Desktop AI Lab extension to a RAG chatbot deployed on OpenShift and OpenShift AI.


* <a href="#arch">Architecture</a>
* <a href="#req">Requirements</a>
* <a href="#podman_ai_lab">Podman AI Lab</a>
* <a href="#deploy_rhoai">Deploy RHAOI</a>
* <a href="#deploy_elastic">Deploy Elasticsearch Vector DB</a>
* <a href="#deploy_minio">Deploy s3 Storage (Minio)</a>
* <a href="#custom_runtime">Create Custom Model Serving Runtime</a>
* <a href="#update_chat">Update the Chat Recipe Application</a>


## <div id="arch">High Level Architecture</a>

![Architecture](img/high_level_overview_arch.png)

## <div id="req">Requirements</a>
It is expected that you have admin access to an OpenShift 4.12+ cluster. The follwing code was tested with an OpenShift 4.15 cluster.

# <div id="podman_ai_lab">Podman AI Lab</a>
## Install Podman Desktop and Podman AI Lab extension
Follow the installation instructions for Podman Desktop and the Podman AI Lab extension in the below Red Hat Developer article. The article also gives a great overview of the features in Podman AI Lab. 
https://developers.redhat.com/articles/2024/05/07/podman-ai-lab-getting-started#

## Download the model
We will be downloading and using the TheBloke/Mistral-7B-Instruct-v0.2-GGUF. This model is quantised (smaller) version of the full Mistral-7B-Instruct-v0.2. The smaller model will allow us to run inferencing on CPUs if GPUs are not an option.

<ol>
<li> Go to the AI Lab extension and select Catalog under Models.

![Catalog](img/AI_lab_catalog.png)

</li>
<li> If you haven't already, download the TheBloke/Mistral-7B-Instruct-v0.2-GGUF model

![Download Model](img/mistral_download.png)

The model is around 4GB so it might take some time.
![Download Progress](img/mistral_download_progress.png)
</li>
<li>
Podman AI Lab allows you to get started quickly with downloaded models through Services, Playgrounds, and the Recipes Catalog. 
<ul>
<li><b>Services</b><br/>
The Services section allows you to create a model service endpoint for models you've downloaded. Client code is provided (cURL by default) in multiple formats to get you started quickly with sending in requests to the model service endpoint. 

![Podman AI Lab Services](img/podman_AI_services.png)

</li>
<li><b>Playgrounds</b><br/>
The Playgrounds area allows you to define system prompts and experiment with different settings like temperature, max tokens, and top-p.

![Podman AI Lab Playgrounds](img/podman_AI_playground.png)

</li>
<li><b>Recipes Catalog</b><br/>
The Recipes Catalog contains demo applications for Natural Language Processing (NLP), Computer Vision, and Audio. We'll be using the ChatBot recipe demo code in this example.<br/><br/>
<b>Create the Chatbot</b>
<ol>
<li>
Make sure to select <b><i>TheBloke/Mistral-7B-Instruct-v0.2-GGUF</i></b> as your model and then click <b><i>Start AI App</i></b>

![Start Chatbot](img/start_chatbot_recipe.png)

</li>
<li>
After the chatbot has started open it up to test it out.
</li>

![Chatbot UI](img/chatbot_recipe_UI.png)

<li>
At the bottom of the AI App Details section you'll see a <b><i>Open in VSCode</i></b> button. Clicking on that will open all of the code that is running your chatbot. Later we'll modify that code to connect langchain, TheBloke/Mistral-7B-Instruct-v0.2-GGUF model, and the Elasticsearch Vector Database. 

![Podman AI Chatbot Recipe](img/podman_AI_chatbot.png)

</li>

</li>
</ol>
</ul>
</li>
</ol>

# <div id="deploy_rhoai">Deploying OpenShift AI</div>

<ol>
<li>
Login to your OpenShift cluster in a terminal with the API token. You can get your API token from the OpenShift web console.

![OpenShift API Login Command](img/ocp_api_login.png)

<pre>oc login --token=<i>YOUR_OPENSHIFT_API_TOKEN</i> --server=https://<i>YOUR_OPENSHIFT_API_URL</i>:6443</pre>
</li>
<li>
We'll first deploy the OpenShift AI operator.
<pre>oc apply -k ./components/openshift-ai/operator/overlays/fast</pre>
</li>
<li>
Now we'll create a Data Science Cluster. Make sure the operator is fully deployed before creating the Data Science Cluster.
<pre>watch oc get pods -n redhat-ods-operator</pre>

![OpenShift AI Operator Status](img/oc_rhoai_operator_status.png)

Once the pod has a Running status and is ready you can run the below command.
<pre>oc apply -k ./components/openshift-ai/instance/overlays/fast</pre>
</li>
</ol>

# <div id="deploy_elastic">Deploy Elasticsearch Vector DB</div>

<ol>

<li>
We'll now deploy the Elasticsearch operator. This will be our vector database.

<pre>oc apply -k ./components/elasticsearch/base/</pre>
</li>
<li>Now we can create an Elasticsearch cluster instance. Make sure the Elasticsearch operatior pod is in a running state and ready.
<pre>watch oc get pods -n elastic-vectordb</pre>

![Elasticserach Operator Status](img/oc_elastic_operator_status.png)

<pre>oc apply -f ./components/elasticsearch/cluster/instance.yaml</pre>
</li>
</ol>

## Ingest data into the Elasticsearch Vector Database

Now that the Elasticsearch operator has been deployed and an instance created, we can ingest some data and query the vector database.

<ol>
<li>
Go to your OpenShift AI Dashboard. You can get the URL either from the below oc command or the OpenShift web console.
<pre>oc get routes -n redhat-ods-applications</pre>
OR<br/>

Select the redhat-ods-applications project, the Networking -> Routes, and then open the URL under Location.

![RHOAI Dashboard](img/rhoai_dashboard_route.png)

</li>
<li>
Login to the dashboard and select <b>Data Science Projects</b> and click the <b>Create Data Science Project</b> button.

![RHOAI Create Project](img/rhoai_create_project.png)

Name the project <i>podman-ai-lab-rag-project</i> and click the <b>Create</b> button.

![RHOAI Name Project](img/rhoai_name_project.png)

</li>
<li>
We'll now create a workbench where we can upload a Jupyter notebook to ingest data into the Elasticsearch vector DB. We'll then test it out by querying for some data. Click the <b>Create a workbench</b> button.

![RHOAI Create Workbench](img/rhoai_create_workbench.png)

Name the workbench <i>elastic-vectordb-workbench</i>, select a <i>Standard Data Science</i> notebook, and select a <i>Medium</i> size.

![RHOAI Setup Workbench 1](img/rhoai_workbench_1.png)

You'll also want to set two environment variables so we can connect to Elasticsearch from the notebook. 
<ul>
<li>
CONNECTION_STRING - Copy the CLUSTER-IP and PORT from this oc command
<pre>oc get service elasticsearch-sample-es-http -n elastic-vectordb</pre>
Add the CONNECTION_STRING key/value as a ConfigMap environment variable.
<br/><br/>
</li>
<li>
PASSWORD - Create a secret environment variable with the Elasticsearch secret value.
<pre>oc get secret elasticsearch-sample-es-elastic-user -n elastic-vectordb -o jsonpath="{.data['elastic']}" | base64 -d > elastic_pass.txt</pre>
Add the PASSWORD key/value as a Secret environment variable. The password is in the <b>elastic_pass.txt</b> file that was created by the above oc command.
</li>
</li>
</ul>
<br/>

![RHOAI Create Workbench](img/rhoai_workbench_2.png)

<br/><b>NOTE:</b> <i>You can delete the elastic_pass.txt file that you got the password from after you add it to the environment variable.</i>

Click on the <b>Create Workbench</b> button. Your workbench should start in a few minutes.

</li>
<li>
Open your workbench after it has started and login.
<br/><b>Note:</b><i> If you have insufficient resources to start a medium container size then stop the workbench and change the workbench to start as a small container size.</i>
<br/><br/>
</li>
<li>
Upload or import the ./notebooks/Langchain-ElasticSearchVector-ingest.ipynb notebook to your workbench.

![RHOAI Workbench Notebook](img/vector_ingest_notebook_upload.png)

</li>
<li>
Run the first 3 cells (<i>Shift + Enter in each cell to run</i>). Make sure you can connect to your Elasticsearch cluster.

![Notebook Execution - First Section](img/verify_elastic_connection.png)

</li>
<li>
Continue to run through each cell while reading through what is occurring in each one. The <i>Create the index and ingest the documents</i> cell is where all of the websites and pdfs are stored with embeddings into the Elasticsearch vector database.
<br/><br/>
This cell will take a while to run. Good time for a coffee break.

![Notebook Execution - Second Section](img/ingest_data_cell.png)

</li>
<li>
After all of the data is stored into our vector database we can directly query it. Run the last 2 cells to make sure the data was stored successfully and we get back the results we expect.

![Notebook Execution - Third Section](img/query_data_cell.png)

</li>

</ol>

# <div id="deploy_minio">Deploy s3 Storage (Minio)</a>
OpenShift AI model serving has a dependency on s3 storage. For this, we'll deploy Minio. 
<ol>
<li>
Make sure you're still logged into your cluster in your terminal. Run the below command to deploy Minio.
<pre>oc apply -k ./components/minio/base</pre>
Make sure the pod is running.
<pre>watch oc get pods -n minio</pre>

![Minio Pod Status](img/minio_pod_status.png)

</li>
<li>
Login to the Minio UI. You can find the route in either the web console or from the oc cli in your terminal. Login with <i>minio/minio123</i>. Minio contains 2 routes, an API route and UI route. Make sure you use the UI route.

![Minio Login](img/minio_login.png)

</li>
<li>
Create a bucket named <i>models</i> and click the <b>Create Bucket</b> button.

![Minio bucket](img/minio_bucket.png)

</li>
<li>
Go to <b>Object Browser</b>, select the <i>models</i> bucket you just created, and click the <b>Create new path</b> button. Name the folder path <i>mistral7b</i> and click the <b>Create</b> button.

![Minio path](img/minio_path.png)

</li>
<li>
Upload the Mistral7b model to the folder path you just created. You can find out where the model was downloaded if you go back to Podman AI Lab and click the <b>Open Model Folder</b> icon.

![Model folder](img/podman_ai_model_folder.png)

In Minio click on the <b>Upload File</b> button and select the model file under the <i>hf.TheBloke.mistral-7b-instruct-v0.2.Q4_K_M</i> directory.

![Model upload](img/minio_model_upload.png)

</li>
<li>
If the model is uploaded successfully you should see the below screen.

![Model upload success](img/minio_model_upload_success.png)

</li>
</ol>

# <div id="custom_runtime">Create Custom Model Serving Runtime</div>

<ol>
<li>
We first need to enable the single serving runtime before we can add our custom serving runtime.
<ol>
<li>
Run the following oc command to deploy Service Mesh.
<pre>oc apply -k ./components/openshift-servicemesh/operator/overlays/stable</pre>
</li>
<li>
Run the following oc command to deploy Serverless.
<pre>oc apply -k ./components/openshift-serverless/operator/overlays/stable</pre>
</li>
<li>
We'll be using the single stack serving in OpenShift AI so we'll want use a trusted certificate instead of a self signed one. This will allow our chatbot to access the model inference endpoint.
<br/><br/>
Run the below oc commands
<ul>
<li>
Get the name of the ingress cert we will need to copy.
<pre>
oc get secrets -n openshift-ingress | grep ingress-certs-*
</pre>

![Ingress Cert Secret Name](img/ingress_cert_secret.png)

</li>
<li>
Copy the full name of the secret and replace the name in the below oc command. Make sure you're in the top level directory of this project and run the below command.
<pre>
oc extract secret/<b>ingress-certs-2024-06-03</b> -n openshift-ingress --to=ingress-certs --confirm
</pre>

You should now have a <i>ingress-certs</i> directory with a tls.crt and tls.key file.

![Ingress Cert Directory](img/ingress_certs_directory.png)

</li>
<li>
We'll now update the secret that will be used in our OpenShift AI data science cluster.

<pre>
cd ingress-certs

oc create secret generic knative-serving-cert -n istio-system --from-file=. --dry-run=client -o yaml | oc apply -f -

cd ..
</pre>
<b>NOTE:</b><i>You can delete the ingress-certs folder after you have created the knative-serving-cert secret.</i>
</li>
</ul>
<li>
Run the following oc commands to enable the Single Model Serving runtime for OpenShift AI. We'll refresh the RHOAI dashboard by deleting the pods.
<pre>oc apply -k ./components/model-server/components-serving
oc delete pod -l app=rhods-dashboard -n redhat-ods-applications
</pre>
</li>
</ol>
<li>
Go to the OpenShift AI dashboard and expand <b>Settings</b> and select <b>Serving Runtimes</b>. You should now see that Single-model serving enabled at the top of the page.
<br/><b>NOTE:</b><i>You might need to refresh the page and it could take a few minutes for the changes to be applied.</i>

![Single serving enabled](img/rhoai_single_serving_enabled.png)

</li>
</ol>

## Add a Custom Serving Runtime
We'll now add a custom serving runtime so we can deploy GGUF versions of models.

<ol>
<li>
Click on the <b>Add serving runtime</b> button. 

![Add Serving runtime button](img/rhoai_add_serving_runtime.png)

</li>
<li>
Select <b>Single-model serving platform</b> for the runtime and select <b>REST</b> for the API protocol. Upload the <i>./components/custom-model-serving-runtime/llamacpp-runtime-custom.yaml</i> file as the serving runtime. Click the <b>Create</b> button.

![Add Serving runtime](img/rhoai_add_serving_runtime_custom.png)

<b>NOTE:</b> <i>I've included a pre-built image that is public. You can build your own image with the Containerfile under ./components/ucstom-model-serving-runtime if you would rather pull from your own repository.</i>
</li>
<li>
If the serving runtime was added was succesfully you should now see it in the list of serving runtimes available. 

![Serving runtime list](img/rhoai-llamacpp-runtime.png)

</li>
<li>
Go to your <i>podman-ai-lab-rag-project</i> and select <b>Models</b>. You should see two model serving type options. Click on the <b>Deploy model</b> under the Single-model serving platform. 

![Serving runtime list](img/rhoai_project_model_servers.png)

</li>
<li>
Fill in the following values and click the <b>Deploy</b> button at the bottom of the form.
<ul>
<li>
Model name = <b>mistral7b</b>
</li>
<li>
Serving rutnime = <b>LlamaCPP</b>
</li>
<li>
Model framework = <b>any</b>
</li>
<li>
Model server size = <b>Medium</b>
</li>
<li>
Select <b>New data connection</b>
</li>
<li>
Name = <b>models</b>
</li>
<li>
Access key = <b>minio</b>
</li>
<li>
Secret key = <b>minio123</b>
</li>
<li>
Endpoint = <b>Your Minio API URL</b>
</li>
<li>
Region = <b>us-east-1</b>
</li>
<li>
Bucket = <b>models</b>
</li>
<li>
Path = <b>mistral7b</b>
</li>
</ul>

![Model Deployment 1](img/rhoai_model_serving_1.png)

![Model Deployment 2](img/rhoai_model_serving_2.png)

![Model Deployment 3](img/rhoai_model_serving_3.png)

</li>
<li>
If your model deploys successfully you should see the following page.

![Deployed Model](img/rhoai_deployed_model.png)

</li>
<li>
Test your model to make sure you can send in a request and get a response. You can use the client code that is provided by the model service in Podman AI Lab. 

<br/>Make sure to update the URL in the cURL command to the Inference endpoint on OpenShift AI.

<pre>
curl -k --location 'https://<b>YOUR-OPENSHIFT-AI-INFERENCE-ENDPOINT</b>/v1/chat/completions' --header 'Content-Type: application/json' --data '{
  "messages": [
    {
      "content": "You are a helpful assistant.",
      "role": "system"
    },
    {
      "content": "How large is the capital of France?",
      "role": "user"
    }
  ]
}'
</pre>

Your response should be similar to the following

<pre>
{"id":"chatcmpl-c76974b1-4709-41a5-87cf-1951e10886fe","object":"chat.completion","created":1717616440,"model":"/mnt/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf","choices":[{"index":0,
"message":{"content":" The size of a city's area, including its metropolitan area, can vary greatly, and when referring to the 
\"capital\" of a country like France, people usually mean the city itself rather than its total metropolitan area. Paris, the capital 
city of France, covers an urban area of approximately 105 square 
kilometers (40.5 square miles) within its administrative limits.
\n\nHowever, if you are asking about the total area of the Paris 
Metropolitana region, which includes suburban areas and their 
combined population, it is much larger at around 13,022 square 
kilometers (5,028 square miles). This encompasses more than just the city of Paris.",
"role":"assistant"},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":32,"completion
</pre>
</li>
</ol>

# <div id="update_chat">Update the Chat Recipe Application</div>
We'll now update the chat recipe application that we created from Podman AI Lab to use Langchain to connect the model we just deployed on OpenShift AI and the Elasticsearch vector database.

<ol>
<li>
We'll start from the default chatbot recipe code accessible from Podman AI Lab. In Podman AI Lab, after clicking the <b>Open in VSCode</b> button you should see the following.

![Chatbot in VSCode](img/chatbot_vscode.png)

The only code we'll need to modify is under the <i>app</i> directory.
</li>
<li>
Open the ./components/app/chatbot_ui.py file. 
<br/><br/>
<ul>
<li>
We'll first get some environment variables.

![Chatbot Environment Variables](img/chat_app_env_vars.png)

</li>
<li>
Then we'll add in the Langchain code to give us our RAG functionality. Note the items highligted in red. Specifically where the model_service or your OpenShif AI inference endpoint URL and the Elasticsearch setup. Finally, take note of how both of these are passed to Langchain (chain).

![Chatbot RAG](img/chat_app_rag.png)

</li>
<li>
The last updates to the code are just to format the response so that the relevant documents will be included. Extra packages were also added to the ./components/app/requirements.txt file.
</li>
</ul>

</li>
<li>
You can build the Containerfile and push it to your own repository or you can use the one at quay.io/jhurlocker/elastic-vectordb-chat.
</li>
<li>
Update the ./components/deployment.yaml file with your values for the MODEL_ENDPOINT, ELASTIC_URL, and ELASTIC_PASS environment variables.
<br/><br/>

![Deployment Environment Variables](img/update_deployment_vars.png)

</li>
<li>
Create the project

<pre>oc new-project elastic-vectordb-chat</pre>
</li>
<li>
Apply the deployment.yaml you just updated to deploy the chatbot application.

<pre>
oc apply -f ./components/app/deployment.yaml
</pre>
</li>
<li>
Get the route to the chatbot application

<pre>
oc get route -n elastic-vectordb-chat
</pre>

Open the application in your browser

<div style="border: 2px solid black;">
<img src="img/chatbot_on_openshift.png" alt="Chatbot Deployed on OpenShift" />
</div>

</li>
<li>
Type in a message and press Enter. It might take awhile to respond if the model is deployed on a CPU.

<img src="img/chatbot_on_openshift_message.png" alt="Chatbot message" style="border: 2px solid black;" />

</li>
<li>
In the OpenShift web console you can check the model server logs under the podman-ai-lab-rag-project -> Workloads -> Pods (mistral7b-*) -> Logs. Note the log statements when a message is sent to the model inference endpoint.

![Model Log](img/model_log.png)

</li>
<li>
Congratulations! You've successfully taken a model and application from Podman AI Lab and created a RAG chatbot deployed on OpenShift and OpenShift AI.
</li>
</ol>


