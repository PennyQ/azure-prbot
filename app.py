from flask import Flask
import os, json
import requests
import base64

def get_pipeline_run_results(pipeline_id=15872, run_id=1112141):
    base_url = "https://dev.azure.com/cbsp-abnamro/MAAP2/_apis/pipelines/{}/runs/{}?api-version=6.0-preview.1"
    username = "" # This can be an arbitrary value or you can just let it empty
    password = "eecmbibcnl3r65izksvqsed75kxvzjj6w6lyod6jvmdjvskyrjxa"
    userpass = username + ":" + password
    b64 = base64.b64encode(userpass.encode()).decode()

    headers = {"Authorization" : "Basic %s" % b64, 'Content-Type': 'application/json'}

    final_url = base_url.format(pipeline_id, run_id)
    response_get = requests.get(final_url, headers=headers).json()
    comment_payload = {
        'status': response_get['state'],
        'result': response_get['result'],
    }
    return comment_payload

def post_comment_on_pr(pr_id, comment):
    base_url = "https://dev.azure.com/cbsp-abnamro/MAAP2/_apis/git/repositories/mlops-repo-actions-bot/pullRequests/{}/threads/?api-version=6.0"
    username = "" # This can be an arbitrary value or you can just let it empty
    password = "eecmbibcnl3r65izksvqsed75kxvzjj6w6lyod6jvmdjvskyrjxa"
    userpass = username + ":" + password
    b64 = base64.b64encode(userpass.encode()).decode()

    headers = {"Authorization" : "Basic %s" % b64, 'Content-Type': 'application/json'}

    payload = {
      "comments": [
        {
          "parentCommentId": 0,
          "content": comment,
          "commentType": 1
        }
      ],
      "status": 1
    }

    final_url = base_url.format(pr_id)
    response = requests.post(final_url, data=json.dumps(payload), headers=headers)

    return response

def trigger_pipeline(repo_endpoint_url):
    repo_endpoint_url = repo_endpoint_url

    username = "" # This can be an arbitrary value or you can just let it empty
    # TODO: how to encrypt this password?
    password = "eecmbibcnl3r65izksvqsed75kxvzjj6w6lyod6jvmdjvskyrjxa"
    userpass = username + ":" + password
    b64 = base64.b64encode(userpass.encode()).decode()
    headers = {"Authorization" : "Basic %s" % b64, 'Content-Type': 'application/json'}

    response_get = requests.get(repo_endpoint_url, headers=headers)
    print("list pipeline:", response_get.status_code) # Expect 200

    data={
        "resources": {
            "repositories": {
                "self": {
                    "refName": "refs/heads/master"
                }
            }
        }
    }
    response_post = requests.post(repo_endpoint_url, headers=headers, data=json.dumps(data))
    print("run pipeline:", response_post.status_code)
    print(response_post.content)
    return response_post.status_code


app = Flask(__name__)

@app.route("/")
def hello():
    return "MLEOps PR Actions bot"


@app.route('/api/event_handler/', methods=['GET', 'POST'])
def event_handler():
    # Assuming to receive this json from https://docs.microsoft.com/en-us/azure/devops/service-hooks/events?view=azure-devops#git.pullrequest.updated
    # event = request.get_json(silent=True)

    # TODO: we fake the event message and manually "hook" to the PR request change
    # ref: https://docs.microsoft.com/en-us/azure/devops/service-hooks/events?view=azure-devops#work-item-commented-on
    with open('commented_on_event.json') as f:
        event = json.load(f)
    print(event)

    if "/run-full-test" in event['detailedMessage']['text']:
        # we trigger the matched pipeline here using PR api https://docs.microsoft.com/en-us/rest/api/azure/devops/pipelines/runs/run-pipeline?view=azure-devops-rest-6.0
        status_code = trigger_pipeline("https://dev.azure.com/cbsp-abnamro/MAAP2/_apis/pipelines/15872/runs?api-version=6.0-preview.1")
        if status_code == '200':
            # we post the status to PR thread as a comment
            # TODO
            comment = get_pipeline_run_results()
            post_comment_on_pr(95016, comment) # replace the PR ID with organic ID
    return "Events handled"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
