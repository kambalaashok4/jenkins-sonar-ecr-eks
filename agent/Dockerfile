FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    docker.io \
    gnupg \
    lsb-release

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

# Install Terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - \
    && apt-add-repository "deb https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    && apt-get update && apt-get install -y terraform

# Install Sonar Scanner
RUN curl -o sonar-scanner.zip -L https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip \
    && unzip sonar-scanner.zip \
    && mv sonar-scanner-*/ /opt/sonar-scanner

ENV PATH="/opt/sonar-scanner/bin:${PATH}"