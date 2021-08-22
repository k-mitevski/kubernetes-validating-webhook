# Kubernetes Validating Webhook
This is a Kubernetes validating webhook written in Python using Flask.

I've written a blog post, and if you like can [read more on the whole setup here.](https://kmitevski.com/writing-a-kubernetes-validating-webhook-using-python)

It works by intercepting Deployment creation, if there isn't a required label set, the request will be rejected.

The required label is set through environment variable in the webhook deployment file.

```
env:
- name: LABEL
  value: development
```

![webhook-image](https://i.imgur.com/igX0OWI.png)