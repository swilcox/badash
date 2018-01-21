# Welcome to BADash

To contribute to this project or view the source, visit [github.com/swilcox/badash](https://github.com/swilcox/badash).

## Overview

BADash is designed as a simple dashboard for viewing a variety of data output elements from many different jobs.

Conceptually, there are 3 layers of organization:

1. _Event_ - a single point in time output of a job.
2. _Job_ - a task that is run somewhere and has output values.
3. _Dashboard_ - a collection of jobs that are grouped together for viewing purposes.

The output of a Job could be almost anything: raw text stdout/errout from a cronjob type job, a numerical reading from a sensor, map coordinates to something, etc. Every event from a Job has a result. A result of 0 implies no error and that the Job ran correctly. Beyond the result, any additional data can be used as a primary display field for that job.

## Project layout

    badash-api/       # The configuration file.
    badash-docs/      # The source of this documentation.
    badash-frontend/  # The vue.js source for the frontend

## API Installation

The API is written in Python using the Hug framework. To start developing or run the server locally, create a new python (Python 3.6.x) virtual environment, then:

    cd badash-api
    pip install -r requirements/local.txt

You will need a MongoDB database for persistence. The default localhost and collection name can be overridden via setting an environment variable:

    export MONGODB_URI=mongodb://localhost:27017/badash

The API can also be deployed to AWS Lambda via the Zappa package.

*TODO:* instructions on zappa (link to zappa) and a sample configuration file along with deployment command(s).

## Frontend Development

*TODO:* how to work with the Vue.js stuff.
