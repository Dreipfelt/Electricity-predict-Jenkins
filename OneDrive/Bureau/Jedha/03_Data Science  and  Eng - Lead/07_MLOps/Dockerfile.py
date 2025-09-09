FROM jenkins/jenkins:2.504.2-jdk21
USER root
RUN apt-get update &amp;&amp; apt-get install -y lsb-release ca-certificates curl &amp;&amp; \
    install -m 0755 -d /etc/apt/keyrings &amp;&amp; \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc &amp;&amp; \
    chmod a+r /etc/apt/keyrings/docker.asc &amp;&amp; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/debian $(. /etc/os-release &amp;&amp; echo \"$VERSION_CODENAME\") stable" \
    | tee /etc/apt/sources.list.d/docker.list &gt; /dev/null &amp;&amp; \
    apt-get update &amp;&amp; apt-get install -y docker-ce-cli &amp;&amp; \
    apt-get clean &amp;&amp; rm -rf /var/lib/apt/lists/*
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow json-path-api"