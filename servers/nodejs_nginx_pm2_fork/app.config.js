module.exports = {
  apps : [
      {
        name: "app",
        script: "./app.js",
        instances: 'max',
        exec_mode: "fork",
        increment_var : 'PORT',
        env: {
            "PORT": 3000,
            "NODE_ENV": "production"
        }
      }
  ]
}
