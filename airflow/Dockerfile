FROM apache/airflow:2.8.1-python3.10

USER root

# Install default JRE (Debian-friendly, often OpenJDK 11 or 17)
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

# Set JAVA_HOME (most likely location for default-jre)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:$PATH"

USER airflow

# Copy and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt