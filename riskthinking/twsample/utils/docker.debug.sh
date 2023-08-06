docker run --env-file ./kaggle.env -it -p 5000:5000 -v ~/data:/twdata $IMAGE /bin/bash
