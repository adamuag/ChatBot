# ChatBot
A course FAQ chatbot that helps users answer common questions. This is part of the zoomcamp-llm-course workshop and uses data from #ZoomCampLLMCourse.

# Requirements
- Docker
- OPenAI
- Elastic Search

# Preparing the Environment 

Create a virtual environment using pipenv for dependency management. 

```bash
pip install pipenv
```

Install the packages

```bash
pipenv install tqdm notebook==7.1.2 openai elasticsearch
```


To manage OpenAI keys, we use direnv:

```bash
sudo apt update
sudo apt install direnv 
direnv hook bash >> ~/.bashrc
```

Create `.evnrc` and add the following, replacing sk-proj-key with your keys.

```bash
export OPENAI_API_KEY='sk-proj-key'
```

Allow direnv to run:

```bash
direnv allow
```

In another terminal, run elasticsearch with docker:

```bash
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```

Verify that ES is running

```bash
curl http://localhost:9200
```

You should get something like this:

```json
{
  "name" : "63d0133fc451",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "AKW1gxdRTuSH8eLuxbqH6A",
  "version" : {
    "number" : "8.4.3",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "42f05b9372a9a4a470db3b52817899b99a76ee73",
    "build_date" : "2022-10-04T07:17:24.662462378Z",
    "build_snapshot" : false,
    "lucene_version" : "9.3.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```