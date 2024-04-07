# Use an official Ruby runtime as a parent image
FROM ruby:3.2.2

# Create a new user and group 'appuser'
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the Gemfile and Gemfile.lock into the container at /app
COPY src/Gemfile src/Gemfile.lock ./

# Install any needed packages specified in Gemfile
RUN bundle install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ .

# Change ownership of the /app directory to appuser and adjust permissions
RUN chown -R appuser:appgroup /app \
    && chmod -R 775 /app

# Ensure the log directory exists and has the correct permissions
RUN mkdir -p log && chmod -R 0664 log

# Ensure the user has access to the master key and other necessary files
# Note: Adjust this according to your application's specific file permission needs
RUN touch config/master.key \
    && chown appuser:appgroup config/master.key \
    && chmod 0660 config/master.key

# Switch to the new user
USER appuser

ARG mailgun_api_key
ENV MAILGUN_API_KEY=${mailgun_api_key}

ARG http_port
ENV HTTP_PORT=${http_port}

ARG rails_master_key
ENV RAILS_MASTER_KEY=${rails_master_key}

ENV RAILS_ENV=production

RUN rails db:migrate
RUN rails db:seed

ARG flag
ENV FLAG=${flag}

RUN rails runner "Flag.find_or_create_by!(value: '$flag')"

RUN echo "rails server -b 0.0.0.0 -p $HTTP_PORT" > docker_entrypoint.sh

ENTRYPOINT ["sh", "docker_entrypoint.sh"]
