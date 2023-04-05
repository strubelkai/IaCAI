import os
import json
import openai
from flask import Flask, redirect, render_template, request, url_for
import samples
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        resources = request.form["resource"]
        prefix = request.form["prefix"]
        cloud = request.form["cloud"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(cloud, resources, prefix),
            max_tokens=1000,
            temperature=0,
        )
        json_response = json.dumps(response.choices[0].text, sort_keys = False, indent = 2)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(cloud, resources, prefix):
    return """

{}

{}

{}

Instruction: Given the three examples above, complete the below entry. Generate one complete sample Terraform code to deploy the given cloud resource using name prefix provided. 
    
Cloud: {}
Resource: {}
Name Prefix: {}
Terraform:""".format(
        samples.storage_sample,
        samples.cosmos_sample,
        samples.multiple,
        cloud,
        resources,
        prefix,
    )
