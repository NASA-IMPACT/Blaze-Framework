# HLS Data Transfer Dashboard React App

## Prerequisites

1. Node JS (v12.22.9)
2. NPM (v8.5.1)
3. Grafana (Ensure Grafana is up and running)


### `Steps to deploy the Dashboard`

1. Clone or pull source code from github repository(git clone https://github.com/ub0005/HLS-Transfer-Workflows.git or git pull)
2. cd into HLS-Transfer-Workflows/Data-Transfer-ReactJS-Dashboard.
3. Update your json config file with your grafana panels iframe URL's.
4. Execute command **npm install** to install all the dependencies.
5. Execute command **npm run build** to create the build out of source code.
6. Execute command **npm install pm2 -g** to install pm2 globally
7. Execute command **pm2 serve {path-to-build}/ {port}  --name "{name}"** to deploy the build(e.g : pm2 serve build/ 5000 --name "my-react-app").
8. Execute command **pm2 list** to see the status of the react apps
9. Exectue commadn **pm2 stop/start/delete <process id/process name>** to manage the react apps.
