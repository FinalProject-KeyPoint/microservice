const pm2Config = {
  apps: [
    {
      name: 'Utility',
      script: './app.py',
      exec_mode: 'cluster_mode',
      instances: 1,
    },
  ],
}

module.exports = pm2Config