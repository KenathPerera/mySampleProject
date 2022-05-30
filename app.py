#!/usr/bin/env python3

import aws_cdk as cdk

from my_sample_project.my_sample_project_stack import MySampleProjectStack


app = cdk.App()
MySampleProjectStack(app, "my-sample-project")

app.synth()
